import os
from dotenv import load_dotenv
import pandas as pd
# import requests
# import json

load_dotenv()
# Import Mapbox API Key from environment
mapbox_api_token = os.getenv("MAPBOX_TOKEN")
mapbox_style_building = 'mapbox://styles/chjch/cl8d69pxo000m14mqbbttpqfa'

building_geojson = 'app/data/psj_bldg.geojson'
critical_assets_geojson = 'app/data/psj_critical_infrastructure.geojson'

cesium_token = os.getenv("CESIUM_TOKEN")


def geojson_to_json_point(data_url, properties):
    df = pd.read_json(data_url)
    df['lon'], df['lat'] = zip(*list(df['features']
                                     .str.get('geometry')
                                     .str.get('coordinates')
                                     .values))
    for p in properties:
        df[p] = df['features'].str.get('properties').str.get(p)
    return df.drop(['type', 'features'], axis=1)


# modify the JSON data and bring properties one level upper
def flatten_geojson_property(
        json_dict: dict, key: str, add_comma: bool = False
) -> dict:
    for feature in json_dict['features']:
        if add_comma:
            feature[f'property_{key}'] = f"{feature['properties'][key]:,}"
        else:
            feature[f'property_{key}'] = feature['properties'][key]
    return json_dict


def cesium_tile_url(asset_id):
    return f'https://assets.cesium.com/{asset_id}/tileset.json'


# def get_cesium_asset_token(asset_id):
#     headers = {'Authorization': f'Bearer {cesium_token}'}
#     response = requests.get(
#         f'https://api.cesium.com/v1/assets/{asset_id}/endpoint',
#         headers=headers
#     )
#     return json.loads(response.text)['accessToken']
