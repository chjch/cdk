from dash import html

msg = """
Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor
incididunt ut labore et dolore magna aliqua. Lobortis elementum nibh tellus
molestie nunc non blandit. Morbi blandit cursus risus at. Mus mauris vitae
ultricies leo integer malesuada nunc vel risus. Nunc lobortis mattis aliquam
faucibus purus in massa tempor nec. Feugiat sed lectus vestibulum mattis.
Posuere urna nec tincidunt praesent semper feugiat nibh. Id venenatis a
condimentum vitae sapien pellentesque habitant morbi. Ac tortor vitae purus
faucibus ornare suspendisse sed nisi. Ornare aenean euismod elementum nisi quis
eleifend quam adipiscing. Id volutpat lacus laoreet non curabitur gravida arcu.
Morbi non arcu risus quis varius quam. Nec sagittis aliquam malesuada bibendum
arcu. Euismod nisi porta lorem mollis aliquam ut porttitor leo. Sagittis vitae
et leo duis ut diam quam nulla. Vitae et leo duis ut diam quam.
Ut tortor pretium viverra suspendisse potenti nullam ac.
"""

intro = html.Div(
    [
        html.H4('Vulnerability Assessment'),
        html.P(msg.strip())
    ]
)
