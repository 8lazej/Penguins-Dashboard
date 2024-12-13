import html
from dash import dcc, html

my_dash_layout = html.Div(
    [
        html.H1("Penguin Dashboard", style={"textAlign": "center"}),
        html.H4(
            "This is an interactive dashboard based on Plotly Dash, enabling the analysis of penguin data - filtering by species, gender and parameter.",
            style={"textAlign": "center"},
        ),
        # Filters
        html.Div(
            [
                html.Div(
                    [
                        html.Label("Select Species", style={"color": "white"}),
                        dcc.Dropdown(
                            id="species-filter",
                            multi=True,
                            style={
                                "backgroundColor": "rgba(0,0,0,0.8)",
                                "color": "white",
                            },                           
                        ),
                    ],
                    style={
                        "width": "30%",
                        "display": "inline-block",
                        "padding": "10px",
                    },
                ),
                html.Div(
                    [
                        html.Label("Select Sex", style={"color": "white"}),
                        dcc.Dropdown(
                            id="sex-filter",
                            multi=True,
                            style={
                                "backgroundColor": "rgba(0,0,0,0.8)",
                                "color": "white",
                            },
                        ),
                    ],
                    style={
                        "width": "30%",
                        "display": "inline-block",
                        "padding": "10px",
                    },
                ),
                html.Div(
                    [
                        html.Label("Select Parameter", style={"color": "white"}),
                        dcc.Dropdown(
                            id="parameter-filter",
                            options=[
                                {"label": "Body Mass (g)", "value": "body_mass_g"},
                                {
                                    "label": "Flipper Length (mm)",
                                    "value": "flipper_length_mm",
                                },
                                {
                                    "label": "Bill Length (mm)",
                                    "value": "bill_length_mm",
                                },
                            ],
                            value="body_mass_g",
                            style={
                                "backgroundColor": "rgba(0,0,0,0.8)",
                                "color": "red",
                            },
                        ),
                    ],
                    style={
                        "width": "30%",
                        "display": "inline-block",
                        "padding": "10px",
                    },
                ),
            ],
            style={
                "textAlign": "center",
                "padding": "20px",
                "display": "flex",
                "justifyContent": "space-around",
            },
        ),
        # Charts
        html.Div(
            [
                dcc.Graph(id="island-average-chart"),
                dcc.Graph(id="distribution-chart"),
            ],
            style={"width": "70%", "display": "inline-block"},
        ),
        # Data table
        html.Div(
            [
                html.H3("Filtered Data Table"),
                html.Table(
                    id="data-table", style={"width": "100%", "overflowX": "scroll"}
                ),
            ],
            style={"padding": "20px"},
        ),
        # Data stores
        dcc.Store(id="raw-data"),
        dcc.Store(id="filtered-data"),
    ]
)
