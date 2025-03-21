import dash
from dash import dcc, html
import pandas as pd
import plotly.express as px

# Lecture des données scrappées
df = pd.read_csv('data.csv', names=['timestamp', 'price'])
df['timestamp'] = pd.to_datetime(df['timestamp'])
# Suppression d'éventuelles virgules et conversion en float
df['price'] = df['price'].str.replace(',', '').astype(float)

# Création du graphique de la série temporelle
fig = px.line(df, x='timestamp', y='price', title='Évolution du Prix du Bitcoin')

# Configuration du layout du dashboard
app = dash.Dash(__name__)
app.layout = html.Div([
    html.H1("Dashboard Bitcoin"),
    dcc.Graph(figure=fig),
    html.Div(id='daily-report')  # Espace réservé pour le rapport quotidien
])

if __name__ == '__main__':
    # Le dashboard sera accessible sur le port 8050 de votre VM
    app.run_server(debug=True, host='0.0.0.0', port=8050)
