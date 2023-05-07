from dash import html
import dash_bootstrap_components as dbc

NAVBAR_LOGO = "/assets/image/seagrantuf.png"
NAVBAR_BRAND_TITLE = "Resilient Cedar Key"

navbar_brand = html.A(
    # Use row and col to control vertical alignment of logo / brand
    dbc.Row(
        [
            dbc.Col(html.Img(src=NAVBAR_LOGO, height="40px")),
            dbc.Col(dbc.NavbarBrand(NAVBAR_BRAND_TITLE,
                                    className="ms-2",
                                    style={"font-size": "1.6em",
                                           "padding-left": "20px"})),
        ],
        align="center",
        className="g-0",
    ),
    href="/",
    style={"textDecoration": "none"},
)


def navbar_link(name: str, href: str):
    return dbc.Col(
        dbc.Button(
            name, color="primary",
            id=f"{name.replace(' ', '').lower()}-button",
            href=f'/viewer/{href}',
            className="ms-2 rounded-pill btn", n_clicks=0,
        ),
        width="auto",
    )


overview_link = navbar_link('Housing',
                            'housing')
transport_link = navbar_link('Transportation',
                             'transportation')
housing_link = navbar_link('Critical Infrastructure',
                           'critical-infrastructure')
community_link = navbar_link('Community Services',
                             'community-services')
resource_link = navbar_link('Natural & Cultural Resources',
                            'natural-cultural-resources')
tourist_link = navbar_link('Local Economy',
                           'local-economy')

navbar_right = dbc.Row(
    [
        overview_link,
        transport_link,
        housing_link,
        community_link,
        resource_link,
        tourist_link
    ],
    className="g-0 ms-auto flex-nowrap mt-3 mt-md-0",
    align="center",
)

navbar = dbc.Navbar(
    dbc.Container(
        [
            navbar_brand,
            dbc.NavbarToggler(id="navbar-toggler", n_clicks=0),
            dbc.Collapse(
                navbar_right,
                id="navbar-collapse",
                is_open=False,
                navbar=True
            )
        ],
        fluid=True,
        class_name='px-4',
    ),
    color="#ffffff",
    dark=False,
    class_name='px-4 py-3',
    # style={'box-shadow': '1px 1px 1px black'}
)
