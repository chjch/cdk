import os

import dash
from dash import Dash, html, Input, Output
import dash_bootstrap_components as dbc

# external JS scripts
external_scripts = [
    {
        "src": "https://cdnjs.cloudflare.com/ajax/libs/shepherd.js/11.1.1/js/shepherd.min.js"
    },
    {"src": "https://cdn.jsdelivr.net/npm/@floating-ui/core@1.3.0"},
    {"src": "https://cdn.jsdelivr.net/npm/@floating-ui/dom@1.3.0"},
]
# external CSS stylesheets
BS = "https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/css/bootstrap.min.css"
external_stylesheets = [
    {
        "src": "https://api.tiles.mapbox.com/mapbox-gl-js/v2.6.1/mapbox-gl.css",
        "rel": "stylesheet",
    },
    "https://cdnjs.cloudflare.com/ajax/libs/shepherd.js/11.1.1/css/shepherd.css",
    "https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600&display=swap",
    dbc.themes.MATERIA,
    dbc.icons.FONT_AWESOME,  # Font Awesome icons
    # BS
]

app = Dash(
    __name__,
    use_pages=True,
    external_scripts=external_scripts,
    external_stylesheets=external_stylesheets,
    suppress_callback_exceptions=True,
)
app.title = "Cedar Key Dashboard"
server = app.server
app.layout = html.Div(dash.page_container)
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        <!-- Google tag (gtag.js) --> 
        <script async src=https://www.googletagmanager.com/gtag/js?id=G-B38C8RBNMV></script> 
        <script> 
            window.dataLayer = window.dataLayer || []; 
            function gtag(){dataLayer.push(arguments);} 
            gtag('js', new Date()); gtag('config', 'G-B38C8RBNMV'); 
        </script>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

app.clientside_callback(
    """function () {
        setTimeout(function() {addListeners()}, 1000);
        setTimeout(function() {createIntroTour()}, 300);
        return 0;
    }""",
    Output("intro-message", "n_clicks"),
    Input("line-chart", "figure"),
)

if __name__ == "__main__":
    app.run_server(
        debug=False, host="0.0.0.0", port=int(os.environ.get("PORT", 8080))
    )