import dash
from dash import Input, Output, State, html, callback
import dash_bootstrap_components as dbc

dash.register_page(__name__, path="/", title="Cedar Key Dashboard")

@callback(
    Output("modal", "is_open"),
    [Input("open", "n_clicks"), Input("close", "n_clicks")],
    [State("modal", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open


disclaimer = """
    The data and maps in this tool illustrate the scale of
    potential flooding, not the exact location, and do not account
    for erosion, subsidence, or future construction.
    Although every effort has been made to ensure that information
    is comprehensive and accurate, errors and omissions may exist.
    The data and the information included therein is provided on an
    "as is" basis.
    The Florida Institute for Built Environment Resilience (FIBER),
    Florida Sea Grant, the University of Florida, or any of their
    respective faculty, staff, or administration specifically
    disclaim any warranty, either expressed or implied, including
    but not limited to the implied warranties of merchantability
    and fitness for a particular use.
    The entire risk as to quality and performance is with the user.
    This tool should be used strictly as a planning reference tool
    and not for navigation, permitting, or other legal purposes.
"""

layout = html.Div(
    children=[
        html.H1(
            children="Resilient Cedar Key",
            style={
                "color": "white",
                "font-family": "sans-serif!important",
                "font-size": "3em",
                "line-height": "200%",
                "text-align": "center",
                "margin-bottom": "0px",
            },
            className="hidden-mobile",
        ),
        html.Div(
            children="""
                A Dashboard to explore the impacts of compound flooding with
                different storm events under different sea-level rise
                scenarios.
            """,
            style={
                "color": "white",
                "width": "30%",
                "text-align": "center",
                "margin-left": "auto",
                "margin-right": "auto",
            },
            className="hidden-mobile",
        ),
        html.Img(
            src="../assets/image/rck_logo.png",
            style={"width": "350px", "margin-bottom": "20px"},
        ),
        html.Div(
            children=[
                dbc.Button("GET STARTED", className="homebtn", href="/viewer/housing"),
                # dbc.Button("LIVE TRACKER", className="homebtn", href="/tracker", style={"margin-left": "20px"})
            ],
            style={"display": "inline-block"},
        ),
        html.Div(
            children="Disclaimer",
            className="hidden-mobile",
            style={
                "color": "white",
                "font-weight": "bold",
                "font-size": "0.9em",
                "margin-top": "60px",
            },
        ),
        html.Div(
            children=disclaimer,
            className="hidden-mobile",
            style={
                "color": "#dddddd",
                "font-size": "0.8em",
                "margin-top": "10px",
                "width": "70%",
                "text-align": "center",
                "margin-left": "auto",
                "margin-right": "auto",
            },
        ),
        dbc.Button(html.I(className="fa-solid fa-info", style={"margin-left":"auto", "margin-right": "auto"}),className="show-mobile info-btn", id="open", n_clicks=0, 
                   style={
                       "height": "35px", 
                       "width": "35px", 
                       "margin-top": "25px"
                       }
                    ),
        dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle("Disclaimer"), close_button=True, className="disclaimer-header btn-close-white"),
                dbc.ModalBody(disclaimer),
                dbc.ModalFooter(
                    dbc.Button(
                        "Close", id="close", className="ms-auto show-mobile", n_clicks=0
                    )
                ),
            ],
            id="modal",
            is_open=False,
        ),
    ],
    style={
        "background-image": "url('../assets/image/splash_bg.png')",
        "background-position": "center top",
        "background-size": "cover",
        "background-repeat": "no-repeat",
        "height": "100vh",
        "align-items": "center",
        "justify-content": "center",
        "display": "flex",
        "flex-direction": "column",
    },
)