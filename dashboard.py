import plotly.graph_objects as go
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from mongo_utils import load_features_time_series
from dash.dependencies import Input, Output, State
import numpy as np
import plotly.express as px
from math import sqrt


# songs_features, data_genres = load_features_time_series()
from predict import predict

songs_features = pd.read_csv('songs_features.csv')
data_genre = pd.read_csv('data_genre.csv')
songs_features = songs_features.groupby('Date').mean().round(4).reset_index()
features = ['Acousticness', 'Danceability', 'Energy', 'Instrumentalness', 'Liveness', 'Speechiness', 'Valence']
######## PREPARANDO TAB 1 ########
fig_features = go.Figure()
for f in features:
    fig_features.add_trace(go.Scatter(name=f, x=songs_features['Date'], y=songs_features[f]))

fig_features2 = go.Figure()
fig_features2.add_trace(go.Scatter(name='Loudness', x=songs_features['Date'], y=songs_features['Loudness'],
                                   marker=dict(
                                       color='#e377c2',
                                   )))

fig_features3 = go.Figure()
fig_features3.add_trace(go.Scatter(name='Tempo', x=songs_features['Date'], y=songs_features['Tempo'],
                                   marker=dict(
                                       color='#ff7f0e',
                                   )))

fig_features.update_xaxes(rangeslider_visible=True)
fig_features2.update_xaxes(rangeslider_visible=True)
fig_features3.update_xaxes(rangeslider_visible=True)
######## PREPARANDO TAB 1 ########

######## PREPARANDO TAB 3 ########
genres = np.unique(data_genre['Genre'].tolist())
aux_data = data_genre[['Genre', 'Title', 'Artist(s)']]
aux_data.loc[:, 'Artist(s)'] = aux_data['Artist(s)'].apply(lambda x: x.strip('[').strip(']').strip('"'))
tab_3_rows = []
for g in genres:
    g_data = aux_data[aux_data['Genre'] == g]
    table = dbc.Table.from_dataframe(g_data.tail(4), striped=True, hover=True)
    tab_3_rows.append(dbc.Row([
        dbc.Col(table, width={"size": 4, "offset": 1}),
    ]))
    tab_3_rows.append(html.Br())

grouped_data = data_genre.groupby('Genre').mean().round(4).reset_index()
######## PREPARANDO TAB 4 ########
all_features = ['Acousticness', 'Danceability', 'Energy', 'Instrumentalness', 'Liveness', 'Speechiness', 'Valence',
                'Tempo', 'Loudness']
genres_size = data_genre.groupby('Genre').size().reset_index()
genres_size[0] = genres_size[0].apply(sqrt)
######## PREPARANDO TAB 4 ########

content = html.Div(
    [
        html.H1('Spotify Data',
                style={'textAlign': 'center'}),
        html.Hr(),
    ]
)

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
app.layout = html.Div([
    content,
    dcc.Tabs(id="tabs", value='tab-1', children=[
        dcc.Tab(label='Series temporales de Features', value='tab-1'),
        dcc.Tab(label='Clusterización de una nueva canción', value='tab-2'),
        dcc.Tab(label='Análisis de clusters', value='tab-3'),
        dcc.Tab(label='Comparación de clusters', value='tab-4'),
    ]),
    html.Div(id='tabs-content')
])


@app.callback(Output('tabs-content', 'children'),
              Input('tabs', 'value'))
