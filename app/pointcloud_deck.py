import os
import pandas as pd
import pydeck as pdk
import dash_deck

from dotenv import load_dotenv

load_dotenv()

MAPBOX_API_KEY = os.getenv("MAPBOX_TOKEN")
mapbox_style = 'dark'


DATA_URL = "https://media.githubusercontent.com/media/chjch/psj/main/app/data/psj_lidar_80_31_colorized_wgs84_nav88m_filtered.csv"
df = pd.read_csv(DATA_URL)

point_cloud_layer = pdk.Layer(
    "PointCloudLayer",
    data=DATA_URL,
    get_position=["X", "Y", "Z"],
    get_color=["R", "G", "B"],
    # get_position=["x", "y", "z"],
    # get_color=["r", "g", "b"],
    # get_normal=[0, 0, 15],
    # auto_highlight=True,
    pickable=False,
    point_size=0.5,
)

# Set viewport to Downtown PSJ
view_state = pdk.ViewState(
    # target=target,
    # controller=True,
    latitude=29.8126632, longitude=-85.303558,
    # rotation_x=15, rotation_orbit=30,
    bearing=30, pitch=55,
    zoom=16, min_zoom=13, max_zoom=18
)

r = pdk.Deck(point_cloud_layer, initial_view_state=view_state,
             map_provider='mapbox',
             map_style=mapbox_style,
             api_keys={'mapbox': MAPBOX_API_KEY},
             # views=[view]
             )

point_cloud_deck = dash_deck.DeckGL(r.to_json(), id="point-deck",
                                    mapboxKey=MAPBOX_API_KEY)
