import os

import dash
from dash import Dash, html, Input, Output
import dash_bootstrap_components as dbc

# external CSS stylesheets
BS = "https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/css/bootstrap.min.css"
external_stylesheets = [
    {'src': 'https://api.tiles.mapbox.com/mapbox-gl-js/v2.6.1/mapbox-gl.css',
     'rel': 'stylesheet'},
    dbc.themes.MATERIA,
    # BS
]

app = Dash(
    __name__,
    use_pages=True,
    external_stylesheets=external_stylesheets,
    suppress_callback_exceptions=True
)
app.title = 'Cedar Key Dashboard'

server = app.server

app.layout = html.Div(
    dash.page_container
)

app.clientside_callback(
    """function () {
        setTimeout(function() {addListeners()}, 1000);
        return 0;
    }""",
    Output("intro-message", 'n_clicks'),
    Input("line-chart", 'figure')
)

if __name__ == "__main__":
    app.run_server(
        debug=False, host="0.0.0.0",
        port=int(os.environ.get('PORT', 8080))
    )
