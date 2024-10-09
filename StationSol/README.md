# Installation des utilitaires de commande
Pour intéragir directement avec la station sol, deux modes possibles : 
- Mode « téléversement »
- Mode « console » 

## Sur Linux
Pour chacun des deux modes, un utilitaire de CLI différent. 
Le mode « téléversement », rshell et le mode « console », minicom. 
Pour installer minicom : 
> sudo apt install minicom 

Pour installer rshell :
> sudo pip install rshell --break-system-packages 

## Sur Windows
Sur Windows, la méthode d’upload se fera par MicroPico à travers Visual Studio code 
et l’accès à la console par PuTTY. 

# Connexion aux utilitaires de commande
## Sur linux
Une fois relié, il vous faut détecter le bon port à l’aide de dmesg:  
> sudo dmesg

Vous obtiendrez une série de lignes ressemblant à ceci :
``` 
[ 2675.278610] usb 2-1: Manufacturer: MicroPython 
[ 2675.278611] usb 2-1: SerialNumber: e661640843748a28 
[ 2675.358437] cdc_acm 2-1:1.0: ttyACM0: USB ACM device
```
Cherchez bien cette dernière ligne, elle vous donneras le port à utiliser pour accèder à la pico. 
***Faites bien attention à vous assurer être sur les bonnes lignes, certains autres équipements utilisant aussi les ports ACM (arduino uno, etc...) !***

Si vous avez besoin de téléverser un nouveau code sur votre carte, vous utiliserez rshell : 
sudo rshell -p /dev/[nom du port] 
Vous devriez obtenir une console se trouvant dans votre répertoire courant, afin de téléverser le code, vous allez devoir utiliser une version miniaturisée de « cp », l’utilitaire copy de linux : 
cp [chemin de votre nouveau script] /pyboard/main.py 
Et pour téléverser des librairies, la commande est la même, à la différence du chemin de fin. 
  
Si vous avez besoin d’accèder à la console REPL présente sur la carte, vous utiliserez minicom : 
sudo minicom -oD /dev/[nom du port]  
Pour journaliser les échanges :  
sudo minicom -oD /dev/[nom du port] -C [emplacement et nom du fichier log qui sera créé] 
Vous obtiendrez une console resemblant à ceci : 
```
>>>
```
Faites un Ctrl-D afin de vous assurer que la carte est bel et bien opérationnelle, vous devriez obtenir une sortie vous précisant la version de micropython si celle-ci l’est bel et bien. 

## Sur Windows

Pour accèder à la console en utilisant PuTTY il suffira de sélectionner l’option « Serial », de préciser le port trouvable dans le gestionnaire de périphérique, la carte devrait porter un nom comme COM11 ou COM12, laissez le baud rate comme tel et appuyez sur « OK ». 
La console qui s’ouvre fonctionne comme celle de minicom, Ctrl-D pour vérifier son fonctionnement. 
Pour journaliser les échanges, il vous faudra d’activer l’option « All Session Data » et de choisir l’emplacement du fichier de log dans la section « Logging » sous « Session ». 

# Utilisation de la console

La console affichera les informations reçues automatiquement sous la forme de cette trame : 
"RX Done”, message reçu, erreur (ou “ERR_NONE” si il n’y en as pas), RSSI (en dBm), temps depuis le dernier paquet (en ms) 
Pour envoyer des paquets, il suffira d’entrer la commande suivante : 
```
sxTX.send(b'[texte à envoyer]’) 
```
Les commandes uplink d’éveil et de veille sont les suivantes : 
```
sxTX.send(b’SIG2’) #éveil 
sxTX.send(b’SIG1’) #veille 
```

# Erreurs
La plupart des erreurs sont liées à des erreurs de branchement, veuillez réviser le branchement à l’aide du chart suivant :  
![Chart branchements](https://cdn.discordapp.com/attachments/163416842864558081/1282324096645861468/image-3.png)
