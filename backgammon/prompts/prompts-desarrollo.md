# Registro de Prompts de IA: Desarrollo

## 2025-09-01 — tablero.py (Estructura Inicial)
**Herramienta:** ChatGPT

Prompt:
Teniendo en cuenta la consigna que te envié, ¿Me ayudás a escribir un archivo `tablero.py` sencillo en Python con una clase `Tablero` con `PUNTOS = 24`, un arreglo/lista de 24 puntos (listas vacías adentro), un método `punto(i)` y validación de índice que tire `ValueError` si es inválido? Código corto, en español, con comentarios simples.

Respuesta:
```python
# backgammon/core/tablero.py
PUNTOS = 24
FICHAS_POR_JUGADOR = 15

class Tablero:
    def __init__(self):
        # 24 puntos (listas vacías)
        self.__puntos__ = [[] for _ in range(PUNTOS)]
        self.__salidas__ = {}  # fichas que salieron por jugador
        self.__barra__ = {}    # fichas en la barra por jugador
        self.preparar_posicion_inicial()

    # ... [métodos punto, validar_indice_punto, etc.]
Instrucciones del sistema: Ninguna. Uso: Usada sin cambios (Estructura inicial). Archivo Final: core/tablero.py

2025-08-29 — jugador.py (inicial)
Herramienta: ChatGPT Prompt: Hacé una clase Jugador básica en Python con nombre y un id autoincremental. Usá atributos internos con __...__. Código corto y en español. Respuesta: [Código de la clase Jugador] Instrucciones del sistema: Ninguna. Uso: Usada sin cambios. Archivo Final: core/jugador.py

2025-09-03 — dados.py (lógica de tiro)
Herramienta: ChatGPT Prompt: Necesito un método tirar en mi clase Dados. Debe generar dos números (d1, d2) entre 1 y 6. Si son iguales (doble), la lista de movimientos debe contener el valor repetido 4 veces. Si son distintos, solo d1 y d2. Debe usar random.Random para semillas reproducibles. Respuesta: [Generó el código del método tirar, incluyendo el chequeo de doble y el uso de random.Random.] Instrucciones del sistema: Ninguna. Uso: Usada con modificaciones (Ajustes menores en la inicialización y el getter del último tiro). Archivo Final: core/dados.py

2025-09-05 — Dockerfile y .dockerignore
Herramienta: ChatGPT

Prompt: Necesito un Dockerfile simple para un proyecto Python. Que use una imagen liviana oficial, instale requirements.txt, copie el paquete backgammon/ y deje como comando por defecto ejecutar los tests con python -m unittest discover backgammon/tests. También un .dockerignore mínimo para no copiar cachés. Texto corto y en español.

Respuesta: [Contenido completo del Dockerfile y .dockerignore] Instrucciones del sistema: Ninguna. Uso: Usada sin cambios. Archivo Final: Dockerfile, .dockerignore

2025-10-15 — checker.py (Implementación POO)
Herramienta: Gemini Advanced

Prompt: Necesito implementar la clase Checker (Ficha) en core/checker.py. Debe tener un atributo privado para el ID del dueño (pid) y un @property owner_id. Incluye un método eq para comparar la ficha con otra ficha o con el ID del dueño.

Respuesta: [Generó el código de la clase Checker con el método eq.] Instrucciones del sistema: Actúa como un experto en Python y diseño de POO. Uso: Usada sin cambios (lógica de eq). Archivo Final: core/checker.py

2025-10-16 — tablero.py (Lógica de Quitar Ficha con Checker)
Herramienta: Gemini Advanced

Prompt: Mi lista de puntos en el tablero ahora contiene objetos Checker, no solo IDs. Escribe el nuevo método 'quitar_ficha(jugador_id, punto)' que solo quite la PRIMERA instancia de Checker cuyo owner_id coincida con jugador_id en ese punto, y devuelva True o False.

Respuesta: [Generó el bucle enumerate y el uso de casilla.pop(i) para asegurar que solo se quite una ficha.] Instrucciones del sistema: Asegúrate de que solo se remueva un elemento para simular el movimiento de una sola pieza. Uso: Usada con modificaciones (Asegurar que la búsqueda use .owner_id). Archivo Final: core/tablero.py

2025-10-17 — juego.py (Lógica de Over-Bearing)
Herramienta: Gemini Advanced

Prompt: Necesito la función es_ficha_mas_lejana(jugador_id, punto) en core/juego.py. Debe verificar si no hay fichas del jugador más alejadas de la zona de salida (puntos 1-6 para Negras, 19-24 para Blancas) que la ficha en 'punto'.

Respuesta: [Generó la lógica de los rangos y el chequeo any().] Instrucciones del sistema: La capa core solo debe usar los datos disponibles en Tablero. Uso: Usada sin cambios. Archivo Final: core/juego.py

2025-10-21 — tablero.py (Implementación Estándar)
Herramienta: ChatGPT

Prompt: Escribe el código para la función 'posicion_inicial_estandar(j1_id, j2_id)' en tablero.py, que utiliza 'self.colocar_ficha'. La distribución es: J1: (2 fichas en 23, 5 en 12, 3 en 7, 5 en 5). J2: (2 fichas en 0, 5 en 11, 3 en 16, 5 en 18).

Respuesta: [Generó la lista de tuplas con las cantidades y puntos, y el bucle for anidado para la colocación.] Instrucciones del sistema: Asegúrate de que los índices sean 0-23 y que la suma de fichas sea 15 para cada jugador. Uso: Usada sin cambios. Archivo Final: core/tablero.py

2025-10-21 — juego.py (Lógica de Reingreso)
Herramienta: Gemini Advanced

Prompt: Necesito la función auxiliar _entrada_para(pid) en juego.py. Debe devolver el índice de punto correcto para reingreso desde la barra: 0 para el Jugador 1 (id impar) y 23 para el Jugador 2 (id par).

Respuesta: [Generó la lógica if/else simple para determinar el punto de reingreso (0 o 23).] Instrucciones del sistema: Asegúrate de que el código sea muy conciso y utilice el id de los jugadores disponibles en la clase. Uso: Usada sin cambios. Archivo Final: core/juego.py

2025-10-23 — juego.py (Lógica de Aplicar Movimiento)
Herramienta: Gemini Advanced

Prompt: Revisa mi método aplicar_movimiento y simplifica la lógica de consumo de dados para el Bearing Off, extrayendo la validación de dado mayor (over-bearing) a un bloque if/else final, después de verificar el movimiento normal y el reingreso.

Respuesta: [Generó una estructura de aplicar_movimiento más limpia, basando el consumo en la variable distancia y los condicionales de hasta==PUNTOS.] Instrucciones del sistema: Mantener la claridad y evitar la repetición de código para el consumo de dados. Uso: Usada con modificaciones (Ajuste del consumo final de distancia). Archivo Final: core/juego.py

## 2025-10-24 — juego.py (Aplicación del Principio DIP/SRP)
**Herramienta:** Gemini Advanced 

Prompt:
Necesito la clase Juego para coordinar el estado. Asegúrate de que los atributos principales (tablero, dados, jugadores) se inicialicen en el constructor para demostrar la Inversión de Dependencias (DIP) y se acceda a ellos mediante @property.

Respuesta:
[Generó el constructor inicial de Juego, incluyendo los atributos __tablero__, __dados__, y __jugadores__, y definió las propiedades correspondientes.]
**Instrucciones del sistema:** La clase debe ser el único punto de control del flujo principal.
**Uso:** Usada sin cambios.
**Archivo Final:** core/juego.py

## 2025-10-24 — tablero.py (Validación de Índice)
**Herramienta:** ChatGPT 

Prompt:
Para la validación de índice en tablero.py, necesito el código del método validar_indice_punto(i) que lance un ValueError con un mensaje específico si el índice no está entre 0 y 23.

Respuesta:
[Generó la función con el chequeo de rango y el raise ValueError.]
**Instrucciones del sistema:** Ninguna.
**Uso:** Usada sin cambios.
**Archivo Final:** core/tablero.py

## 2025-10-25 — tablero.py (Lógica de Bloqueo)
**Herramienta:** Gemini Advanced 

Prompt:
Escribe el método _bloqueado_por_oponente(jugador_id, punto) para Tablero. Debe verificar que, si hay fichas en el destino, el dueño de la primera ficha no sea jugador_id Y que la cantidad de fichas sea >= 2. La pila contiene objetos Checker.

Respuesta:
[Generó la lógica de validación con destino[0].owner_id y len(destino) >= 2.]
**Instrucciones del sistema:** El código debe ser eficiente y usar la propiedad owner_id de Checker.
**Uso:** Usada sin cambios.
**Archivo Final:** core/tablero.py

## 2025-10-25 — tablero.py (Lógica de Bloqueo)
**Herramienta:** Gemini Advanced 

Prompt:
Escribe el método _bloqueado_por_oponente(jugador_id, punto) para Tablero. Debe verificar que, si hay fichas en el destino, el dueño de la primera ficha no sea jugador_id Y que la cantidad de fichas sea >= 2. La pila contiene objetos Checker.

Respuesta:
[Generó la lógica de validación con destino[0].owner_id y len(destino) >= 2.]
**Instrucciones del sistema:** El código debe ser eficiente y usar la propiedad owner_id de Checker.
**Uso:** Usada sin cambios.
**Archivo Final:** core/tablero.py

## 2025-10-25 — tablero.py (Colocación de Ficha)
**Herramienta:** ChatGPT 

Prompt:
Añade el método 'colocar_ficha(jugador_id, punto)' a la clase Tablero. Debe validar el índice y luego crear una nueva instancia de Checker(jugador_id) y añadirla al punto.

Respuesta:
[Generó el código del método, incluyendo la validación y la instanciación de Checker.]
**Instrucciones del sistema:** Asegúrate de que la función utilice el método validar_indice_punto interno.
**Uso:** Usada con modificaciones (se corrigió el tipo de dato devuelto a booleano).
**Archivo Final:** core/tablero.py

## 2025-10-25 — juego.py (Lógica de Home Board)
**Herramienta:** Gemini Advanced 

Prompt:
Necesito la lógica de _validar_movimiento que evite que el Jugador 1 (ID impar) mueva una ficha si el índice de destino (hasta) es menor que el índice de origen (desde), ya que solo deben moverse hacia adelante (índices crecientes).

Respuesta:
[Generó la condición if (pid % 2 != 0 and hasta < desde) para bloquear movimientos inversos en la fase de movimiento normal.]
**Instrucciones del sistema:** La validación debe aplicarse solo en el bloque de movimiento normal, no reingreso o bearing off.
**Uso:** Usada sin cambios.
**Archivo Final:** core/juego.py

## 2025-10-29 — juego.py (DIP y Propiedades)
**Herramienta:** Gemini Advanced 

Prompt:
Necesito la clase Juego para coordinar el estado. Asegúrate de que los atributos principales (tablero, dados, jugadores) se inicialicen en el constructor para demostrar la Inversión de Dependencias (DIP) y se acceda a ellos mediante @property.

Respuesta:
[Generó el constructor inicial de Juego, incluyendo los atributos __tablero__, __dados__, y __jugadores__, y definió las propiedades correspondientes.]
**Instrucciones del sistema:** La clase debe ser el único punto de control del flujo principal.
**Uso:** Usada sin cambios.
**Archivo Final:** core/juego.py

## 2025-10-29 — tablero.py (Validación de Colocación)
**Herramienta:** ChatGPT 

Prompt:
Añade el método 'colocar_ficha(jugador_id, punto)' a la clase Tablero. Debe validar el índice y luego crear una nueva instancia de Checker(jugador_id) y añadirla al punto. Asegúrate de que la función retorne un booleano (True).

Respuesta:
[Generó el código del método, incluyendo la validación, la instanciación de Checker, y el retorno de True.]
**Instrucciones del sistema:** La función debe utilizar el método validar_indice_punto interno.
**Uso:** Usada con modificaciones (se corrigió el tipo de dato devuelto a booleano).
**Archivo Final:** core/tablero.py

## 2025-10-30 — juego.py (Lógica de Home Board para Bearing Off)
**Herramienta:** Gemini Advanced 

Prompt:
Necesito la lógica final en juego.py para que el Jugador 1 (ID impar) no pueda mover una ficha de un punto más cercano a la salida (ej: 23) si todavía tiene una ficha en un punto más lejano (ej: 21) y solo tiene un dado de valor [2]. La función 'es_ficha_mas_lejana' debe validar esta restricción en el chequeo de over-bearing.

Respuesta:
[Generó un ajuste a la lógica de 'es_ficha_mas_lejana' para que busque si hay alguna ficha en los puntos entre el origen y el borde de la casa.]
**Instrucciones del sistema:** La regla debe ser estricta para garantizar que las fichas se saquen en orden correcto.
**Uso:** Usada con modificaciones (Ajuste de la condición de rango).
**Archivo Final:** core/juego.py

## 2025-10-30 — tablero.py (Manejo de Error de Índice)
**Herramienta:** ChatGPT 

Prompt:
Necesito agregar el manejo de excepciones al método 'punto(i)' en Tablero. Debe llamar a 'validar_indice_punto(i)' para asegurar que si se pide un índice fuera de rango (ej. 24 o -1), se lance un ValueError con el mensaje correcto.

Respuesta:
[Generó la función punto(i) que contiene la llamada al método validar_indice_punto.]
**Instrucciones del sistema:** El código debe ser corto y limpio, solo realizando el chequeo de índice.
**Uso:** Usada sin cambios.
**Archivo Final:** core/tablero.py