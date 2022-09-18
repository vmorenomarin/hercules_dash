import pandas as pd
import plotly.express as px


# Importando el dataset que se generó el módulo data_clean
df = pd.read_csv('./assets/data/dash_dataset.csv', header=0)


def dataset_plot_by_offer(offer_type: str, area: str = None, business_unity=None, service=None):
    """Returna un dataset específico

    Args:
        offer_type (str): Tipo de oferta de la cual se retorna el dataset.
        area (str): Área de la cual se retorna el dataset asociado.
        business_unity: Unidad de negocio de la cual se retorna el dataset asociado.


    Returns:
        Returna un dateset de acuerdo al tipo de oferta y de área especificada.
    """
    if area:
        dataset = df.pivot_table(values=['Evento'], columns=[
                                 'Área', 'Tipo de Oferta'], index='Mes Registro', aggfunc='count').fillna(0)['Evento']
        return dataset[area][offer_type].reset_index('Mes Registro')
    if business_unity:
        dataset = df.pivot_table(values=['Evento'], columns=[
                                 'UNIDAD DE NEGOCIO', 'Tipo de Oferta'], index='Mes Registro', aggfunc='count').fillna(0)['Evento']
        return dataset[business_unity][offer_type].reset_index('Mes Registro')
    if service:
        dataset=df.pivot_table(values=['Evento'], columns=['Nivel', 'Tipo de Oferta'], index='Mes Registro', aggfunc='count').fillna(0)['Evento']
        return dataset[service][offer_type].reset_index('Mes Registro')
            

    dataset = df.pivot_table(values=['UNIDAD DE NEGOCIO'], columns=[
                             'Tipo de Oferta'], index='Mes Registro', aggfunc='count').fillna(0)['UNIDAD DE NEGOCIO']
    return dataset[offer_type].reset_index('Mes Registro')


def dataset_plot(area: str=None, business_unity=None, service=None):
    """Retorna un dataset específico para unidad de negocio o área.

    Args: 
        area (str): Área de la cual se retorna el dataset asociado.
        business_unity: Unidad de negocio de la cual se retorna el dataset asociado.
         

    Returns:
        Returna un dateset de acuerdo al tipo de oferta y de área especificada.
    """
    if area:
        dataset=df.pivot_table(values=['Evento'], columns=['Área'], index='Mes Registro', aggfunc='count').fillna(0)['Evento']
        return dataset[area].reset_index('Mes Registro')
    if business_unity:
        dataset=df.pivot_table(values=['Evento'], columns=['UNIDAD DE NEGOCIO'], index='Mes Registro', aggfunc='count').fillna(0)['Evento']
        return dataset[business_unity].reset_index('Mes Registro')
    if service:
        dataset=df.pivot_table(values=['Evento'], columns=['Nivel'], index='Mes Registro', aggfunc='count').fillna(0)['Evento']
        return dataset[service].reset_index('Mes Registro')    

def get_areas(business_unity: str, only_fosfec: bool = False) -> list:
    """Returna las áreas (sublíneas) de una unidad de negocio del  portafolio de servicios.

    Args:
        business_unity (str): Unidad de negocio.
        only_fosfec (bool, optional): Indica si returna las áreas de FOSFEC. False por defecto.

    Returns:
        list: Returna una lista de áreas.
    """
    areas = list(df['Área'][df['UNIDAD DE NEGOCIO']
                 == business_unity].unique())
    return areas


def get_services(area: str, only_fosfec: bool = False) -> list:
    """Returna los servicios (materales) de una área (sublínea) del  portafolio de servicios.

    Args:
        area (str): Sublínea.
        only_fosfec (bool, optional): Indica si retorna sólo materiales de FOSFEC. False por defecto.

    Returns:
        list: Returna una lista de materiales.
    """
    services = list(df['Nivel'][df['Área'] == area].unique())
    return services


def get_offer_types(service: str) -> list:
    """Returna los tipos de oferta de una unidad de negocio del  portafolio de servicios.

    Args:
        business_unity (str): Unidad de Negocio.

    Returns:
        list: Returna una lista de tipos de oferta.
    """
    offer_types = list(df['Tipo de Oferta']
                       [df['Nivel'] == service].unique())
    return offer_types
