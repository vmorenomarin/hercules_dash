
import dash
from dash import html
import dash_bootstrap_components as dbc

navbar=dbc.Row(
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
                        dbc.DropdownMenuItem([html.I(className="fa fa-store me-2"), "Venta Directa"], href="#"),
                        dbc.DropdownMenuItem([html.I(className="fa fa-person-chalkboard me-2"),"FOSFEC"], href="#"),
                        dbc.DropdownMenuItem([html.I(className="fa fa-sack-dollar me-2"), "Excedentes del 55%"], href="#"),
                        dbc.DropdownMenuItem(divider=True),
                        dbc.DropdownMenuItem([html.I(className="fa fa-arrow-rotate-left me-2"),"Devoluciones"], href="#"),
                    ],
                    nav=True,
                    toggle_style=True,
                    label="Tipo de Oferta",
                ),
            ],
        ), class_name="border border-0"
    ),
    
)