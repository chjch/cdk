import pandas as pd
import plotly.express as px

transport_depth_df = pd.read_csv("app/data/transport_depths.csv")


def line_chart():
    fig = px.line(transport_depth_df, x="depth", y="percent", color='scenario',
                  symbol='scenario', template='plotly_white')
    fig.update_layout(margin=dict(l=0, r=0, t=0, b=0))
    return fig
