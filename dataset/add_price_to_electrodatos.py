import requests
from datetime import datetime

years = [2021, 2022, 2023]
enddays = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

prices = dict()


for year in years:
    for month in range(1, 13):
        url = f"https://apidatos.ree.es/es/datos/mercados/precios-mercados-tiempo-real?start_date={year}-{month}-01T00:00&end_date={year}-{month}-{enddays[month-1]}T23:59&geo_limit=peninsular&time_trunc=hour"

        data = requests.get(url).json()

        for day in data["included"][0]["attributes"]["values"]:
            date = datetime.fromisoformat(day["datetime"])
            price = day["value"]

            prices[date.timestamp()] = price


with open("dataset/electrodatos.csv", "r") as f:
    with open("electrodatos-conprecios.csv", "w") as g:
        g.write("cod,ano,mes,dia,dow,hora,Consumo,obtencion,precio\n")

        for line in f.readlines()[1:]:
            cod, fecha, hora, Consumo, obtencion, datetime_value = line.strip().split(
                ","
            )
            date = datetime.strptime(
                f"{fecha} {int(hora)-1}:00:00", "%Y-%m-%d %H:%M:%S"
            )

            price = float(prices[date.timestamp()]) or 0

            g.write(
                f"{cod},{date.year},{date.month},{date.day},{date.weekday()},{date.hour},{Consumo},{obtencion},{price}\n"
            )
