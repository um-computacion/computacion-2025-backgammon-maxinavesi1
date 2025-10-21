# Registro de Prompts de IA: Documentación

## 2025-09-03 — Dockerfile y .dockerignore
**Herramienta:** ChatGPT 

Prompt:
Necesito un Dockerfile simple para un proyecto Python. Que use una imagen liviana oficial, instale requirements.txt, copie el paquete backgammon/ y deje como comando por defecto ejecutar los tests con python -m unittest discover backgammon/tests. También un .dockerignore mínimo para no copiar cachés. Texto corto y en español.

Respuesta:
[Contenido completo del Dockerfile inicial y .dockerignore]
**Instrucciones del sistema:** Ninguna.
**Uso:** Usada sin cambios.
**Archivo Final:** Dockerfile, .dockerignore

## 2025-09-10 — Docstrings (Dados)
**Herramienta:** Gemini Advanced 

Prompt:
Revisa mi clase Dados y genera docstrings en formato profesional para cada método, indicando qué recibe y qué devuelve.

Respuesta:
[Generó docstrings para __init__, tirar, y fijar_semilla con el formato Recibe/Devuelve.]
**Instrucciones del sistema:** El docstring debe ser conciso y no usar jerga innecesaria.
**Uso:** Usada con modificaciones (se tradujo el formato final a español).
**Archivo Final:** core/dados.py


## 2025-10-23 — Docstrings (Juego)
**Herramienta:** Gemini Advanced 

Prompt:
Revisa mi método 'aplicar_movimiento' en juego.py y genera un docstring completo en español, detallando Recibe, Hace y Devuelve, especialmente cómo maneja el consumo de dados después de un hit o bearing off.

Respuesta:
[Generó un docstring detallado explicando las tres ramas (Bearing Off, Reingreso, Normal) y el consumo de 'dado_consumido'.]
**Instrucciones del sistema:** El docstring debe ser exhaustivo y explicar los casos especiales.
**Uso:** Usada sin modificaciones.
**Archivo Final:** core/juego.py

## 2025-10-27 — Docstrings (Juego/Tablero)
**Herramienta:** Gemini Advanced 

Prompt:
Necesito docstrings concisos para los métodos estado_dict (Juego), resumen_estado (Juego) y validar_indice_punto (Tablero), especificando qué reciben y qué devuelven.

Respuesta:
[Generó los docstrings para los tres métodos, enfocados en la información que retornan.]
**Instrucciones del sistema:** Usa el formato Recibe/Devuelve.
**Uso:** Usada sin cambios.
**Archivo Final:** core/juego.py, core/tablero.py

## 2025-10-28 — .pylintrc
**Herramienta:** ChatGPT 

## 2025-10-27 — Docstrings (Juego/Tablero)
**Herramienta:** Gemini Advanced 

Prompt:
Necesito docstrings concisos para los métodos estado_dict (Juego), resumen_estado (Juego) y validar_indice_punto (Tablero), especificando qué reciben y qué devuelven.

Respuesta:
[Generó los docstrings para los tres métodos, enfocados en la información que retornan.]
**Instrucciones del sistema:** Usa el formato Recibe/Devuelve.
**Uso:** Usada sin cambios.
**Archivo Final:** core/juego.py, core/tablero.py


## 2025-10-29 — Docstrings (Jugador)
**Herramienta:** Gemini Advanced 

Prompt:
Para la clase Jugador, genera los docstrings para __init__, la propiedad nombre y la propiedad id, asegurando que sigan la convención Recibe/Devuelve.

Respuesta:
[Generó los docstrings con las descripciones de los atributos y el valor retornado para las propiedades.]
**Instrucciones del sistema:** El código debe ser simple.
**Uso:** Usada sin cambios.
**Archivo Final:** core/jugador.py

## 2025-10-31 — Docstrings (Tablero: Posición Inicial)
**Herramienta:** Gemini Advanced 

Prompt:
Genera un docstring completo en español para la función 'posicion_inicial_estandar' en tablero.py, detallando qué recibe (j1_id, j2_id) y qué hace (configura el tablero según la regla 2/5/3/5).

Respuesta:
[Generó el docstring detallando el propósito de la función y lo que se espera de j1_id y j2_id.]
**Instrucciones del sistema:** El docstring debe ser muy claro sobre la distribución inicial.
**Uso:** Usada sin cambios.
**Archivo Final:** core/tablero.py

## 2025-10-31 — Docstrings (Juego: Propiedades)
**Herramienta:** ChatGPT 

Prompt:
Escribe docstrings para las propiedades @property tablero, @property estado, y @property jugador_actual en la clase Juego. Deben ser concisos.

Respuesta:
[Generó los docstrings de las propiedades, indicando el tipo de objeto que devuelve cada una.]
**Instrucciones del sistema:** Ninguna.
**Uso:** Usada sin cambios.
**Archivo Final:** core/juego.py



