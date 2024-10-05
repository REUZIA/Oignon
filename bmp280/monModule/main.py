from micropython import const
from picozero import Speaker
from machine import I2C, Pin
import neopixel
import utime as time
import ustruct

# Constantes pour le BMP280
_BMP280_ADDRESS_76 = const(0x76)  # Adresse I2C par défaut
_BMP280_ADDRESS_77 = const(0x77)  # Adresse alternative

_BMP280_REGISTER_CHIPID = const(0xD0)
_BMP280_REGISTER_RESET = const(0xE0)
_BMP280_REGISTER_STATUS = const(0xF3)
_BMP280_REGISTER_CONTROL = const(0xF4)
_BMP280_REGISTER_CONFIG = const(0xF5)
_BMP280_REGISTER_PRESSUREDATA = const(0xF7)
_BMP280_REGISTER_TEMPDATA = const(0xFA)
_BMP280_REGISTER_DIG_T1 = const(0x88)
_BMP280_REGISTER_DIG_T2 = const(0x8A)
_BMP280_REGISTER_DIG_T3 = const(0x8C)
_BMP280_REGISTER_DIG_P1 = const(0x8E)
_BMP280_REGISTER_DIG_P2 = const(0x90)
_BMP280_REGISTER_DIG_P3 = const(0x92)
_BMP280_REGISTER_DIG_P4 = const(0x94)
_BMP280_REGISTER_DIG_P5 = const(0x96)
_BMP280_REGISTER_DIG_P6 = const(0x98)
_BMP280_REGISTER_DIG_P7 = const(0x9A)
_BMP280_REGISTER_DIG_P8 = const(0x9C)
_BMP280_REGISTER_DIG_P9 = const(0x9E)

# Modes de puissance
BMP280_POWER_SLEEP = const(0)
BMP280_POWER_FORCED = const(1)
BMP280_POWER_NORMAL = const(3)

# Oversampling
BMP280_OS_ULTRALOW = const(0)
BMP280_OS_LOW = const(1)
BMP280_OS_STANDARD = const(2)
BMP280_OS_HIGH = const(3)
BMP280_OS_ULTRAHIGH = const(4)

# Standby settings in ms
BMP280_STANDBY_0_5 = const(0)
BMP280_STANDBY_62_5 = const(1)
BMP280_STANDBY_125 = const(2)
BMP280_STANDBY_250 = const(3)
BMP280_STANDBY_500 = const(4)
BMP280_STANDBY_1000 = const(5)
BMP280_STANDBY_2000 = const(6)
BMP280_STANDBY_4000 = const(7)

# IIR Filter setting
BMP280_IIR_FILTER_OFF = const(0)
BMP280_IIR_FILTER_2 = const(1)
BMP280_IIR_FILTER_4 = const(2)
BMP280_IIR_FILTER_8 = const(3)
BMP280_IIR_FILTER_16 = const(4)

# Matrix de suréchantillonnage (Oversampling)
_BMP280_OS_MATRIX = [
    [1, 1, 7],
    [2, 1, 9],
    [4, 1, 14],
    [8, 1, 23],
    [16, 2, 44]
]

# Cas d'utilisation
BMP280_CASE_HANDHELD_LOW = const(0)
BMP280_CASE_HANDHELD_DYN = const(1)
BMP280_CASE_WEATHER = const(2)
BMP280_CASE_FLOOR = const(3)
BMP280_CASE_DROP = const(4)
BMP280_CASE_INDOOR = const(5)

# Matrix pour les cas d'utilisation
_BMP280_CASE_MATRIX = [
    [BMP280_POWER_NORMAL, BMP280_OS_ULTRAHIGH, BMP280_IIR_FILTER_4, BMP280_STANDBY_62_5],
    [BMP280_POWER_NORMAL, BMP280_OS_STANDARD, BMP280_IIR_FILTER_16, BMP280_STANDBY_0_5],
    [BMP280_POWER_FORCED, BMP280_OS_ULTRALOW, BMP280_IIR_FILTER_OFF, BMP280_STANDBY_0_5],
    [BMP280_POWER_NORMAL, BMP280_OS_STANDARD, BMP280_IIR_FILTER_4, BMP280_STANDBY_125],
    [BMP280_POWER_NORMAL, BMP280_OS_LOW, BMP280_IIR_FILTER_OFF, BMP280_STANDBY_0_5],
    [BMP280_POWER_NORMAL, BMP280_OS_ULTRAHIGH, BMP280_IIR_FILTER_16, BMP280_STANDBY_0_5]
]

