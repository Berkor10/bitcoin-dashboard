import pandas as pd

# Lecture des données depuis le fichier CSV
df = pd.read_csv('/home/ubuntu/bitcoin-dashboard/data.csv', names=['timestamp', 'price'])
df['timestamp'] = pd.to_datetime(df['timestamp'])

# Nettoyage et conversion de la colonne 'price'
df['price'] = pd.to_numeric(
    df['price'].astype(str).str.replace(',', '').str.strip(), 
    errors='coerce'
)

# Supprimer les lignes où 'price' est NaN
df = df.dropna(subset=['price'])

# Filtrer les données de la journée actuelle
today = pd.to_datetime("today").normalize()
daily_data = df[df['timestamp'] >= today]

if not daily_data.empty:
    open_price = daily_data.iloc[0]['price']
    close_price = daily_data.iloc[-1]['price']
    volatility = daily_data['price'].std()
    evolution = ((close_price - open_price) / open_price) * 100
    daily_min = daily_data['price'].min()
    daily_max = daily_data['price'].max()
    
    report = f"""Rapport du {today.date()} :
- Prix d'ouverture : {open_price:.2f} $
 
- Prix de clôture : {close_price:.2f} $

- Prix minimum : {daily_min:.2f} $

- Prix maximum : {daily_max:.2f} $

- Volatilité : {volatility:.2f}

- Évolution : {evolution:.2f} %
"""
else:
    report = "Aucune donnée disponible pour aujourd'hui."

# Écriture du rapport dans le fichier daily_report.txt
with open('/home/ubuntu/bitcoin-dashboard/daily_report.txt', 'w') as f:
    f.write(report)
