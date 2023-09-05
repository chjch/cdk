import dash
from dash import html, dcc, callback, Input, Output, State, no_update
import dash_deck
import dash_bootstrap_components as dbc
from plotly.validator_cache import ValidatorCache

import pandas as pd
import json

from utils import cesium_tile_url, mapbox_token, cesium_token

CDK_LATITUDE = 29.139219
CDK_LONGITUDE = -83.040895
CESIUM_ASSET_ID = 1891205

dash.register_page(
    __name__, title="Live Storm Tracker", path_template="/tracker"
)


def noaa_data_url(layer_id, where="1=1"):
    return (
        f"https://services9.arcgis.com/RHVPKKiFTONKtxq3/ArcGIS/rest/"
        f"services/Active_Hurricanes_v1/FeatureServer/{layer_id}/"
        f"query?where={where}&outFields=*&f=pgeojson"
    )


error_cone_layer = {
    "@@type": "GeoJsonLayer",
    "id": "error-cone-layer",
    "data": noaa_data_url(4, "STORMNAME%3D%27Idalia%27"),
    "stroked": True,
    "filled": True,
    "lineWidthMinPixels": 2,
    "opacity": 0.5,
    "getLineColor": [55, 110, 183],
    "getFillColor": [55, 110, 183, 50],
    "getDashArray": [4, 3],
    "extensions": [
        {
            "@@type": "PathStyleExtension",
            "dash": True,
            "highPrecisionDash": True,
        }
    ],
}


COLOR_RANGE = [
    [55, 110, 183],
    [214, 123, 40],
    [213, 94, 33],
    [171, 38, 18],
    [118, 23, 28],
    [65, 9, 24],
]

STORM_CATEGORY = [
    "Tropical Storm",
    "Category 1",
    "Category 2",
    "Category 3",
    "Category 4",
    "Category 5",
]

BREAKS = [64, 83, 96, 113, 137, 200]


def color_scale(val):
    for i, b in enumerate(BREAKS):
        if val <= b:
            return COLOR_RANGE[i]
    return COLOR_RANGE[0]


def storm_level(val):
    for i, b in enumerate(BREAKS):
        if val < b:
            return STORM_CATEGORY[i]


tooltip_html = """
    <strong>{FullDate}</strong>
    <br />
    <table>
        <tr>
            <td><strong>Max Wind Speed</strong></td>
            <td>{Max Wind Speed} knots</td>
        </tr>
        <tr>
            <td><strong>Wind Gust Speed</strong></td>
            <td>{Wind Gust Speed}</td>
        </tr>
        <tr>
            <td><strong>Hurricane Level</strong></td>
            <td>{STORMLEVEL}</td>
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

forecast_position_json = pd.read_json(
    noaa_data_url(0, "STORMNAME%3D%27Idalia%27")
)
df = pd.DataFrame()

df["geometry"] = forecast_position_json["features"].apply(
    lambda row: row["geometry"]
)
df["Tropical Cyclone Development"] = forecast_position_json["features"].apply(
    lambda row: row["properties"]["TCDVLP"]
)
df["DateLabel"] = forecast_position_json["features"].apply(
    lambda row: row["properties"]["DATELBL"].replace(":00", "")
)
df["FullDate"] = forecast_position_json["features"].apply(
    lambda row: row["properties"]["FLDATELBL"]
)
df["Max Wind Speed"] = forecast_position_json["features"].apply(
    lambda row: row["properties"]["MAXWIND"]
)
df["Wind Gust Speed"] = forecast_position_json["features"].apply(
    lambda row: row["properties"]["GUST"]
)
df["STORMLEVEL"] = forecast_position_json["features"].apply(
    lambda row: storm_level(row["properties"]["MAXWIND"])
)
df["fill_color"] = forecast_position_json["features"].apply(
    lambda row: color_scale(row["properties"]["MAXWIND"])
)

forecast_position_layer = {
    "@@type": "GeoJsonLayer",
    "id": "forecast-position-layer",
    "data": json.loads(df.to_json(orient="records")),
    "stroked": True,
    "pickable": True,
    "pointRadiusMinPixels": 5,
    "filled": True,
    "getLineColor": [255, 255, 255],
    "getFillColor": "@@=fill_color",
    "lineWidthMinPixels": 2,
    "getPointRadius": 700,
    "pointRadiusScale": 5
}

forecast_position_text_layer = {
    "@@type": "TextLayer",
    "id": "forecast-position-text-layer",
    "data": json.loads(df.to_json(orient="records")),
    "getText": "@@=DateLabel",
    "getPosition": "@@=geometry.coordinates",
    "getSize": 14,
    "getTextAnchor": 'middle',
    "getAlignmentBaseline": 'center',
    "getPixelOffset": [50, 5],
}

forecast_track_layer = {
    "@@type": "GeoJsonLayer",
    "id": "forecast-track-layer",
    "data": noaa_data_url(2, "STORMNAME%3D%27Idalia%27"),
    "stroked": True,
    "lineWidthMinPixels": 3,
    "getLineColor": [0, 255, 255],
}

HURRICANE_FORCE_COLOR_RANGE = [
    [35,104,0],
    [50,158,0],
    [69,226,0],
    [255,255,0],
    [227,226,0],
    [158,101,0],
    [226,141,0],
    [226,0,0],
    [104,34,0],
    [120,5,158],
]

HURRICANE_FORCE_BREAKS = [20, 30, 40, 50, 60, 70, 80, 90, 100, 110]

def hurricane_force_color_scale(val):
    for i, b in enumerate(HURRICANE_FORCE_BREAKS):
        if val < b:
            return HURRICANE_FORCE_COLOR_RANGE[i]


hurricane_force_json = pd.read_json(
    noaa_data_url(9, )
)
hurricane_force_df = pd.DataFrame()
hurricane_force_df["geometry"] = hurricane_force_json["features"].apply(
    lambda row: row["geometry"]
)
hurricane_force_df["fill_color"] = hurricane_force_json["features"].apply(
    lambda row: hurricane_force_color_scale(row["properties"]["PWIND120"])
)
hurricane_force_layer = {
    "@@type": "GeoJsonLayer",
    "id": "hurricane-force-layer",
    "data": json.loads(hurricane_force_df.to_json(orient="records")),
    "stroked": False,
    "filled": True,
    "LineWidthMinPixels": 2,
    "opacity": 0.05,
    "getFillColor": "@@=fill_color",
}

json_data = {
    "initialViewState": {
        "bearing": 0,
        "latitude": CDK_LATITUDE,
        "longitude": CDK_LONGITUDE,
        "maxZoom": 11,
        "minZoom": 4,
        "pitch": 0,
        "zoom": 4.5,
    },
    "layers": [
        error_cone_layer,
        forecast_track_layer,
        hurricane_force_layer,
        forecast_position_layer,
        forecast_position_text_layer,
    ],
    "mapProvider": "mapbox",
    "mapStyle": "mapbox://styles/mapbox/light-v11",
    "views": [{"@@type": "MapView", "controller": True}],
    # "effects": [lighting_effect]
}

map_container = html.Div(
    children=[
        dash_deck.DeckGL(
            json_data,
            id="tracker-deck",
            tooltip={"html": tooltip_html, "style": tooltip_style},
            mapboxKey=mapbox_token,
        )
    ],
    id="map-container",
)


def layout(asset_type=None):
    return html.Div(
        [
            map_container,
        ]
    )
