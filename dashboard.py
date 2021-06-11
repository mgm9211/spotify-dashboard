import plotly.graph_objects as go
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from mongo_utils import load_features_time_series
from dash.dependencies import Input, Output, State


songs_features = load_features_time_series()
songs_features = songs_features.groupby('Date').mean().reset_index()
features = ['Acousticness', 'Danceability', 'Energy', 'Instrumentalness', 'Liveness', 'Loudness', 'Speechiness',
                            'Tempo', 'Valence']
fig_features = go.Figure()
for f in features:
    fig_features.add_trace(go.Scatter(name=f, x=songs_features['Date'], y=songs_features[f]))

fig_features.update_xaxes(rangeslider_visible=True)
content = html.Div(
    [
        html.H1('Spotify Data',
                style={'textAlign': 'center'}),
        html.Hr(),
    ]
)
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
app.layout = html.Div([
    content,
    dcc.Tabs(id="tabs", value='tab-1', children=[
        dcc.Tab(label='Tab Gráficas - Poner título', value='tab-1'),
        dcc.Tab(label='Tab Gráficas - Poner título', value='tab-2'),
    ]),
    html.Div(id='tabs-content')
])

@app.callback(Output('tabs-content', 'children'),
              Input('tabs', 'value'))
def render_content(tab):
    if tab == 'tab-1':
        return html.Div([
            html.H3('Poner titulito contenido TAB 1 :)',
                    style={'textAlign': 'center'}),
            html.Hr(),
            dbc.Row(
                [
                    dbc.Col(dcc.Graph(id="graph", figure=fig_features),
                            width={"size": 8, "offset": 2}),
                ]
            )
        ])
    elif tab == 'tab-2':
        return html.Div([
            html.H3('Poner titulito contenido TAB 1 :)',
                    style={'textAlign': 'center'}),
            html.Hr(),
        ])



if __name__ == '__main__':
    app.run_server(port=8083)
