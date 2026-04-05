import os
import base64
import io
import pandas as pd
import plotly.express as px
import psycopg2
import dash
from dash import dcc, html, Input, Output, State

# Récupérer les variables d'environnement pour la base de données
DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_HOST = os.environ.get("DB_HOST")
DB_NAME = os.environ.get("DB_NAME")



# Initialisation du dashboard
app = dash.Dash(__name__)
app.title = "Dashboard Data App - Web Pro"

# Layout de base
app.layout = html.Div([
    html.H1("Dashboard Data App - Web Pro"),

    # Upload CSV
    dcc.Upload(
        id='upload-data',
        children=html.Div(['Glissez-déposez ou sélectionnez un fichier CSV']),
        style={
            'width': '50%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
        multiple=False
    ),

    html.Div(id='file-info', style={'marginBottom': '20px'}),

    # Filtres et sélecteurs
    html.Div([
        html.Label("X axis:"),
        dcc.Dropdown(id="x-dropdown"),

        html.Label("Y axis:"),
        dcc.Dropdown(id="y-dropdown"),

        html.Label("Filtre numérique (>=)"),
        dcc.Input(id="num-filter", type="number", placeholder="Valeur min"),
        dcc.Dropdown(id="num-col-dropdown", placeholder="Colonne numérique"),

        html.Label("Filtre catégorie"),
        dcc.Dropdown(id="cat-col-dropdown", placeholder="Colonne catégorie"),
        dcc.Dropdown(id="cat-val-dropdown", placeholder="Valeur catégorie"),

        html.Button("Mettre à jour les graphiques", id="update-button")
    ], style={'display': 'grid', 'gridTemplateColumns': '1fr 1fr', 'gap': '10px', 'marginBottom': '20px'}),

    # Onglets pour graphiques multiples
    dcc.Tabs(id="tabs", value='tab1', children=[
        dcc.Tab(label='Graphique 1', value='tab1'),
        dcc.Tab(label='Graphique 2', value='tab2')
    ]),
    dcc.Graph(id="graph")
])

# Stocker le DataFrame en mémoire
df_store = {}

# Callback pour charger le CSV
@app.callback(
    Output('file-info', 'children'),
    Output('x-dropdown', 'options'),
    Output('y-dropdown', 'options'),
    Output('num-col-dropdown', 'options'),
    Output('cat-col-dropdown', 'options'),
    Input('upload-data', 'contents'),
    State('upload-data', 'filename')
)
def load_csv(contents, filename):
    if contents is None:
        return "Aucun fichier chargé", [], [], [], []

    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    try:
        df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
    except Exception as e:
        return f"Erreur lecture CSV : {e}", [], [], [], []

    # Stocker dans le dictionnaire
    df_store['df'] = df

    cols = [{"label": c, "value": c} for c in df.columns]

    return f"Fichier chargé : {filename}", cols, cols, cols, cols

# Callback pour mettre à jour les valeurs catégories
@app.callback(
    Output('cat-val-dropdown', 'options'),
    Input('cat-col-dropdown', 'value')
)
def update_cat_values(cat_col):
    if 'df' not in df_store or not cat_col:
        return []
    unique_vals = df_store['df'][cat_col].dropna().unique()
    options = [{"label": "Tous", "value": "Tous"}] + [{"label": str(v), "value": str(v)} for v in sorted(unique_vals)]
    return options

# Callback pour générer les graphiques
@app.callback(
    Output('graph', 'figure'),
    Input('update-button', 'n_clicks'),
    State('x-dropdown', 'value'),
    State('y-dropdown', 'value'),
    State('num-col-dropdown', 'value'),
    State('num-filter', 'value'),
    State('cat-col-dropdown', 'value'),
    State('cat-val-dropdown', 'value')
)
def update_graph(n_clicks, x_col, y_col, num_col, num_val, cat_col, cat_val):
    if 'df' not in df_store:
        return px.line()

    df_plot = df_store['df'].copy()

    # Filtre numérique
    if num_col and num_val is not None:
        df_plot = df_plot[df_plot[num_col] >= num_val]

    # Filtre catégorie
    if cat_col and cat_val and cat_val != "Tous":
        df_plot = df_plot[df_plot[cat_col].astype(str) == cat_val]

    if not x_col or not y_col:
        return px.line()

    fig = px.line(df_plot, x=x_col, y=y_col, markers=True, title=f"{y_col} vs {x_col}")
    return fig

# Lancement de l'app pour Render
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8050))
    app.run(debug=True, host="0.0.0.0", port=port)

