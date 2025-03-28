import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output, State
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import requests

# Utilisation du thème FLATLY de Bootstrap (vous pouvez changer selon vos goûts)
external_stylesheets = [dbc.themes.FLATLY]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = dbc.Container([
    # Titre
    dbc.Row([
        dbc.Col(html.H1("Dashboard Bitcoin"), width=12)
    ], className="mb-4"),
    
    # Section Prix actuel et Conversion
    dbc.Row([
        dbc.Col(
            dbc.Card([
                dbc.CardHeader("Prix actuel du Bitcoin"),
                dbc.CardBody([
                    html.H2(id='current-price-usd', style={'color': 'blue', 'fontSize': '32px'}),
		    html.H2(id='current-price-eur', style={'color': 'green', 'fontSize': '32px'})
                ])
            ]), width=6
        ),
        dbc.Col(
            dbc.Card([
                dbc.CardHeader("Conversion BTC -> USD"),
                dbc.CardBody([
                    dbc.Label("Quantité de BTC :"),
                    dbc.Input(id='btc-amount', type='number', value=1.0, className="mb-2"),
                    dbc.Button("Convertir", id='convert-button', color="primary", className="mb-2"),
                    html.Div(id='conversion-result', style={'fontSize': '24px', 'color': 'blue'})
                ])
            ]), width=6
        )
    ], className="mb-4"),
    
    # Texte explicatif pour le graphique principal
    dbc.Row([
        dbc.Col(
            dbc.Card(
                dbc.CardBody(
                    html.P(
                        "Le graphique ci-dessous montre l'évolution des prix du Bitcoin et, si désiré, la comparaison avec le prix de l'Ether. "
                        "Utilisez la checklist ci-dessous pour choisir d'afficher le prix BTC, sa moyenne mobile sur 5 points, et/ou "
                        "la courbe de l'Ether (affichée sur l'axe de gauche, avec BTC sur l'axe de droite).",
                        className="card-text"
                    )
                )
            ), width=12
        )
    ], className="mb-4"),
    
    # Checklist pour les traces
    dbc.Row([
        dbc.Col(
            dcc.Checklist(
                id='toggle-traces',
                options=[
                    {'label': 'Afficher le prix BTC', 'value': 'btc'},
                    {'label': 'Afficher la Moyenne Mobile (5 points)', 'value': 'ma'},
                    {'label': 'Comparer avec Ether', 'value': 'eth'}
                ],
                value=['btc'],  # Par défaut, affichage du BTC uniquement
                labelStyle={'display': 'inline-block', 'marginRight': '20px'}
            ), width=12
        )
    ], className="mb-4"),
    
    # Graphique principal
    dbc.Row([
        dbc.Col(dcc.Graph(id='price-graph'), width=12)
    ], className="mb-4"),
    
    # Rapport quotidien
    dbc.Row([
        dbc.Col(
            dbc.Card([
                dbc.CardHeader("Rapport quotidien"),
                dbc.CardBody(
                    html.Pre(id='daily-report', style={'whiteSpace': 'pre-wrap', 'fontFamily': 'monospace'})
                )
            ]), width=12
        )
    ], className="mb-4"),
    
    # Graphique de volatilité roulante
    dbc.Row([
        dbc.Col(
            dbc.Card([
                dbc.CardHeader("Volatilité roulante"),
                dbc.CardBody(dcc.Graph(id='volatility-graph'))
            ]), width=12
        )
    ], className="mb-4"),
    
    # Intervalles de rafraîchissement
    dcc.Interval(id='interval-component', interval=120000, n_intervals=0),  # toutes les 2 minutes
    dcc.Interval(id='interval-current-price', interval=45000, n_intervals=0)  # toutes les 45 secondes
], fluid=True)

# --------------------------
# Callback 1 : Mise à jour du prix BTC en direct
# --------------------------
@app.callback(
    [Output('current-price-usd', 'children'),
     Output('current-price-eur', 'children')],
    Input('interval-current-price', 'n_intervals')
)
def update_current_price(n):
    try:
        url = (
            "https://api.coingecko.com/api/v3/simple/price"
            "?ids=bitcoin&vs_currencies=usd,eur"
        )
        response = requests.get(url)
        data = response.json()
        
        price_usd = data['bitcoin']['usd']  # ex. 83968
        price_eur = data['bitcoin']['eur']  # ex. 77532
        
        usd_text = f"{price_usd:.2f} USD"
        eur_text = f"{price_eur:.2f} EUR"
        
        return usd_text, eur_text
    except Exception as e:
        return f"Erreur : {e}", f"Erreur : {e}"

# --------------------------
# Callback 2 : Conversion BTC -> USD basée sur le prix actuel
# --------------------------
@app.callback(
    Output('conversion-result', 'children'),
    Input('convert-button', 'n_clicks'),
    State('btc-amount', 'value'),
    State('current-price-usd', 'children')
)
def convert_btc_to_usd(n_clicks, amount, current_price_text):
    if n_clicks is None:
        return ""
    try:
        price_str = current_price_text.split()[0]
        price = float(price_str)
        result = amount * price
        return f"{amount} BTC = {result:.2f} USD"
    except Exception as e:
        return f"Erreur de conversion : {e}"

# --------------------------
# Callback 3 : Mise à jour du graphique principal (BTC et option ETH)
# --------------------------
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
    
    # Lecture des données ETH si sélectionné
    if 'eth' in toggle_values:
        df_eth = pd.read_csv('/home/ubuntu/bitcoin-dashboard/data_eth.csv', names=['timestamp', 'price'])
        df_eth['timestamp'] = pd.to_datetime(df_eth['timestamp'])
        df_eth['price'] = pd.to_numeric(df_eth['price'].str.replace(',', ''), errors='coerce')
        df_eth.dropna(subset=['price'], inplace=True)
    
    if 'eth' in toggle_values:
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        
        # Trace ETH sur l'axe de gauche
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
        # Trace BTC sur l'axe de droite
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
            # Moyenne mobile (5 points) pour BTC si sélectionnée
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
        fig.update_layout(
            title="Comparaison BTC/ETH",
            xaxis_title="Temps",
            legend=dict(itemclick=False, itemdoubleclick=False),
            showlegend=True
        )
        fig.update_yaxes(title_text="Prix ETH (USD)", secondary_y=False)
        fig.update_yaxes(title_text="Prix BTC (USD)", secondary_y=True)
    else:
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

# --------------------------
# Callback 4 : Mise à jour du rapport quotidien
# --------------------------
@app.callback(
    Output('daily-report', 'children'),
    Input('interval-component', 'n_intervals')
)
def update_daily_report(n):
    try:
        with open('/home/ubuntu/bitcoin-dashboard/daily_report.txt', 'r') as f:
            report = f.read()
    except Exception:
        report = "Rapport quotidien non disponible pour le moment."
    return report

# --------------------------
# Callback 5 : Mise à jour du graphique de volatilité roulante
# --------------------------
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
