import machine
import os
import sdcard
from _thread import allocate_lock
import time
import gc


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
        isGood : bool = True
        try : 
            self.fichier.write(text)
            self.indexNbFlushData += 1
            if self.indexNbFlushData == self.nBflushData:
                self.fermet()
                self.ouvrir()
                self.indexNbFlushData = 0
        except : 
            isGood:bool=False
        return isGood

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
        nbspi: int = 0,
        baudrate: int = 10000,
        pinSck: int = 2,
        pinMiso: int = 3,
        pinMosi: int = 4,
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
        self.pinSC = pinSC
        self.fichierName = fichierName
        self.colmSvg = colmSvg
        self.attAvantRecoSD = 5
        self.conveurAttAvantRecoSD = 0

        self.lock = allocate_lock()  # Créer un verrou

        self.spi.init()

        self.isSDopen = False

        self.initSD()

    def initSD(self):
        try:
            self.isSDopen = True

            self.sd = sdcard.SDCard(
                self.spi, machine.Pin(self.pinSC)
            )  # Compatible avec le PCB

            self.vfs = os.VfsFat(self.sd)
            self.mount()
            self.fich = (
                FichierInteligen(  # vas crée un nouv fichier à chaque déconnection sd
                    "/fc/" + self.fichierName, 30
                )
            )  # représente le nombre de trame avant écriture dans la SD

            print(os.listdir("/fc"))
            self.write(self.colmSvg)

        except:
            print("faile init sd")
            self.isSDopen = False

    def is_sd_mounted(self):
        try:
            # Essayez de lister les fichiers du répertoire monté
            os.listdir("/fc")
            return True  # Le système de fichiers est monté
        except OSError:
            return False  # Le système de fichiers n'est pas monté

    def write(self, chaineCara: str) -> bool:
        res: bool = False
        if self.isSDopen:
            with self.lock:  # Acquérir le verrou
                res = self.fich.write(chaineCara + "\n")
            if res:
                return res
        self.conveurAttAvantRecoSD+=1
        print("erreur")
        if self.conveurAttAvantRecoSD >=self.attAvantRecoSD:
           self.conveurAttAvantRecoSD=1 

        if self.conveurAttAvantRecoSD==1:
            self.conveurAttAvantRecoSD=1
            print("init sd")
            self.initSD()
        return res

    def read(self) -> str:
        res: str = ""
        if self.isSDopen:
            with self.lock:
                self.fich.read()
        else :
            self.isSDopen = False
        return res

    def mount(self) -> None:
        if self.isSDopen:
            with self.lock:  # Acquérir le verrou
                if not self.is_sd_mounted():
                    os.mount(self.vfs, "/fc")
            
        else:
            self.initSD()  # on essaye de la monter

    def umount(self) -> None:
        if not self.isSDopen:
            try : 
                with self.lock:  # Acquérir le verrou
                    if self.is_sd_mounted():
                        os.umount("/fc")
            except:
                pass
        else:
            pass  # plus de sd


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
        nbspi=0,
        baudrate=20000,
        pinSck=2,
        pinMiso=4,
        pinMosi=3,
        pinSC=5,
        fichierName="TEST",
        colmSvg="",
    )

    # sd = SDOignon(
    #     nbspi = 0,
    #     baudrate = 10000,
    #     pinSck = 18,
    #     pinMiso = 16,
    #     pinMosi = 19,
    #     pinSC = 5,
    #     fichierName = "TEST",
    #     colmSvg = ""
    # )

    # gc.collect()

    print("Fin inint")
    for i in range(10):
        print("ecire")
        sd.write("oui;ono;oui")
        time.sleep(0.1)

    # print("res" , sd.read())
    sd.umount()
