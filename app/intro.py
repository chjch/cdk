from dash import html
from dash import dcc

trans_msg = dcc.Markdown("""
    **Overview**: Cedar Key is connected to the mainland along State Road 24
    across a series of low bridges; secondary roads including 3rd Ave.,
    Whiddon Ave., Gulf Blvd., and Hodges Ave serve to connect the entire
    island.
    
    **Challenges**: Areas of State Road 24 and internal feeder roads are at
    risk from nuisance flooding and completely impassable during storms.
    Residents and visitors may face travel disruptions, lack of reliable
    municipal services, and significant damage to vehicles and other property
    that comes into contact with salty floodwaters.
    
    **Value Statement**: Improving the community connections across the City
    of Cedar Key and maintaining consistent access to the mainland.
    Ensuring access routes weather the rise and fall of tides is of primary
    importance. 
""")

comm_msg = dcc.Markdown("""
    **Overview**: Cedar Key derives strength from the diversity of its
    community services. The city has a historic walkable downtown, a school,
    churches, library, and other amenities that contribute to the wellbeing of
    its residents. These elements contribute to the sense of place that
    attracts and retains a mix of long-term residents and visitors to the
    community.
    
    **Challenges**: Rising tides and erosion of shorelines has also led to
    increased exposure of community assets to flooding. Assets at risk include
    access to the school, main pedestrian tourist and restaurant areas,
    post office, library, city hall, fire station, and food bank. Due to the
    location of these assets near to the coast and their important services,
    they are of highest priority for protection from sea level rise and flood
    risk.

    **Value Statement**: Strengthening the network of community services
    against flooding is a key to the long-term resilience of the community
    including economic prosperity and quality of life to residents of the
    greater community.
""")

resrc_msg = dcc.Markdown("""
    **Overview**: Cedar Key is a community with much forestland and an active
    coastline. Whether for timber, fiber, fishing, clamming, or tourism,
    Cedar Key’s ecosystem services are the reason for the City’s prosperity
    over time. This environment has changed over time and the City of Cedar
    Key has evolved alongside these changes.
    
    **Challenges**: Erosion of shorelines has led to loss of recreational
    areas and increased exposure of assets to flooding. Aquaculture leases are
    at risk due to rising temperatures and sport fisheries share concerns as
    habitat mosaics and fish species continue to change. Increasing
    sanitization of groundwater is stressing urban trees and upland
    vegetation, leading to die-offs in certain areas.
     
    **Value Statement**: Bolstering the ecosystem services that support the
    clam economy, sport fishing, outdoor recreation, and coastal tourism
    against flooding is critical for the city’s natural and cultural capital.
    Cedar Key serves as an example community for other natural-resource-based
    coastal economies.
""")

economy_msg = dcc.Markdown("""
    **Overview**: Cedar Key’s mix of hard clam/oyster aquaculture, sport
    fishing, recreational boating, watersports, and coastal tourism provides
    the city’s economic vitality and community character.
    From earlier times as a port, through years as a fishing area, to its
    current clam aquaculture industry, Cedar Key has also maintained a vibrant
    water-based economy that provides economic resilience to Cedar Key.
    
    **Challenges**: The city’s economy relies heavily on high water quality
    and limited disruptions to the transportation system.
    This is not only true for the aquaculture industry, but also most workers
    in town, who live off the island and commute long distances to work.
    With increased tidal flooding and storm impacts, assets at risk include
    the main shops, restaurants, and tourist areas downtown along the water’s
    edge, as well as the viability of the clamming industry.
    
    **Value Statement**: Maintaining an economic and cultural identity tied to
    the working coast is critical; the city should pursue a diverse array of
    strategies to address flooding in ways that expand aquaculture and maintain
    sport fishing, recreational boating, watersports, and coastal tourism
    activities; as well as prioritize support for the coastal workforce (such
    as affordable housing, education, etc.).
""")

housing_msg = dcc.Markdown("""
    **Overview**: Cedar Key is a historic community with a range of housing
    stock, ages, construction types, and economic values. This housing stock
    traditionally supported a diverse community across race, age, and economic
    status.
    
    **Challenges**: Like many coastal communities in Florida, Cedar Key has
    seen property values rise substantially in recent years, making housing
    unaffordable to many people. Coupled with increased risk from rising
    tides/coastal flooding, structure age, and costs of upkeep, Cedar Key’s
    housing stock is vulnerable to storm damage as well as conversion to
    short-term rental properties.
    
    **Value Statement**: Cedar Key’s housing should be affordable, resilient
    to flooding, and diverse in order to support the diverse members of the
    community.
""")

infra_msg = dcc.Markdown("""
    **Overview**: Cedar Key is a small town that has invested significantly
    in local drinking water, sewer, and stormwater networks that maintain
    critical services and functions within the City limits.
    More extensive networks of roads, electrical grids, and solid waste
    facilities maintained by the county, state, or other cooperating entities
    provide essential connectivity to mainland services.
    
    **Challenges**: Critical facilities related to drinking water and sewage
    treatment that service Cedar Key and septic tanks/private wells that
    service unincorporated areas may be more threatened by saltwater intrusion
    and rainwater flooding in the future. Contamination from shallow wells and
    septic systems impacted by sea level rise is a future risk.
    
    **Value Statement**: Ensuring the continuous functionality of these
    critical services even in exceptional flood events is a primary concern
    for the community.
""")

overall_msg = dcc.Markdown("""
    **What is Critical Asset**: “Critical asset” means an asset whose… loss…
    would result in significant adverse impacts to human life or health,
    national security, or critical economic assets.
    
    **Project Objective**: to assess comprehensive flooding vulnerability and
    create a resilience plan for the City.
    This project is funded by DEP’s Resilient Florida Program and will set
    Cedar Key up to access state infrastructure funds in the coming years to
    address flooding vulnerability.
""")

msg_dict = {
    'comm': ["Community Services", comm_msg],
    'infra': ["Critical Infrastructure", infra_msg],
    'resrc': ["Ecosystem Services, Natural & Cultural Resources", resrc_msg],
    'trans': ["Transportation Connectivity", trans_msg],
    'economy': ["Local Economy", economy_msg],
    'housing': ["Affordable Housing", housing_msg]
}


def intro_msg(msg: str = 'overall'):
    if msg == 'overall':
        return html.Div([overall_msg])
    header = msg_dict[msg][0]
    return html.Div(
        [
            html.H4(header),
            msg_dict[msg][1]
        ]
    )
