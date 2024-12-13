import pandas as pd
import plotly.express as px

from dash import Dash, html, Input, Output
from dash_layout import my_dash_layout

app = Dash(__name__)

URL = "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/penguins.csv"
data = pd.read_csv(URL)

app.layout = my_dash_layout

@app.callback(
    Output("raw-data", "data"),
    Input("parameter-filter", "value"), 
)
def load_data(_):
    return data.to_json(orient="records") 


@app.callback(
    [
        Output("species-filter", "options"),
        Output("species-filter", "value"),
        Output("sex-filter", "options"),
        Output("sex-filter", "value"),
    ],
    Input("raw-data", "data"),
)
def set_dropdown_options(raw_data):
    df = pd.read_json(raw_data) 
    species_dropna_unique = df["species"].dropna().unique()
    species_options = [
        { 
            "label": species, 
            "value": species 
        }
        for species in species_dropna_unique
    ]
    sex_dropna_unique = df["sex"].dropna().unique()
    sex_options = [
        {
            "label": sex, 
            "value": sex
        } 
        for sex in sex_dropna_unique]
    return (
        species_options,
        [option["value"] for option in species_options],
        sex_options,
        [option["value"] for option in sex_options],
    )

clientcallback_function = """
    function(raw_data, species, sex) {
        const df = JSON.parse(raw_data);
        let filteredData = df;

        if (species && species.length > 0) {
            filteredData = filteredData
                .filter(row => species.includes(row.species));
        }
        if (sex && sex.length > 0) {
            filteredData = filteredData
                .filter(row => sex.includes(row.sex));
        }

        return JSON.stringify(filteredData);
    }
"""

app.clientside_callback(
    clientcallback_function,
    Output("filtered-data", "data"),
    [
        Input("raw-data", "data"),
        Input("species-filter", "value"),
        Input("sex-filter", "value"),
    ],
)


@app.callback(
    Output("island-average-chart", "figure"),
    [
        Input("filtered-data", "data"), 
        Input("parameter-filter", "value")
    ],
)
def update_island_chart(filtered_data, parameter):
    df = pd.read_json(filtered_data) 
    if df.empty:
        return px.bar(title="No Data Available")

    island_avg = df.groupby("island")[parameter].mean().reset_index()
    island_avg = island_avg.sort_values(by=parameter, ascending=True)  

    fig = px.bar(
        island_avg,
        x="island",
        y=parameter,
        title="Average Parameter per Island",
        color="island", 
        color_discrete_map={
            "Biscoe": "rgb(255,100,0)",
            "Dream": "rgb(100,255,100)",
            "Torgersen": "rgb(0,100,255)",
        },
    )
    fig.update_layout(xaxis_title="Island", yaxis_title="Average Value")
    fig.update_layout(
        plot_bgcolor="rgba(0, 0, 0, 0)",  
        paper_bgcolor="rgba(0, 0, 0, 0)", 
        font=dict(color="white"), 
    )
    return fig

@app.callback(
    Output("distribution-chart", "figure"),
    [Input("filtered-data", "data"), Input("parameter-filter", "value")],
)

def update_distribution_chart(filtered_data, parameter):
    df = pd.read_json(filtered_data)  
    if df.empty:
        return px.histogram(title="No Data Available")
    fig = px.histogram(df, x=parameter, title="Distribution of Selected Parameter")
    fig.update_layout(
        plot_bgcolor="rgba(0, 0, 0, 0)",  
        paper_bgcolor="rgba(0, 0, 0, 0)", 
        font=dict(color="white"), 
    )
    return fig


@app.callback(Output("data-table", "children"), Input("filtered-data", "data"))
def update_table(filtered_data):

    def extractCellValue(df, i, col):
        return df.iloc[i][col]

    df = pd.read_json(filtered_data)  
    if df.empty:
        return [html.Tr([html.Td("No data available")])]
    header = [html.Tr([html.Th(col) for col in df.columns])]
    body = [
        html.Tr([html.Td(extractCellValue(df, i, col)) for col in df.columns])
        for i in range(len(df))
    ]
    return header + body


if __name__ == "__main__":
    app.run_server(debug=True)
