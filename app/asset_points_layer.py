import json
import pandas as pd

from utils import asset_points_json

icon_data = {
    '/transportation': [
        'TRANSPORTATION',
        {"url": "/assets/image/transportation.png",
         "width": 100, "height": 87, "anchorY": 96,
         "mask": True}
    ],
    '/critical-infrastructure': [
        'CRITICAL INFRASTRUCTURE',
        {"url": "/assets/image/critical_infrastructure.png",
         "width": 100, "height": 96, "anchorY": 96,
         "mask": True}
    ],
    '/community-services': [
        'COMMUNITY AND EMERGENCY FACILITIES',
        {"url": "/assets/image/community_service.png",
         "width": 96, "height": 96, "anchorY": 96,
         "mask": True}
    ],
    '/natural-cultural-resources': [
        'NATURAL/CULTURAL/HISTORICAL RESOURCE',
        {"url": "/assets/image/natural_cultural.png",
         "width": 105, "height": 100, "anchorY": 96,
         "mask": True}
    ],
    '/local-economy': [
        'TOURISM/ECONOMY',
        {"url": "/assets/image/local_economy.png",
         "width": 105, "height": 91, "anchorY": 96,
         "mask": True}
    ]
}


def asset_points_data(scn, year, pathname):
    asset_class = icon_data[pathname][0]
    df = pd.read_json(asset_points_json).loc[
        lambda x: x['Asset Class'] == asset_class,
        ['Asset Name',
         'Asset Type',
         f'{scn}_{year}',
         f'{scn}_{year}_color',
         'lon',
         'lat']
    ]
    df.rename(
        columns={
            f'{scn}_{year}': 'Flood Depth (ft)',
            f'{scn}_{year}_color': 'color'
        },
        inplace=True
    )
    df['icon_data'] = df.apply(lambda x: icon_data.get(pathname)[1], axis=1)
    # print(df)
    return df.to_json(orient='records')


def asset_points_layer(scn_code, year, pathname):
    return {
        "@@type": "IconLayer",
        "data": json.loads(
            asset_points_data(scn_code, year, pathname)
        ),
        "getIcon": "@@=icon_data",
        "getColor": "@@=color",
        "getSize": 4,
        "sizeScale": 5,
        "sizeMinPixels": 10,
        "sizeMaxPixels": 30,
        "getPosition": "@@=[lon, lat]",
        "pickable": True,
        # "billboard": False,
    }
