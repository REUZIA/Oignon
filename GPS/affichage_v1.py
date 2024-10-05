import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

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

# Création des graphes
plt.figure(figsize=(10, 6))

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

# Afficher le graphique
plt.tight_layout()
plt.show()
