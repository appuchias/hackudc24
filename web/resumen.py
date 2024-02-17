from datetime import date
import pandas as pd


def top_5_meses(df: pd.DataFrame):

    # Calcular el consumo total por mes
    consumo_por_mes = (
        df.groupby(df["Fecha_Hora"].dt.to_period("M"))["Consumo_KWh"]
        .sum()
        .reset_index()
    )

    # Seleccionar los meses con mayor consumo (todos si hay menos de 3)
    top_meses = consumo_por_mes.nlargest(min(3, len(consumo_por_mes)), "Consumo_KWh")

    # print("Los meses con mayor consumo del año (ordenados de mayor a menor consumo):")
    # print(top_meses)

    return top_meses


def top_5_dias(df: pd.DataFrame):

    # Calcular el consumo total por día
    consumo_por_dia = (
        df.groupby(df["Fecha_Hora"].dt.date)["Consumo_KWh"].sum().reset_index()
    )

    # Seleccionar los días con mayor consumo (todos si hay menos de 10)
    top_dias = consumo_por_dia.nlargest(min(10, len(consumo_por_dia)), "Consumo_KWh")

    # print(
    #     "\nLos días con mayor consumo del dataset (ordenados de mayor a menor consumo):"
    # )
    # print(top_dias)

    return top_dias


def top_5_horas(df: pd.DataFrame):
    # Agrupar por hora y calcular la media de consumo
    media_consumo_por_hora = (
        df.groupby(df["Fecha_Hora"].dt.hour)["Consumo_KWh"].mean().reset_index()
    )

    # print("Media de consumo para cada hora a lo largo de todos los días:")
    # print(media_consumo_por_hora.shape)

    # Seleccionar las 5 horas con mayor consumo promedio
    top_5_horas = media_consumo_por_hora.nlargest(5, "Consumo_KWh")

    # print("\nLas 5 horas del día con mayor consumo promedio:")
    # print(top_5_horas)

    return top_5_horas


def datos_consumo_horas(df: pd.DataFrame, dia: date = date(2023, 2, 15)):
    # Filtrar el DataFrame para el día seleccionado
    df_dia = df[df["Fecha_Hora"].dt.date == dia]

    # Agrupar por hora y calcular la media de consumo
    media_consumo_por_hora = (
        df_dia.groupby(df_dia["Fecha_Hora"].dt.hour)["Consumo_KWh"].mean().reset_index()
    )

    return media_consumo_por_hora


def datos_precio_horas(df: pd.DataFrame, dia: date = date(2023, 2, 15)):
    # Filtrar el DataFrame para el día seleccionado
    df_dia = df[df["Fecha_Hora"].dt.date == dia]

    # Agrupar por hora y calcular la media de consumo
    media_precio_por_hora = (
        df_dia.groupby(df_dia["Fecha_Hora"].dt.hour)["Precio"].mean().reset_index()
    )

    return media_precio_por_hora


def datos_consumo_dow(df: pd.DataFrame):
    # Agrupar por día de la semana y calcular la media de consumo
    media_consumo_por_dow = (
        df.groupby(df["Fecha_Hora"].dt.dayofweek)["Consumo_KWh"].mean().reset_index()
    )

    return media_consumo_por_dow


def datos_consumo_meses(df: pd.DataFrame):
    # Agrupar por mes y calcular la media de consumo
    media_consumo_por_mes = (
        df.groupby(df["Fecha_Hora"].dt.month)["Consumo_KWh"].mean().reset_index()
    )

    return media_consumo_por_mes
