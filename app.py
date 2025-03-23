import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import requests  # si besoin pour d'autres appels

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Dashboard Bitcoin"),
    # Affichage du prix actuel qui se met à jour chaque minute
    html.Div([
        html.H2("Prix actuel du Bitcoin : "),
        html.H2(id='current-price', style={'color': 'blue', 'fontSize': '40px'})
    ], style={'display': 'flex', 'alignItems': 'center', 'marginBottom': '20px'}),
    # Texte explicatif
    html.Div([
        html.P(
            "Ce graphique montre l'évolution des prix du Bitcoin et de l'Ether. "
            "Vous pouvez choisir d'afficher la courbe du Bitcoin (en bleu), la moyenne mobile sur 5 points pour le Bitcoin (en rouge), "
            "et/ou la courbe de l'Ether (en vert). Si vous sélectionnez la comparaison, le graphique affichera l'Ether sur l'axe de gauche et le Bitcoin sur l'axe de droite."
        )
    ], style={'margin': '20px', 'fontSize': '16px'}),
    
    dcc.Checklist(
        id='toggle-traces',
        options=[
            {'label': 'Afficher le prix BTC', 'value': 'btc'},
            {'label': 'Afficher la Moyenne Mobile (5 points)', 'value': 'ma'},
            {'label': 'Afficher Ether', 'value': 'eth'}
        ],
        # Par défaut, on affiche uniquement les données BTC (prix + MA)
        value=['btc', 'ma'],
        labelStyle={'display': 'inline-block', 'marginRight': '20px'}
    ),
    
    dcc.Graph(id='price-graph'),
    
    # Les autres composants restent inchangés (rapport quotidien, volatilité, etc.)
    html.H2("Rapport quotidien"),
    html.Div("Ce rapport présente des indicateurs financiers clés calculés sur la journée.", style={'margin': '10px'}),
    html.Pre(id='daily-report', style={'whiteSpace': 'pre-wrap', 'fontFamily': 'monospace'}),
    
    html.H2("Volatilité roulante"),
    html.Div("Ce graphique affiche l'évolution de la volatilité (écart-type des rendements sur une fenêtre mobile).", style={'margin': '10px'}),
    dcc.Graph(id='volatility-graph'),
    
    dcc.Interval(
        id='interval-component',
        interval=120000,  # mise à jour toutes les 2 minutes
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

# Callback pour mettre à jour le graphique principal
@app.callback(
    Output('price-graph', 'figure'),
    Input('interval-component', 'n_intervals'),
    Input('toggle-traces', 'value')
)
def update_graph(n, toggle_values):
    # Lecture des données BTC
    df_btc = pd.read_csv('/home/ubuntu/bitcoin-dashboard/data.csv', names=['timestamp', 'price'])
    df_btc['timestamp'] = pd.to_datetime(df_btc['timestamp'])
    df_btc['price'] = pd.to_numeric(df_btc['price'].str.replace(',', ''), errors='coerce')
    df_btc.dropna(subset=['price'], inplace=True)
    
    # Si l'option ETH est sélectionnée, on lit aussi les données ETH
    if 'eth' in toggle_values:
        df_eth = pd.read_csv('/home/ubuntu/bitcoin-dashboard/data_eth.csv', names=['timestamp', 'price'])
        df_eth['timestamp'] = pd.to_datetime(df_eth['timestamp'])
        df_eth['price'] = pd.to_numeric(df_eth['price'].str.replace(',', ''), errors='coerce')
        df_eth.dropna(subset=['price'], inplace=True)
    
    # Si on souhaite comparer BTC et ETH, on utilise un graphique à double axe
    if 'eth' in toggle_values:
        # Création d'un graphique à double axe
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        
        # Trace ETH sur l'axe de gauche (secondary_y=False)
        fig.add_trace(
            go.Scatter(
                x=df_eth['timestamp'],
                y=df_eth['price'],
                mode='lines',
                name='ETH (Ether)',
                line=dict(color='green')
            ),
            secondary_y=False
        )
        # Trace BTC sur l'axe de droite (secondary_y=True)
        if 'btc' in toggle_values:
            fig.add_trace(
                go.Scatter(
                    x=df_btc['timestamp'],
                    y=df_btc['price'],
                    mode='lines',
                    name='BTC (Bitcoin)',
                    line=dict(color='blue')
                ),
                secondary_y=True
            )
            # Si la moyenne mobile est sélectionnée, on l'ajoute sur BTC
            if 'ma' in toggle_values:
                df_btc['MA5'] = df_btc['price'].rolling(window=5).mean()
                fig.add_trace(
                    go.Scatter(
                        x=df_btc['timestamp'],
                        y=df_btc['MA5'],
                        mode='lines',
                        name='MA5 BTC',
                        line=dict(color='red')
                    ),
                    secondary_y=True
                )
        # Mise en page du graphique à double axe
        fig.update_layout(
            title="Comparaison BTC/ETH",
            xaxis_title="Temps",
            legend=dict(itemclick=False, itemdoubleclick=False),
            showlegend=True
        )
        fig.update_yaxes(title_text="Prix ETH (USD)", secondary_y=False)
        fig.update_yaxes(title_text="Prix BTC (USD)", secondary_y=True)
    else:
        # Sinon, on affiche seulement BTC avec un graphique simple
        fig = go.Figure()
        if 'btc' in toggle_values:
            fig.add_trace(go.Scatter(
                x=df_btc['timestamp'],
                y=df_btc['price'],
                mode='lines',
                name='BTC (Bitcoin)',
                line=dict(color='blue')
            ))
        if 'ma' in toggle_values:
            df_btc['MA5'] = df_btc['price'].rolling(window=5).mean()
            fig.add_trace(go.Scatter(
                x=df_btc['timestamp'],
                y=df_btc['MA5'],
                mode='lines',
                name='MA5 BTC',
                line=dict(color='red')
            ))
        fig.update_layout(
            title="Évolution du prix du Bitcoin",
            xaxis_title="Temps",
            yaxis_title="Prix (USD)",
            legend=dict(itemclick=False, itemdoubleclick=False),
            showlegend=True
        )
    
    return fig

# Callback pour le rapport quotidien
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

# Callback pour le graphique de volatilité roulante
@app.callback(
    Output('volatility-graph', 'figure'),
    Input('interval-component', 'n_intervals')
)
def update_volatility(n):
    df = pd.read_csv('/home/ubuntu/bitcoin-dashboard/data.csv', names=['timestamp', 'price'])
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['price'] = pd.to_numeric(df['price'].str.replace(',', ''), errors='coerce')
    df.dropna(subset=['price'], inplace=True)
    
    df['return'] = df['price'].pct_change() * 100
    window = 10
    df['volatility'] = df['return'].rolling(window=window).std()

    fig = px.line(df, x='timestamp', y='volatility',
                  title=f'Volatilité roulante (fenêtre de {window} points)')
    fig.update_layout(xaxis_title="Temps", yaxis_title="Volatilité (%)")
    return fig

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8050)
