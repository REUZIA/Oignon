from machine import I2C, Pin

i2c =  I2C(1, sda=Pin(2), scl=Pin(3)) 

# Ensuite, scanner les périphériques I2C
devices = i2c.scan()
if len(devices) == 0:
    print("Aucun périphérique I2C trouvé")
else:
    print("Périphériques I2C trouvés (adresses hexadécimales):")
    for device in devices:
        print("Adresse: #%02X" % device)
