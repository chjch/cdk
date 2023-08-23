import dash
from dash import html, dcc, callback, Input, Output, State, no_update
import dash_bootstrap_components as dbc
from plotly.validator_cache import ValidatorCache

from navbar import navbar
from slr_deck import slr_scenario
from charts import line_chart, bar_chart
from intro import intro_msg

dash.register_page(
    __name__, title="Cedar Key Dashboard", path_template="/viewer/<asset_type>"
)

# chart dbc column
chart_panels = dbc.Col(
    [
        html.Div(
            children=[],
            id="intro-message",
            className="pretty_container",
            style={"height": "25vh", "overflow": "auto"},
        ),
        dcc.Graph(
            # figure={},
            id="line-chart",
            responsive=True,
            hoverData=None,
            className="pretty_container",
            config={"displayModeBar": False},
            style={"height": "33vh"},
        ),
        dcc.Graph(
            # figure={},
            id="bar-chart",
            responsive=True,
            className="pretty_container",
            style={"height": "28vh"},
        ),
    ],
    width=4,
)

map_x_slider = html.Div(
    [
        html.Div(
            "Projection Year",
            style={
                "width": "200px",
                "font-family": "Poppins",
                "font-size": "1.2em",
                "padding": "0px 0px 0px 50px",
                "color": "#0E3183",
            },
        ),
        html.Div(
            dcc.Slider(
                id="map-x-slider",
                step=None,
                marks={
                    2022: {"label": "2022", "style": {"color": "#0E3183"}},
                    2040: {"label": "2040", "style": {"color": "#0E3183"}},
                    2070: {"label": "2070", "style": {"color": "#0E3183"}},
                },
                value=2040,
                persistence=True,
            ),
            style={
                "padding": "7px 25px 0px 0px",
                "width": "calc(100% - 200px)",
            },
        ),
    ],
    className="hstack gap-2",
)

marks = {
    1: {"label": "MHHW", "style": {"color": "#0E3183"}},
    2: {"label": "EWL1R", "style": {"color": "#0E3183"}},
    3: {"label": "EWL2R", "style": {"color": "#0E3183"}},
    4: {"label": "EWL10R", "style": {"color": "#0E3183"}},
    5: {"label": "NFHL100", "style": {"color": "#0E3183"}},
    6: {"label": "CAT1", "style": {"color": "#0E3183"}},
    7: {"label": "CAT3", "style": {"color": "#0E3183"}},
    8: {"label": "CAT5", "style": {"color": "#0E3183"}},
}

map_y_slider = html.Div(
    [
        html.Div(
            "Scenario",
            style={
                "font-size": "1.2em",
                "font-family": "Poppins",
                "color": "#0E3183",
                "padding": "30px 0px 0px 0px",
            },
        ),
        html.Div(
            dcc.Slider(
                id="map-y-slider",
                step=None,
                vertical=True,
                marks=marks,
                value=3,  # EWL2R
                persistence=True,
            ),
            style={"padding": "0px 0px 0px 0px"},
        ),
    ],
    className="vstack gap-2",
    style={"height": "100%", "position": "relative"},
)

map_legend = html.Div(
    children=[],
    id="map-legend",
    className="legend",
)

map_legend_toast = html.Div(
    [
        dbc.Button(
            "Show Legend",
            id="legend-toast-toggle",
            color="primary",
            style={
                "margin-bottom": "5px",
                "text-transform": "none",
                "width": "100%",
                "font-family": "Sans-Serif",
            },
            # className="mb-3",
            n_clicks=0,
        ),
        dbc.Toast(
            [map_legend],
            id="legend-toast",
            header="",
            header_style={
                "font-size": "13.5px",
                "font-family": "Sans-Serif",
                "font-weight": "bold",
                "margin-right": "0px",
            },
            # icon="primary",
            dismissable=False,
            is_open=False,
        ),
    ],
    style={
        "bottom": "70px",
        "left": "45px",
        "width": "17%",
        "height": "auto",
        "position": "absolute",
        "z-index": 1,
    },
)

