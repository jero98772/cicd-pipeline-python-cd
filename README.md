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

## Evidencias

- Pull Request de la seccion 9: https://github.com/jero98772/entregable-2-cicd/pull/2
- Ejecucion fallida del pipeline por el error intencional: https://github.com/jero98772/entregable-2-cicd/actions/runs/43619952751
- Ejecucion final exitosa del PR: https://github.com/jero98772/entregable-2-cicd/actions/runs/43619997110

## Respuestas

### 1. Ventajas de un pipeline de CI

1. **Retroalimentacion rapida y automatica.** Cada push y cada Pull Request
   ejecuta formato, linters, pruebas, construccion de la imagen y analisis de
   calidad sin intervencion humana. Un error se detecta en minutos, cuando el
   cambio todavia es pequeno y el autor recuerda el contexto, y no semanas
   despues en produccion.
2. **Calidad consistente y objetiva.** Las mismas reglas (Black, cobertura
   >= 80 %, Quality Gate de SonarCloud, 0 issues) se aplican a todos los
   cambios por igual, en un entorno limpio y con las mismas versiones fijadas.
   Se elimina el "en mi maquina funciona" y la revision no depende de que
   alguien se acuerde de correr las pruebas.
3. **`main` siempre integrable y desplegable.** Junto con la regla
   `proteger-main`, ningun cambio entra a `main` si el check `build-and-test`
   no esta en verde. Asi `main` refleja siempre una version que paso todas las
   validaciones y la imagen publicada en Docker Hub es confiable para el
   despliegue del Taller 3.
4. **Trazabilidad.** Cada imagen se etiqueta con el SHA del commit, y cada
   ejecucion guarda logs y reportes (artefactos), por lo que se puede saber
   exactamente que codigo esta en cada imagen y por que fallo un cambio.

### 2. Prueba unitaria, de componente y de aceptacion

Ejemplo: una **tienda en linea** donde el usuario agrega productos al carrito
y paga; el total se calcula con descuentos e impuestos.

- **Unitaria:** prueba una funcion aislada, sin servidor ni base de datos.
  Ej.: `calcular_total(items, descuento)` devuelve 90 para un producto de 100
  con 10 % de descuento. En este taller: `restar(5, 2) == 3`.
- **De componente:** prueba un componente completo (rutas + logica +
  plantilla) a traves de su interfaz, sin levantar servidores reales ni
  navegador. Ej.: un POST a `/carrito` con el cliente de pruebas de Flask
  responde 200 y el HTML muestra "Total: 90". En este taller: `test_app.py`
  envia el formulario y verifica `Resultado: 5.0`.
- **De aceptacion:** prueba la aplicacion como lo haria un usuario, con un
  navegador real sobre la aplicacion en ejecucion. Ej.: Selenium abre la
  tienda, agrega un producto, va al carrito y comprueba que el total visible
  es el esperado. En este taller: `test_acceptance_app.py` llena el
  formulario en Chrome headless contra el contenedor Docker.

### 3. Steps del workflow

| Step | Que hace | Para que |
|---|---|---|
| Checkout | Clona el repositorio con historial completo (`fetch-depth: 0`). | Tener el codigo; SonarCloud usa el historial para identificar el codigo nuevo. |
| Set up Python | Instala Python 3.13. | Usar la misma version que el Dockerfile y el entorno local. |
| Install dependencies | Instala `requirements-dev.txt` verificando hashes y solo con wheels. | Herramientas identicas en cada ejecucion y sin ejecutar scripts de instalacion de terceros. |
| Run Black | `black app --check`. | Detener el pipeline si hay codigo sin formatear. |
| Run Pylint / Run Flake8 | Generan `pylint-report.txt` y `flake8-report.txt` con `--exit-zero`. | Enviar sus hallazgos a SonarCloud, que decide con el Quality Gate; si la herramienta no corre, el paso si falla. |
| Run Unit and Component Tests | `pytest` sin aceptacion y con `--cov-fail-under=80`. | Fallar rapido si una prueba falla o la cobertura total baja de 80 %; genera `coverage.xml`. |
| Build Docker image | Construye la imagen una sola vez con la etiqueta del SHA. | Empaquetar la version exacta del codigo que se va a probar y publicar. |
| Start container | Corre la imagen en el puerto 8000 y espera hasta 30 s a que responda. | Tener la app empaquetada en ejecucion para las pruebas de aceptacion. |
| Run Acceptance Tests | Selenium (Chrome headless) contra `http://localhost:8000`. | Validar la imagen real desde la perspectiva del usuario. |
| Show container logs on failure | Muestra `docker logs` solo si algo fallo. | Diagnosticar fallos del contenedor. |
| Upload Test Reports Artifacts | Sube reportes de pruebas, cobertura y linters (`if: always()`). | Revisar los resultados aun cuando el pipeline falla. |
| SonarCloud Scan | Envia codigo y reportes a SonarCloud y espera el Quality Gate. | Bloquear el cambio si no cumple la calidad (issues, hotspots, cobertura). |
| Login to Docker Hub | Inicia sesion con la variable `DOCKERHUB_USERNAME` y el secreto `DOCKERHUB_TOKEN` (solo push a `main`). | Autorizar la publicacion sin exponer credenciales. |
| Push Docker image | Etiqueta la imagen probada como `latest` y publica `latest` y el SHA (solo push a `main`). | Publicar exactamente la imagen validada, solo cuando el cambio ya esta integrado. |

