import pydeck as pdk


def building_layer(geojson_data, fill_color_rgba=None, pickable=True):
    if not fill_color_rgba:
        fill_color_rgba = [235, 235, 235, 170]
    line_color_rgba = [0, 0, 0, 255]

    geojson_layer = pdk.Layer(
        "GeoJsonLayer",
        data=geojson_data,
        id='geojson',
        opacity=1,
        stroked=True,
        filled=True,
        extruded=True,
        wireframe=True,
        get_elevation="properties.fakefloors * 3",
        get_fill_color=fill_color_rgba,
        get_line_color=line_color_rgba,
        pickable=pickable,
        material=False,
        tooltip=True
    )
    return geojson_layer
