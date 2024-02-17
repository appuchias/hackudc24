#!/usr/bin/env python3

from datetime import date, datetime
from flask import Flask, render_template, redirect, abort, request
from werkzeug.utils import secure_filename

from medias_dinamicas import peticion
from procesado import consumptions_csv_to_df, anadir_precios
from resumen import *

app = Flask(__name__)

UPLOADS_FOLDER = "subidas"


# Rutas de la aplicación
@app.route("/")
def home():
    return render_template("inicio.html")


@app.route("/sobre-nosotros")
def about():
    return render_template("sobre-nosotros.html")


@app.route("/subir", methods=["GET", "POST"])
def subir():
    if request.method == "POST":
        # Primer archivo
        archivo = request.files[request.files.keys().__iter__().__next__()]
        newfilename = f"{datetime.now().timestamp()}_{secure_filename(archivo.filename)}"  # type: ignore
        archivo.save(f"{UPLOADS_FOLDER}/{newfilename}")

        # Añadir precios
        anadir_precios(f"{UPLOADS_FOLDER}/{newfilename}")

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
        precios=datos_precio_horas(df).to_dict(orient="records"),
    )


@app.route("/peticion/<path:filename>", methods=["GET", "POST"])
def peticion_filename(filename):
    if request.method == "GET":
        return render_template("peticion.html", filename=filename)

    df = consumptions_csv_to_df(f"{UPLOADS_FOLDER}/{filename}")

    Hora = request.form.get("Hora", None)
    DOW = request.form.get("DOW", None)
    mes = request.form.get("mes", None)
    año = request.form.get("ano", None)

    avg = peticion(Hora, DOW, mes, año, df)

    return f'<h1 id="media">La media es: {round(avg, 5)} kWh</h1>'


# HTMX
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
        precios=datos_precio_horas(df).to_dict(orient="records"),
    )


# Fixes
@app.route("/favicon.ico")
def favicon():
    return redirect("/static/favicon.png")


# Easter eggs
@app.route("/teapot")
def teapot():
    abort(418)
