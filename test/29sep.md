### **Fiche de Test LoRa**

#### **Composants modifiables** :
- **BW (Bande Passante)** : 
  - Plage : 125 - 500 kHz
  - + page = + Temps de transmission - Porté
- **SF (Facteur d’Étalement)** :
  - Plage : 7 - 12
  - + SF élevé = + Portée mais + Temps de transmission
- **CR (Correction d’erreurs)** :
  - Plage : 5 - 8
  - + CR élevé = + Fiabilité mais + Temps de transmission (moins de bits d'informations transmis)
- **Puissance d’émission (Power)** : 
  - Plage : 2 - 14 dBm
  - + Forte puissance = + Distance mais + Consommation d'énergie

- **test**
    - variable inchanger
        temps : 10 seconde d'essai
        
        
    - variable changente
        - distance 0m,100m(à terre),1km,2km
            - lora.setup(869.75,bw=500,sf=12,cr=8,power=14)
            - lora.setup(869.75,bw=250,sf=12,cr=8,power=14)
            - lora.setup(869.75,bw=125,sf=12,cr=8,power=14)
            - lora.setup(869.75,bw=500,sf=9,cr=8,power=14)
            - lora.setup(869.75,bw=500,sf=7,cr=8,power=14)
            - lora.setup(869.75,bw=500,sf=12,cr=6,power=14)
            - lora.setup(869.75,bw=500,sf=12,cr=5,power=14)
            - lora.setup(869.75,bw=500,sf=12,cr=8,power=7)
            - lora.setup(869.75,bw=500,sf=12,cr=8,power=2)