import pandas as pd
import plotly.express as px

depth_df = pd.read_csv("data/cdk_critical_assets_flood_depth.csv")

asset_dict = {'comm': "Community and Emergency Facilities",
              'infra': "Critical Infrastructure",
              'resrc': "Natural Cultural and Historical Resources",
              'trans': "Transportation",
              'trism': "Tourism and Economy",
              'overall': "All Critical Assets"}


def line_chart(asset: str = 'overall'):
    partial_df = depth_df[depth_df['asset'] == asset]
    fig = px.line(partial_df, x="year", y="percent", color='scenario',
                  symbol='scenario', template='plotly_white',
                  color_discrete_sequence=px.colors.qualitative.Plotly)
    fig.update_xaxes(
        ticktext=["2022", "2040", "2070"],
        tickvals=[2022, 2040, 2070],
    )
    fig.update_yaxes(range=[-5, 105])
    fig.update_layout(
        title={'text': asset_dict[asset],
               'font': {'size': 20},
               'x': 0.5},
        legend=dict(
            title=dict(
                text='Storm scenario<br>',
            ),
            tracegroupgap=15
        ),
        margin=dict(l=0, r=0, t=50, b=0)
    )
    return fig
