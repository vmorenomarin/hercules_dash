import pandas as pd

import dash
from dash import dcc, html
from dash.dependencies import Output, Input
import dash_bootstrap_components as dbc
import plotly.express as px

# Importing UI components

from components import navbar

navbar = navbar.navbar

df = pd.read_csv("./assets/data/dash_dataset.csv")

# Create a Dash instance.
app = dash.Dash(
    __name__,
    update_title="Comfenalco Antioquia - Tablero de Hércules",
    external_stylesheets=[
        dbc.themes.LITERA,
        dbc.icons.FONT_AWESOME,
        "./assets/style/tipography.css",
    ],
    assets_external_path="/assets/",
    meta_tags=[
        {
            "name": "viewport",
            "content": "width=devide-width, initial-scale=1",
            "title": "Comfenalco Antioquia - Hércules Dashboard",
        }
    ],
)

# Layout section, In this part, add the html code and plotty Dash componentss associated to the dataset variables.
# total_offer = df['Documento'].shape[0]
title_card = "Total matrículas"
app.layout = dbc.Container(
    [
        navbar,
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Div(
                            dbc.Card(
                                [
                                    dbc.CardHeader(
                                        children=title_card,
                                        id="card_header",
                                        className="fw-bold",
                                    ),
                                    dbc.CardBody(
                                        children=df["Documento"].shape[0],
                                        id="total_card",
                                    ),
                                ],
                                style={"width": "260px"},
                            ),
                        ),
                        dcc.Dropdown(
                            options=[
                                {"label": offer_type, "value": offer_type}
                                for offer_type in df["Tipo de Oferta"].unique()
                            ],
                            id="dropdown_offer",
                            value="Total Matrículas",
                            placeholder="Seleccione oferta...",
                            style={"width": "260px"},
                            # className='',
                        ),
                    ],
                ),
                dbc.Col(
                    [dcc.Graph(id="enroll-evolution", figure={})],
                    class_name="border border-1 rounded shadow",
                ),
            ],
            class_name="my-3",
            justify="evenly",
        ),
    ],
    # fluid=True,
)


@app.callback(
    [Output("total_card", "children"), Output("card_header", "children")],
    Input("dropdown_offer", "value"),
)
def update_card(value):
    children = df[df["Tipo de Oferta"] == value].shape[0]
    title_card = value
    if value is None:
        children = df["Documento"].shape[0]
        title_card = "Total Matrículas"
        return children, title_card

    return children, title_card


@app.callback(
    Output("enroll-evolution", 'figure'),
    Input("dropdown_offer", "value")
)
def update_graph(value):
    dff=df[["Fecha Registro", "Tipo de Oferta"]]
    figure_line = px.line(dff[dff.isin([value])], x=dff["Fecha Registro"], y="Tipo de Oferta")
    return figure_line

if __name__ == "__main__":
    app.run_server(debug=True, port=3000)
