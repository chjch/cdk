import pandas as pd
import plotly.express as px
from utils import scenarios, line_color_map, asset_axis_title


depth_df = pd.read_csv("app/data/cdk_critical_assets_flood_depth.csv")
class_df = pd.read_csv(
    "app/data/cdk_critical_assets_flood_depth_classification.csv"
)

color_map = {}

asset_dict = {
    "comm": "Community Services",
    "infra": "Critical Infrastructure",
    "resrc": "Natural & Cultural Resources",
    "trans": "Transportation",
    "economy": "Local Economy",
    "housing": "Housing",
}


def line_chart(asset: str, scenario: str):
    partial_df = depth_df[depth_df["asset"] == asset]
    global color_map
    color_map = line_color_map("G10", scenario, 0.2)
    fig = px.line(
        partial_df,
        x="year",
        y="percent",
        color="scenario",
        symbol="scenario",
        template="plotly_white",
        custom_data=["scenario"],
        color_discrete_map=color_map
    )
    fig.update_xaxes(
        ticktext=["2022", "2040", "2070"],
        tickvals=[2022, 2040, 2070],
        title=None,
    )
    fig.update_yaxes(range=[-1, 101], title="Total Assets Flooded (%)")
    fig.update_layout(
        # title={'text': asset_dict[asset],
        #        'font': {'size': 16},
        #        'x': 0.5},
        legend=dict(
            title=dict(text="scenario", font=dict(size=14)), tracegroupgap=10
        ),
        margin=dict(l=0, r=0, t=0, b=0),
    )
    return fig


def bar_chart(asset: str, scenario: str, year: int):
    bar_trace = f"{scenario}_{str(year)}"
    bar_df = class_df[class_df["Asset class"] == asset]
    x_title = f"Assets Flooded by Depth (%) under {scenario} in {year}"
    fig = px.bar(
        bar_df,
        x="Flood depth",
        y=bar_trace,
        color="Asset class",
        template="plotly_white"
    )
    fig.update_yaxes(range=[-1, 101], title=None)
    fig.update_xaxes(title=x_title)
    fig.update_traces(marker_color=color_map[scenario])
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
        margin=dict(l=20, r=0, t=20, b=0),
    )
    fig.add_annotation(
        x='>27 ft', y=85,
        # xshift=-40,
        text=f"{asset_axis_title[asset]}",
        showarrow=False,
        yshift=10,
        font=dict(size=14)
    )
    return fig