### 4. Problemas encontrados y como se solucionaron

**Daniel Arango Sohm:**

- **Quality Gate en rojo por issues de seguridad.** SonarCloud reporto como
  issues (no como hotspots) varias reglas: acciones de GitHub sin fijar a un
  SHA (S7637), `pip install` sin versiones bloqueadas ni hashes (S8544) y sin
  `--only-binary :all:` (S8541), y la proteccion CSRF deshabilitada en Flask
  (S4502). Se corrigieron en el codigo, sin marcarlos como aceptados: las
  acciones se fijaron a su SHA completo, las dependencias se generan con
  `pip-compile --generate-hashes` y se instalan con `--require-hashes
  --only-binary :all:`, y se habilito `CSRFProtect` de Flask-WTF con el token
  en el formulario. Para que los 4 workers de Gunicorn validen el mismo token
  se uso `--preload` (comparten la `SECRET_KEY`), y en las pruebas de
  componente se desactiva CSRF porque el cliente de pruebas no envia el token.
- **Workflow invalido.** La linea `run: pip install ... --only-binary :all: -r
  ...` rompia el YAML (": " dentro de un escalar plano) y GitHub ni siquiera
  ejecutaba el job. Se soluciono usando un bloque `run: |`.
- **Sin Chrome en el equipo local.** Las pruebas de Selenium se validan en el
  pipeline (el runner de Ubuntu trae Chrome); localmente se comprueba que el
  contenedor responde y muestra la calculadora.
- **Equipo de un solo integrante.** GitHub no permite aprobar el propio Pull
  Request, por lo que el rol Admin quedo en la Bypass list del ruleset para
  poder integrar los PR.

### 5. Ventajas de probar y publicar la misma imagen

- **Se prueba lo que se entrega.** Las pruebas de aceptacion corren contra el
  contenedor real (sistema operativo base, dependencias de ejecucion,
  Gunicorn, puerto, archivos copiados), no solo contra el codigo. Errores como
  olvidar copiar `templates/`, una dependencia faltante en `requirements.txt`
  o un `CMD` mal escrito se detectan antes de publicar.
- **Sin diferencias entre lo probado y lo publicado.** Reconstruir la imagen
  despues de probar podria traer otra version de la imagen base o de una
  dependencia. Al etiquetar y publicar la misma imagen (mismo SHA) se
  garantiza que lo validado es exactamente lo que se despliega.
- **Trazabilidad y despliegues reproducibles.** La etiqueta del SHA permite
  saber que commit contiene cada imagen y volver a una version anterior si es
  necesario; `latest` siempre apunta a la ultima version validada de `main`.

### 6. Pull Request de la seccion 9

**Pruebas agregadas y que error detectaria cada una:**

- `test_operaciones_con_decimales`: `sumar(0.1, 0.2) == pytest.approx(0.3)`,
  `multiplicar(0.5, 0.2)` y `dividir(1, 3)` con decimales. Detectaria que una
  operacion convierta a entero o redondee (por ejemplo usar `//` en lugar de
  `/` en `dividir`, o `int()` sobre los operandos).
- `test_operaciones_con_dos_negativos`: las 4 operaciones con dos negativos
  (`restar(-2, -3) == 1`, `multiplicar(-2, -3) == 6`, etc.). Detectaria un
  manejo incorrecto de signos, como usar `abs()` o invertir los operandos en
  `restar`.
- `test_index_post_un_numero_invalido` (componente): envia `num1='2'` y
  `num2='abc'`. Detectaria que la aplicacion solo valide el primer numero o
  que falle con un error 500 en lugar de mostrar
  "Error: Introduce numeros validos".

**Error intencional:** `restar` se cambio a `return a + b`. El pipeline fallo
en el paso **Run Unit and Component Tests** (`test_restar` y
`test_index_post_restar` fallaron). Los pasos **Build Docker image, Start
container, Run Acceptance Tests, SonarCloud Scan, Login to Docker Hub y Push
Docker image no se ejecutaron**; solo corrieron los de diagnostico (`if:
failure()`) y la subida de reportes (`if: always()`).

**Como se impidio que llegara a `main` y a Docker Hub:** el ruleset
`proteger-main` exige un Pull Request y que el check `build-and-test` este en
verde, asi que el PR quedo bloqueado para el merge mientras el check estaba
en rojo y nadie podia hacer push directo a `main`. Ademas, la publicacion
solo ocurre en un push a `main` y despues de que todos los pasos anteriores
pasen, por lo que la imagen con el error nunca se construyo ni se publico.
Tras corregir `restar`, el pipeline del PR volvio a verde y el PR se integro.
