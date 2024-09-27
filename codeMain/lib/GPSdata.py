import machine
import time
from micropyGPS import MicropyGPS  # https://github.com/inmcm/micropyGPS


class GPSdata:
    def __init__(
        self, uartPin, baudRate=9600, tx=8, rx=9, timeout=1000, timeout_char=1000
    ) -> None:
        self.uart = machine.UART(
            uartPin,
            baudrate=baudRate,
            tx=machine.Pin(tx),
            rx=machine.Pin(rx),
            timeout=timeout,
            timeout_char=timeout_char,
        )  # initialisation UART
        self.gps = MicropyGPS()  # création d'un objet GPS

    def convert_to_dms(self, coords: list) -> str:
        """_summary_

        Args:
            coords (list): altitude ou longiture

        Returns:
            str: degree:minutes:seconds:direction
        """
        # avoir les valeur
        degrees: int = coords[0]
        decimal_minutes: float = coords[1]
        direction: str = coords[2]
        # Séparer la partie entière des minutes de la partie décimale
        minutes: int = int(decimal_minutes)
        # Convertir la partie décimale des minutes en secondes
        seconds: float = (decimal_minutes - minutes) * 60
        # Retourner le format en DMS avec 1 décimale pour les secondes
        return f"{degrees}:{minutes}:{seconds:.1f}:{direction}"

    def update(self) -> int:
        if self.uart.any():

            donnees_brutes = self.uart.readline()  # fonction bloquante
            if donnees_brutes is None :

                return 0
            else :

                donnees_brutes = str(donnees_brutes)
                for x in donnees_brutes:
                    self.gps.update(x)
                return 1
        else :

            return 0

    def to_sleep(self) -> None:
        pass

    def wake_up(self) -> None:
        pass

    def __str__(self) -> str:
        """renvoie donner gps après actualisation 
        latitude (degree:minutes:seconds:direction)
        longitude (degree:minutes:seconds:direction)
        altitude
        nombre_satellite_utiliser
        nombre_satellite_visible 
        vitesse(km/h)

        Returns:
            str: _description_
        """
        if self.update():
            lati: str = self.convert_to_dms(self.gps.latitude)
            longi: str = self.convert_to_dms(self.gps.longitude)
            alti: str = str(self.gps.altitude)
            satelieNBinUse: str = str(self.gps.satellites_in_use)
            # print("satelite:", self.gps.satellites_visible())
            satelieNBvisible: str = str(len(self.gps.satellites_visible()))
            speed: str = self.gps.speed_string("km/h")[:-5]
            hour: str = str(self.gps.timestamp[0])
            minute: str = str(self.gps.timestamp[1])
            second: str = str(self.gps.timestamp[2])
            showhour: str = f"{hour}:{minute}:{second}"  # self.gps.gprmc()

            return f"{lati};{longi};{alti};{satelieNBinUse};{satelieNBvisible};{speed};{showhour}"
            # latitude;longitude;altitude;nombre_satellite_utiliser;nombre_satellite_visible;vitesse;heure
        else :
            return "00;00;00;00;00;00;00"


if __name__ == "__main__":
    gp = GPSdata(1, rx=9, tx=8)
    while True:
        print(gp)
        time.sleep(0.5)

"""
# tester uart 
import machine
from time import sleep

# Define the UART pins and create a UART object
gps_serial = machine.UART(1, baudrate=9600, tx=8, rx=9)

while True:
    if gps_serial.any():
        line = gps_serial.readline()  # Read a complete line from the UART
        if line:
            line = line.decode('utf-8')
            print(line.strip())
    else:
        print("r")
    sleep(1)
"""