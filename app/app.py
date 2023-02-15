import os
from dash import Dash, html, dcc, Input, Output, State
import dash_bootstrap_components as dbc

from navbar import navbar
from commuter_deck import commuter_deck
from commuter_panel import commuter_panel, njob_options
from building_deck import building_deck
# from critical_asset_deck import icon_deck
from terrain_deck import terrain_deck
from tile3d_deck import tile3d_deck
from intro import intro
from charts import line_chart

# external CSS stylesheets
BS = "https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/css/bootstrap.min.css"
external_stylesheets = [
    {'src': 'https://api.tiles.mapbox.com/mapbox-gl-js/v2.6.1/mapbox-gl.css',
     'rel': 'stylesheet'},
    dbc.themes.LITERA,
    BS
]

app = Dash(__name__,
           external_stylesheets=external_stylesheets,
           suppress_callback_exceptions=True)
app.title = 'Cedar Key Dashboard'

server = app.server

try:
    IS_DEV = int(os.environ['PYCHARM_HOSTED'])
except KeyError:
    IS_DEV = 0

if IS_DEV:
    brand_href = 'http://127.0.0.1:8050/'
else:
    brand_href = 'https://portstjoe.herokuapp.com/'

map_x_slider = html.Div(
    [
        html.Div('Projection Year',
                 style={'width': '200px',
                        'font-size': '1.2em',
                        'padding': '0px 0px 0px 50px'}),
        html.Div(dcc.Slider(id='map-x-slider',
                            step=None,
                            marks={2022: '2022',
                                   2040: '2040',
                                   2070: '2070'},
                            value=2022),
                 style={'padding': '7px 25px 0px 0px',
                        'width': 'calc(100% - 200px)'})
    ],
    className="hstack gap-2"
)

map_y_slider = html.Div(
    [
        html.Div('Scenario',
                 style={
                        'font-size': '1.2em',
                        'padding': '30px 0px 0px 0px'}),
        html.Div(dcc.Slider(id='map-y-slider',
                            step=None,
                            vertical=True,
                            # verticalHeight=800,
                            marks={1: 'MHHW', 2: 'EWL1R',
                                   3: 'EWL2R', 4: 'EWL10R',
                                   5: 'NFHL100', 6: 'CAT1',
                                   7: 'CAT3', 8: 'CAT5'},
                            value=1),
                 style={'padding': '0px 0px 0px 0px'})
    ],
    className="vstack gap-2", style={"height": "100%", "position": "relative"}
)

app.layout = html.Div([
    dcc.Location(id='map-link'),
    dbc.Row(navbar),
    dbc.Row(
        children=[dbc.Col(children=[html.Div(children=intro,
                                             id='intro-message',
                                             className='pretty_container'),
                                    dcc.Graph(figure=line_chart(),
                                              id='line-chart',
                                              responsive=True,
                                              className='pretty_container',
                                              style={'height': '47vh'})],
                          width=4),
                  dbc.Col(html.Div(
                      [
                          html.Div([html.Div(children=[],
                                             id='map-container',
                                             className='pretty_container'),
                                    map_x_slider],
                                   style={'width': '95%'}),
                          map_y_slider
                      ],
                      className="hstack gap-2"))
                  ],
        class_name='g-0 px-3')
])

commuter_map = html.Div(children=[],
                        id='commuter-map',
                        className='map_window')

building_map = html.Div(children=building_deck(),
                        id='building-map',
                        className='map_window')

terrain_map = html.Div(children=[terrain_deck],
                       id='terrain-map',
                       className='map_window')

point_cloud_map = html.Div(children=[tile3d_deck],
                           id='point-cloud-map',
                           className='map_window')

report_asset = html.A('Report An Asset',
                      href='https://www.arcgis.com/apps/CrowdsourceReporter/'
                           'index.html?appid=95373653e2fc4373be0d8b572f20e501',
                      className='external-link',
                      target='_blank')


@app.callback(
    Output('commuter-map', 'children'),
    [Input('njob-picker', 'value')]
)
def update_commuter_deck(selected_njob_option):
    if selected_njob_option:
        if type(njob_options[selected_njob_option]) is int:
            selected_njob_option = [njob_options[selected_njob_option]]
        else:
            selected_njob_option = list(njob_options[selected_njob_option])
        return commuter_deck(selected_njob_option)
    else:
        return commuter_deck()


@app.callback(
    Output("map-container", "children"),
    [Input("map-link", "pathname")]
)
def update_map(pathname):
    # if pathname == "/3d-built-environment":
    #     return building_map
    if pathname == '/flood-risk-and-slr':
        return terrain_map
    elif pathname == '/lidar-point-cloud':
        return terrain_map
    # elif pathname == '/critical-assets':
    #     return icon_map
    else:
        return terrain_map


# add callback for toggling the collapse on small screens
@app.callback(
    Output("navbar-collapse", "is_open"),
    [Input("navbar-toggler", "n_clicks")],
    [State("navbar-collapse", "is_open")],
)
def toggle_navbar_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


if __name__ == "__main__":
    app.run_server(debug=False, host="0.0.0.0",
                   port=int(os.environ.get('PORT', 8080)))
