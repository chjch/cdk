import os
from dotenv import load_dotenv

load_dotenv()

import plotly.express as px
import dash_bootstrap_components as dbc


# Import Mapbox API Key from environment
mapbox_token = os.getenv("MAPBOX_TOKEN")
cesium_token = os.getenv("CESIUM_TOKEN")
mapbox_style_building = "mapbox://styles/chjch/cl8d69pxo000m14mqbbttpqfa"
road_json = "app/data/road_segments.json"
bfp_json = "app/data/bfp_props.json"
asset_points_json = "app/data/asset_points_color.json"

scenarios = [
    "MHHW",
    "EWL1R",
    "EWL2R",
    "EWL10R",
    "NFHL100",
    "CAT1",
    "CAT3",
    "CAT5",
]
asset_axis_title = {
    "CRITICAL COMMUNITY AND EMERGENCY FACILITIES": "Community Services",
    "CRITICAL INFRASTRUCTURE": "Critical Infrastructure",
    "NATURAL, CULTURAL, AND HISTORICAL RESOURCES": "Natural & Cultural Resources",
    "TRANSPORTATION": "Transportation",
    "ECONOMY": "Local Economy",
    "HOUSING": "Housing",
}


def cesium_tile_url(asset_id):
    return f"https://assets.ion.cesium.com/{asset_id}/tileset.json"


def scn_tile_url(scn_code, year):
    return (
        "https://tiles.arcgis.com/tiles/LBbVDC0hKPAnLRpO/arcgis/"
        + f"rest/services/CDK_{scn_code}_{year}/MapServer/WMTS/tile/"
        f"1.0.0/CDK_{scn_code}_{year}/default/default028mm"
        + "/{z}/{y}/{x}.png"
    )


def line_color_map(color_sequence_name, scenario=None, opacity=0):
    colors = getattr(px.colors.qualitative, color_sequence_name)
    color_map = {}
    i = 0
    for scn in scenarios:
        color_map[scn] = f"rgba{px.colors.hex_to_rgb(colors[i])}".replace(
            ")", f", {opacity})"
        )
        i += 1
    color_map[scenario] = color_map[scenario].replace(f"{opacity})", "1)")
    return color_map


def collapse_component(
        dash_component, is_open=False, dash_component_id=None, dimension="height"
):
    if dash_component_id is None:
        dash_component_id = f"{dash_component.id}-collapse"
    if isinstance(dash_component, dbc.Col):
        return dbc.Collapse(
            dash_component.children,
            id=dash_component_id,
            is_open=is_open,
            className=f"col-{dash_component.width}",
            dimension=dimension,
        )
    return dbc.Collapse(
        dash_component,
        id=dash_component_id,
        is_open=is_open,
        dimension=dimension
    )
