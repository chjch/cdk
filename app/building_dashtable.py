import pandas as pd
import json

data_url = r"./data/psj_bldg.geojson"
geojson_data = json.load(open(data_url))

# flatten JSON data
df = pd.json_normalize(geojson_data['features'])
# get all properties and remove GeoJSON attributes such as coordinates
df = df[[c for c in df.columns if c.startswith('properties')]]
# rename the property columns by removing `properties.` in their names
df.rename(columns=dict(zip(df.columns,
                           [c[len('properties.'):] for c in df.columns]
                           )),
          inplace=True)