import pandas as pd
import plotly.express as px

depth_df = pd.read_csv("app/data/cdk_critical_assets_flood_depth.csv")
class_df = pd.read_csv(
    "app/data/cdk_critical_assets_flood_depth_classification.csv"
)

asset_dict = {'comm': "Community Services",
              'infra': "Critical Infrastructure",
              'resrc': "Natural & Cultural Resources",
              'trans': "Transportation",
              'economy': "Local Economy",
              'overall': "All Critical Assets"}

category_orders = {
    'Asset class': ['TRANSPORTATION',
                    'CRITICAL INFRASTRUCTURE',
                    'COMMUNITY SERVICES',
                    'NATURAL & CULTURAL RESOURCES',
                    'LOCAL ECONOMY']
}


def line_chart(asset: str = 'overall'):
    partial_df = depth_df[depth_df['asset'] == asset]
    fig = px.line(partial_df, x="year", y="percent", color='scenario',
                  symbol='scenario', template='plotly_white',
                  custom_data=['scenario'],
                  color_discrete_sequence=px.colors.qualitative.Plotly)
    fig.update_xaxes(
        ticktext=["2022", "2040", "2070"],
        tickvals=[2022, 2040, 2070],
        title=None
    )
    fig.update_yaxes(range=[-1, 101],
                     title='Assets inundated (%)')
    fig.update_layout(
        # title={'text': asset_dict[asset],
        #        'font': {'size': 16},
        #        'x': 0.5},
        legend=dict(
            title=dict(
                text='scenario',
                font=dict(size=14)
            ),
            tracegroupgap=10
        ),
        margin=dict(l=0, r=0, t=0, b=0)
    )
    return fig


def bar_chart(asset: str = 'overall',
              scenario: str = 'MHHW',
              year: int = 2022):
    bar_trace = f"{scenario}_{str(year)}"
    if asset != 'overall':
        bar_df = class_df[class_df['Asset class'] == asset]
        x_title = f"{asset} (%) by flood depth"
    else:
        bar_df = class_df
        x_title = f"All critical assets (%) by flood depth"
    fig = px.bar(bar_df, x='Flood depth', y=bar_trace, color='Asset class',
                 barmode='group', category_orders=category_orders,
                 template='plotly_white',
                 color_discrete_sequence=['#5289B0', '#AAB543', '#EA9731',
                                          '#838383', '#F6C540'])
    fig.update_yaxes(range=[-1, 103],
                     title=None)
    fig.update_xaxes(title=x_title)
    fig.update_layout(
        legend=dict(
            orientation="h",
            itemwidth=70,
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            title=None,

        ),
        bargroupgap=0.15,
        showlegend=False,
        margin=dict(l=0, r=0, t=0, b=0)
    )
    return fig