# map dbc column
map_panel = dbc.Col(
    [
        html.Div(
            [
                html.Div(
                    [
                        html.Div(
                            children=[],
                            id="map-container",
                            className="map_window",
                        ),
                        dcc.Dropdown(
                            ["Satellite", "Road map"],
                            # "Road map",
                            id="basemap-dropdown",
                            placeholder="Choose a basemap",
                            clearable=False,
                            searchable=False,
                            style={
                                "top": "25px",
                                "right": "25px",
                                "width": "41%",
                                "height": "30px",
                                "position": "absolute",
                                "z-index": 1,
                            },
                        ),
                        map_legend_toast,
                    ],
                    className="pretty_container",
                ),
                map_x_slider,
            ],
            style={"width": "95%"},
        ),
        map_y_slider,
    ],
    className="hstack gap-2",
)


def layout(asset_type=None):
    return html.Div(
        [
            dcc.Location(id="sub-path"),
            dbc.Row(navbar),
            dbc.Row(
                children=[chart_panels, map_panel],
                class_name="g-0 px-3",
            ),
        ]
    )


@callback(Output("housing-button", "active"), Input("sub-path", "pathname"))
def update_housing_button_status(pathname):
    pathname = "/" + pathname.split("/")[-1]
    if pathname == "/housing":
        return True


@callback(
    Output("map-container", "children"),
    [
        Input("sub-path", "pathname"),
        Input("map-x-slider", "value"),
        Input("map-y-slider", "value"),
        Input("basemap-dropdown", "value"),
    ],
)
def update_map(pathname, x_value, y_value, basemap):
    pathname = "/" + pathname.split("/")[-1]
    if pathname == "/viewer":
        pathname = "/"
    return slr_scenario(pathname, marks[y_value]["label"], x_value, basemap)


@callback(
    [Output("map-legend", "children"), Output("legend-toast", "header")],
    [Input("sub-path", "pathname")],
)
def update_legend(pathname):
    pathname = "/" + pathname.split("/")[-1]
    if pathname == "/transportation":
        return [
            html.Li([html.Span(className="road-level1"), "0.1 - 0.5 ft"]),
            html.Li([html.Span(className="road-level2"), "0.51 - 1 ft"]),
            html.Li([html.Span(className="road-level3"), "1.1 - 1.5 ft"]),
            html.Li([html.Span(className="road-level4"), "1.51 - 2 ft"]),
            html.Li([html.Span(className="road-level5"), "> 2 ft"]),
        ], "Depth of road flooding"
    elif pathname == "/housing":
        return [
            html.Li([html.Span(className="tile-level1"), "0.1 - 0.5 ft"]),
            html.Li([html.Span(className="tile-level2"), "0.51 - 1 ft"]),
            html.Li([html.Span(className="tile-level3"), "1.1 - 3 ft"]),
            html.Li([html.Span(className="tile-level4"), "3.1 - 6 ft"]),
            html.Li([html.Span(className="tile-level5"), "6.1 - 9 ft"]),
            html.Li([html.Span(className="tile-level6"), "9.1 - 18 ft"]),
            html.Li([html.Span(className="tile-level7"), "18.1 - 27 ft"]),
            html.Li([html.Span(className="tile-level8"), "> 27 ft"]),
        ], "Depth of flooding"
    else:
        return [
            html.P(
                "Based on First Floor Elevation (FFE) or "
                "relevant level to asset",
                style={
                    "text-align": "left",
                    "font-family": "Sans-Serif",
                    "font-size": "11px",
                },
            ),
            html.Li([html.Span(className="asset-level1"), "0.1 - 0.5 ft"]),
            html.Li([html.Span(className="asset-level2"), "0.51 - 1 ft"]),
            html.Li([html.Span(className="asset-level3"), "1.1 - 3 ft"]),
            html.Li([html.Span(className="asset-level4"), "3.1 - 6 ft"]),
            html.Li([html.Span(className="asset-level5"), "6.1 - 9 ft"]),
            html.Li([html.Span(className="asset-level6"), "9.1 - 18 ft"]),
            html.Li([html.Span(className="asset-level7"), "18.1 - 27 ft"]),
            html.Li([html.Span(className="asset-level8"), "> 27 ft"]),
        ], "Depth of asset flooding"


