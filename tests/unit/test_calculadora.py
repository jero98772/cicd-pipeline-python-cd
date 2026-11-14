import pytest

from app import calculadora

pytestmark = pytest.mark.unit


def test_autor_tiene_tres_integrantes():
    assert len(calculadora.AUTOR.split(",")) == 3


def test_sumar():
    assert calculadora.sumar(2, 3) == 5


def test_restar():
    assert calculadora.restar(5, 3) == 2


def test_multiplicar():
    assert calculadora.multiplicar(4, 3) == 12


def test_dividir():
    assert calculadora.dividir(10, 4) == 2.5


def test_dividir_entre_cero():
    with pytest.raises(ZeroDivisionError):
        calculadora.dividir(1, 0)
