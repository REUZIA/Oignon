DOC Oignon **ODC**

# Avant qu'on ne touche plus le payload
supprimer tout les elemnt test (dans le fichier test) de la board 
vider la sd
lancer le main.py

# Composant 
- Carte PCB Lora + SD
- Carte PCB GPS + ICM
- Carte sd 64G vert
- 1x Antenne gps 
- 2x Antenne lora 
- 4 jst double alim
- 6 jst 4pin 
- carte alim(maitre en haut à droite voir cablage)

# Shema et repartition code
discode : https://discord.com/channels/610534406922174495/1263142960497688578/1291515100024541275

2 fichier; l'un avec les librery de compiler, l'autre avec les librery en clair, se qui à été mis sur la carte c des compiler pour gagnier espace mémoir 

carte lier :
  - séquanceur altimétrique (led tout les couleur)
    - usb b + led + buzzer
  - laison montant (Oingon upLink) 
    - loral + rp
  - ICM + gps 
  - lora + sd


# Compiler 
https://pypi.org/project/mpy-cross/
```console
mpy-cross my_app.py
```
tout les fichier non compier son dans "ODV_NonCompiter"

# SD
Protocole : 
    nbspi = 0,
    baudrate = 2000000,#même baudrate que le lora 
    pinSck = 2,
    pinMiso = 4, 
    pinMosi = 3,
    pinSC = 5,

vas essayer de reconnecter sd quand écire si pas ouvert, à chaque réouverture réssuite var écire un nouv fichier "dataX.csv"
se reconnec tout les 5 cyle si jamais déco (self.attAvantRecoSD)
tout les 30 donner écrit il flush dans la sd (il écrite dessus ligne 107)

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

essaye de lire avec try si ya erreur essaye de se reco

# GPS
gp :
  rx = 9
  tx = 8

il y une fonction bloquante, mais elle prend pas beaucoup de temps et même si il y a pas de fixe il continue à tournée
+ peut pas fair d'erreur car lis spi si ya rien renvoie 0
on sessayer de recuperai tout les **0.2s**


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

envoie + init + setup avec try, si sa marche pas ne fait rien 
si le paquer pas envoyer totalement (prend plus de temps que temps de la boucle) ne l'envoie pas


# TEST 
testModuleClass = tester tout les module
test_LoraSD = batterie de teste avec la gnd station
scanI2C : test les module i2C
laison montant + sequanceur altimatrique : juste lis gpio


# Erreur courante 
```
Traceback (most recent call last):
  File "<stdin>", line 6, in <module>
  File "/lib/lora.py", line 16, in <module>
  File "/lib/sx1262.py", line 2, in <module>
MemoryError: memory allocation failed, allocating 4168 bytes
```
Je sais pas bonne chance ! 
OLD solution il faut forcée un garbege collectore dans le code 
```python
import gc
gc.collect()
```

si sd problème
  voir parti sd

si problème non résolue => nuc la raspy

## module Tom
si il clignote pas eteindre son module et le ralumer (débrancher jst)
si c blanc se qu'il à a atein l'apoger si vous le voyer avant lenvoie il faut le reset (débrancher et rebrancher)
doit enlever le timer max (quand ne clignote plus faut l'eteindre et rallumer )

# main 
att temps pour boucl 0.2 timeWaitBoucl
quand allumer : 
  envoie en lora(quand il peut) + sd
  acceleroXYZ;gyroXYZ;latitude;longitude;altitude;nombre_satellite_utiliser;nombre_satellite_visible;vitesse;heure
  ex: -0.03:-0.00:9.91;0.01:0.00:0.01;0:0:0.0:N;0:0:0.0:W;0.0;0;1;0.0;0:0:0.0


# Remarque 
le file alimentnat la raspy + module (en haut à droite) son inverser (rouge = - et noir = + )