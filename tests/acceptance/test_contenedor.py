import os

import pytest
import requests

pytestmark = pytest.mark.acceptance

BASE_URL = os.getenv("BASE_URL", "http://localhost:5000")


def _get(ruta, **params):
    return requests.get(f"{BASE_URL}{ruta}", params=params, timeout=5)


def test_contenedor_responde():
    r = _get("/")
    assert r.status_code == 200
    assert r.json()["estado"] == "ok"


def test_sumar_via_contenedor():
    r = _get("/sumar", a=2, b=3)
    assert r.status_code == 200
    assert r.json()["resultado"] == 5


def test_dividir_entre_cero_via_contenedor():
    assert _get("/dividir", a=1, b=0).status_code == 400
