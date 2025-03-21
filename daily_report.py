import pandas as pd

# Lecture des données
df = pd.read_csv('data.csv', names=['timestamp', 'price'])
df['timestamp'] = pd.to_datetime(df['timestamp'])
df['price'] = df['price'].str.replace(',', '').astype(float)

# Filtrer les données de la journée actuelle
today = pd.to_datetime("today").normalize()
daily_data = df[df['timestamp'] >= today]

if not daily_data.empty:
    open_price = daily_data.iloc[0]['price']
    close_price = daily_data.iloc[-1]['price']
    volatility = daily_data['price'].std()
    evolution = ((close_price - open_price) / open_price) * 100

    report = f"""Rapport du {today.date()} :
    - Prix d'ouverture : {open_price}
    - Prix de clôture : {close_price}
    - Volatilité : {volatility}
    - Évolution : {evolution:.2f} %
    """
else:
    report = "Aucune donnée disponible pour aujourd'hui."

# Écrire le rapport dans un fichier texte
with open('daily_report.txt', 'w') as f:
    f.write(report)
