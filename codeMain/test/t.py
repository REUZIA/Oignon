# code du module tom 
import machine, neopixel, bmp280, time
from machine import Pin, I2C, Timer
from picozero import Speaker
from micropython import const
from collections import deque
import rp2

# Tout revérifier
# Ajouter le GPIO
# changer le delay du fenetrage temporel
# changer les fonctions blocantes par des fonctions millis
# faire une explication de comment on flash
# nettoyer le git
# tester la monté


optimal_delay = const(900000)

altitude_treshold = const(15)  # for launch detection in m
speed_treshold = const(3)  # m/s
min_delay = const(5000)
max_delay = const(optimal_delay + 1000)


max_alt = const(300)  # Force deployment at this altitude


# Colors
COLOR_RED = const((5, 0, 0))  # STANDBY blink
COLOR_GREEN = const((0, 5, 0))  # STANDBY blink and forced deployment
COLOR_BLUE = const((0, 0, 5))  # LAUNCHED
COLOR_WHITE = const((5, 5, 5))  # DEPLOYED
COLOR_BLACK = const((0, 0, 0))  # OFF

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

led = neopixel.NeoPixel(Pin(17), 1)

# speaker = Speaker(25)

led_out = Pin(25, Pin.OUT)
led_out.value(0)


bmp = bmp280.BMP280(
    I2C(1, sda=Pin(2), scl=Pin(3)), use_case=bmp280.BMP280_CASE_HANDHELD_DYN
)
bmp_refresh_period = const(13)
bmp_last_measure_ticks = 0

# data 
f = open("DATA.txt", "a")
last_flush = 0


def flush_logs(buffer,f,last_flush,mustRight=False):
    timeNow = time.ticks_ms()
    if mustRight or (timeNow - last_flush > 500):    
        try:
            line = buffer
        except IndexError:
            time.sleep(0.01)

        if type(line) == str:
            if not line.endswith("\n"):
                line = buffer
                del buffer
            f.write(line)
        elif type(line) == tuple:
            f.write("|".join([str(value) for value in line]) + "\n")
        f.flush()
        last_flush = timeNow
    return last_flush

def write_color(color):
    led[0] = color
    led.write()

last_flush = flush_logs(f"{time.ticks_ms()}|{FRAME_LOG}|START",f,last_flush)# Log into buffer


# speaker.play(500)
time.sleep(0.1)

bmp_last_measure_ticks = 0
sea_level_pressure = 0


def get_bmp_data():
    global bmp_last_measure_ticks, sea_level_pressure
    time.sleep_ms(
        max(0, 1 + bmp_refresh_period - (time.ticks_ms() - bmp_last_measure_ticks))
    )  # Ensure "bmp_refresh_period" is waited between measurements

    #! pas sur while true
    bmp_last_measure_ticks = time.ticks_ms()
    pressure, temperature = bmp.pressure, bmp.temperature


    if sea_level_pressure == 0:
        sea_level_pressure = pressure  # Set reference pressure

    altitude = 44330 * (1.0 - pow(pressure / sea_level_pressure, 0.1903))
    return bmp_last_measure_ticks, altitude, pressure, temperature


def deploy():
    global ticks_deployed, status,last_flush
    if (
        time.ticks_ms() - ticks_launched > min_delay and status != STATUS_DEPLOYED
    ):  # If time elapsed since launch is greather than min_delay
        status = STATUS_DEPLOYED
        ticks_deployed = time.ticks_ms()
        last_flush = flush_logs(f"{ticks_deployed}|{FRAME_LOG}|DEPLOYED\n",f,last_flush,mustRight=True)# Log into buffer
        write_color(COLOR_WHITE)
        led_out.value(1)
        time.sleep(0.5)
        led_out.value(0)
    else:
        last_flush = flush_logs(f"{time.ticks_ms()}|{FRAME_LOG}|INVALID DEPLOY ORDER",f,last_flush,mustRight=True)# Log into buffers



def deploy_callback(t):
    global last_flush
    deploy()
    last_flush = flush_logs(f"{time.ticks_ms()}|{FRAME_LOG}|DEPLOYED BY TIMER",f,last_flush,mustRight=True)# Log into buffers


def avg_speed(altitude_buffer):
    speeds = list()
    for i in range(len(altitude_buffer) - 1):
        speeds.append(
            (altitude_buffer[i + 1][1] - altitude_buffer[i][1])
            / ((altitude_buffer[i + 1][0] - altitude_buffer[i][0]) / 1_000)
        )
    return sum(speeds) / len(speeds)



