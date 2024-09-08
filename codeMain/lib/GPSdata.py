import machine
from utime import sleep
from micropyGPS import MicropyGPS  # https://github.com/inmcm/micropyGPS


class GPSdata:
    def __init__(self,uartPin,baudRate=9600) -> None:
            self.uart= machine.UART(uartPin,baudrate=baudRate)  # initialisation UART
            self.gps = MicropyGPS() # création d'un objet GPS
    
    def update(self)->int:
        if self.uart.any(): 
            donnees_brutes = str(self.uart.readline())
            for x in donnees_brutes:
                self.gps.update(x)

            return 1
        return 0
    
    def to_sleep(self)->None:
        pass
    def wake_up(self)->None:
        pass

    def __str__(self) -> str:
        self.update()
        return str(self.gps.latitude_string())+";"+str(self.gps.longitude_string())+";"+str(self.gps.altitude())+";"+str(self.gps.speed_string('kph'))+";"+str(self.gps.date_string('s_dmy'))
    
if __name__ == "__main__":
    gp = GPSdata(1)
    print(gp)