from datetime import datetime

consumptions = dict()

with open("dataset/consumptions.csv", "r") as f:
    data = f.readlines()

for line in data[1:]:
    cups, fecha, hora, kWh, metodo = line.strip().split(";")

    fecha = fecha.split("/")[::-1]

    fechahora = datetime.strptime(
        f"{fecha[0]}-{fecha[1]}-{fecha[2]} {int(hora)-1}:00:00", "%Y-%m-%d %H:%M:%S"
    )

    consumptions[fechahora.timestamp()] = float(kWh.replace(",", "."))

print(consumptions)
