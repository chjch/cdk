import os
from dotenv import load_dotenv
import pandas as pd

import dash_deck
from asset_points_layer import asset_points_layer
from utils import (scn_tile_url, cesium_tile_url, cesium_token,
                   road_json, bfp_json, asset_points_json)

import json

load_dotenv()

MAPBOX_API_KEY = os.getenv("MAPBOX_TOKEN")  # import MAPBOX_API_KEY from .env
roadmap = 'mapbox://styles/chjch/ckv84490t0hku14rzd7040xvt'
satellite = 'mapbox://styles/mapbox/satellite-v9'

CDK_LATITUDE = 29.136219
CDK_LONGITUDE = -83.035895

# pdk.settings.custom_libraries = [
#     {
#         "libraryName": "MyTileLayerLibrary",
#         "resourceUri": "https://cdn.jsdelivr.net/gh/agressin/pydeck_myTileLayer@master/dist/bundle.js",
#     }
# ]


sun_light = {
    "@@type": "DirectionalLight",
    # "timestamp": 1554927200000,
    "color": [128, 128, 0],
    "intensity": 1,
    "_shadow": True,
    "direction": [-10, 10, -30]
}
# ambient_light = {
#     "@@type": "AmbientLight",
#     # "intensity": 1,
#     "color": [255, 0, 0]
# }

# camera_light = {
#     "@@type": "_CameraLight",
#     "intensity": 1,
#     "color": [11, 11, 11]
# }

point_light = {
    "@@type": "PointLight",
    # "timestamp": 1554927200000,
    "color": [128, 128, 0],
    "intensity": 1,
    "position": [CDK_LONGITUDE, CDK_LATITUDE, 30]
}

lighting_effect = {
    "@@type": "LightingEffect",
    "shadowColor": [0, 0, 0, 0.5],
    # "ambientLight": ambient_light,
    # "cameraLight": camera_light,
    "directionalLights": [sun_light],
    "pointLights": [point_light]
}


tooltip_transportation_html = '''
    <table>
        <tr>
            <td><strong>Asset Name</strong></td>
            <td>{Asset Name}</td>
        </tr>

        <tr>
            <td><strong>Flood Depth (ft)</strong></td>
            <td>{Flood Depth (ft)}</td>
        </tr>
    </table>
'''

tooltip_housing_html = '''
    <table>
        <tr>
            <td><strong>Asset Name</strong></td>
            <td>{Asset Name}</td>
        </tr>
        <tr>
            <td><strong>First Floor (FF) Height</strong></td>
            <td>{First Floor Height (ft)}</td>
        </tr>
        <tr>
            <td><strong>FF Flood Depth (ft)</strong></td>
            <td>{FF Flood Depth (ft)}</td>
        </tr>
    </table>
'''

tooltip_asset_html = '''
    <table>
        <tr>
            <td><strong>Asset Name</strong></td>
            <td>{Asset Name}</td>
        </tr>
        <tr>
            <td><strong>Asset Type</strong></td>
            <td>{Asset Type}</td>
        </tr>
        <tr>
            <td><strong>Flood Depth (ft)</strong></td>
            <td>{Flood Depth (ft)}</td>
        </tr>
    </table>
'''


tooltip_style = {
    "font-size": "14px",
    "background-color": "rgba(255, 255, 255, 0.83)",
    "color": "black",
    "padding": "5px 5px 5px 5px",
    "border-radius": "5px"
}


def road_path_layer_data(scn, year):
    df = pd.read_json(road_json)[
        ['Asset Name', 'Length (ft)',
         f'{scn}_{year}', f'{scn}_{year}_color', 'path']
    ]
    df.rename(columns={f'{scn}_{year}': 'Flood Depth (ft)',
                       f'{scn}_{year}_color': 'color'},
              inplace=True)
    df['Flood Depth (ft)'] = df['Flood Depth (ft)'].round(2)
    return df.to_json(orient='records')


