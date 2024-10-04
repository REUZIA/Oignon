import time
from machine import Pin

# Configurer GP0 en mode pull-down
gp1 = Pin(1, Pin.IN, Pin.PULL_DOWN)

# Configurer GP14 en mode pull-down
gp14 = Pin(14, Pin.IN, Pin.PULL_DOWN)

print("att")
while True:
    # Lire l'état des broches GP0 et GP14
    gp1_state = gp1.value()
    gp14_state = gp14.value()

    if gp1_state or gp14_state:
        # Afficher l'état des broches sur la console
        print(f"GPun: {gp1_state}, GPdeux: {gp14_state}")
    
    time.sleep(0.1)
