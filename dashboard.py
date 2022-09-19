from cgitb import text
from turtle import title
import pandas as pd

import dash
from dash import dcc, html
from dash.dependencies import Output, Input
import dash_bootstrap_components as dbc
import plotly.express as px


from data_measurements import *

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
                                        children=df["Evento"].shape[0],
                                        id="total_card",
                                    ),
                                ],
                            ),
                        ),

                    ], class_name='col-4'
                ),
                dbc.Col([
                    dbc.([
                        dcc.Dropdown(
                            options=[
                                {"label": business_unity.title(),
                                 "value": business_unity}
                                for business_unity in df["UNIDAD DE NEGOCIO"].unique()
                            ],
                            id="dropdown_business_unities",
                            placeholder="Seleccione unidad de negocio...",
                        ),
                        dcc.Dropdown(
                            options=[
                                {"label": area,
                                 "value": area}
                                for area in get_areas(business_unity=None)
                            ],
                            id="dropdown_areas",
                            placeholder="Seleccione sublínea...",
                        ),
                        dcc.Dropdown(
                            options=[
                                {"label": service,
                                 "value": service}
                                for service in get_services(area=None)
                            ],
                            id="dropdown_services",
                            placeholder="Seleccione material...",
                        ),
                        dcc.Dropdown(
                            options=[],
                            id="dropdown_offer_types",
                            placeholder="Seleccione tipo oferta...",
                        )
                    ]),
                    dcc.Graph(id="enroll-evolution", figure={})],
                    class_name="border border-1 rounded shadow col-8",
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
    Input("dropdown_business_unities", "value"),
)
def update_card(value):
    children = df[df["UNIDAD DE NEGOCIO"] == value].shape[0]
    title_card = value
    if value is None:
        children = df["Evento"].shape[0]
        title_card = "Total Matrículas"
        return children, title_card

    return children, title_card


@app.callback(
    Output("dropdown_offer_types", "options"),
    Input("dropdown_services", "value")
)
def update_dropdown_offer_types(service):
    options = [
        {"label": type_offer,
         "value": type_offer}
        for type_offer in get_offer_types(service=service)
    ]
    return options


@app.callback(
    Output("dropdown_areas", "options"),
    Input("dropdown_business_unities", "value")
)
def update_dropdown_area(business_unity):
    options = [
        {"label": area,
         "value": area}
        for area in get_areas(business_unity=business_unity)
    ]
    return options


@app.callback(
    Output("dropdown_services", "options"),
    Input("dropdown_areas", "value")
)
def update_dropdown_services(value):
    options = [
        {"label": service,
         "value": service}
        for service in get_services(area=value)
    ]
    return options


