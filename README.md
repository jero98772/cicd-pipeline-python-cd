# entregable-2-cicd

Calculadora web en Python (Flask) con un pipeline de Integracion Continua en
GitHub Actions: Black, Pylint, Flake8, pruebas unitarias y de componente con
cobertura >= 80 %, imagen Docker, pruebas de aceptacion con Selenium contra el
contenedor, analisis en SonarCloud (Quality Gate) y publicacion en Docker Hub
de la misma imagen probada, solo en push a `main`.

## Integrantes

| # | Nombre completo | Usuario de GitHub | Rol |
|---|---|---|---|
| 1 | Daniel Arango Sohm | [jero98772](https://github.com/jero98772) | Propietario del repositorio |

> Equipo de un solo integrante (`AUTOR` en `app/calculadora.py` = "Daniel Arango Sohm").

## Enlaces

- Repositorio: https://github.com/jero98772/entregable-2-cicd
- SonarCloud: https://sonarcloud.io/project/overview?id=jero98772_entregable-2-cicd
- Docker Hub: https://hub.docker.com/r/jero98772/entregable-2-cicd (`jero98772/entregable-2-cicd`)

## Ejecucion local

```bash
python -m venv venv && source venv/bin/activate
pip install --require-hashes --only-binary :all: -r requirements-dev.txt
pytest --ignore=tests/test_acceptance_app.py --cov-fail-under=80
docker build -t mi-calculadora-local . && docker run -d -p 8080:8000 mi-calculadora-local
```
