import plotly.graph_objects as go
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State


data = pd.read_csv('songs.csv', engine='python')
# Drop id to scale features
songs_features = data.drop(['_id'], axis=1)
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
        dbc.Row(
            [
                dbc.Col(dcc.Graph(id="graph", figure=fig_features),
                        width={"size": 8, "offset": 2}),
            ]
        )
    ]
)
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
app.layout = html.Div([content])

if __name__ == '__main__':
    app.run_server(port=8083)
