
import time

from machine import Pin

# Configurer GP0 en mode pull-down
gp0 = Pin(0, Pin.IN, Pin.PULL_DOWN)

print("att")
while True:
    # Lire l'état des broches GP0 et GP14
    gp0_state = gp0.value()

    if gp0_state:
        # Afficher l'état des broches sur la console
        print(f"GPzero: {gp0_state}")
    
    time.sleep(0.1)
