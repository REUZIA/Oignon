DOC Oignon **ODC**

# à la fin quand on touche plus au code 
supprimer tout les elemnt test de la board 
vider la sd

# Composant 
- Carte PCB Lora + SD
- Carte PCB GPS + ICM
- Carte sd 64G vert
- Antenne gps 
- Antenne lora 

# Shema 
discode : https://discord.com/channels/610534406922174495/1263142960497688578/1291515100024541275

# SD
Protocole : 
    nbspi = 0,
    baudrate = 2000000,
    pinSck = 2,
    pinMiso = 4, 
    pinMosi = 3,
    pinSC = 5,

faut fair quand sd déco histoire de se reco 
vas essayer de reconnecter sd quand écire si pas ouvert, à chaque réouverture réssuite var écire un nouv fichier "dataX.csv"
"faile init sd" => surment problème pin pour sd non reconue faudra tester (code en dessous ) dans le constructeur pour voir l'erreur
```python
  self.sd = sdcard.SDCard(
      self.spi, machine.Pin(self.pinSC)
  )  # Compatible avec le PCB
```


sd prend formater en  fat

# ICM
Procole I2C : 
    sda=Pin(6)
    scl=Pin(7)

```python
Parametrage composant 
self.icm.accelerometer_range = icm20948.RANGE_8G # Plage de détection de l'accélération maximale à ±8g # ? 0.7Mach envion 1.8G on prend au dessus pour être su r
self.icm.acc_dlpf_cutoff = icm20948.FREQ_246_0 # Fréquence de coupure du filtre passe-bas de l'accéléromètre à 246 Hz
    # beaucoup vibration => je doit filter beaucoup => pourquoi c si haut 
# Configuration du gyroscope
self.icm.gyro_full_scale = icm20948.FS_500_DPS # Plage de mesure de la rotation maximale à ±500 degrés par seconde
self.icm.gyro_dlpf_cutoff = icm20948.G_FREQ_51_2 # Fréquence de coupure du filtre passe-bas du gyroscope à 11,6 Hz
    # beaucoup vibration => je doit filter beaucoup => pourquoi c si haut 
```


# GPS
gp :
  rx = 9
  tx = 8
il y une fonction bloquante, mais elle prend pas beaucoup de temps et même si il y a pas de fixe il continue à tournée

# LORA sx
lora:
  spi_bus : 0
  clk = 2
  mosi = 3
  miso = 4
  cs = 27
  irq = 20
  rst = 15
  gpio = 26
initalisation de lora 
band pasante (w):
lora.setup(869.75,sf=12,cr=8)


# TEST 
testModuleClass = tester tout les module
test_LoraSD = batterie de teste avec la gnd station
scanI2C : test les module i2C

# Erreur courante 
```
Traceback (most recent call last):
  File "<stdin>", line 6, in <module>
  File "/lib/lora.py", line 16, in <module>
  File "/lib/sx1262.py", line 2, in <module>
MemoryError: memory allocation failed, allocating 4168 bytes
```
Je sais pas bonne chance ! 
OLD il faut forcée un garbege collectore dans le code 
```python
import gc
gc.collect()
```

