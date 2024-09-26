import machine
import time
from micropyGPS import MicropyGPS  # https://github.com/inmcm/micropyGPS

def convert_to_dms(coords):

        degrees, decimal_minutes, direction = coords
        # Séparer la partie entière des minutes de la partie décimale
        minutes = int(decimal_minutes)
        # Convertir la partie décimale des minutes en secondes
        seconds = (decimal_minutes - minutes) * 60
        # Retourner le format en DMS avec 1 décimale pour les secondes
        return f"{degrees}deg{minutes}'{seconds:.1f}\"{direction}"

class GPSdata:
    def __init__(self,uartPin,baudRate=9600,tx=8, rx=9, timeout=5000, timeout_char=5000) -> None:
            self.uart= machine.UART(uartPin,baudrate=baudRate,tx=machine.Pin(tx), rx=machine.Pin(rx), timeout=timeout, timeout_char=timeout_char)  # initialisation UART
            print(self.uart)
            self.gps = MicropyGPS() # création d'un objet GPS
    
    def update(self)->int:
        if self.uart.any(): 
            donnees_brutes = str(self.uart.readline())  #fonction bloquante
            for x in donnees_brutes:
                self.gps.update(x)

            return 1
        print("pas uart")
        return 0
    
    def to_sleep(self)->None:
        pass
    def wake_up(self)->None:
        pass

    def __str__(self) -> str:
        self.update()
        #return str(self.gps.latitude_string())+";"+str(self.gps.longitude_string())+";"+str(self.gps.altitude())+";"+str(self.gps.speed_string('kph'))+";"+str(self.gps.date_string('s_dmy'))
        # return str("00")+";"+str("00")+";"+str("00")+";"+str("00")+";"+str("00")
        return str(convert_to_dms(self.gps.latitude) + ";" + convert_to_dms(self.gps.longitude) + ";" +  self.gps.altitude() + ";" + self.gps.satellites_visible() + ";" + self.gps.speed_string('km/h') + ";" +  self.gps.gprmc())
        #latitude;longitude;altitude;nombre satellite;vitesse;heure

if __name__ == "__main__":
    gp = GPSdata(1,rx=9,tx=8)
    while True:
        print(gp)
        time.sleep(0.5)