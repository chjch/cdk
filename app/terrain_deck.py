import pydeck as pdk
import os
from dotenv import load_dotenv
import dash_deck

load_dotenv()

# Import Mapbox API Key from environment
MAPBOX_API_KEY = os.getenv("MAPBOX_TOKEN")
# print(MAPBOX_API_KEY)
MAPBOX_STYLE = 'mapbox://styles/chjch/ckv84490t0hku14rzd7040xvt'

CDK_LATITUDE = 29.132572
CDK_LONGITUDE = -83.043874

pdk.settings.custom_libraries = [
    {
        "libraryName": "MyTileLayerLibrary",
        "resourceUri": "https://cdn.jsdelivr.net/gh/agressin/pydeck_myTileLayer@master/dist/bundle.js",
    }
]

SURFACE_IMAGE = "https://tiles.arcgis.com/tiles/LBbVDC0hKPAnLRpO/arcgis/" \
                "rest/services/CDK_MHHW_2022/MapServer/WMTS/tile/" \
                "1.0.0/CDK_MHHW_2022/default/default028mm/{z}/{y}/{x}.png"

custom_layer = pdk.Layer(
    "MyTileLayer",
    SURFACE_IMAGE,
    opacity=0.85
)

view_state = pdk.ViewState(
    latitude=CDK_LATITUDE, longitude=CDK_LONGITUDE,
    bearing=11, pitch=50, zoom=15.3,
    max_zoom=18,
    min_zoom=12,
)

r = pdk.Deck(custom_layer,
             initial_view_state=view_state,
             map_provider='mapbox',
             map_style=MAPBOX_STYLE,
             api_keys={'mapbox': MAPBOX_API_KEY}
             )

terrain_deck = dash_deck.DeckGL(r.to_json(), id="terrain-deck",
                                mapboxKey=MAPBOX_API_KEY)
