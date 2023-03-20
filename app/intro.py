from dash import html

trans_msg = """
Cedar Key is connected to the mainland along state road 24 across a series of
low bridges.
Secondary roads including 3rd Ave., Whiddon Ave., Gulf Blvd., and Hodges Ave.
serve to connect the entire island.
Areas of 24 and the internal feeder roads are at risk from nuisance flooding
and sever risk from storms.
"""

comm_msg = """
Cedar Key is a fully functioning community with a historic walkable downtown,
a school, churches, library and other amenities that contribute to the
well-being of its residents.
The community derives strength form the diversity of its community serving
assets. 
"""

resrc_msg = """
Cedar Key has always been a place where the natural ecosystem has been
instrumental to the success of the Island.
Whether for timber, fishing, clamming, or tourism, Cedar Key’s ecosystem
services are the reason for the city’s prosperity over time.
"""

trism_msg = """
Cedar Key’s mix of fishery, port, and tourist economies gives the community
character and resilience to economic or natural system changes.
From its earlier times as a port, through years as a fishing area, to its
current clamming industry. Cedar Key has also maintained a vibrant service
sector that now supports its tourist economy.
"""

overall_msg = """
“… an asset whose loss… would result in significant adverse
impacts to human life or health, national security, or critical economic
assets."
Assets have been determined through an analysis of publicly available data then
edited through engagement with Cedar Key residents and stakeholders.
"""

infra_msg = """
Cedar Key has a small number of critical infrastructures that keep it working.
"""

msg_dict = {
    'comm': ["Community and Emergency Facilities", comm_msg],
    'infra': ["Critical Infrastructure", infra_msg],
    'resrc': ["Natural Cultural and Historical Resources", resrc_msg],
    'trans': ["Transportation", trans_msg],
    'trism': ["Tourism and Economy", trism_msg],
    'overall': ["All Critical Assets", overall_msg]
}


def intro_msg(msg: str = 'overall'):
    if msg == 'overall':
        header = 'Critical Assets Exposure Analysis'
    else:
        header = msg_dict[msg][0]
    return html.Div(
        [
            html.H4(header),
            html.P(msg_dict[msg][1].strip())
        ]
    )
