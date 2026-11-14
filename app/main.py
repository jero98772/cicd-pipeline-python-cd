"""API HTTP que expone las operaciones de la calculadora."""

import math
import os
import secrets

from flask import Flask, jsonify, request
from flask_wtf.csrf import CSRFProtect

from app import calculadora

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY") or secrets.token_hex(32)
csrf = CSRFProtect(app)

OPERACIONES = {
    "sumar": calculadora.sumar,
    "restar": calculadora.restar,
    "multiplicar": calculadora.multiplicar,
    "dividir": calculadora.dividir,
}


def _error(mensaje, codigo):
    return jsonify({"error": mensaje}), codigo


def _leer_operandos():
    """Devuelve (a, b) como float, o None si faltan o no son numeros finitos."""
    try:
        a = float(request.args["a"])
        b = float(request.args["b"])
    except (KeyError, ValueError):
        return None
    if not (math.isfinite(a) and math.isfinite(b)):
        return None
    return a, b


@app.get("/")
def raiz():
    return jsonify({"estado": "ok", "autor": calculadora.AUTOR})


@app.get("/<operacion>")
def operar(operacion):
    funcion = OPERACIONES.get(operacion)
    if funcion is None:
        return _error("operacion no soportada", 404)
    operandos = _leer_operandos()
    if operandos is None:
        return _error("a y b son obligatorios y deben ser numeros", 400)
    try:
        resultado = funcion(*operandos)
    except ZeroDivisionError:
        return _error("division entre cero", 400)
    return jsonify({"operacion": operacion, "resultado": resultado})
