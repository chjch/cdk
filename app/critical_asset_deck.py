import json
import pydeck as pdk
import dash_deck

from utils import *
from building_deck import building_layer

icon_data = {
    'Electric Power Plant': {"url": "assets/image/electricity.png",
                             "width": 292, "height": 292, "anchorY": 292},
    'Communication Facility': {"url": "assets/image/communication.png",
                               "width": 292, "height": 292, "anchorY": 292},
    'Drinking Water Facility': {"url": "assets/image/drink-water.png",
                                "width": 292, "height": 292, "anchorY": 292},
    'Hazardous Waste Facility': {"url": "assets/image/haz-waste.png",
                                 "width": 292, "height": 292, "anchorY": 292},
    'Solid Waste Facility': {"url": "assets/image/solid-waste.png",
                             "width": 292, "height": 292, "anchorY": 292}
}

df = geojson_to_json_point(critical_assets_geojson,
                           ['Name', 'Address', 'Facility Type'])

df['icon_data'] = df['Facility Type'].apply(lambda x: icon_data.get(x))

view_state = pdk.ViewState(
    latitude=29.805019, longitude=-85.298468,
    bearing=28, pitch=55, zoom=15.2,
)

icon_layer = pdk.Layer(
    type="IconLayer",
    data=df,
    get_icon="icon_data",
    get_size=20,
    size_scale=2,
    get_position=["lon", "lat"],
    pickable=True,
)

building_geojson_data = json.load(open(building_geojson))

r = pdk.Deck(layers=[building_layer(building_geojson_data,
                                    [200, 200, 200, 80],
                                    pickable=False),
                     icon_layer],
             initial_view_state=view_state,
             map_provider='mapbox',
             map_style=mapbox_style_building,
             api_keys={'mapbox': mapbox_api_token})

tooltip_html = '''
    <table>
        <tr>
            <td><strong>Facility Type</strong></td>
            <td>{Facility Type}</td>
        </tr>
        <tr>
            <td><strong>Name</strong></td>
            <td>{Name}</td>
        </tr>
        <tr>
            <td><strong>Address</strong></td>
            <td>{Address}</td>
        </tr>
    </table>
'''

tooltip_style = {
    'color': 'white',
    'padding': '10px',
    'border-radius': '15px',
    'background-color': 'rgba(0, 0, 0, 0.8)'
}

icon_deck = dash_deck.DeckGL(r.to_json(), id="icon-deck",
                             mapboxKey=mapbox_api_token,
                             tooltip={'html': tooltip_html,
                                      "style": tooltip_style})
