import machine
import os
import sdcard
from _thread import allocate_lock


# ! vider donbner sd avant envoie


class FichierInteligen:
    def __init__(self, fichierName, nBflushData):
        """on créra un nouv fichier avec le len des fichier davant"""
        self.fichierName = fichierName + str(len(os.listdir("/fc"))) + ".csv"
        self.nBflushData = nBflushData
        self.indexNbFlushData = 0

        # ouvrir automatiquement
        self.fichier = open(self.fichierName, "w")

    def ouvrir(self) -> None:
        if not self.fichier:
            try:
                self.fichier = open(self.fichierName, "a")
            except OSError as e:
                self.fichier = None
                print(f"Erreur d'ouverture du fichier : {e}")
            return None

    def fermet(self) -> None:
        if self.fichier:
            try:
                self.fichier.close()
                self.fichier = None
            except OSError as e:
                print(f"Erreur de fermeture du fichier : {e}")

    def write(self, text) -> None:
        """tout les"""
        self.fichier.write(text)
        self.indexNbFlushData += 1
        if self.indexNbFlushData == self.nBflushData:
            print("femet")
            self.fermet()
            self.ouvrir()
            print("on")
            self.indexNbFlushData = 0

    def read(self) -> str:
        self.fermet()
        fichierRead = open(self.fichierName, "r")
        res = fichierRead.read()
        fichierRead.close()
        self.ouvrir()
        return res


class SDOignon:
    def __init__(
        self,
        nbspi: int = 2,
        baudrate: int = 10000,
        pinSck: int = 4, 
        pinMiso: int = 3,
        pinMosi: int = 5,
        pinSC: int = 5,
        fichierName: str = "data",
        colmSvg: str = "",
    ):
        self.spi = machine.SPI(
            nbspi,
            baudrate=baudrate,
            polarity=1,
            phase=0,
            mosi=machine.Pin(pinMosi),
            sck=machine.Pin(pinSck),
            miso=machine.Pin(pinMiso),
        )

        self.lock = allocate_lock()  # Créer un verrou

        self.spi.init()

        self.sd = sdcard.SDCard(self.spi, machine.Pin(pinSC))  # Compatible with PCB

        self.vfs = os.VfsFat(self.sd)

        self.mount()
        self.fich = FichierInteligen("/fc/" + fichierName, 100)

        print("Filesystem check")
        print(os.listdir("/fc"))
        self.write(colmSvg)



    def is_sd_mounted(self):
        try:
            # Essayez de lister les fichiers du répertoire monté
            os.listdir("/fc")
            return True  # Le système de fichiers est monté
        except OSError:
            return False  # Le système de fichiers n'est pas monté

    def write(self, chaineCara: str) -> None:
        with self.lock:  # Acquérir le verrou
            self.fich.write(chaineCara + "\n")
            print("bytes written")

    def read(self) -> str:
        with self.lock:
            return self.fich.read()

    def mount(self) -> None:
        with self.lock:  # Acquérir le verrou
            if not self.is_sd_mounted():
                os.mount(self.vfs, "/fc")

    def umount(self) -> None:
        with self.lock:  # Acquérir le verrou
            if self.is_sd_mounted():
                os.umount("/fc")


if __name__ == "__main__":
    # sd = SDOignon(
    #     1,
    #     machine.Pin(10),
    #     machine.Pin(12),
    #     machine.Pin(11),
    #     machine.Pin(13),
    #     "data",
    # )

    sd = SDOignon(
        nbspi = 0,
        baudrate = 10000,
        pinSck = 2,
        pinMiso = 4, 
        pinMosi = 3,
        pinSC = 5,
        fichierName = "TEST",
        colmSvg = ""
    )

    sd.write("oui")
    print(sd.read())
    sd.umount()