class BMP280:
    def __init__(self, i2c, addr=_BMP280_ADDRESS_76, use_case=BMP280_CASE_HANDHELD_DYN):
        self.i2c = i2c
        self.addr = addr

        # Lire les données de calibration
        self._T1 = ustruct.unpack('<H', self._read(_BMP280_REGISTER_DIG_T1, 2))[0]
        self._T2 = ustruct.unpack('<h', self._read(_BMP280_REGISTER_DIG_T2, 2))[0]
        self._T3 = ustruct.unpack('<h', self._read(_BMP280_REGISTER_DIG_T3, 2))[0]
        self._P1 = ustruct.unpack('<H', self._read(_BMP280_REGISTER_DIG_P1, 2))[0]
        self._P2 = ustruct.unpack('<h', self._read(_BMP280_REGISTER_DIG_P2, 2))[0]
        self._P3 = ustruct.unpack('<h', self._read(_BMP280_REGISTER_DIG_P3, 2))[0]
        self._P4 = ustruct.unpack('<h', self._read(_BMP280_REGISTER_DIG_P4, 2))[0]
        self._P5 = ustruct.unpack('<h', self._read(_BMP280_REGISTER_DIG_P5, 2))[0]
        self._P6 = ustruct.unpack('<h', self._read(_BMP280_REGISTER_DIG_P6, 2))[0]
        self._P7 = ustruct.unpack('<h', self._read(_BMP280_REGISTER_DIG_P7, 2))[0]
        self._P8 = ustruct.unpack('<h', self._read(_BMP280_REGISTER_DIG_P8, 2))[0]
        self._P9 = ustruct.unpack('<h', self._read(_BMP280_REGISTER_DIG_P9, 2))[0]

        # Initialisation des variables internes
        self._t_raw = 0
        self._t_fine = 0
        self._t = 0

        self._p_raw = 0
        self._p = 0

        self.read_wait_ms = 0  # intervalle entre la mesure forcée et la lecture
        self._new_read_ms = 200  # intervalle entre les lectures
        self._last_read_ts = 0

        if use_case is not None:
            self.use_case(use_case)

    def _read(self, addr, size=1):
        """Lecture des données depuis le registre I2C spécifié."""
        return self.i2c.readfrom_mem(self.addr, addr, size)

    def _write(self, addr, data):
        """Écriture des données dans le registre I2C spécifié."""
        if not isinstance(data, bytearray):
            data = bytearray([data])
        self.i2c.writeto_mem(self.addr, addr, data)

    def _gauge(self):
        """Lecture de toutes les données de capteur en une fois (comme spécifié dans le document technique)."""
        d = self._read(_BMP280_REGISTER_PRESSUREDATA, 6)

        self._p_raw = (d[0] << 12) + (d[1] << 4) + (d[2] >> 4)
        self._t_raw = (d[3] << 12) + (d[4] << 4) + (d[5] >> 4)

        self._t_fine = 0
        self._t = 0
        self._p = 0

    def reset(self):
        """Réinitialise le capteur BMP280."""
        self._write(_BMP280_REGISTER_RESET, 0xB6)

    def load_test_calibration(self):
        """Charge les données de calibration de test."""
        self._T1 = 27504
        self._T2 = 26435
        self._T3 = -1000
        self._P1 = 36477
        self._P2 = -10685
        self._P3 = 3024
        self._P4 = 2855
        self._P5 = 140
        self._P6 = -7
        self._P7 = 15500
        self._P8 = -14600
        self._P9 = 6000

    def load_test_data(self):
        """Charge les données de test pour température et pression."""
        self._t_raw = 519888
        self._p_raw = 415148

    def print_calibration(self):
        """Affiche les données de calibration."""
        print("T1: {} {}".format(self._T1, type(self._T1)))
        print("T2: {} {}".format(self._T2, type(self._T2)))
        print("T3: {} {}".format(self._T3, type(self._T3)))
        print("P1: {} {}".format(self._P1, type(self._P1)))
        print("P2: {} {}".format(self._P2, type(self._P2)))
        print("P3: {} {}".format(self._P3, type(self._P3)))
        print("P4: {} {}".format(self._P4, type(self._P4)))
        print("P5: {} {}".format(self._P5, type(self._P5)))
        print("P6: {} {}".format(self._P6, type(self._P6)))
        print("P7: {} {}".format(self._P7, type(self._P7)))
        print("P8: {} {}".format(self._P8, type(self._P8)))
        print("P9: {} {}".format(self._P9, type(self._P9)))

    @property
    def chip_id(self):
        """Renvoie l'identifiant unique du capteur BMP280."""
        return self._read(_BMP280_REGISTER_CHIPID, 1)[0]

    @property
    def temperature(self):
        """Calcul et renvoie la température en degrés Celsius."""
        if (self._t == 0) and (self._t_raw > 0):
            var1 = ((((self._t_raw >> 3) - (self._T1 << 1))) * (self._T2)) >> 11
            var2 = (((((self._t_raw >> 4) - (self._T1)) * ((self._t_raw >> 4) - (self._T1))) >> 12) * (self._T3)) >> 14
            self._t_fine = var1 + var2
            self._t = (self._t_fine * 5 + 128) >> 8

        return self._t / 100.0  # température en degrés Celsius

    @property
    def pressure(self):
        """Calcul et renvoie la pression en Pascals."""
        if (self._p == 0) and (self._p_raw > 0) and (self._t_fine > 0):
            var1 = (self._t_fine) - 128000
            var2 = var1 * var1 * self._P6
            var2 = var2 + ((var1 * self._P5) << 17)
            var2 = var2 + ((self._P4) << 35)
            var1 = ((var1 * var1 * self._P3) >> 8) + ((var1 * self._P2) << 12)
            var1 = (((1) << 47) + var1) * (self._P1) >> 33

            if var1 == 0:
                return 0

            p = 1048576 - self._p_raw
            p = (((p << 31) - var2) * 3125) // var1
            var1 = ((self._P9) * (p >> 13) * (p >> 13)) >> 25
            var2 = ((self._P8) * p) >> 19
            p = ((p + var1 + var2) >> 8) + ((self._P7) << 4)

            self._p = p

        return self._p / 256.0  # pression en Pascals

    def use_case(self, case):
        """Configure le capteur selon un cas d'utilisation prédéfini."""
        self.power_mode, os_mode, iir_mode, standby = _BMP280_CASE_MATRIX[case]

        # Mise à jour de l'intervalle d'attente entre lecture et mesure forcée
        self._new_read_ms = 1000 * (_BMP280_OS_MATRIX[os_mode][2] + 0.5) / 1000

        # Configuration du capteur BMP280 selon le cas d'utilisation
        self._write(_BMP280_REGISTER_CONTROL, (os_mode << 5) + (os_mode << 2) + self.power_mode)
        self._write(_BMP280_REGISTER_CONFIG, (standby << 5) + (iir_mode << 2))

    def force_measure(self):
        """Force une mesure sur le capteur BMP280."""
        self._write(_BMP280_REGISTER_CONTROL, (self.os_mode << 5) + (self.os_mode << 2) + BMP280_POWER_FORCED)

    def update_sensor(self):
        """Met à jour les données de température et de pression."""
        ts = time.ticks_ms()
        if self._last_read_ts == 0 or time.ticks_diff(ts, self._last_read_ts) >= self._new_read_ms:
            if self.power_mode == BMP280_POWER_FORCED:
                self.force_measure()
                time.sleep_ms(self.read_wait_ms)
            self._gauge()
            self._last_read_ts = ts

