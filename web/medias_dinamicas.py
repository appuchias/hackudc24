# Antón Liñares
# Función peticion para realizar una petición de años, meses o días y obtener
# la media para esos años, meses o días. Puedes mandar aquellos atributos
# deseados.

import pandas as pd
import statistics

from procesado import consumptions_csv_to_df


def peticion(Hora=None, DOW=None, mes=None, año=None, df=None):
    """Devuelve la media para los parámetros deseados.
    Hora, DOW (día de la semana), mes, año, df"""

    mascara = [int(atributo is not None) for atributo in [Hora, DOW, mes, año]]
    print(mascara)

    avg = []
    for index, row in df.iterrows():  # type: ignore
        if (
            (row["Hora"] == Hora or mascara[0])
            and (row["DOW"] == DOW or mascara[1])
            and (row["Mes"] == mes or mascara[2])
            and (row["Ano"] == año or mascara[3])
        ):
            avg.append(row[2])

    return statistics.mean(avg)


if __name__ == "__main__":
    df = consumptions_csv_to_df("dataset_365dias.csv")
    print(peticion(Hora=3, df=df))
    pass
