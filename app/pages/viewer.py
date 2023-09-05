import dash
from dash import html, dcc, callback, Input, Output, State, no_update
import dash_bootstrap_components as dbc
from plotly.validator_cache import ValidatorCache

from navbar import navbar
from slr_deck import slr_scenario
from charts import line_chart, bar_chart
from intro import intro_msg
from utils import collapse_component

dash.register_page(
    __name__, title="Flood Risk Viewer", path_template="/viewer/<asset_type>"
)

# chart dbc column
chart_column = dbc.Col(
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
chart_column = collapse_component(
    chart_column,
    is_open=True,
    dash_component_id="chart-panel-collapse",
    dimension="width",
)
x_slider_marks = {
    2022: {"label": "2022", "style": {"color": "#0E3183"}},
    2040: {"label": "2040", "style": {"color": "#0E3183"}},
    2070: {"label": "2070", "style": {"color": "#0E3183"}},
}
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
                marks=x_slider_marks,
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
map_x_slider = collapse_component(map_x_slider, True, "map-x-slider-collapse")
y_slider_marks = {
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
                marks=y_slider_marks,
                value=3,  # EWL2R
                persistence=True,
            ),
            style={"padding": "0px 0px 0px 0px"},
        ),
    ],
    className="vstack gap-2",
    style={"height": "100%", "position": "relative"},
)
map_y_slider = collapse_component(
    map_y_slider, True, "map-y-slider-collapse", dimension="width"
)
map_legend = html.Div(
    children=[],
    id="map-legend",
    className="legend",
)
map_legend_btn_content = html.Span(
    [
        html.Div(
            "Show Legend",
            id="legend-text",
            style={"paddingRight": "0.5vw", "display": "inline-block"},
        ),
        html.I(
            className="	fa fa-chevron-circle-up",
            id="legend-icon",
            style={"display": "inline-block"},
        ),
    ]
)
map_legend_toast = html.Div(
    [
        dbc.Button(
            map_legend_btn_content,
            id="legend-button",
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
        "width": "15%",
        "max-width": "200px",
        "min-width": "160px",
        "height": "auto",
        "position": "absolute",
        "z-index": 1,
    },
)
basemap_dropdown = dcc.Dropdown(
    ["Satellite", "Road map"],
    id="basemap-dropdown",
    placeholder="Choose a basemap",
    clearable=False,
    searchable=False,
    style={
        "top": "20px",
        "right": "20px",
        "width": "41%",
        "height": "30px",
        "max-width": "230px",
        "min-width": "200px",
        "position": "absolute",
        "z-index": 1,
    },
)
map_expansion_btn = dbc.Button(
    children=html.I(className="fas fa-expand", id="map-expansion-icon"),
    id="map-expansion-btn",
    color="primary",
    # className="mb-3",
    n_clicks=0,
    style={
        "top": "40px",
        "left": "40px",
        "padding": "5px",
        "width": "40px",
        "height": "40px",
        "font-size": "1.2em",
        "position": "absolute",
        "z-index": 1,
    },
)
main_map = html.Div(
    children=[],
    id="map",
    className="map_viewport",
)
# --- map dbc column ---
map_column = dbc.Col(
    [
        html.Div(
            [
                html.Div(
                    [
                        main_map,
                        map_expansion_btn,
                        basemap_dropdown,
                        map_legend_toast,
                    ],
                    id="map-container",
                    className="pretty_container",
                ),
                map_x_slider,
            ],
            id="map-panel",
            style={"width": "95%"},
        ),
        map_y_slider,
    ],
    className="hstack gap-2",
)


# the main layout of the page
def layout(asset_type=None):
    return html.Div(
        [
            dcc.Location(id="sub-path"),
            dbc.Row(navbar),
            dbc.Row(
                id="content",
                children=[chart_column, map_column],
                className="g-0 px-3",
            ),
        ]
    )


@callback(Output("housing-button", "active"), Input("sub-path", "pathname"))
def update_housing_button_status(pathname):
    pathname = "/" + pathname.split("/")[-1]
    if pathname == "/housing":
        return True


@callback(
    Output("map", "children"),
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
    return slr_scenario(
        pathname, y_slider_marks[y_value]["label"], x_value, basemap
    )


@callback(
    [
        Output("map-y-slider-collapse", "is_open"),
        Output("map-x-slider-collapse", "is_open"),
        Output("chart-panel-collapse", "is_open"),
        Output("map-panel", "style"),
        Output("map-container", "className"),
        Output("map", "className"),
        Output("content", "className"),
    ],
    [Input("map-expansion-btn", "n_clicks")],
)
def expand_map(n):
    if n == 0:
        return no_update
    if n % 2 == 0:
        return (
            True,
            True,
            True,
            {"width": "95%"},
            "pretty_container",
            "map_viewport",
            "g-0 px-3",
        )
    else:
        return (
            False,
            False,
            False,
            {"width": "100%"},
            "pretty_container_expanded",
            "map_viewport_expanded",
            "g-0 px-0",
        )


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


@callback(
    Output("line-chart", "figure"),
    [Input("sub-path", "pathname"), Input("map-y-slider", "value")],
)
def update_line_chart(pathname, y_value):
    pathname = "/" + pathname.split("/")[-1]
    if pathname == "/housing":
        return line_chart("housing", y_slider_marks[y_value]["label"])
    elif pathname == "/critical-infrastructure":
        return line_chart("infra", y_slider_marks[y_value]["label"])
    elif pathname == "/transportation":
        return line_chart("trans", y_slider_marks[y_value]["label"])
    elif pathname == "/community-services":
        return line_chart("comm", y_slider_marks[y_value]["label"])
    elif pathname == "/natural-cultural-resources":
        return line_chart("resrc", y_slider_marks[y_value]["label"])
    elif pathname == "/local-economy":
        return line_chart("economy", y_slider_marks[y_value]["label"])


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
        scenario = (y_slider_marks[y_value]["label"],)
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
            "COMMUNITY SERVICES", scenario, year
        )
    elif pathname == "/natural-cultural-resources":
        return bar_chart(
            "NATURAL & CULTURAL RESOURCES", scenario, year
        )
    elif pathname == "/local-economy":
        return bar_chart("LOCAL ECONOMY", scenario, year)


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
    [Input("legend-button", "n_clicks")],
)
def open_toast(n):
    if n == 0:
        return no_update
    if n % 2 == 0:
        return False
    else:
        return True


@callback(
    [Output("legend-icon", "className"), Output("legend-text", "children")],
    [Input("legend-toast", "is_open")],
)
def update_map_legend_button(is_open):
    if is_open:
        return "fa fa-chevron-circle-down", "Hide Legend"
    else:
        return "fa fa-chevron-circle-up", "Show Legend"


@callback(
    Output("map-expansion-icon", "className"),
    [Input("map-x-slider-collapse", "is_open")],
)
def toggle_map_expand_btn(is_open):
    if is_open:
        return "fas fa-expand"
    else:
        return "fas fa-compress"


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
