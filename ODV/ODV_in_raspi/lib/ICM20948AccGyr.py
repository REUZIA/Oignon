#https://github.com/jposada202020/MicroPython_ICM20948/tree/master
import time
from machine import Pin, I2C
import icm20948


class ICM20948AccGyr:
    def __init__(self, i2c_bus:int=1,sda_nbPin:int=6,scl_nbPin:int=7):
        self.i2c =  I2C(i2c_bus, sda=Pin(sda_nbPin), scl=Pin(scl_nbPin))
        self.isinit:bool= True
        self.init()

    def init(self)->None:
        
        try :
            self.isinit:bool= True 
            # Initialisation de l'objet ICM20948 avec l'interface I2C fournie
            self.icm = icm20948.ICM20948(self.i2c)

            # Configuration de l'ICM20948
            self.icm.clock_select = icm20948.CLK_SELECT_BEST  # Sélection de l'horloge la plus précise

            # Configuration de l'accéléromètre # voir doc codeMain
            self.icm.accelerometer_range = icm20948.RANGE_8G 
            self.icm.acc_dlpf_cutoff = icm20948.FREQ_246_0 
            # Configuration du gyroscope
            self.icm.gyro_full_scale = icm20948.FS_500_DPS 
            self.icm.gyro_dlpf_cutoff = icm20948.G_FREQ_51_2

            # Activation des capteurs
            self.icm.gyro_enabled = icm20948.GYRO_ENABLED
            self.icm.acc_enabled = icm20948.ACC_ENABLED
        except OSError as e:
            print("Error accessing ICM:", e)
            self.isinit:bool= False

    def to_sleep(self) -> None:
        if self.isinit:
            # Met l'ICM20948 en mode veille
            self.icm.sleep = icm20948.SLEEP_ENABLED

    def wake_up(self) -> None:
        if self.isinit:
            # Réveille l'ICM20948 du mode veille
            self.icm.sleep = icm20948.SLEEP_DISABLED

    @property
    def acceleration(self) -> tuple[float, float, float]:
        # Renvoie les valeurs d'accélération (x, y, z) en g
        if self.isinit:
            return self.icm.acceleration
        return (0.0,0.0,0.0)

    @property
    def gyro(self) -> tuple[float, float, float]:
        # Renvoie les valeurs de rotation (x, y, z) en degrés par seconde
        if self.isinit:
            return self.icm.gyro
        return (0.0,0.0,0.0)
    
    def __str__(self):
        # Renvoie quand str du l'object une chaîne de caractères représentant les valeurs d'accélération et de rotation
        if self.isinit :
            try :
                accx, accy, accz = self.acceleration
                gyrox, gyroy, gyroz = self.gyro
            except:
                self.init()
                accx, accy, accz = (0.0,0.0,0.0)
                gyrox, gyroy, gyroz = (0.0,0.0,0.0)
        else:
            self.init()
            accx, accy, accz = (0.0,0.0,0.0)
            gyrox, gyroy, gyroz = (0.0,0.0,0.0)

        return f"{accx:.2f}:{accy:.2f}:{accz:.2f};{gyrox:.2f}:{gyroy:.2f}:{gyroz:.2f}"

if __name__ == "__main__":
    #init
    sen = ICM20948AccGyr(i2c_bus=1,sda_nbPin=6,scl_nbPin=7)
    
    # commande 
    sen.to_sleep()
    time.sleep(0.1)
    sen.wake_up()
    time.sleep(0.1)
    

    # affiche valeur
    for i in range(1):
        # accx, accy, accz = sen.icm.acceleration
        # gyrox, gyroy, gyroz = sen.icm.gyro
        # print(f"x: {accx:.2f}m/s2, y: {accy:.2f}m/s2, z: {accz:.2f}m/s2")
        # print("x:{:.2f}deg/s, y:{:.2f}deg/s, z:{:.2f}deg/s".format(gyrox, gyroy, gyroz))
        print(f"[{i}]",sen)

        time.sleep(1)
