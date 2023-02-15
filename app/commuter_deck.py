import os
from dotenv import load_dotenv
import pandas as pd
import dash_deck
import pydeck as pdk

load_dotenv()

mapbox_api_token = os.getenv('MAPBOX_TOKEN')
mapbox_style = 'mapbox://styles/chjch/cl7taqajn000x14mwr6915mcw'

data_url = r"https://media.githubusercontent.com/media/chjch/psj/main/app/data/PSJ_Place_2019_od.csv"
njob_class = 'njob_class'  # column name contains number of jobs classes


def commuter_deck(njob_option=None):
    cyan_rgba = [0, 159, 176, 80]
    magenta_rgba = [245, 44, 246, 80]

    df = pd.read_csv(data_url)
    if njob_option is None:
        commuter_df = df
    else:
        commuter_df = df[df[njob_class].isin(njob_option)]

    # Specify a deck.gl ArcLayer
    arc_layer = pdk.Layer(
        "ArcLayer",
        data=commuter_df,
        get_width="njob_class * 3",
        get_height=0.5,
        get_source_position=["lng_h", "lat_h"],
        get_target_position=["lng_w", "lat_w"],
        get_tilt=10,
        get_source_color=cyan_rgba,
        get_target_color=magenta_rgba,
        pickable=True,
        auto_highlight=True,
    )

    # Set viewport to Downtown PSJ
    view_state = pdk.ViewState(
        latitude=29.9981657, longitude=-85.2519762,
        bearing=0, pitch=60, zoom=9,
    )

    # Renderer
    r = pdk.Deck(
        arc_layer, initial_view_state=view_state,
        map_style=mapbox_style,
        api_keys={'mapbox': mapbox_api_token}
    )

    tooltip_text = {
        "html": "{s000} jobs <br /> Home (cyan) to Work (magenta)."
    }

    return dash_deck.DeckGL(r.to_json(), id="commuter-deck",
                            tooltip=tooltip_text,
                            mapboxKey=mapbox_api_token)
