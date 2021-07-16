from logging import PlaceHolder
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from dash_html_components.Figure import Figure
import plotly.express as px
from data import (
    countries_df,
    make_country_df,
    make_global_df,
    totals_df,
    dropdown_options,
)
from builders import make_table


stylesheets = [
    # 배경색을 넣어줬는데, 테투리에 여전히 흰색이 남아 있다.
    # 이것은 기존의 html이 세팅되어 있기 때문에 발생되는 현상이니 reset css를 하여 초기화해주는 것이다.
    "https://cdn.jsdelivr.net/npm/reset-css@5.0.1/reset.min.css"
]
# app에 대시보드 스타일시트 기록하기 위한 코드
app = dash.Dash(__name__, external_stylesheets=stylesheets)

server = app.server

countries_df.iloc[0, 3] = countries_df.iloc[0, 1] - countries_df.iloc[0, 2]

bubble_map = px.scatter_geo(
    countries_df,
    template="plotly_dark",
    color="Confirmed",
    size="Confirmed",
    size_max=50,
    title="Confirmed By Country",
    locations="Country_Region",
    locationmode="country names",
    hover_name="Country_Region",
    projection="natural earth",
    hover_data={
        "Confirmed": ":,2f",
        "Deaths": ":,2f",
        "Recovered": ":,2f",
        "Country_Region": False,
    },
)
bubble_map.update_layout(margin=dict(l=100, r=300, t=25, b=0))

totals_df = totals_df.sort_values(by="count", ascending=False)
bars_graph = px.bar(
    totals_df,
    x="condition",
    y="count",
    template="plotly_dark",
    title="Total global Cases",
    hover_data={"count": ":,f"},
    labels={"condition": "Condition", "count": "Count"},
)
bars_graph.update_traces(marker_color=["#34495e", "#16a085", "#95a5a6"])

app.layout = html.Div(
    style={
        "minHeight": "100vh",
        "backgroundColor": "#111111",
        "color": "white",
    },
    children=[
        html.Header(
            style={
                "textAlign": "center",
                "paddingTop": "50px",
                "paddingBottom": "50px",
            },
            children=[html.H1("Covid19 DashBoard", style={"fontSize": 50})],
        ),
        html.Div(
            style={
                "display": "grid",
                "gridTemplateColumns": "repeat(4, 1fr)",
                "gap": 50,
            },
            children=[
                html.Div(
                    style={
                        "grid-column": "span 3",
                    },
                    children=[dcc.Graph(figure=bubble_map)],
                ),
                html.Div(
                    style={
                        "backgroundColor": "#111111",
                    },
                    children=[make_table(countries_df)],
                ),
            ],
        ),
        html.Div(
            style={
                "display": "grid",
                "gridTemplateColumns": "repeat(4, 1fr)",
                "gap": 50,
            },
            children=[
                html.Div(
                    style={"grid-column": "span 3"},
                    children=[
                        dcc.Dropdown(
                            style={
                                "width": 320,
                                "margin": "0 auto",
                                "color": "#111111",
                            },
                            id="country",
                            options=[
                                {"label": country, "value": country}
                                for country in dropdown_options
                            ],
                        ),
                        dcc.Graph(id="country-graph"),
                    ],
                ),
                html.Div(children=[dcc.Graph(figure=bars_graph)]),
            ],
        ),
    ],
)


@app.callback(Output("country-graph", "figure"), [Input("country", "value")])
def update_hello(value):
    if value:
        df = make_country_df(value)
    else:
        df = make_global_df()
    fig = px.line(
        df,
        x="date",
        y=["confirmed", "deaths", "recovered"],
        template="plotly_dark",
        labels={"value": "Cases", "variable": "Condition", "date": "Date"},
        hover_data={"value": ":,", "variable": False, "date": False},
    )
    # fig.update_xaxes(rangeslider_visible=True) 그래프를 확대하는 코드 인데, 속도를 저하시켜서 주석처리함
    fig["data"][0]["line"]["color"] = "#34495e"
    fig["data"][1]["line"]["color"] = "#95a5a6"
    fig["data"][2]["line"]["color"] = "#16a085"
    return fig
