import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import requests

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Dashboard Bitcoin"),
    
    # Affichage du prix actuel qui se met à jour chaque minute
    html.Div([
        html.H2("Prix actuel du Bitcoin : "),
        html.H2(id='current-price', style={'color': 'blue', 'fontSize': '40px'})
    ], style={'display': 'flex', 'alignItems': 'center', 'marginBottom': '20px'}),
    
    # Texte explicatif pour le graphique principal
    html.Div([
        html.P("Ce graphique montre l'évolution du prix du Bitcoin au fil du temps. "
               "Il affiche la courbe du prix initial (en bleu) et la courbe de la moyenne mobile (calculée sur 5 points, en rouge).")
    ], style={'margin': '20px', 'fontSize': '16px'}),
    
    # Checklist (si vous souhaitez garder le choix)
    dcc.Checklist(
        id='toggle-traces',
        options=[
            {'label': 'Afficher le prix', 'value': 'price'},
            {'label': 'Afficher la Moyenne Mobile (5 points)', 'value': 'ma'}
        ],
        value=['price', 'ma'],  # par défaut, afficher les deux
        labelStyle={'display': 'inline-block', 'marginRight': '20px'}
    ),
    
    dcc.Graph(id='price-graph'),
    
    # Section du rapport quotidien
    html.H2("Rapport quotidien"),
    html.Div("Ce rapport présente des indicateurs financiers clés (prix d'ouverture, prix de clôture, volatilité, évolution) "
             "calculés sur la journée.", style={'margin': '10px'}),
    html.Pre(id='daily-report', style={'whiteSpace': 'pre-wrap', 'fontFamily': 'monospace'}),
    
    # Graphique de volatilité roulante
    html.H2("Volatilité roulante"),
    html.Div("Ce graphique affiche l'évolution de la volatilité, c'est-à-dire l'écart-type des rendements sur une fenêtre mobile, "
             "ce qui permet d'évaluer la variabilité du prix du Bitcoin.", style={'margin': '10px'}),
    dcc.Graph(id='volatility-graph'),
    
    # Intervalle pour rafraîchir les données du graphique et du rapport (toutes les 2 minutes)
    dcc.Interval(
        id='interval-component',
        interval=100000,  # 2 minutes
        n_intervals=0
    ),
    # Intervalle pour rafraîchir le prix actuel (toutes les 1 minute)
    dcc.Interval(
        id='interval-current-price',
        interval=45000,  
        n_intervals=0
    )
])

# Callback pour mettre à jour le prix actuel toutes les minutes via l'API CoinGecko
@app.callback(
    Output('current-price', 'children'),
    Input('interval-current-price', 'n_intervals')
)
def update_current_price(n):
    try:
        # Utilisation de l'API CoinGecko pour récupérer le prix du Bitcoin en USD
        url = (
    "https://api.coingecko.com/api/v3/coins/bitcoin"
    "?tickers=false&market_data=true&community_data=false"
    "&developer_data=false&sparkline=false"
)
        response = requests.get(url)
        data = response.json()
        price = data["market_data"]["current_price"]["usd"]
        return f"{price:.2f} USD"
    except Exception as e:
        return "Erreur"

# Callback pour le graphique principal (prix + MA5) qui se met à jour toutes les 2 minutes
@app.callback(
    Output('price-graph', 'figure'),
    Input('interval-component', 'n_intervals'),
    Input('toggle-traces', 'value')
)
def update_graph(n, toggle_values):
    df = pd.read_csv('/home/ubuntu/bitcoin-dashboard/data.csv', names=['timestamp', 'price'])
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['price'] = pd.to_numeric(df['price'].astype(str).str.replace(',', ''), errors='coerce')
    df = df.dropna(subset=['price'])
    
    fig = go.Figure()
    
    if 'price' in toggle_values:
        fig.add_trace(go.Scatter(
            x=df['timestamp'],
            y=df['price'],
            mode='lines',
            name='Prix du Bitcoin',
            line=dict(color='blue')
        ))
    
    df['MA5'] = df['price'].rolling(window=5).mean()
    if 'ma' in toggle_values:
        fig.add_trace(go.Scatter(
            x=df['timestamp'],
            y=df['MA5'],
            mode='lines',
            name='Moyenne Mobile (5 points)',
            line=dict(color='red')
        ))
    
    fig.update_layout(
        title="Évolution du prix du Bitcoin",
        xaxis_title="Temps",
        yaxis_title="Prix (USD)",
	showlegend=True,
        legend=dict(
            itemclick=False,
            itemdoubleclick=False
        )
    )
    return fig

# Callback pour le rapport quotidien (mise à jour toutes les 2 minutes)
@app.callback(
    Output('daily-report', 'children'),
    Input('interval-component', 'n_intervals')
)
def update_report(n):
    try:
        with open('/home/ubuntu/bitcoin-dashboard/daily_report.txt', 'r') as f:
            report = f.read()
    except Exception:
        report = "Rapport quotidien non disponible pour le moment."
    return report

# Callback pour le graphique de volatilité roulante (toutes les 2 minutes)
@app.callback(
    Output('volatility-graph', 'figure'),
    Input('interval-component', 'n_intervals')
)
def update_volatility(n):
    df = pd.read_csv('/home/ubuntu/bitcoin-dashboard/data.csv', names=['timestamp', 'price'])
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['price'] = pd.to_numeric(df['price'].astype(str).str.replace(',', ''), errors='coerce')
    df = df.dropna(subset=['price'])
    
    df['return'] = df['price'].pct_change() * 100
    window = 10
    df['volatility'] = df['return'].rolling(window=window).std()
    
    fig = px.line(df, x='timestamp', y='volatility',
                  title=f'Volatilité roulante (fenêtre de {window} points)')
    fig.update_layout(xaxis_title="Temps", yaxis_title="Volatilité (%)")
    return fig

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8050)
