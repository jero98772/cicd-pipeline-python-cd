"""Aplicacion web Flask que expone la calculadora mediante un formulario."""

import os
import secrets

from flask import Flask, render_template, request
from flask_wtf.csrf import CSRFProtect

from .calculadora import dividir, multiplicar, restar, sumar

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY") or secrets.token_hex(32)
csrf = CSRFProtect(app)

OPERACIONES = {
    "sumar": sumar,
    "restar": restar,
    "multiplicar": multiplicar,
    "dividir": dividir,
}


@app.route("/", methods=["GET", "POST"])
def index():
    """Muestra el formulario y, si es un POST, calcula el resultado."""
    resultado = None
    if request.method == "POST":
        try:
            num1 = float(request.form["num1"])
            num2 = float(request.form["num2"])
            operacion = OPERACIONES.get(request.form["operacion"])
            if operacion is None:
                resultado = "Operación no válida"
            else:
                resultado = operacion(num1, num2)
        except ValueError:
            resultado = "Error: Introduce números válidos"
        except ZeroDivisionError:
            resultado = "Error: No se puede dividir por cero"

    return render_template("index.html", resultado=resultado)


@app.route("/health")
def health():
    """Health check usado por el Load Balancer. Incluye la versión desplegada."""
    return {"status": "ok", "version": os.environ.get("APP_VERSION", "local")}


if __name__ == "__main__":  # pragma: no cover
    app.run(port=5000)
