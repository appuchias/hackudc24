from datetime import datetime, date
import pandas as pd
import requests


def consumptions_csv_to_df(path: str = "dataset/consumptions.csv") -> pd.DataFrame:
    consumptions = pd.read_csv(path, delimiter=";")

    # Adaptar campos
    consumptions["Fecha_Hora"] = pd.to_datetime(
        consumptions["Fecha"] + " " + (consumptions["Hora"] - 1).astype(str) + ":00:00",
        format="%d/%m/%Y %H:%M:%S",
    )
    consumptions["Ano"] = consumptions["Fecha_Hora"].dt.year
    consumptions["Mes"] = consumptions["Fecha_Hora"].dt.month
    consumptions["Dia"] = consumptions["Fecha_Hora"].dt.day
    consumptions["Hora"] = consumptions["Fecha_Hora"].dt.hour
    consumptions["DOW"] = consumptions["Fecha_Hora"].dt.dayofweek
    consumptions = consumptions.drop(columns=["Fecha"])

    # Cambiar consumo a float si es string
    if consumptions["Consumo_KWh"].dtype == "O":
        consumptions["Consumo_KWh"] = (
            consumptions["Consumo_KWh"].str.replace(",", ".").astype(float)
        )

    return consumptions


def anadir_precios(path: str):
    with open(path, "r") as f:
        consumptions = list(f.readlines())

    primer_dia = date(*[int(i) for i in consumptions[1].split(";")[1].split("/")[::-1]])
    ultimo_dia = date(
        *[int(i) for i in consumptions[-1].split(";")[1].split("/")[::-1]]
    )

    precios = requests.get(
        f"https://apidatos.ree.es/es/datos/mercados/precios-mercados-tiempo-real?start_date={primer_dia}T00:00&end_date={ultimo_dia}T23:59&geo_limit=peninsular&time_trunc=hour"
    ).json()["included"][0]["attributes"]["values"]

    for i, consumo in enumerate(consumptions):
        if i == 0:
            consumptions[0] = consumptions[0].strip() + ";Precio\n"
            continue

        precio = precios[i - 1]["value"]

        consumptions[i] = f"{consumo.strip()};{precio}\n"

    with open(path, "w") as f:
        f.writelines(consumptions)


def consumptions_csv_to_dict(path: str = "dataset/consumptions.csv") -> dict:

    consumptions = {}

    with open(path, "r") as f:
        data = f.readlines()

    for line in data[1:]:
        cups, fecha, hora, kWh, metodo = line.strip().split(";")

        fecha = fecha.split("/")[::-1]

        fechahora = datetime.strptime(
            f"{fecha[0]}-{fecha[1]}-{fecha[2]} {int(hora)-1}:00:00", "%Y-%m-%d %H:%M:%S"
        )

        consumptions[fechahora.timestamp()] = float(kWh.replace(",", "."))

    return consumptions
