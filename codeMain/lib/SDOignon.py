import machine
import os
import sdcard

# ! vider donbner sd avant envoie

class FichierInteligen:
    def __init__(self, fichierName,nBflushData):
        """on créra un nouv fichier avec le len des fichier davant"""
        self.fichierName=fichierName + str(len(os.listdir("/fc")))+".csv"
        self.nBflushData = nBflushData
        self.indexNbFlushData = 0

        # ouvrir automatiquement
        self.fichier = open(self.fichierName, "w")

    def ouvrir(self)->None:
        if not self.fichier:
            try:
                self.fichier = open(self.fichierName, "a")
            except OSError as e:
                self.fichier=None
                print(f"Erreur d'ouverture du fichier : {e}")
            return None
        
    def fermet(self)->None: 
        if self.fichier:
            try:
                self.fichier.close()
                self.fichier=None
            except OSError as e:
                print(f"Erreur de fermeture du fichier : {e}")

    def write(self,text)->None:
        """tout les """
        self.fichier.write(text)
        self.indexNbFlushData+=1
        if self.indexNbFlushData == self.nBflushData:
            self.fermet()
            self.ouvrir()
            self.indexNbFlushData=0
    
    def read(self)->str:
        self.fermet()
        fichierRead = open(self.fichierName, "r")
        res = fichierRead.read()
        fichierRead.close()
        self.ouvrir()
        return res

class SDOignon:
    def __init__(self, nbspi, pinSck, pinMiso, pinMosi, pinSC, fichierName):
        self.spi = machine.SPI(
            nbspi,
            baudrate=10000,
            polarity=1,
            phase=0,
            mosi=pinMiso,
            sck=pinSck,
            miso=pinMosi,
        )

        self.spi.init()

        self.sd = sdcard.SDCard(self.spi, pinSC)  # Compatible with PCB

        self.vfs = os.VfsFat(self.sd)

        self.mount()
        self.fich = FichierInteligen("/fc/" + fichierName,10)

        
        print("Filesystem check")
        print(os.listdir("/fc"))
        self.add("----------------\n")


    def is_sd_mounted(self):
        try:
            # Essayez de lister les fichiers du répertoire monté
            os.listdir('/fc')  
            return True  # Le système de fichiers est monté
        except OSError:
            return False  # Le système de fichiers n'est pas monté


    def right(self, chaineCara: str) -> None:
        """Attention efface tout les donnée"""
        print("desactiver")


    def add(self, chaineCara: str) -> None:
        self.fich.write(chaineCara+"\n")
        print("bytes written")

    def read(self) -> str:
        return self.fich.read()

    def mount(self) -> None:
        if not self.is_sd_mounted():
            os.mount(self.vfs, "/fc")

    def umount(self) -> None:
        if self.is_sd_mounted():
            os.umount("/fc")


if __name__ == "__main__":

    sd = SDOignon(
        1,
        machine.Pin(10),
        machine.Pin(11),
        machine.Pin(12),
        machine.Pin(13),
        "data",
    )
    sd.add("oui")
    print(sd.read())
    sd.umount()