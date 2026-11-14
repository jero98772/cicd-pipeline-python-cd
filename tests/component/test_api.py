import pytest

pytestmark = pytest.mark.component


@pytest.mark.parametrize(
    "operacion,a,b,esperado",
    [
        ("sumar", 2, 3, 5),
        ("restar", 5, 3, 2),
        ("multiplicar", 4, 3, 12),
        ("dividir", 10, 4, 2.5),
    ],
)
def test_operaciones(client, operacion, a, b, esperado):
    r = client.get(f"/{operacion}", query_string={"a": a, "b": b})
    assert r.status_code == 200
    assert r.get_json()["resultado"] == esperado


def test_raiz(client):
    r = client.get("/")
    assert r.status_code == 200
    assert r.get_json()["estado"] == "ok"


def test_operacion_desconocida(client):
    assert client.get("/potencia?a=1&b=2").status_code == 404


def test_faltan_parametros(client):
    assert client.get("/sumar?a=1").status_code == 400


def test_parametro_no_numerico(client):
    assert client.get("/sumar?a=x&b=2").status_code == 400


def test_parametro_no_finito(client):
    assert client.get("/sumar?a=nan&b=2").status_code == 400


def test_division_entre_cero(client):
    assert client.get("/dividir?a=1&b=0").status_code == 400
