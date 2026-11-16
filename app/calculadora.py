"""Operaciones basicas de la calculadora."""

# Nombres completos de los integrantes, separados por " | " y en el mismo
# orden de la seccion Integrantes del README.
AUTOR = "Daniel Arango Sohm"


def sumar(a, b):
    """Retorna la suma de a y b."""
    return a + b


def restar(a, b):
    """Retorna la resta de a menos b."""
    return a - b


def multiplicar(a, b):
    """Retorna el producto de a por b."""
    return a * b


def dividir(a, b):
    """Retorna a dividido b. Lanza ZeroDivisionError si b es cero."""
    if b == 0:
        raise ZeroDivisionError("No se puede dividir por cero")
    return a / b


def potencia(a, b):
    """Retorna a elevado a la b. Lanza OverflowError si el resultado es muy grande."""
    return a**b


def modulo(a, b):
    """Retorna el residuo de dividir a entre b. Lanza ZeroDivisionError si b es cero."""
    if b == 0:
        raise ZeroDivisionError("No se puede dividir por cero")
    return a % b
