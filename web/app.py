#!/usr/bin/env python3

from datetime import date, datetime
from flask import Flask, render_template, redirect, abort, request
from werkzeug.utils import secure_filename

from procesado import consumptions_csv_to_df
from resumen import *

app = Flask(__name__)

UPLOADS_FOLDER = "subidas"


# Rutas de la aplicación
@app.route("/")
def home():
    return render_template("inicio.html")


@app.route("/subir", methods=["GET", "POST"])
def subir():
    if request.method == "POST":
        # Primer archivo
        archivo = request.files[request.files.keys().__iter__().__next__()]
        newfilename = f"{datetime.now().timestamp()}_{secure_filename(archivo.filename)}"  # type: ignore
        archivo.save(f"{UPLOADS_FOLDER}/{newfilename}")

        return redirect(f"/resumen/{newfilename}")

    return render_template("subir.html")


@app.route("/resumen")
def resumen():
    return redirect("/subir")


@app.route("/resumen/<path:filename>")
def resumen_filename(filename):
    df = consumptions_csv_to_df(f"{UPLOADS_FOLDER}/{filename}")

    top5m = top_5_meses(df)
    top5d = top_5_dias(df)
    top5h = top_5_horas(df)

    precision = 2  # Número de decimales a mostrar

    consumo_plot_meses = datos_consumo_meses(df)
    consumo_plot_dow = datos_consumo_dow(df)
    consumo_plot_horas = datos_consumo_horas(df)

    return render_template(
        "resumen.html",
        filename=filename,
        top={
            "mes": {
                "key": top5m["Fecha_Hora"].values[0],
                "consumo": round(top5m["Consumo_KWh"].values[0], precision),
            },
            "dia": {
                "key": top5d["Fecha_Hora"].values[0],
                "consumo": round(top5d["Consumo_KWh"].values[0], precision),
            },
            "hora": {
                "key": top5h["Fecha_Hora"].values[0],
                "consumo": round(top5h["Consumo_KWh"].values[0], precision),
            },
        },
        consumos={
            "meses": consumo_plot_meses.to_dict(orient="records"),
            "dow": consumo_plot_dow.to_dict(orient="records"),
            "horas": consumo_plot_horas.to_dict(orient="records"),
        },
    )


# Actualización del gráfico de horas
@app.route("/horas/<path:filename>", methods=["POST"])
def horas(filename):
    df = consumptions_csv_to_df(f"{UPLOADS_FOLDER}/{filename}")

    fecha = date.fromisoformat(request.form["dia"])

    consumo_plot_horas = datos_consumo_horas(df, fecha)

    return render_template(
        "hx-horas.html",
        consumos=consumo_plot_horas.to_dict(orient="records"),
        dia=fecha,
        filename=filename,
    )


# Fixes
@app.route("/favicon.ico")
def favicon():
    return redirect("/static/favicon.png")


# Easter eggs
@app.route("/teapot")
def teapot():
    abort(418)
