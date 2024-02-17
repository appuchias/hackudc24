import pandas as pd
from datetime import datetime
import plotly.express as px

# Cargar el archivo CSV y procesar los datos
df = pd.read_csv("dataset_365dias.csv", delimiter=";")
df["Fecha_Hora"] = pd.to_datetime(
    df["Fecha"] + " " + (df["Hora"] - 1).astype(str) + ":00:00",
    format="%d/%m/%Y %H:%M:%S",
)

# Inicializar la aplicación Dash
app = dash.Dash(name)

# Diseño de la aplicación
app.layout = html.Div(
    [
        # Dropdown para seleccionar un día específico
        html.Label("Seleccionar un día:"),
        dcc.Dropdown(
            id="dropdown-dia",
            options=[{"label": dia, "value": dia} for dia in df["Fecha"].unique()],
            value=df["Fecha"].iloc[0],
            multi=False,
        ),
        # Gráfico de barras para el consumo total por meses
        dcc.Graph(id="consumo-meses"),
        # Gráfico de barras para el consumo por horas en un día específico
        dcc.Graph(id="consumo-dia"),
    ]
)


# Callback para actualizar el gráfico de consumo total por meses
@app.callback(Output("consumo-meses", "figure"), [Input("dropdown-dia", "value")])
def actualizar_consumo_meses(dia_seleccionado):
    # Filtrar el DataFrame para el día seleccionado
    df_dia = df[df["Fecha"] == dia_seleccionado]

    # Calcular el consumo total por mes
    consumo_por_mes = (
        df_dia.groupby(df_dia["Fecha_Hora"].dt.month)["Consumo_KWh"].sum().reset_index()
    )

    # Crear el gráfico
    fig = px.bar(
        consumo_por_mes,
        x="Fecha_Hora",
        y="Consumo_KWh",
        labels={"Fecha_Hora": "Mes", "Consumo_KWh": "Consumo total (KWh)"},
        title=f"Consumo total por mes - {dia_seleccionado}",
    )

    return fig


# Callback para actualizar el gráfico de consumo por horas en un día específico
@app.callback(Output("consumo-dia", "figure"), [Input("dropdown-dia", "value")])
def actualizar_consumo_dia(dia_seleccionado):
    # Filtrar el DataFrame para el día seleccionado
    df_dia = df[df["Fecha"] == dia_seleccionado]

    # Crear el gráfico
    fig = px.bar(
        df_dia,
        x="Hora",
        y="Consumo_KWh",
        labels={"Hora": "Hora del día", "Consumo_KWh": "Consumo (KWh)"},
        title=f"Consumo por horas - {dia_seleccionado}",
    )

    return fig


# Ejecutar la aplicación
if name == "main":
    app.run_server(debug=True)
