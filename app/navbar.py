from dash import html
import dash_bootstrap_components as dbc

NAVBAR_LOGO = "/assets/image/seagrantuf.png"
NAVBAR_BRAND_TITLE = "Resilient Cedar Key"

navbar_brand = html.A(
    # Use row and col to control vertical alignment of logo / brand
    dbc.Row(
        [
            dbc.Col(html.Img(src=NAVBAR_LOGO, height="40px")),
            dbc.Col(
                dbc.NavbarBrand(
                    NAVBAR_BRAND_TITLE,
                    className="ms-2",
                    style={
                        "font-size": "1.6em",
                        "font-family": "poppins",
                        "padding-left": "20px",
                        "color": "#0E3183",
                    },
                )
            ),
        ],
        align="center",
        className="g-0",
    ),
    href="/",
    style={"textDecoration": "none"},
)


def navbar_btn(name: str, href: str):
    return dbc.Col(
        dbc.Button(
            name,
            color="primary",
            id=f"{name.replace(' ', '').lower()}-button",
            href=f"/viewer/{href}",
            className="ms-2 rounded-pill btn",
            n_clicks=0,
        ),
        width="auto",
    )


navbar_right = dbc.Row(
    [
        navbar_btn("Housing", "housing"),
        navbar_btn("Transportation", "transportation"),
        navbar_btn("Critical Infrastructure", "critical-infrastructure"),
        navbar_btn("Community Services", "community-services"),
        navbar_btn(
            "Natural & Cultural Resources", "natural-cultural-resources"
        ),
        navbar_btn("Local Economy", "local-economy"),
    ],
    className="g-0 ms-auto flex-nowrap mt-3 mt-md-0",
    id="navbar-links-group",
    # align="center",
)

navbar = dbc.Navbar(
    dbc.Container(
        [
            navbar_brand,
            dbc.NavbarToggler(id="navbar-toggler", n_clicks=0),
            dbc.Collapse(
                navbar_right, id="navbar-collapse", is_open=False, navbar=True
            ),
        ],
        fluid=True,
        class_name="px-4",
    ),
    color="#ffffff",
    dark=False,
    class_name="px-4 py-3",
    # style={'box-shadow': '1px 1px 1px black'}
)
