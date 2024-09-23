import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
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

# Flag pour arrêter la mise à jour
stop = False

# Fonction pour mettre à jour les graphes
def mise_a_jour_graphique():
    if not stop:
        # Créer la figure
        fig = plt.Figure(figsize=(10, 6))
        
        # Graphique de l'altitude
        ax1 = fig.add_subplot(211)
        ax1.plot(df.index, df['altitude'], label='Altitude (m)', color='blue')
        ax1.set_xlabel('Time')
        ax1.set_ylabel('Altitude (m)')
        ax1.set_title('Progression de l\'altitude selon le temps')
        ax1.grid(True)
        
        # Graphique de la vitesse
        ax2 = fig.add_subplot(212)
        ax2.plot(df.index, df['speed'], label='Vitesse (km/h)', color='green')
        ax2.set_xlabel('Time')
        ax2.set_ylabel('Speed (km/h)')
        ax2.set_title('Progression de la vitesse selon le temps')
        ax2.grid(True)
        
        # Créer la figure tkinter
        canvas = FigureCanvasTkAgg(fig, master=root)
        canvas.draw()
        canvas.get_tk_widget().pack()
    
# Fonction pour rafraîchir manuellement les graphes
def refresh():
    for widget in root.winfo_children():
        if isinstance(widget, tk.Canvas):
            widget.destroy()  # Détruire le canvas précédent
    mise_a_jour_graphique()

# Fonction pour arrêter le programme
def stop_program():
    global stop
    stop = True
    root.quit()

# Interface Tkinter
root = tk.Tk()
root.title("Graphique Altitude et Vitesse")

# Bouton pour rafraîchir
refresh_button = tk.Button(root, text="Rafraîchir", command=refresh)
refresh_button.pack()

# Bouton pour arrêter
stop_button = tk.Button(root, text="Arrêter", command=stop_program)
stop_button.pack()

# Démarrer l'affichage initial
mise_a_jour_graphique()

# Lancer la boucle principale de tkinter
root.mainloop()
