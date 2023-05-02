import os
from dotenv import load_dotenv
# import requests
# import json

load_dotenv()
# Import Mapbox API Key from environment
mapbox_api_token = os.getenv("MAPBOX_TOKEN")
mapbox_style_building = 'mapbox://styles/chjch/cl8d69pxo000m14mqbbttpqfa'
road_json = 'app/data/road_segments.json'
bfp_json = 'app/data/bfp_props.json'
asset_points_json = 'app/data/asset_points_color.json'
cesium_token = os.getenv("CESIUM_TOKEN")


def cesium_tile_url(asset_id):
    return f'https://assets.ion.cesium.com/{asset_id}/tileset.json'


def scn_tile_url(scn_code, year):
    return "https://tiles.arcgis.com/tiles/LBbVDC0hKPAnLRpO/arcgis/" + \
           f"rest/services/CDK_{scn_code}_{year}/MapServer/WMTS/tile/" \
           f"1.0.0/CDK_{scn_code}_{year}/default/default028mm" + \
           "/{z}/{y}/{x}.png"
