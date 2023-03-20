import os
from dash import Dash, html, dcc, Input, Output, State
import dash_bootstrap_components as dbc

from navbar import navbar
from slr_deck import slr_scenario
from intro import intro_msg
from charts import line_chart, bar_chart

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

marks = {1: 'MHHW', 2: 'EWL1R',
         3: 'EWL2R', 4: 'EWL10R',
         5: 'NFHL100', 6: 'CAT1',
         7: 'CAT3', 8: 'CAT5'}

map_y_slider = html.Div(
    [
        html.Div('Scenario',
                 style={
                        'font-size': '1.2em',
                        'padding': '30px 0px 0px 0px'}),
        html.Div(dcc.Slider(id='map-y-slider',
                            step=None,
                            vertical=True,
                            # tooltip={"placement": "bottom", "always_visible": False},
                            # verticalHeight=800,
                            marks=marks,
                            value=1),
                 style={'padding': '0px 0px 0px 0px'})
    ],
    className="vstack gap-2", style={"height": "100%", "position": "relative"}
)

app.layout = html.Div([
    dcc.Location(id='sub-path'),
    dbc.Row(navbar),
    dbc.Row(
        children=[dbc.Col(children=[html.Div(children=[],
                                             id='intro-message',
                                             className='pretty_container',
                                             style={'height': '20vh',
                                                    'overflow': 'auto'}),
                                    dcc.Graph(figure=line_chart(),
                                              id='line-chart',
                                              responsive=True,
                                              hoverData={
                                                  'points': [{
                                                      'x': 2022,
                                                      'customdata': ['MHHW']
                                                  }]
                                              },
                                              className='pretty_container',
                                              style={'height': '38vh'}),
                                    dcc.Graph(figure=bar_chart(),
                                              id='bar-chart',
                                              responsive=True,
                                              className='pretty_container',
                                              style={'height': '27vh'})],
                          width=4),
                  dbc.Col(html.Div(
                      [
                          html.Div([html.Div([
                                        html.Div(children=[],
                                                 id='map-container',
                                                 className='map_window'),
                                        html.Img(
                                            id='map-legend',
                                            src='assets/image/map-legend.png',
                                            style={'bottom': '70px',
                                                   'right': '70px',
                                                   'width': '10%',
                                                   'height': 'auto',
                                                   'position': 'absolute',
                                                   'z-index': 1}),
                                    ], className='pretty_container'),
                                    map_x_slider],
                                   style={'width': '95%'}),
                          map_y_slider
                      ],
                      className="hstack gap-2"))
                  ],
        class_name='g-0 px-3')
])


@app.callback(
    Output("map-container", "children"),
    [Input("sub-path", "pathname"),
     Input("map-x-slider", "value"),
     Input("map-y-slider", "value")]
)
def update_map(pathname, x_value, y_value):
    if pathname == '/overview':
        return slr_scenario(marks[y_value], x_value)
    else:
        return slr_scenario(marks[y_value], x_value)


@app.callback(
    Output("intro-message", "children"),
    [Input("sub-path", "pathname")]
)
def update_intro_msg(pathname):
    if pathname == "/overview":
        return intro_msg('overall')
    elif pathname == '/critical-infrastructure':
        return intro_msg('infra')
    elif pathname == '/transportation':
        return intro_msg('trans')
    elif pathname == '/community-emergency-facilities':
        return intro_msg('comm')
    elif pathname == '/natural-cultural-historical':
        return intro_msg('resrc')
    elif pathname == '/tourism-economy':
        return intro_msg('trism')
    else:
        return intro_msg('overall')


@app.callback(
    Output("line-chart", "figure"),
    [Input("sub-path", "pathname")]
)
def update_line_chart(pathname):
    if pathname == "/overview":
        return line_chart('overall')
    elif pathname == '/critical-infrastructure':
        return line_chart('infra')
    elif pathname == '/transportation':
        return line_chart('trans')
    elif pathname == '/community-emergency-facilities':
        return line_chart('comm')
    elif pathname == '/natural-cultural-historical':
        return line_chart('resrc')
    elif pathname == '/tourism-economy':
        return line_chart('trism')
    else:
        return line_chart('overall')


@app.callback(
    Output("bar-chart", "figure"),
    [Input("line-chart", 'hoverData'),
     Input("sub-path", "pathname")]
)
def update_bar_chart(hoverdata, pathname):
    year = hoverdata['points'][0]['x']
    scenario = hoverdata['points'][0]['customdata'][0]
    if pathname == "/overview":
        return bar_chart('overall', scenario, year)
    elif pathname == '/critical-infrastructure':
        return bar_chart('CRITICAL INFRASTRUCTURE', scenario, year)
    elif pathname == '/transportation':
        return bar_chart('TRANSPORTATION', scenario, year)
    elif pathname == '/community-emergency-facilities':
        return bar_chart('COMMUNITY AND EMERGENCY FACILITIES', scenario, year)
    elif pathname == '/natural-cultural-historical':
        return bar_chart('NATURAL/CULTURAL/HISTORICAL RESOURCE', scenario, year)
    elif pathname == '/tourism-economy':
        return bar_chart('TOURISM/ECONOMY', scenario, year)
    else:
        return bar_chart('overall', scenario, year)


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


app.clientside_callback(
    """function () {
        setTimeout(function() {addListeners()}, 1000);
        return 0;
    }""",
    Output("intro-message", 'n_clicks'),
    Input("line-chart", 'figure')
)

if __name__ == "__main__":
    app.run_server(debug=False, host="0.0.0.0",
                   port=int(os.environ.get('PORT', 8080)))