# Configuration I2C pour Raspberry Pi Pico
i2c = I2C(1, scl=Pin(3), sda=Pin(2))  # Ajustez les broches SCL et SDA si nécessaire

# Scannez les périphériques I2C pour détecter l'adresse du BMP280
devices = i2c.scan()

if not devices:
    raise Exception("Aucun périphérique I2C trouvé. Vérifiez les connexions.")

if _BMP280_ADDRESS_76 in devices:
    bmp_addr = _BMP280_ADDRESS_76
elif _BMP280_ADDRESS_77 in devices:
    bmp_addr = _BMP280_ADDRESS_77
else:
    raise Exception("BMP280 non détecté. Vérifiez l'adresse et les connexions.")

# Initialisation du capteur BMP280
bmp = BMP280(i2c, addr=bmp_addr)

def actual_pressure():
    bmp.update_sensor()
    temperature = bmp.temperature
    pressure=bmp.pressure
    print("Pression : {:.2f} hPa".format(pressure / 100))
    time.sleep(0.1)
    return pressure/100


#definition 
pressure_actual=0
liste_actual_pressure_flush=[]
liste_actual_pressure=[]
iterator_liste=0
dec = "SOL"
Etat="Aucun"
ecart=1
ecart_pas=1


#Allumage de la led en vert
np = neopixel.NeoPixel(machine.Pin(17), 1)
np[0]=(0,120,0)
np.write()
time.sleep(0.1)

