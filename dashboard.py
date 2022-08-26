import pandas as pd

import dash
from dash import dcc, html
from dash.dependencies import Output, Input
import dash_bootstrap_components as dbc
import plotly.express as px


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


# Vriable style:
# comfe_colors = {'green1':'#005644', 'green2':'#c0d507'}
# comfe_fonts = ['font-family: 'Mitr';font-size: 22px;', 2]

navbar = dbc.Row(
    dbc.Navbar(
        dbc.Container(
            [
                html.A(
                    dbc.Row(
                        [
                            dbc.Col(
                                html.Img(
                                    src="https://www.matriculascomfenalcoantioquia.com.co/uploads/9235be6bd26cede21ecad29db3bfad3833ca12af.png",
                                    height="30px",
                                ),
                            ),
                            dbc.Col(
                                dbc.NavbarBrand(
                                    "Tablero Hércules",
                                    class_name="ms-2",
                                    style={"color": "#c0d507"},
                                ),
                            ),
                        ]
                    ),
                    href="#",
                    style={"text-decoration": "none"},
                ),
                dbc.DropdownMenu(
                    children=[
                        dbc.DropdownMenuItem("Seleccione tipo de oferta", header=True),
                        dbc.DropdownMenuItem("Venta Directa", href="#"),
                        dbc.DropdownMenuItem("FOSFEC", href="#"),
                        dbc.DropdownMenuItem("Excedentes del 55%", href="#"),
                        dbc.DropdownMenuItem(divider=True),
                        dbc.DropdownMenuItem("Devoluciones", href="#"),
                    ],
                    nav=True,
                    toggle_style=True,
                    label="Tipo de Oferta",
                ),
            ],
        ), class_name="border border-0"
    ),
    
)

app.layout = dbc.Container(
    [
        navbar,
        dbc.Row(
            [
                dbc.Col(
                    [html.Div(html.P("Ejemplo"))],
                    # style={"background-color": "red"},
                    class_name="border border-1 rounded mx-4 shadow",
                ),
                dbc.Col(
                    [html.Div(html.P("Ejemplo"))],
                    # style={"background-color": "#202124"},
                    class_name="border border-1 rounded mx-4 shadow",
                ),
            ],
            class_name="py-3",
        ),
    ],
)

if __name__ == "__main__":
    app.run_server(debug=True, port=3000)
