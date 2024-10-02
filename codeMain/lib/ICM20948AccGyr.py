#https://github.com/jposada202020/MicroPython_ICM20948/tree/master
import time
from machine import Pin, I2C
import icm20948


class ICM20948AccGyr:
    def __init__(self, i2c: I2C):
        # Initialisation de l'objet ICM20948 avec l'interface I2C fournie
        self.icm = icm20948.ICM20948(i2c)

        # Configuration de l'ICM20948
        self.icm.clock_select = icm20948.CLK_SELECT_BEST  # Sélection de l'horloge la plus précise

        # Configuration de l'accéléromètre
        self.icm.accelerometer_range = icm20948.RANGE_8G # Plage de détection de l'accélération maximale à ±8g
        self.icm.acc_dlpf_cutoff = icm20948.FREQ_246_0 # Fréquence de coupure du filtre passe-bas de l'accéléromètre à 246 Hz

        # Configuration du gyroscope
        self.icm.gyro_full_scale = icm20948.FS_500_DPS # Plage de mesure de la rotation maximale à ±500 degrés par seconde
        self.icm.gyro_dlpf_cutoff = icm20948.G_FREQ_11_6 # Fréquence de coupure du filtre passe-bas du gyroscope à 11,6 Hz

        # Activation des capteurs
        self.icm.gyro_enabled = icm20948.GYRO_ENABLED
        self.icm.acc_enabled = icm20948.ACC_ENABLED

    def to_sleep(self) -> None:
        # Met l'ICM20948 en mode veille
        self.icm.sleep = icm20948.SLEEP_ENABLED

    def wake_up(self) -> None:
        # Réveille l'ICM20948 du mode veille
        self.icm.sleep = icm20948.SLEEP_DISABLED

    @property
    def acceleration(self) -> tuple[float, float, float]:
        # Renvoie les valeurs d'accélération (x, y, z) en g
        return self.icm.acceleration

    @property
    def gyro(self) -> tuple[float, float, float]:
        # Renvoie les valeurs de rotation (x, y, z) en degrés par seconde
        return self.icm.gyro

    def __str__(self):
        # Renvoie quand str du l'object une chaîne de caractères représentant les valeurs d'accélération et de rotation
        accx, accy, accz = self.acceleration
        gyrox, gyroy, gyroz = self.gyro
        return f"{accx:.2f}:{accy:.2f}:{accz:.2f};{gyrox:.2f}:{gyroy:.2f}:{gyroz:.2f}"

if __name__ == "__main__":
    #init
    i2c = I2C(1, sda=Pin(6), scl=Pin(7))
    sen = ICM20948AccGyr(i2c)
    
    # commande 
    sen.to_sleep()
    time.sleep(0.1)
    print(sen.icm.sleep)
    sen.wake_up()
    time.sleep(0.1)
    print(sen.icm.sleep)

    # affiche valeur
    while True:
        # accx, accy, accz = sen.icm.acceleration
        # gyrox, gyroy, gyroz = sen.icm.gyro
        # print(f"x: {accx:.2f}m/s2, y: {accy:.2f}m/s2, z: {accz:.2f}m/s2")
        # print("x:{:.2f}deg/s, y:{:.2f}deg/s, z:{:.2f}deg/s".format(gyrox, gyroy, gyroz))
        print(sen)

        print()
        time.sleep(1)
