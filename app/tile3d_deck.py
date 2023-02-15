import dash_deck
from utils import cesium_token, mapbox_api_token, cesium_tile_url

mapbox_dark = 'mapbox://styles/mapbox/dark-v10'
mapbox_streets = 'mapbox://styles/mapbox/streets-v11'
mapbox_satellite_street = 'mapbox://styles/mapbox/satellite-streets-v11'
mapbox_satellite = 'mapbox://styles/mapbox/satellite-v9'
mapbox_light = 'mapbox://styles/mapbox/light-v10'
SURFACE_IMAGE = f"https://api.mapbox.com/v4/mapbox.satellite/" \
                f"{{z}}/{{x}}/{{y}}@2x.png?access_token={mapbox_api_token}"


ambient_light = {"@@type": "AmbientLight",
                 "color": [255, 255, 255],
                 "intensity": 2.7}
lighting_effect = {
    "@@type": "LightingEffect",
    "ambientLight": ambient_light,
}

data = {
    "initialViewState": {
        "bearing": 30,
        "latitude": 29.8126632,
        "longitude": -85.303558,
        "maxZoom": 17.5,
        "minZoom": 13,
        "pitch": 55,
        "zoom": 16,
        "maxPitch": 89
    },
    "layers": [
        {
            "@@type": "Tile3DLayer",
            "id": "tiles-psj-80_31",
            "loader": "@@#I3SLoader",
            "pointSize": 1.6,
            "opacity": 1,
            "data": cesium_tile_url(1400026),
            "loadOptions": {
                "cesium-ion": {
                    "accessToken": cesium_token
                },
            }
        },
        {
            "@@type": "Tile3DLayer",
            "id": "tiles-psj-80_29",
            "loader": "@@#CesiumIonLoader",
            "pointSize": 1.6,
            "opacity": 1,
            "data": cesium_tile_url(1400036),
            "loadOptions": {
                "cesium-ion": {
                    "accessToken": cesium_token
                },
            }
        },
        # {
        #     "@@type": "MyTileLayer",
        #     "id": "65bec2d1-2020-4670-b570-77afbca54fa0",
        #     "data": SURFACE_IMAGE,
        #     "getPolygonOffset": "[0,1]",
        # },
    ],
    "views": [
        {
            "@@type": "MapView",
            "mapStyle": mapbox_light,
            "controller": True,
            "position": [0, 0, -27],  # down shift basemap to avoid overlapping
        }
    ],
    "effects": [lighting_effect]
}

tile3d_deck = dash_deck.DeckGL(data,
                               id="tile3d-deck",
                               mapboxKey=mapbox_api_token)
