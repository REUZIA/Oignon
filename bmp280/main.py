import machine, neopixel, bmp280, time
import _thread
from machine import Pin, I2C, Timer
from micropython import const, schedule
from collections import deque
import rp2

servo_open = const(900_000)
servo_closed = const(1_850_000)

optimal_delay = const(9000)

altitude_treshold = const(15) # for launch detection in m
speed_treshold = const(3) # m/s
min_delay = const(1000)
max_delay = const(optimal_delay+1000)

max_alt = const(300) # Force deployment at this altitude

# Colors
COLOR_RED = const((255, 0, 0)) # STANDBY blink
COLOR_GREEN = const((0, 255, 0)) # STANDBY blink and forced deployment
COLOR_BLUE = const((0, 0, 255)) # LAUNCHED
COLOR_WHITE = const((255, 255, 255)) # DEPLOYED
COLOR_BLACK = const((0, 0, 0)) # OFF

# STATUS
STATUS_STANDBY = const(0)
STATUS_LAUNCHED = const(1)
STATUS_DEPLOYED = const(2)
STATUS_TOUCHDOWN = const(3)

# FRAME TYPES
FRAME_LOG = const(0)
FRAME_BMP = const(1)
FRAME_SPEED = const(2)

status = STATUS_STANDBY

ticks_launched = 0
ticks_deployed = 0
ticks_touchdown = 0

timeout = const(10_000)

led = neopixel.NeoPixel(Pin(16), 1)

buzz = Pin(7, Pin.OUT)
buzz.off()

bmp = bmp280.BMP280(I2C(0, sda=Pin(4), scl=Pin(5)), use_case=bmp280.BMP280_CASE_HANDHELD_DYN)
bmp_refresh_period = const(13)
bmp_last_measure_ticks = 0

servo = machine.PWM(Pin(13))
servo.freq(50)
servo.duty_ns(servo_closed)

measure_buffer = deque((), 80)
log_buffer = deque((), 100)
log_buffer.append(f"{time.ticks_ms()}|{FRAME_LOG}|START")

def flush_logs(buffer):
    f = open("DATA.txt", "a")
    last_flush = 0
    
    while True:
        if time.ticks_ms()-last_flush > 1000: # Flush every seconds
            f.flush()
            last_flush = time.ticks_ms()
        
        try:
            line = buffer.popleft() # Try to fetch one line
        except IndexError:
            time.sleep(0.01)
            continue
        
        if type(line) == str:
            if not line.endswith("\n"): line += "\n"
            f.write(line)
        elif type(line) == tuple:
            f.write("|".join([str(value) for value in line])+"\n")
        
def write_color(color):
    led[0] = color
    led.write()

buzz.on()
time.sleep(0.1)
buzz.off()

bmp_last_measure_ticks = 0
sea_level_pressure = 0
def get_bmp_data():
    global bmp_last_measure_ticks, sea_level_pressure
    time.sleep_ms(max(0, 1 + bmp_refresh_period-(time.ticks_ms()-bmp_last_measure_ticks))) # Ensure "bmp_refresh_period" is waited between measurements

    while True:
        bmp_last_measure_ticks = time.ticks_ms()
        try:
            pressure, temperature = bmp.pressure, bmp.temperature
        except OSError:
            time.sleep_ms(bmp_refresh_period)
            continue
        
        if pressure > 71300: # Workaround first measurement glitch
            break
        else:
            time.sleep_ms(bmp_refresh_period)
    
    if sea_level_pressure == 0: sea_level_pressure = pressure # Set reference pressure
    
    altitude = 44330 * (1.0 - pow(pressure / sea_level_pressure, 0.1903))
    return bmp_last_measure_ticks, altitude, pressure, temperature
    
def deploy():
    global ticks_deployed, status
    if time.ticks_ms() - ticks_launched > min_delay and status != STATUS_DEPLOYED: # If time elapsed since launch is greather than min_delay
        servo.duty_ns(servo_open)
        status = STATUS_DEPLOYED
        ticks_deployed = time.ticks_ms()
        schedule(log_buffer.append, f"{ticks_deployed}|{FRAME_LOG}|DEPLOYED\n")
        write_color(COLOR_WHITE)
    else:
        schedule(log_buffer.append, f"{time.ticks_ms()}|{FRAME_LOG}|INVALID DEPLOY ORDER")
        
