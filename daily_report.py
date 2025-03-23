import pandas as pd

# Lecture des données
df = pd.read_csv('/home/ubuntu/bitcoin-dashboard/data.csv', names=['timestamp', 'price'])
df['timestamp'] = pd.to_datetime(df['timestamp'])
df['price'] = pd.to_numeric(df['price'].astype(str).str.replace(',', ''), errors='coerce')
df = df.dropna(subset=['price'])

# Filtrer les données de la journée
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
- Volatilité : {volatility:.2f}
- Évolution : {evolution:.2f} %
"""
else:
    report = "Aucune donnée disponible pour aujourd'hui."

# Écrire le rapport dans un fichier (avec chemin absolu)
with open('/home/ubuntu/bitcoin-dashboard/daily_report.txt', 'w') as f:
    f.write(report)