np[0]=(0,0,0)
np.write()
time.sleep(0.1)

np[0]=(0,120,0)
np.write()
time.sleep(0.1)

np[0]=(0,0,0)
np.write()
time.sleep(0.3)

#Son 1
speaker = Speaker(25)
speaker.play(500)
time.sleep(0.2)


#Clignotement en vert et rouge

# Son 2

# Algo 2 : 

while len(liste_actual_pressure_flush)<20:
    liste_actual_pressure_flush.append(actual_pressure())
    np[0]=(0,120,120)
    np.write()
    time.sleep(0.001)
    np[0]=(0,0,0)
    np.write()
    time.sleep(0.1)

    

while len(liste_actual_pressure)<=4:
    liste_actual_pressure.append(actual_pressure())
    np[0]=(120,120,120)
    np.write()
    time.sleep(0.001)
    np[0]=(0,0,0)
    np.write()
    time.sleep(0.001)


while len(liste_actual_pressure)>4:
    i=len(liste_actual_pressure)
    moy=(liste_actual_pressure[i-2]+liste_actual_pressure[i-3]+liste_actual_pressure[i-4])/3
    np[0]=(10,180,50)
    np.write()
    time.sleep(0.001)
    np[0]=(0,0,0)
    np.write()
    time.sleep(0.1)
    print("pas moyen :", moy)
    print("actual",liste_actual_pressure[i-1])
    if(abs(liste_actual_pressure[i-1]-moy)>ecart):
        print("Decollage")
        np[0]=(180,0,120)
        np.write()
        time.sleep(1)
        break
    else :
        liste_actual_pressure.append(actual_pressure())

while len(liste_actual_pressure)>4:
    i=len(liste_actual_pressure)
    #pas moyen 
    pas_moyen= (abs(liste_actual_pressure[i-1]-liste_actual_pressure[i-2]))
    if (abs(pas_moyen) < ecart ): 
        print("Apogée")
        ########### GPIO OUT HIGH
        time.sleep(1)
        break
    else :
        liste_actual_pressure.append(actual_pressure())

liste_actual_pressure.append(actual_pressure())
liste_actual_pressure.append(actual_pressure())
liste_actual_pressure.append(actual_pressure())
liste_actual_pressure.append(actual_pressure())

while len(liste_actual_pressure)>4:
    i=len(liste_actual_pressure)
    #pas moyen 
    pas_moyen= (abs(liste_actual_pressure[i-1]-liste_actual_pressure[i-2]))
    if (abs(pas_moyen) < ecart ): 
        print("Atterissage")
        time.sleep(1)
        break
    else :
        liste_actual_pressure.append(actual_pressure())