def render_content(tab):
    if tab == 'tab-1':
        return html.Div([
            html.H3('Evolución de Features a lo largo del tiempo',
                    style={'textAlign': 'center', 'margin-top': '15px'}),
            html.Hr(),
            dbc.Row(
                [
                    dbc.Col(html.H3('Features'), width={"size": 8, "offset": 2}),
                ]
            ),
            dbc.Row(
                [
                    dbc.Col(dcc.Graph(id="graph", figure=fig_features),
                            width={"size": 8, "offset": 2}),
                ]
            ),
            dbc.Row(
                [
                    dbc.Col(html.H3('Loudness'), width={"size": 8, "offset": 2}),
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
                    dbc.Col(html.H3('Tempo'), width={"size": 8, "offset": 2}),
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
            html.H3('Introduzca las características de la canción',
                    style={'textAlign': 'center', 'margin-top': '15px'}),
            html.Hr(),
            # Acousticness, Danceability & Energy
            dbc.Form([dbc.Row([
                dbc.Col(dbc.InputGroup(
                [
                    dbc.InputGroupAddon("Acousticness", addon_type="prepend"),
                    dbc.Input(id="acousticness", type="number", placeholder="Acousticness",
                                      min=0, max=1, step=0.0001, required=True),
                ],
                className="mb-3",
                ), width={"size": 3, "offset": 1}),
                dbc.Col(
                    dbc.InputGroup(
                        [
                            dbc.InputGroupAddon("Danceability", addon_type="prepend"),
                            dbc.Input(id="danceability", type="number", placeholder="Danceability",
                                      min=0, max=1, step=0.0001, required=True),
                        ],
                        className="mb-3",
                    ), width={"size": 3}
                ),
                dbc.Col(dbc.InputGroup(
                    [
                        dbc.InputGroupAddon("Energy", addon_type="prepend"),
                        dbc.Input(id="energy", type="number", placeholder="Energy", min=0, max=1,
                                  step=0.0001, required=True),
                    ],
                    className="mb-3",
                ), width={"size": 3, "offset": -1})
            ]),
            # Instrumentalness, Liveness & Loudness
            dbc.Row([
                dbc.Col(
                    dbc.InputGroup(
                        [
                            dbc.InputGroupAddon("Instrumentalness", addon_type="prepend"),
                            dbc.Input(id="instrumentalness", type="number", placeholder="Instrumentalness",
                                      min=0, max=1, step=0.0001, required=True),
                        ],
                        className="mb-3",
                    ), width={"size": 3, "offset": 1}
                ),
                dbc.Col(dbc.InputGroup(
                    [
                        dbc.InputGroupAddon("Liveness", addon_type="prepend"),
                        dbc.Input(id="liveness", type="number", placeholder="Liveness", min=0,
                                  max=1, step=0.0001, required=True),
                    ],
                    className="mb-3",
                ), width={"size": 3}),
                dbc.Col(
                    dbc.InputGroup(
                        [
                            dbc.InputGroupAddon("Loudness", addon_type="prepend"),
                            dbc.Input(id="loudness", type="number", placeholder="Loudness",
                                      min=-60, max=0, step=0.0001, required=True),
                        ],
                        className="mb-3",
                    ), width={"size": 3, "offset": -1}
                )
            ]),

            # Tempo, Valence & Speechiness
            dbc.Row([
                dbc.Col(dbc.InputGroup(
                    [
                        dbc.InputGroupAddon("Tempo", addon_type="prepend"),
                        dbc.Input(id="tempo", type="number", placeholder="Tempo", min=50, max=150,
                                  step=0.0001, required=True),
                    ],
                    className="mb-3",
                ), width={"size": 3, "offset": 1}),
                dbc.Col(
                    dbc.InputGroup(
                        [
                            dbc.InputGroupAddon("Valence", addon_type="prepend"),
                            dbc.Input(id="valence", type="number", placeholder="Valence", min=0,
                                      max=1, step=0.0001, required=True),
                        ],
                        className="mb-3",
                    ), width={"size": 3}
                ),
                dbc.Col(dbc.InputGroup(
                    [
                        dbc.InputGroupAddon("Speechiness", addon_type="prepend"),
                        dbc.Input(id="speechiness", type="number", placeholder="Speechiness",
                                  min=0, max=1, step=0.0001, required=True),
                    ],
                    className="mb-3",
                ), width={"size": 3, "offset": -1}),
            ]),

            dbc.Row([
                dbc.Col(
                    dbc.Button("Enviar", color="warning", className="mr-1", id='submit-val',
                               size='md'), width={"size": 4, "offset": 5})
                ]
            )]),
            html.Hr(),
            html.H5('Resultados obtenidos:',
                    style={'textAlign': 'center'}, id='prediction-form'),
        ])
    elif tab == 'tab-3':
        return html.Div([
            html.H3('Características agrupadas por Cluster',
                    style={'textAlign': 'center', 'margin-top': '15px'}),
            html.Hr(),
            dbc.Row(
                [
                    dbc.Col(dcc.Dropdown(
                        id="dropdown",
                        options=[{"label": x, "value": x} for x in genres],
                        value=genres[0],
                        clearable=False,
                    ),
                        width={"size": 2, "offset": 1})
                ]
            ),
            dbc.Row(
                [
                    dbc.Col(dcc.Graph(id="bar-chart"),
                            width={"size": 8, "offset": 1}),
                ]
            ),
            dbc.Row(
                [
                    dbc.Col(id="genre-table", width={"size": 8, "offset": 1}),
                ]
            )

        ])
    elif tab == 'tab-4':
        return html.Div([
            html.H3('Comparación de características entre clusters', style={'textAlign': 'center', 'margin-top': '15px'}),
            html.Hr(),
            dbc.Row(
                [
                    dbc.Col(dcc.Dropdown(
                        id="dropdownF",
                        options=[{"label": x, "value": x} for x in all_features],
                        value=all_features[0],
                        clearable=False,
                    ),
                        width={"size": 2, "offset": 1})
                ]
            ),
            dbc.Row(
                [
                    dbc.Col(dcc.Graph(id="box-plot"),
                            width={"size": 10, "offset": 1}),
                ]
            ),
            html.H3('Popularidad por Feature', style={'textAlign': 'center', 'margin-top': '15px'}),
            html.Hr(),
            dbc.Row(
                [
                    dbc.Col(dcc.Graph(id="bubble-plot"),
                            width={"size": 10, "offset": 1}),
                ]
            ),
        ])


@app.callback(
    Output("number-out", "children"),
    Input("dfalse", "value"),
    Input("dtrue", "value"),
    Input("input_range", "value"),
)
def number_render(fval, tval, rangeval):
    return "dfalse: {}, dtrue: {}, range: {}".format(fval, tval, rangeval)


# Botón enviar formulario
@app.callback(
    Output("prediction-form", "children"),
    [Input("submit-val", "n_clicks")],
    [State("acousticness", "value"), State("danceability", "value"),
     State("energy", "value"),
     State("instrumentalness", "value"),
     State("liveness", "value"),
     State("loudness", "value"), State("tempo", "value"),
     State("valence", "value"),
     State("speechiness", "value")],
)
def update_output(n_clicks, v_acousticness, v_danceability, v_energy,
                  v_instrumentalness, v_liveness, v_loudness, v_tempo, v_valence, v_speechiness):
    if n_clicks > 0:
        print()
        return 'Género al que pertenece {}'.format(
            predict(
                [[v_acousticness, v_danceability, v_energy, v_instrumentalness, v_liveness, v_loudness, v_speechiness,
                  v_tempo, v_valence]])[0]
        )


@app.callback(
    Output("bar-chart", "figure"),
    Output("genre-table", "children"),
    [Input("dropdown", "value")])
def update_bar_chart(genre):
    values = grouped_data[grouped_data['Genre'] == genre]
    values = values[features]
    data_dict = {
        'Feature': [],
        'Value': []
    }
    for c in values.columns:
        data_dict['Feature'].append(c)
        data_dict['Value'].append(values[c].values[0])

    df = pd.DataFrame(data=data_dict, columns=['Feature', 'Value'])
    fig = go.Figure()
    fig.add_trace(go.Bar(x=df['Feature'], y=df['Value'], marker_color=px.colors.qualitative.Pastel1))

    return fig, dbc.Table.from_dataframe(aux_data[aux_data['Genre'] == genre].head(4), striped=True, hover=True)


@app.callback(
    Output("box-plot", "figure"),
    Output("bubble-plot", "figure"),
    [Input("dropdownF", "value")])
def update_bar_chart(feature):
    fig = go.Figure()
    bubble_fig = go.Figure()
    for genre in np.unique(data_genre['Genre'].tolist()):
        fig.add_trace(go.Box(y=data_genre[data_genre['Genre'] == genre][feature], name=str(genre)))
        bubble_fig.add_trace(go.Scatter(x=grouped_data[grouped_data['Genre'] == genre]['Popularity'],
                                        y=grouped_data[grouped_data['Genre'] == genre][feature], name=str(genre),
                                        marker_size=genres_size[grouped_data['Genre'] == genre][0]))

    fig.update_layout(
        xaxis=dict(
            title='Clusters',
        ),
        yaxis=dict(
            title=feature,
        )
    )
    bubble_fig.update_layout(
        xaxis=dict(
            title='Popularity',
        ),
        yaxis=dict(
            title=feature,
        )
    )
    return fig, bubble_fig


if __name__ == '__main__':
    app.run_server(port=8083, debug=True)
