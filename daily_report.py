import pandas as pd

# Lecture des données depuis le fichier CSV
df = pd.read_csv('/home/ubuntu/bitcoin-dashboard/data.csv', names=['timestamp', 'price'])

# Conversion des dates et nettoyage des prix
df['timestamp'] = pd.to_datetime(df['timestamp'])
df['price'] = pd.to_numeric(df['price'].astype(str).str.replace(',', '').str.strip(), errors='coerce')
df = df.dropna(subset=['price'])

# Définir la journée : de minuit aujourd'hui à minuit demain
today = pd.to_datetime("today").normalize()
tomorrow = today + pd.Timedelta(days=1)
daily_data = df[(df['timestamp'] >= today) & (df['timestamp'] < tomorrow)]

if not daily_data.empty:
    daily_min = daily_data['price'].min()
    daily_max = daily_data['price'].max()
    # Évolution en pourcentage entre le min et le max
    evolution = ((daily_max - daily_min) / daily_min) * 100

    # Calcul des rendements en pourcentage et de la volatilité
    daily_data['return'] = daily_data['price'].pct_change() * 100
    volatility = daily_data['return'].dropna().std()

    report = f"""Rapport du {today.date()} :
- Prix minimum : {daily_min:.2f} USD
- Prix maximum : {daily_max:.2f} USD
- Évolution (min -> max) : {evolution:.2f} %
- Volatilité : {volatility:.2f} %
"""
else:
    report = "Aucune donnée disponible pour aujourd'hui."

# Écriture du rapport dans un fichier texte
with open('/home/ubuntu/bitcoin-dashboard/daily_report.txt', 'w') as f:
    f.write(report)
