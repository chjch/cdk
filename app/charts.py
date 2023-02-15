import pandas as pd
import plotly.express as px

depth_df = pd.read_csv("app/data/cdk_critical_assets_flood_depth.csv")


def line_chart(asset: str = 'comm'):
    partial_df = depth_df[depth_df['asset'] == asset]
    fig = px.line(partial_df, x="year", y="percent", color='scenario',
                  symbol='scenario', template='plotly_white',
                  color_discrete_sequence=px.colors.qualitative.Plotly)
    fig.update_xaxes(
        ticktext=["2022", "2040", "2070"],
        tickvals=[2022, 2040, 2070],
    )
    fig.update_layout(
        title={'text': "Community and Emergency Facilities",
               'font': {'size': 20},
               'x': 0.5},
        legend_title='Storm scenario',
        margin=dict(l=0, r=0, t=50, b=0)
    )
    return fig
