from dash import html
import dash_bootstrap_components as dbc

NAVBAR_LOGO = "assets/image/seagrantuf.png"
NAVBAR_BRAND_TITLE = "Resilient Cedar Key"

navbar_brand = html.A(
    # Use row and col to control vertical alignment of logo / brand
    dbc.Row(
        [
            dbc.Col(html.Img(src=NAVBAR_LOGO, height="30px")),
            dbc.Col(dbc.NavbarBrand(NAVBAR_BRAND_TITLE,
                                    className="ms-2")),
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
            href=f'/{href}',
            className="ms-2 rounded-pill", n_clicks=0
        ),
        width="auto",
    )


overview_link = navbar_link('Overview', 'flood-risk-and-slr')
housing_link = navbar_link('Housing', 'flood-risk-and-slr')
transport_link = navbar_link('Transportation', 'flood-risk-and-slr')
community_link = navbar_link('Community and Emergency Facilities',
                             'flood-risk-and-slr')
resource_link = navbar_link('Natural Cultural and Historical Resources',
                            'flood-risk-and-slr')
tourist_link = navbar_link('Tourism and Economy', 'flood-risk-and-slr')

navbar_right = dbc.Row(
    [overview_link, housing_link,
     transport_link, community_link,
     resource_link, tourist_link],
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
    # color="#",
    dark=False,
    class_name='px-4 py-3',
    # style={'box-shadow': '1px 1px 1px black'}
)
