# À quoi sert le module ?
Le module de séquenceur altimétrique est l'horloge de tout ce système, son objectif est de détecter le décollage, l'apogée et le moment où l'on touche le sol.

# Comment fonctionne le module ?
Le module est une simple RP2040 à laquelle se connecte un baromètre nous permettant d'avoir la pression. À partir de cette pression, il arrive à définir une altitude et donc une vitesse. Si après un décollage la vitesse approxime 0 alors on arrive à l'apogée (et donc il envoie un signal d'apogée).

# Comment le faire fonctionner ?
Le module est alimenté par l'ordinateur de vol et a une connexion à ce dernier via 2 GPIO (un GND et un GPIO précisément).
En considérant que votre carte a déjà un firmware flashé, les étapes pour préparer au lancement sont :
- Alimenter le module 
- Branchez-vous en USB-C. 
- Uploader le projet (les fichiers sur le GitHub) sur la board via l'extension MicroPico de Visual Studio.
- Faite un test en exécutant le main 
- Lorsque la LED clignote en vert et rouge, créer une dépression autour du baromètre (utiliser une seringue, ça facilite la vie).
- La LED doit passer au bleu puis au blanc, lorsqu'elle passe au blanc, c'est qu'elle détecte l'apogée. 
- télécharger les données via l'extension MicroPico sur votre ordinateur. 

Si vous avez le fichier Data.TXT, alors tout va bien et vous venez de vérifier que le module marche.

- Refaite toutes les manipulations jusqu'à l'upload du projet (attention à bien supprimer le fichier DATA.txt).
- Débrancher le module de l'alimentation puis de votre ordinateur.
- Alimenter le module 
- Vérifier que le module va bien jusqu'au clignotement de la LED en rouge et vert.
- Débrancher le module de l'alimentation puis de votre ordinateur (ce n'est pas une erreur, refaite cette partie une seconde fois).
- Alimenter le module 
- Vérifier que le module va bien jusqu'au clignotement de la LED en rouge et vert.

Maintenant, vous avez vérifié que le main s'exécute bien à l'alimentation, vous pouvez intégrer le CAN SAT qui lorsqu'il sera alimenté lancera le séquenceur directement, attention à donc bien l'alimenter une fois en rampe et lorsque la fusée ne bouge plus.

# Récupérer les données de post vol
Vous êtes après le vol et vous avez récupéré la fusée (Dieu merci), il est donc temps de récupérer les données ! 
- Alimenter le module
- Branchez-le en USB-C à votre ordinateur. 
- Télécharger les documents via MicroPico 
- C'est bon, vous avez gagné !

# Remerciements
Je tiens à remercier tous ceux qui ont pu aider de près ou de loin. 
- L'association aérospatiale Air ESIEA et tous ses membres
– Particulièrement, Anatole Boudard pour ses bons conseils en PCB et sa soudure, Jacques Sponton et Pierre Melo pour leur aide sur le code. 
- Maxime Leveque pour son aide sur le delay matching de la flash 
- Hugo Allaire, car le code que nous utilisons est un fork du sien modifié et que ses conseils ont pu être très très précieux.  

# Changement pour une V2 

- Annoter le code
- Vérifier son bon fonctionnement dans différentes conditions 
- Ajouter un adaptateur permettant la charge en USB C