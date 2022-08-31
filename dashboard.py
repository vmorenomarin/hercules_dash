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

total_offer=df["Documento"].shape[0]

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
                                    dbc.CardHeader("Total"),
                                    dbc.CardBody(
                                       children=[total_offer], id="total_card"
                                    ),
                                ],
                                style={'width': '300px'},
                            )
                        ),
                        dcc.Dropdown(
                            options=[
                                offer_type
                                for offer_type in df["Tipo de Oferta"].unique()
                            ],
                            id="dropdown_offer",
                            value=None,
                            placeholder="Seleccione una o más",
                            style={'width': '300px'},
                        ),
                    ]
                ),
                dbc.Col(
                    [html.Div(html.P("Ejemplo"))],
                    class_name="border border-1 rounded mx-4 shadow",
                ),
            ],
            class_name="py-3",
        ),
    ],
)


@app.callback(Output("total_card", "children"), Input("dropdown_offer", "value"))
def update_card(value):
    
    total_offer = df[df["Tipo de Oferta"] == value].shape[0]

    return total_offer


if __name__ == "__main__":
    app.run_server(debug=True, port=3000)
