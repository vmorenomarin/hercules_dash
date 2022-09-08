
import pandas as pd
import plotly.express as px


df = pd.read_csv("./assets/data/dash_dataset.csv", header=0)


# Dataframe que resume y contabiliza los tipos de oferta por mes por unidades de negocio.
type_offer_by_business = (
    df.pivot_table(
        values=["Evento"],
        columns=["UNIDAD DE NEGOCIO", "Área", "Tipo de Oferta"],
        index="Mes Registro",
        aggfunc="count",
    )
    .fillna(0)["Evento"]
    .reset_index()
)

# Dataframe que resume y contabiliza los tipos de oferta por mes para todas las unidades de negocio.
type_offer_all = df.pivot_table(
    values="UNIDAD DE NEGOCIO",
    columns=["Tipo de Oferta"],
    index="Mes Registro",
    aggfunc="count",
).fillna(0)



# type_offer_all_business.reset_index(inplace=True)
# type_offer_all_business.drop(['Tipo de Oferta'], axis=1)
# type_offer_all_business.drop(columns=["Tipo de Oferta"])
# df=type_offer_by_business["Evento"].reset_index()
df = type_offer_by_business
type(df)


def data_geneneral_plot(offer_type: str, area: str):
    pass



figure = px.line(
    type_offer_all, x=type_offer_all.index, y=type_offer_all["Pago Empresarial"]
)
figure


figure = px.line(
    df,
    x=df["Mes Registro"],
    y=df["CULTURA"]["ARTES DANZARIAS"]["Venta Directa"],
    title="Oferta",
)
figure
