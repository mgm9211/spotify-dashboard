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
features = ['Acousticness', 'Danceability', 'Energy', 'Instrumentalness', 'Liveness', 'Speechiness', 'Valence']

features_dict = [{
'feature_name': 'Acousticness',
    'min': 0,
    'max': 3
}]
fig_features = go.Figure()
for f in features:
    fig_features.add_trace(go.Scatter(name=f, x=songs_features['Date'], y=songs_features[f]))

fig_features2 = go.Figure()
fig_features2.add_trace(go.Scatter(name='Loudness', x=songs_features['Date'], y=songs_features['Loudness']))

fig_features3 = go.Figure()
fig_features3.add_trace(go.Scatter(name='Tempo', x=songs_features['Date'], y=songs_features['Tempo']))

fig_features.update_xaxes(rangeslider_visible=True)
fig_features2.update_xaxes(rangeslider_visible=True)
fig_features3.update_xaxes(rangeslider_visible=True)
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

features_rows = []
for feature in features_dict:
    features_rows.append(
        dcc.Input(
            id=feature['feature_name'], type="number", placeholder="input with range",
            min=feature['min'], max=feature['max'], step=3,

    ))


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
            ),

        dbc.Row(
            [
                dbc.Col(dcc.Graph(id="graph2", figure=fig_features2),
                        width={"size": 8, "offset": 2}),
            ]
        ),

        dbc.Row(
            [
                dbc.Col(dcc.Graph(id="graph3", figure=fig_features3),
                        width={"size": 8, "offset": 2}),
            ]
        )
    ])
    elif tab == 'tab-2':
        return html.Div([
            html.H3('Poner titulito contenido TAB 1 :)',
                    style={'textAlign': 'center'}),
            html.Hr(),
            # Acousticness', 'Danceability', 'Energy', 'Instrumentalness', 'Liveness', 'Loudness', 'Speechiness',
            #          'Tempo',
            # 'Valence'
            dbc.Row(
                [
                    dbc.Col(dcc.Input(id="acousticness", type="number", 
                                      placeholder="Acousticness",
                                      min=0, max=1, step=0.01), width={"size": 8, "offset": 2}),
                    # dbc.Col(dcc.Input(id="dfalse", type="number", placeholder="Debounce False"),
                    #         width={"size": 4}),
                ]
            ),
            dbc.Row(
                [
                    dbc.Col(dcc.Input(id="danceability", type="number", placeholder="Danceability",
                                      min=0, max=1, step=0.01), width={"size": 8, "offset": 2}),
                ]
            ),
            dbc.Row(
                [
                    dbc.Col(dcc.Input(id="energy", type="number", placeholder="Energy",
                                      min=0, max=1, step=0.01), width={"size": 8, "offset": 2}),
                ]
            ),
            dbc.Row(
                [
                    dbc.Col(dcc.Input(id="instrumentalness", type="number", placeholder="Instrumentalness",
                                      min=200, max=300, step=1), width={"size": 8, "offset": 2}),
                ]
            ),
            dbc.Row(
                [
                    dbc.Col(dcc.Input(id="liveness", type="number", placeholder="Liveness",
                                      min=0, max=1, step=0.01), width={"size": 8, "offset": 2}),
                ]
            ),
            dbc.Row(
                [
                    dbc.Col(dcc.Input(id="loudness", type="number", placeholder="Loudness",
                                      min=-60, max=0, step=1), width={"size": 8, "offset": 2}),
                ]
            ),
            dbc.Row(
                [
                    dbc.Col(dcc.Input(id="speechiness", type="number", placeholder="Speechiness",
                                      min=0, max=1, step=0.01), width={"size": 8, "offset": 2}),
                ]
            ),
            dbc.Row(
                [
                    dbc.Col(dcc.Input(id="tempo", type="number", placeholder="Tempo",
                                      min=50, max=150, step=0.01), width={"size": 8, "offset": 2}),
                ]
            ),
            dbc.Row(
                [
                    dbc.Col(dcc.Input(id="valence", type="number", placeholder="Valence",
                                      min=50, max=150, step=0.01), width={"size": 8, "offset": 2}),
                ]
            ),
            dbc.Row(
                [
                    dbc.Col(dcc.Input(id="input_range2", type="number", placeholder="input with range",
                                      min=0, max=1, step=0.01),
                            width={"size": 8, "offset": 2}),
                    # dbc.Col(dcc.Input(id="dfalse", type="number", placeholder="Debounce False"),
                    #         width={"size": 4}),
                ]
            ),

            dbc.Row(
                dcc.Input(
                    id="dtrue", type="number",
                    debounce=True, placeholder="Debounce True",
                )
            ),
            dbc.Row(
                dcc.Input(
                    id="input_range", type="number", placeholder="input with range",
                    min=10, max=100, step=3,
                )
            ),
            # dbc.Row(features_rows),
            # features_rows,
            html.Hr(),
            html.Div(id="number-out"),
        ])


@app.callback(
    Output("number-out", "children"),
    Input("input_range2", "value"),
    Input("dfalse", "value"),
    Input("dtrue", "value"),
    Input("input_range", "value"),
)

def number_render(fval, prueba, tval, rangeval):
    return "dfalse: {}, input_range2: {}, dtrue: {}, range: {}".format(fval, tval, prueba, rangeval)


if __name__ == '__main__':
    app.run_server(port=8083, debug=True)
