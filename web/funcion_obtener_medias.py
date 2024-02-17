# Antón Liñares
# Función peticion para realizar una petición de años, meses o días y obtener
# la media para esos años, meses o días. Puedes mandar aquellos atributos
# deseados.
 

from datetime import datetime, date
from datetime import datetime
import pandas as pd
import numpy as np
from datetime import datetime
from dateutil import parser
import statistics



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




def peticion(Hora=None, DOW=None, mes=None, año=None, df=None):
    ''' Devuelve la media para los parámetros deseados.
    Hora, DOW (día de la semana), mes, año, df'''
    
    mascara = [1 if atributo == None else 0 for atributo in [Hora, DOW, mes, año]]
    print(mascara)

    avg=[]
    for index, row in df.iterrows():
        if (row["Hora"]==Hora or mascara[0]) and (row["DOW"]==DOW or mascara[1]) and (row["Mes"]== mes or mascara[2]) and (row["Ano"]==año or mascara[3]):
            avg.append(row[2])
    return statistics.mean(avg)
    



    
   
            
        
        
if __name__ == "__main__":
    df = consumptions_csv_to_df("dataset_365dias.csv")
    print(peticion(Hora=3, df=df))
    pass