@app.callback(
    Output("enroll-evolution", 'figure'),
    Input("dropdown_business_unities", "value"),
    Input("dropdown_offer_types", "value"),
    Input("dropdown_areas", "value"),
    Input("dropdown_services", "value"),
)
def update_graph(business_unity, offer_type, area, service):

    if service and offer_type:
        dataset = dataset_plot_by_offer(offer_type=offer_type, service=service)
        figure_line = px.line(dataset, x='Mes Registro', y=offer_type,
                              title=f'Total registros {service} para {offer_type}: {dataset[offer_type].sum()} ')
        figure_line.update_layout(
            xaxis={
                'tickmode': 'array',
                'tickvals': [i for i in range(1, 13)],
                'ticktext': ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"]},
            title_font={
                "family": "Mitr, sans-serif",
                "size": 18,
                "color": "#c0d507"},
            font={
                "family": "Mitr, sans-serif",
                "size": 14,
                "color": "#202124"},
            plot_bgcolor="#f9f9f9")
        figure_line.update_traces(line_color="#005744")

        return figure_line

    if area and offer_type:
        dataset = dataset_plot_by_offer(offer_type=offer_type, area=area)
        figure_line = px.line(dataset, x='Mes Registro', y=offer_type,
                              title=f'Total registros {area} para {offer_type}: {dataset[offer_type].sum()} ')
        figure_line.update_layout(xaxis={'tickmode': 'array',
                                         'tickvals': [i for i in range(1, 13)],
                                         'ticktext': ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"]},
                                  title_font={
                                      "family": "Mitr, sans-serif", "size": 18, "color": "#c0d507"},
                                  font={"family": "Mitr, sans-serif",
                                        "size": 14, "color": "#202124"},
                                  plot_bgcolor="#f9f9f9")
        figure_line.update_traces(line_color="#005744")
        return figure_line

    if business_unity and offer_type:
        dataset = dataset_plot_by_offer(
            offer_type=offer_type, business_unity=business_unity)
        figure_line = px.line(dataset, x='Mes Registro', y=offer_type,
                              title=f'Total registros {business_unity.title()} para {offer_type}: {dataset[offer_type].sum()}')
        figure_line.update_layout(xaxis={'tickmode': 'array',
                                         'tickvals': [i for i in range(1, 13)],
                                         'ticktext': ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"]},
                                  title_font={
                                      "family": "Mitr, sans-serif", "size": 18, "color": "#c0d507"},
                                  font={"family": "Mitr, sans-serif",
                                        "size": 14, "color": "#202124"},
                                  plot_bgcolor="#f9f9f9")
        figure_line.update_traces(line_color="#005744")

        return figure_line

    if service and not offer_type:
        dataset = dataset_plot(service=service)
        figure_line = px.line(dataset, x="Mes Registro", y=service,
                              title=f'Total registros {service.title()}: {dataset[service].sum()} ')
        figure_line.update_layout(xaxis={'tickmode': 'array',
                                         'tickvals': [i for i in range(1, 13)],
                                         'ticktext': ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"]},
                                  title_font={
            "family": "Mitr, sans-serif", "size": 18, "color": "#c0d507"},
            font={"family": "Mitr, sans-serif",
                  "size": 14, "color": "#202124"},
            plot_bgcolor="#f9f9f9")
        figure_line.update_traces(line_color="#005744")

        return figure_line

    if area and not offer_type:
        dataset = dataset_plot(area=area)
        figure_line = px.line(dataset, x="Mes Registro", y=area,
                              title=f'Total registros {area.title()}: {dataset[area].sum()} ')
        figure_line.update_layout(xaxis={'tickmode': 'array',
                                         'tickvals': [i for i in range(1, 13)],
                                         'ticktext': ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"]},
                                  title_font={
            "family": "Mitr, sans-serif", "size": 18, "color": "#c0d507"},
            font={"family": "Mitr, sans-serif",
                  "size": 14, "color": "#202124"},
            plot_bgcolor="#f9f9f9")
        figure_line.update_traces(line_color="#005744")

        return figure_line

    if business_unity and not offer_type:
        dataset = dataset_plot(business_unity=business_unity)
        figure_line = px.line(dataset, x="Mes Registro", y=business_unity,
                              title=f'Total registros {business_unity.title()}: {dataset[business_unity].sum()}', labels={business_unity: "Cantidad de matrículas"})

        figure_line.update_layout(
            xaxis={
                'tickmode': 'array',
                'tickvals': [i for i in range(1, 13)],
                'ticktext': ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"]},
            title_font={
                "family": "Mitr, sans-serif",
                "size": 18,
                "color": "#c0d507"},
            font={
                "family": "Mitr, sans-serif",
                "size": 14,
                "color": "#202124"},
            plot_bgcolor="#f9f9f9")
        figure_line.update_traces(line_color="#005744")

        return figure_line

    dataset = df.groupby('Mes Registro', axis=0).count()[
        'Evento'].reset_index()
    figure_line = px.line(
        dataset, x="Mes Registro", y='Evento', title=f'Total registros: {df["Evento"].shape[0]}', labels={'Evento': "Cantidad de matrículas"},)

    figure_line.update_layout(
        xaxis={
            'tickmode': 'array',
            'tickvals': [i for i in range(1, 13)],
            'ticktext': ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"]},
        title_font={
            "family": "Mitr, sans-serif",
            "size": 18,
            "color": "#c0d507"},
        font={
            "family": "Mitr, sans-serif",
            "size": 14,
            "color": "#202124"},
        plot_bgcolor="#f9f9f9",

        # tracecolor='rgb(204, 204, 204)',

    )

    figure_line.update_traces(line_color="#005744")

    return figure_line


if __name__ == "__main__":
    app.run_server(debug=True, port=3000)


# if offer_type or business_unity or area:
#         if offer_type and business_unity:
#             print(business_unity)
#             print(offer_type)
#             dataset = dataset_plot_by_offer(offer_type=offer_type, business_unity=business_unity)
#             figure_line = px.line(dataset, x=dataset["Mes Registro"], y=dataset[offer_type],
#                                 title=f'Total de registros para {business_unity.title()}: {dataset[business_unity].sum()}')
#             return figure_line
#         elif offer_type==None:
#             dataset = dataset_plot(business_unity=business_unity)
#             figure_line = px.line(
#                 dataset, x=dataset["Mes Registro"], y=dataset[business_unity], title="plotting Here")
#             return figure_line

#         if offer_type and area and business_unity:
#             print(area)
#             print(offer_type)
#             dataset = dataset_plot(offer_type=offer_type, area=area)
#             figure_line = px.line(dataset, x=dataset["Mes Registro"], y=dataset[offer_type],
#                                 title=f'Total de registros para {area.title()}: {dataset[area].sum()}')
#             return figure_line

#         elif offer_type==None:
#             dataset = dataset_plot(area=area)
#             figure_line = px.line(dataset, x=dataset["Mes Registro"], y=dataset[area])
#             return figure_line