@callback(Output("intro-message", "children"), [Input("sub-path", "pathname")])
def update_intro_msg(pathname):
    pathname = "/" + pathname.split("/")[-1]
    if pathname == "/housing":
        return intro_msg("housing")
    elif pathname == "/critical-infrastructure":
        return intro_msg("infra")
    elif pathname == "/transportation":
        return intro_msg("trans")
    elif pathname == "/community-services":
        return intro_msg("comm")
    elif pathname == "/natural-cultural-resources":
        return intro_msg("resrc")
    elif pathname == "/local-economy":
        return intro_msg("economy")
    else:
        return intro_msg("overall")


@callback(
    Output("line-chart", "figure"),
    [Input("sub-path", "pathname"), Input("map-y-slider", "value")],
)
def update_line_chart(pathname, y_value):
    pathname = "/" + pathname.split("/")[-1]
    if pathname == "/housing":
        return line_chart("overall", marks[y_value]["label"])
    elif pathname == "/critical-infrastructure":
        return line_chart("infra", marks[y_value]["label"])
    elif pathname == "/transportation":
        return line_chart("trans", marks[y_value]["label"])
    elif pathname == "/community-emergency-facilities":
        return line_chart("comm", marks[y_value]["label"])
    elif pathname == "/natural-cultural-resources":
        return line_chart("resrc", marks[y_value]["label"])
    elif pathname == "/local-economy":
        return line_chart("economy", marks[y_value]["label"])
    else:
        return line_chart("overall", marks[y_value]["label"])


@callback(
    Output("bar-chart", "figure"),
    [
        Input("line-chart", "hoverData"),
        Input("sub-path", "pathname"),
        Input("map-y-slider", "value"),
        Input("map-x-slider", "value"),
    ],
)
def update_bar_chart(hoverdata, pathname, y_value, x_value):
    pathname = "/" + pathname.split("/")[-1]
    if hoverdata is None:
        scenario = (marks[y_value]["label"],)
        scenario = scenario[0]
        year = (x_value,)
        year = year[0]
    else:
        year = hoverdata["points"][0]["x"]
        scenario = hoverdata["points"][0]["customdata"][0]
    if pathname == "/housing":
        return bar_chart("HOUSING", scenario, year)
    elif pathname == "/critical-infrastructure":
        return bar_chart("CRITICAL INFRASTRUCTURE", scenario, year)
    elif pathname == "/transportation":
        return bar_chart("TRANSPORTATION", scenario, year)
    elif pathname == "/community-services":
        return bar_chart(
            "CRITICAL COMMUNITY AND EMERGENCY FACILITIES", scenario, year
        )
    elif pathname == "/natural-cultural-resources":
        return bar_chart(
            "NATURAL, CULTURAL, AND HISTORICAL RESOURCES", scenario, year
        )
    elif pathname == "/local-economy":
        return bar_chart("ECONOMY", scenario, year)


@callback(
    Output("line-chart", "hoverData"),
    [
        Input("map-y-slider", "value"),
        Input("map-x-slider", "value"),
    ],
)
def update_line_hover_data(y_value, x_value):
    if x_value or y_value:
        return None


@callback(
    Output("legend-toast", "is_open"),
    [Input("legend-toast-toggle", "n_clicks")],
)
def open_toast(n):
    if n == 0:
        return no_update
    if n % 2 == 0:
        return False
    else:
        return True


@callback(
    Output("legend-toast-toggle", "children"),
    [Input("legend-toast", "is_open")],
)
def change_toggle_text(is_open):
    if is_open:
        return "Hide Legend"
    else:
        return "Show Legend"


# add callback for toggling the collapse on small screens
@callback(
    Output("navbar-collapse", "is_open"),
    [Input("navbar-toggler", "n_clicks")],
    [State("navbar-collapse", "is_open")],
)
def toggle_navbar_collapse(n, is_open):
    if n:
        return not is_open
    return is_open