# FORCE DEPLOYEMENT
write_color(COLOR_GREEN)

time.sleep(2)

if rp2.bootsel_button():
    # ajouter le gpio
    last_flush = flush_logs(f"{time.ticks_ms()}|{FRAME_LOG}|FORCED DEPLOYMENT",f,last_flush,mustRight=True)# Log into buffers
    while True:
        write_color(COLOR_BLACK)
        time.sleep(0.8)
        write_color(COLOR_WHITE)
        time.sleep(0.1)

write_color(COLOR_RED)


# LAUNCH DETECTION
last_log_ticks = 0
timestamp, altitude, pressure, temperature = get_bmp_data()
last_flush = flush_logs((timestamp, FRAME_BMP, altitude, pressure, temperature),f,last_flush,mustRight=True)# Log into buffer
while status == STATUS_STANDBY:  # While waiting for LAUNCH
    timestamp, altitude, pressure, temperature = get_bmp_data()
    last_flush = flush_logs((timestamp, FRAME_BMP, altitude, pressure, temperature),f,last_flush)# Log into buffer

    if altitude > altitude_treshold:  # Detect launch
        last_flush = flush_logs(f"{timestamp}|{FRAME_LOG}|LAUNCHED",f,last_flush)
        changelog_buffer = True
        ticks_launched = timestamp
        status = STATUS_LAUNCHED
        timer = Timer(
            period=max_delay, mode=Timer.ONE_SHOT, callback=deploy_callback
        )  # Start backup timer
        break

    elif timestamp - last_log_ticks > 500:  # Log baro every 500 ms even if not launched
        last_flush = flush_logs((timestamp, FRAME_BMP, altitude, pressure, temperature),f,last_flush)# Log into buffers

        last_log_ticks = timestamp

    if (time.ticks_ms() % 100) < 50:  # Blink led
        write_color(COLOR_GREEN)
    else:
        write_color(COLOR_RED)

    if (time.ticks_ms() % 1_000) < 100:
        # speaker.play(500)
        time.sleep(0.1)

write_color(COLOR_BLUE)


del last_log_ticks

altitude_buffer = list()
timestamp, altitude, pressure, temperature = get_bmp_data()
last_flush = flush_logs((timestamp, FRAME_BMP, altitude, pressure, temperature),f,last_flush,mustRight=True)

while status == STATUS_LAUNCHED:  # While LAUNCHED not DEPLOYED
    timestamp, altitude, pressure, temperature = get_bmp_data()
    altitude_buffer.append((timestamp, altitude))

    if (
        len(altitude_buffer) > 15
    ):  # Rolling average across 15 measurements (15*13 = 195 ms)
        altitude_buffer.pop(0)

    last_flush = flush_logs((timestamp, FRAME_BMP, altitude, pressure, temperature),f,last_flush)


    if altitude > max_alt:
        deploy()
        last_flush = flush_logs(f"{timestamp}|{FRAME_LOG}|FORCED DEPLOYMENT",f,last_flush)

    if len(altitude_buffer) > 2:
        speed = avg_speed(altitude_buffer)
        last_flush = flush_logs(f"{timestamp}|{FRAME_SPEED}|{speed}",f,last_flush)
        if speed < speed_treshold:
            deploy()

            last_flush = flush_logs(f"{timestamp}|{FRAME_LOG}|DEPLOYED BY ALTI",f,last_flush)
    # write data


last_flush = flush_logs((timestamp, FRAME_BMP, altitude, pressure, temperature),f,last_flush,mustRight=True)
while (
    status == STATUS_DEPLOYED or time.ticks_ms() - ticks_touchdown < timeout
):  # Waiting for timeout ms after TOUCHDOWN
    timestamp, altitude, pressure, temperature = get_bmp_data()
    last_flush = flush_logs((timestamp, FRAME_BMP, altitude, pressure, temperature),f,last_flush)

    if status == STATUS_DEPLOYED and altitude < altitude_treshold:
        status = STATUS_TOUCHDOWN
        ticks_touchdown = time.ticks_ms()
        last_flush = flush_logs(f"{timestamp}|{FRAME_LOG}|TOUCHDOWN",f,last_flush)
    # write data

f.close()

"""
il faut faire
"""