def deploy_callback(t):
    deploy()
    schedule(log_buffer.append, f"{time.ticks_ms()}|{FRAME_LOG}|DEPLOYED BY TIMER")
    
def avg_speed(altitude_buffer):
    speeds = list()
    for i in range(len(altitude_buffer)-1):
        speeds.append((altitude_buffer[i+1][1] - altitude_buffer[i][1]) / ((altitude_buffer[i+1][0] - altitude_buffer[i][0])/1_000))
    return sum(speeds)/len(speeds)

# ##### MAIN PROGRAM ######
_thread.start_new_thread(flush_logs, (log_buffer,))

# FORCE DEPLOYEMENT
write_color(COLOR_GREEN)

time.sleep(2)

if rp2.bootsel_button():
    servo.duty_ns(servo_open)
    log_buffer.append(f"{time.ticks_ms()}|{FRAME_LOG}|FORCED DEPLOYMENT")
    while True:
        write_color(COLOR_BLACK)
        time.sleep(0.8)
        write_color(COLOR_WHITE)
        time.sleep(0.1)

write_color(COLOR_RED)

# LAUNCH DETECTION
last_log_ticks = 0
while status == STATUS_STANDBY: # While waiting for LAUNCH
    timestamp, altitude, pressure, temperature = get_bmp_data()
    measure_buffer.append((timestamp, FRAME_BMP, altitude, pressure, temperature)) # Log into circular buffer
    
    if altitude > altitude_treshold: # Detect launch
        log_buffer.append(f"{timestamp}|{FRAME_LOG}|LAUNCHED")
        ticks_launched = timestamp
        status = STATUS_LAUNCHED
        timer = Timer(period=max_delay, mode=Timer.ONE_SHOT, callback=deploy_callback) # Start backup timer
        
        break
    
    elif timestamp - last_log_ticks > 500: # Log baro every 500 ms even if not launched
        log_buffer.append((timestamp, FRAME_BMP, altitude, pressure, temperature))
        last_log_ticks = timestamp
    
    if (time.ticks_ms()%100) < 50: # Blink led
        write_color(COLOR_GREEN)
    else:
        write_color(COLOR_RED)
        
    if (time.ticks_ms()%1_000) < 100:
        buzz.on()
    else:
        buzz.off()

buzz.off()
write_color(COLOR_BLUE)

while True: 
    try:
        log_buffer.append(measure_buffer.popleft()) # Log circular buffer
    except IndexError:
        break

del last_log_ticks, measure_buffer

altitude_buffer = list()

while status == STATUS_LAUNCHED: # While LAUNCHED not DEPLOYED
    timestamp, altitude, pressure, temperature = get_bmp_data()
    altitude_buffer.append((timestamp, altitude))
    
    if len(altitude_buffer) > 15: # Rolling average across 15 measurements (15*13 = 195 ms)
        altitude_buffer.pop(0)
    
    log_buffer.append((timestamp, FRAME_BMP, altitude, pressure, temperature))
    
    if altitude > max_alt:
        deploy()
        log_buffer.append(f"{timestamp}|{FRAME_LOG}|FORCED DEPLOYMENT")
        
    
    if len(altitude_buffer) > 2:
        speed = avg_speed(altitude_buffer)
        log_buffer.append(f"{timestamp}|{FRAME_SPEED}|{speed}")
        if speed < speed_treshold:
            deploy()
            log_buffer.append(f"{timestamp}|{FRAME_LOG}|DEPLOYED BY ALTI")

while status == STATUS_DEPLOYED or time.ticks_ms()-ticks_touchdown < timeout: # Waiting for timeout ms after TOUCHDOWN
    timestamp, altitude, pressure, temperature = get_bmp_data()
    log_buffer.append((timestamp, FRAME_BMP, altitude, pressure, temperature))
    if status == STATUS_DEPLOYED and altitude < altitude_treshold:
        status = STATUS_TOUCHDOWN
        ticks_touchdown = time.ticks_ms()
        log_buffer.append(f"{timestamp}|{FRAME_LOG}|TOUCHDOWN")

while True:
    buzz.on()
    time.sleep(0.1)
    buzz.off()
    time.sleep(0.4)
    