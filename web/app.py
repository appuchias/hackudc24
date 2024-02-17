#!/usr/bin/env python3

from datetime import datetime
from flask import Flask, render_template, redirect, abort, request
from pathlib import Path
from werkzeug.utils import secure_filename

from procesado import consumptions_csv_to_df

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
    return render_template(
        "resumen.html",
        tables=[df.to_html(classes="data")],
        data=[df.to_dict(orient="records")],
    )


# Fixes
@app.route("/favicon.ico")
def favicon():
    return redirect("/static/favicon.png")


# Easter eggs
@app.route("/teapot")
def teapot():
    abort(418)
