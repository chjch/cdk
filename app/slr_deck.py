from dotenv import load_dotenv
import pandas as pd
import json

import dash_deck
from asset_points_layer import asset_points_layer
from utils import (
    scn_tile_url,
    cesium_tile_url,
    mapbox_token,
    cesium_token,
    road_json,
    bfp_json,
)

load_dotenv()

roadmap = "mapbox://styles/chjch/clksmew8z017u01qkbvbd7t32"
satellite = "mapbox://styles/mapbox/satellite-v9"

CDK_LATITUDE = 29.139219
CDK_LONGITUDE = -83.040895

CESIUM_ASSET_ID = 1891205

sun_light = {
    "@@type": "_SunLight",
    "timestamp": 1554987600000,
    "color": [255, 255, 255],
    "intensity": 2,
    "_shadow": True,
    # "direction": [-10, 10, -30]
}
# ambient_light = {
#     "@@type": "AmbientLight",
#     # "intensity": 1,
#     "color": [255, 0, 0]
# }

camera_light = {
    "@@type": "_CameraLight",
    "intensity": 1,
    "color": [11, 11, 11],
}

# point_light = {
#     "@@type": "PointLight",
#     # "timestamp": 1554927200000,
#     "color": [128, 128, 0],
#     "intensity": 1,
#     "position": [CDK_LONGITUDE, CDK_LATITUDE, 30]
# }

lighting_effect = {
    "@@type": "LightingEffect",
    "shadowColor": [100, 100, 100, 0.5],
    # "ambientLight": ambient_light,
    "cameraLight": camera_light,
    "sunLight": sun_light,
    # "pointLights": [point_light]
}


tooltip_transportation_html = """
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
"""

tooltip_housing_html = """
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
"""

tooltip_asset_html = """
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
"""


tooltip_style = {
    "font-size": "14px",
    "background-color": "rgba(255, 255, 255, 0.83)",
    "color": "black",
    "padding": "5px 5px 5px 5px",
    "border-radius": "5px",
}


def road_path_layer_data(scn, year):
    df = pd.read_json(road_json)[
        [
            "Asset Name",
            "Length (ft)",
            f"{scn}_{year}",
            f"{scn}_{year}_color",
            "path",
        ]
    ]
    df.rename(
        columns={
            f"{scn}_{year}": "Flood Depth (ft)",
            f"{scn}_{year}_color": "color",
        },
        inplace=True,
    )
    df["Flood Depth (ft)"] = df["Flood Depth (ft)"].round(2)
    return df.to_json(orient="records")


def bfp_data(scn, year):
    df = pd.read_json(bfp_json)[
        ["Asset Name", "First Floor Height (ft)", f"{scn}_{year}", "geometry"]
    ]
    df.rename(
        columns={
            # 'First Floor Height (ft)': 'First Floor (FF) Height (ft)',
            f"{scn}_{year}": "FF Flood Depth (ft)"
        },
        inplace=True,
    )
    df["FF Flood Depth (ft)"] = df["FF Flood Depth (ft)"].round(2)
    return df.to_json(orient="records")


def slr_scenario(pathname, scn_code, year, default_mb_style="Road map"):
    if default_mb_style == "Satellite":
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
        "opacity": 0.8,
    }

    bldg_3d_layer = {
        "@@type": "Tile3DLayer",
        "id": "bldg-3d",
        "loader": "@@#CesiumIonLoader",
        "opacity": 1,
        "data": cesium_tile_url(CESIUM_ASSET_ID),
        "loadOptions": {
            "cesium-ion": {"accessToken": cesium_token},
        },
        "pickable": False,
        "_subLayerProps": {
            "scenegraph": {
                "_lighting": "pbr",
                "getColor": [340, 340, 340, 300],
                "material": {
                    "ambient": 0.5,
                    "diffuse": 0.5,
                    "specularColor": [255, 255, 255],
                },
            }
        },
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
        "widthScale": 5,
    }

    if pathname == "/transportation":
        layers = [
            slr_tile_layer,
            road_segment_layer,
            asset_points_layer(scn_code, year, pathname),
        ]
        tooltip_html = tooltip_transportation_html
        if not default_mb_style:
            default_mb_style = "Satellite"
    elif pathname == "/housing" or pathname == "/":
        layers = [slr_tile_layer, bldg_3d_layer, bfp_layer]
        tooltip_html = tooltip_housing_html
    else:
        layers = [
            slr_tile_layer,
            bfp_asset_layer,
            asset_points_layer(scn_code, year, pathname),
        ]
        tooltip_html = tooltip_asset_html

    json_data = {
        "initialViewState": {
            "bearing": 0,
            "latitude": CDK_LATITUDE,
            "longitude": CDK_LONGITUDE,
            "maxZoom": 18,
            "minZoom": 12,
            "pitch": 50,
            "zoom": 15.2,
        },
        "layers": layers,
        "mapProvider": "mapbox",
        "mapStyle": mb_style,
        "views": [{"@@type": "MapView", "controller": True}],
        # "effects": [lighting_effect]
    }
    return dash_deck.DeckGL(
        json_data,
        id="terrain-deck",
        tooltip={"html": tooltip_html, "style": tooltip_style},
        mapboxKey=mapbox_token,
    )
