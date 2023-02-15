import json
import dash_deck
import pydeck as pdk

from building_layer import building_layer
from utils import *

tooltip_html = '''
    <table>
        <tr>
            <td><strong>Blockgroup ID</strong></td>
            <td>{property_Blockgroup}</td>
        </tr>
        <tr>
            <td><strong>Number of Floor</strong></td>
            <td>{property_fakefloors}</td>
        </tr>
        <tr>
            <td><strong>Square Footage</strong></td>
            <td>{property_sqft}</td>
        </tr>
    </table>
'''

tooltip_style = {
    "font-size": "14px",
    "backgroundColor": "white",
    "color": "black"
}


def building_deck():
    geojson_data = json.load(open(building_geojson))
    geojson_layer = building_layer(geojson_data)
    # Set viewport to Downtown PSJ
    view_state = pdk.ViewState(
        latitude=29.805019, longitude=-85.298468,
        bearing=28, pitch=55, zoom=15.2,
    )

    # Renderer
    r = pdk.Deck(
        layers=[geojson_layer],
        initial_view_state=view_state,
        map_style=mapbox_style_building,
        api_keys={'mapbox': mapbox_api_token},
    )

    # flatten GeoJSON data to create tooltip
    flatten_geojson_property(geojson_data, 'Blockgroup')
    flatten_geojson_property(geojson_data, 'fakefloors')
    flatten_geojson_property(geojson_data, 'sqft', add_comma=True)

    return dash_deck.DeckGL(r.to_json(), id="building-deck",
                            mapboxKey=mapbox_api_token,
                            tooltip={'html': tooltip_html,
                                     'style': tooltip_style}
                            )
