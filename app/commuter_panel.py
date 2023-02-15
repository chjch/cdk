from dash import html, dcc

njob_options = {
    'Less than 5 jobs': 1,
    'Between 5 and 15 jobs': 2,
    'Between 16 and 30 jobs': 3,
    'More than 30 jobs': (4, 5)
}

commuter_dropdown = dcc.Dropdown(id='njob-picker',
                                 className='dropdown',
                                 options=list(njob_options.keys()))

commuter_range_slider = dcc.RangeSlider(
    min=0,
    max=300,
    step=None,
    marks={
        0: '0',
        5: '5',
        10: '10',
        15: '15',
        20: '20',
        25: '25',
        30: '30',
        300: 'over 30'
    },
    id='njob-slider'
)

commuter_panel = html.Div(
    className='pretty_container',
    children=[
        html.Div("Filter by Number of Jobs"),
        commuter_dropdown
        # commuter_range_slider
    ]
)