def bfp_data(scn, year):
    df = pd.read_json(bfp_json)[
        ['Asset Name',
         'First Floor Height (ft)',
         f'{scn}_{year}',
         'geometry']
    ]
    df.rename(
        columns={
            # 'First Floor Height (ft)': 'First Floor (FF) Height (ft)',
            f'{scn}_{year}': 'FF Flood Depth (ft)'
        },
        inplace=True
    )
    df['FF Flood Depth (ft)'] = df['FF Flood Depth (ft)'].round(2)
    return df.to_json(orient='records')


def slr_scenario(pathname, scn_code, year, mapbox_style='Road map'):
    if mapbox_style == 'Satellite':
        mb_style = satellite
    else:
        mb_style = roadmap

    bfp_layer = {
        "@@type": "GeoJsonLayer",
        "id": "bfp",
        "data": json.loads(bfp_data(scn_code, year)),
        "stroked": False,
        "filled": True,
        "extruded": False,
        "pickable": True,
        "opacity": 0,
    }

    bfp_asset_layer = {
        "@@type": "GeoJsonLayer",
        "id": "bfp",
        "data": json.loads(bfp_data(scn_code, year)),
        "stroked": False,
        "filled": True,
        "extruded": False,
        "pickable": False,
        "getFillColor": [150, 150, 150],
        "opacity": 1,
    }

    slr_tile_layer = {
        "@@type": "MyTileLayer",
        "data": scn_tile_url(scn_code, year),
        "id": f"slr-tile-{scn_code}-{year}",
        "opacity": 0.8
    }

    bldg_3d_layer = {
        "@@type": "Tile3DLayer",
        "id": "bldg-3d",
        "loader": "@@#CesiumIonLoader",
        "opacity": 1,
        "data": cesium_tile_url(1635705),
        "loadOptions": {
            "cesium-ion": {
                "accessToken": cesium_token
            },
        },
        "pickable": False,
        "_subLayerProps": {
            "scenegraph": {
                '_lighting': "pbr",
                'getColor': [200, 220, 240, 220],
                'material': {
                    'ambient': 0, 'diffuse': 0,
                    'specularColor': [255, 255, 255]
                }
            }
        }
    }

    road_segment_layer = {
        "@@type": "PathLayer",
        "data": json.loads(road_path_layer_data(scn_code, year)),
        "getColor": "@@=color",
        "getPath": "@@=path",
        "getWidth": 1,
        "id": "road-segments",
        "pickable": True,
        "capRounded": True,
        "miterLimit": 1,
        "widthMinPixels": 1,
        "widthScale": 5
    }

    if pathname == '/transportation':
        layers = [slr_tile_layer, road_segment_layer,
                  asset_points_layer(scn_code, year, pathname)]
        tooltip_html = tooltip_transportation_html
        mb_style = satellite
    elif pathname == '/housing' or pathname == '/':
        layers = [slr_tile_layer, bldg_3d_layer, bfp_layer]
        tooltip_html = tooltip_housing_html
    else:
        layers = [
            slr_tile_layer,
            bfp_asset_layer,
            asset_points_layer(scn_code, year, pathname)
        ]
        tooltip_html = tooltip_asset_html

    json_data = {
        "initialViewState": {
            "bearing": 0,
            "latitude": CDK_LATITUDE,
            "longitude": CDK_LONGITUDE,
            "maxZoom": 18,
            "minZoom": 12,
            "pitch": 60,
            "zoom": 17
        },
        "layers": layers,
        "mapProvider": "mapbox",
        "mapStyle": mb_style,
        "views": [
            {
                "@@type": "MapView",
                "controller": True
            }
        ],
        # "effects": [lighting_effect]
    }
    return dash_deck.DeckGL(json_data, id="terrain-deck",
                            tooltip={"html": tooltip_html,
                                     "style": tooltip_style},
                            mapboxKey=MAPBOX_API_KEY)
