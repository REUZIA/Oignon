DOC Oignon ordinateur de vole 

# Composant 
- Carte PCB Lora + SD
- Carte PCB GPS + ICM
- Carte sd 64G vert
- Antenne gps 
- Antenne lora 


# Sommaire 

# SD
Protocole : 
    nbspi = 0,
    baudrate = 2000000,
    pinSck = 2,
    pinMiso = 4, 
    pinMosi = 3,
    pinSC = 5,

# ICM
Procole I2C : 
    sda=Pin(6)
    scl=Pin(7)

# GPS
il y une fonction bloquante, mais elle prend pas beaucoup de temps et même si il y a pas de fixe il continue à tournée

# LORA sx


# TEST 

# Erreur courante 
```
Traceback (most recent call last):
  File "<stdin>", line 6, in <module>
  File "/lib/lora.py", line 16, in <module>
  File "/lib/sx1262.py", line 2, in <module>
MemoryError: memory allocation failed, allocating 4168 bytes
```
il faut forcée un garbege collectore dans le code 
```python
import gc
gc.collect()
```

