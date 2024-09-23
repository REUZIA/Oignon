import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import time

# Exemple de données simulées
data = {
    'time': pd.date_range(start='2024-09-23 08:00', periods=100, freq='T'),  # 100 minutes d'échantillons
    'altitude': np.random.normal(300, 50, 100),  # Altitude simulée (en mètres)
    'speed': np.random.normal(60, 5, 100),  # Vitesse simulée (en km/h)
}

# Créer un DataFrame avec les données
df = pd.DataFrame(data)

# Convertir la colonne 'time' en index pour une meilleure visualisation
df.set_index('time', inplace=True)

# Fonction pour afficher et mettre à jour les graphes toutes les 5 secondes
def mise_a_jour_graphique(df):
    for i in range(5):  # Met à jour 5 fois (tu peux ajuster selon tes besoins)
        plt.figure(figsize=(10, 6))  # Nouvelle figure à chaque itération

        # Graphique de l'altitude
        plt.subplot(2, 1, 1)
        plt.plot(df.index, df['altitude'], label='Altitude (m)', color='blue')
        plt.xlabel('Time')
        plt.ylabel('Altitude (m)')
        plt.title('Progression de l\'altitude selon le temps')
        plt.grid(True)

        # Graphique de la vitesse
        plt.subplot(2, 1, 2)
        plt.plot(df.index, df['speed'], label='Vitesse (km/h)', color='green')
        plt.xlabel('Time')
        plt.ylabel('Speed (km/h)')
        plt.title('Progression de la vitesse selon le temps')
        plt.grid(True)

        # Afficher et fermer le graphique après mise à jour
        plt.tight_layout()
        plt.show()

        # Pause de 5 secondes avant la mise à jour suivante
        time.sleep(5)
        
        # Fermer la figure précédente pour libérer la mémoire
        plt.close()

# Appel de la fonction pour démarrer l'affichage
mise_a_jour_graphique(df)
