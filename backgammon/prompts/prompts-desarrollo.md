# Registro de Prompts de IA: Desarrollo

## 2025-08-29 — jugador.py (inicial)
**Herramienta:** ChatGPT 

**Prompt:**
Hacé una clase Jugador básica en Python con nombre y un id autoincremental. Usá atributos internos con `__...__`. Código corto y en español.

**Respuesta:**
[Código de la clase Jugador con atributos `__nombre__` y `__id__`, y contador de clase `_contador_ids`]

**Instrucciones del sistema:** Ninguna.

**Uso:** Usada sin cambios.

**Archivo Final:** `backgammon/core/jugador.py`

---

## 2025-09-01 — tablero.py (Estructura Inicial)
**Herramienta:** ChatGPT

**Prompt:**
Teniendo en cuenta la consigna que te envié, ¿Me ayudás a escribir un archivo `tablero.py` sencillo en Python con una clase `Tablero` con `PUNTOS = 24`, un arreglo/lista de 24 puntos (listas vacías adentro), un método `punto(i)` y validación de índice que tire `ValueError` si es inválido? Código corto, en español, con comentarios simples.

**Respuesta:**
```python
# backgammon/core/tablero.py
PUNTOS = 24
FICHAS_POR_JUGADOR = 15

class Tablero:
    def __init__(self):
        # 24 puntos (listas vacías)
        self.__puntos__ = [[] for _ in range(PUNTOS)]
        self.__salidas__ = {}  # fichas que salieron por jugador
        self.__barra__ = {}    # fichas en la barra por jugador
    # ... [métodos punto, validar_indice_punto, etc.]
```

**Instrucciones del sistema:** Ninguna.

**Uso:** Usada sin cambios (Estructura inicial).

**Archivo Final:** `backgammon/core/tablero.py`

---

## 2025-09-03 — dados.py (lógica de tiro)
**Herramienta:** ChatGPT 

**Prompt:**
Necesito un método tirar en mi clase Dados. Debe generar dos números (d1, d2) entre 1 y 6. Si son iguales (doble), la lista de movimientos debe contener el valor repetido 4 veces. Si son distintos, solo d1 y d2. Debe usar random.Random para semillas reproducibles.

**Respuesta:**
[Generó el código del método tirar, incluyendo el chequeo de doble y el uso de random.Random.]

**Instrucciones del sistema:** Ninguna.

**Uso:** Usada con modificaciones (Ajustes menores en la inicialización y el getter del último tiro).

**Archivo Final:** `backgammon/core/dados.py`

---

## 2025-09-03 — Dockerfile y .dockerignore
**Herramienta:** ChatGPT

**Prompt:**
Necesito un Dockerfile simple para un proyecto Python. Que use una imagen liviana oficial, instale requirements.txt, copie el paquete backgammon/ y deje como comando por defecto ejecutar los tests con python -m unittest discover backgammon/tests. También un .dockerignore mínimo para no copiar cachés. Texto corto y en español.

**Respuesta:**
[Contenido completo del Dockerfile y .dockerignore]

**Instrucciones del sistema:** Ninguna.

**Uso:** Usada sin cambios.

**Archivo Final:** `Dockerfile`, `.dockerignore`

---

## 2025-09-10 — main.py (CLI básica)
**Herramienta:** ChatGPT

**Prompt:**
Crea un archivo main.py con una CLI básica para Backgammon. Debe tener comandos para: --tirar (tirar dados), --mover <desde> <hasta>, --estado (mostrar estado), --ayuda. Usa sys.argv y un bucle while para procesar comandos.

**Respuesta:**
[Generó la estructura básica de main.py con el parser de argumentos y los comandos principales]

**Instrucciones del sistema:** Mantén el código simple y legible.

**Uso:** Usada con modificaciones (Se agregaron comandos --semilla, --demo, --dump-estado).

**Archivo Final:** `main.py`

---

## 2025-10-15 — checker.py (Implementación POO)
**Herramienta:** Gemini Advanced

**Prompt:**
Necesito implementar la clase Checker (Ficha) en core/checker.py. Debe tener un atributo privado para el ID del dueño (pid) y un @property owner_id. Incluye un método __eq__ para comparar la ficha con otra ficha o con el ID del dueño.

**Respuesta:**
[Generó el código de la clase Checker con el método __eq__.]

**Instrucciones del sistema:** Actúa como un experto en Python y diseño de POO.

**Uso:** Usada sin cambios (lógica de __eq__).

**Archivo Final:** `backgammon/core/checker.py`

---

## 2025-10-16 — tablero.py (Lógica de Quitar Ficha con Checker)
**Herramienta:** Gemini Advanced

**Prompt:**
Mi lista de puntos en el tablero ahora contiene objetos Checker, no solo IDs. Escribe el nuevo método 'quitar_ficha(jugador_id, punto)' que solo quite la PRIMERA instancia de Checker cuyo owner_id coincida con jugador_id en ese punto, y devuelva True o False.

**Respuesta:**
[Generó el bucle enumerate y el uso de casilla.pop(i) para asegurar que solo se quite una ficha.]

**Instrucciones del sistema:** Asegúrate de que solo se remueva un elemento para simular el movimiento de una sola pieza.

**Uso:** Usada con modificaciones (Asegurar que la búsqueda use .owner_id).

**Archivo Final:** `backgammon/core/tablero.py`

---

## 2025-10-17 — juego.py (Lógica de Over-Bearing)
**Herramienta:** Gemini Advanced

**Prompt:**
Necesito la función es_ficha_mas_lejana(jugador_id, punto) en core/juego.py. Debe verificar si no hay fichas del jugador más alejadas de la zona de salida (puntos 1-6 para Negras, 19-24 para Blancas) que la ficha en 'punto'.

**Respuesta:**
[Generó la lógica de los rangos y el chequeo any().]

**Instrucciones del sistema:** La capa core solo debe usar los datos disponibles en Tablero.

**Uso:** Usada sin cambios.

**Archivo Final:** `backgammon/core/juego.py`

---

## 2025-10-18 — pygame_ui.py (Estructura inicial)
**Herramienta:** ChatGPT

**Prompt:**
Necesito crear una interfaz gráfica básica con Pygame para Backgammon. Debe mostrar el tablero con 24 triángulos, dibujar fichas como círculos, y permitir clicks para seleccionar origen y destino. Usa constantes para colores y dimensiones.

**Respuesta:**
[Generó la estructura base de pygame_ui.py con funciones de dibujo del tablero, triángulos, y fichas]

**Instrucciones del sistema:** Separa las funciones de dibujo en funciones auxiliares.

**Uso:** Usada con modificaciones (Se agregaron hints visuales, bearing off bars, y manejo completo de eventos).

**Archivo Final:** `backgammon/pygame/pygame_ui.py`

---

## 2025-10-19 — pygame_ui.py (Sistema de hints)
**Herramienta:** ChatGPT

**Prompt:**
Agrega a pygame_ui.py una función _dibujar_hints() que muestre puntos verdes en los destinos válidos cuando el usuario selecciona una ficha. Debe llamar a juego._validar_movimiento() para cada dado disponible.

**Respuesta:**
[Generó la función _dibujar_hints() con el bucle de movimientos y el dibujo de círculos verdes]

**Instrucciones del sistema:** Usa COLOR_HINT para los círculos de destinos válidos.

**Uso:** Usada sin cambios.

**Archivo Final:** `backgammon/pygame/pygame_ui.py`

---

## 2025-10-21 — tablero.py (Implementación Estándar)
**Herramienta:** ChatGPT

**Prompt:**
Escribe el código para la función 'posicion_inicial_estandar(j1_id, j2_id)' en tablero.py, que utiliza 'self.colocar_ficha'. La distribución es: J1: (2 fichas en 23, 5 en 12, 3 en 7, 5 en 5). J2: (2 fichas en 0, 5 en 11, 3 en 16, 5 en 18).

**Respuesta:**
[Generó la lista de tuplas con las cantidades y puntos, y el bucle for anidado para la colocación.]

**Instrucciones del sistema:** Asegúrate de que los índices sean 0-23 y que la suma de fichas sea 15 para cada jugador.

**Uso:** Usada sin cambios.

**Archivo Final:** `backgammon/core/tablero.py`

---

## 2025-10-21 — juego.py (Lógica de Reingreso)
**Herramienta:** Gemini Advanced

**Prompt:**
Necesito la función auxiliar _entrada_para(pid) en juego.py. Debe devolver el índice de punto correcto para reingreso desde la barra: 0 para el Jugador 1 (id impar) y 23 para el Jugador 2 (id par).

**Respuesta:**
[Generó la lógica if/else simple para determinar el punto de reingreso (0 o 23).]

**Instrucciones del sistema:** Asegúrate de que el código sea muy conciso y utilice el id de los jugadores disponibles en la clase.

**Uso:** Usada sin cambios.

**Archivo Final:** `backgammon/core/juego.py`

---

## 2025-10-21 — Corrección de Pylint en pygame_ui.py
**Herramienta:** Claude 3.7 Sonnet (Anthropic)

**Prompt:**
Tengo el siguiente problema con este codigo
[Se adjuntó el código de pygame_ui.py con errores de Pylint]

Mi codigo debe funcionar igual que este, pero respetando las reglas del pylint

**Respuesta:**
La IA proporcionó una versión completa de `pygame_ui.py` con las siguientes correcciones:
- Eliminación de `from __future__ import annotations`
- División de líneas largas (>100 caracteres)
- Creación de funciones auxiliares `_manejar_evento_tirada()` y `_manejar_movimiento()`
- Corrección de acceso a método privado `_validar_movimiento`
- Añadido de línea en blanco al final
- Corrección de indentación

**Instrucciones del sistema:** Ninguna.

**Uso:** Usada con modificaciones menores (Ajuste del método `_validar_movimiento` y del `if __name__ == "__main__"`).

**Archivo Final:** `backgammon/pygame/pygame_ui.py`

---

## 2025-10-21 — Corrección de jugador.py y checker.py
**Herramienta:** Claude 3.7 Sonnet (Anthropic)

**Prompt:**
Soluciona esto
[Se adjuntó código de jugador.py con trailing whitespace]

**Respuesta:**
La IA proporcionó el código corregido eliminando:
- Espacios en blanco al final de las líneas
- Agregó línea en blanco al final del archivo

**Instrucciones del sistema:** Ninguna.

**Uso:** Usada sin cambios.

**Archivo Final:** `backgammon/core/jugador.py`, `backgammon/core/checker.py`

---

## 2025-10-21 — Corrección de main.py (CLI)
**Herramienta:** Claude 3.7 Sonnet (Anthropic)

**Prompt:**
Ahora esto
[Se adjuntó main.py con múltiples errores de Pylint]

**Respuesta:**
La IA corrigió:
- Agregó docstring del módulo
- Agregó docstring a la función `main()`
- Separó declaraciones múltiples en líneas individuales
- Eliminó espacios en blanco trailing
- Agregó línea en blanco al final

**Instrucciones del sistema:** Ninguna.

**Uso:** Usada sin cambios.

**Archivo Final:** `main.py`

---

## 2025-10-21 — Corrección de tablero.py
**Herramienta:** Claude 3.7 Sonnet (Anthropic)

**Prompt:**
ahora esto para tablero.py y test.tablero.py
[Se adjuntaron ambos archivos con errores de Pylint]

**Respuesta:**
La IA corrigió ambos archivos:

**tablero.py:**
- Eliminó trailing whitespace
- Agregó línea en blanco al final

**test_tablero.py:**
- Agregó docstring del módulo
- Agregó docstrings a todas las clases de test
- Agregó docstrings a todos los métodos de test
- Separó declaraciones múltiples
- Corrigió indentación
- Dividió líneas largas

**Instrucciones del sistema:** Ninguna.

**Uso:** Usada sin cambios.

**Archivo Final:** `backgammon/core/tablero.py`, `backgammon/tests/test_tablero.py`

---

## 2025-10-21 — Corrección de juego.py
**Herramienta:** Claude 3.7 Sonnet (Anthropic)

**Prompt:**
Ahora esto
[Se adjuntó juego.py con múltiples errores de Pylint]

**Respuesta:**
La IA corrigió:
- Agregó docstring del módulo
- Eliminó import no usado (Jugador)
- Corrigió indentación (17 espacios → 16 espacios)
- Dividió líneas largas (>100 caracteres)
- Eliminó espacios en blanco trailing
- Corrigió paréntesis innecesarios en expresiones
- Agregó línea en blanco al final

**Instrucciones del sistema:** Ninguna.

**Uso:** Usada con modificaciones menores (Corrección manual de validación de índices).

**Archivo Final:** `backgammon/core/juego.py`

---

## 2025-10-21 — Corrección de dados.py
**Herramienta:** Claude 3.7 Sonnet (Anthropic)

**Prompt:**
Ahora esto
[Se adjuntó dados.py con import redundante]

**Respuesta:**
La IA corrigió:
- Eliminó `import random` redundante dentro del método `fijar_semilla`
- Eliminó trailing whitespace
- Agregó línea en blanco al final

**Instrucciones del sistema:** Ninguna.

**Uso:** Usada sin cambios.

**Archivo Final:** `backgammon/core/dados.py`

---

## 2025-10-21 — Corrección de CI workflow
**Herramienta:** Claude 3.7 Sonnet (Anthropic)

**Prompt:**
Este es el ultimo
[Se adjuntó ci.yml con error de SONAR_TOKEN]

**Respuesta:**
La IA corrigió:
- Agregó condicional `if: env.SONAR_TOKEN != ''` para SonarCloud
- Completó el script de generación de reportes
- Corrigió los valores de sonar.projectKey y sonar.sources
- Agregó más archivos al commit final

**Instrucciones del sistema:** Ninguna.

**Uso:** Usada con modificaciones (Ajuste de valores específicos del proyecto).

**Archivo Final:** `.github/workflows/ci.yml`

---

## 2025-10-23 — juego.py (Lógica de Aplicar Movimiento)
**Herramienta:** Gemini Advanced

**Prompt:**
Revisa mi método aplicar_movimiento y simplifica la lógica de consumo de dados para el Bearing Off, extrayendo la validación de dado mayor (over-bearing) a un bloque if/else final, después de verificar el movimiento normal y el reingreso.

**Respuesta:**
[Generó una estructura de aplicar_movimiento más limpia, basando el consumo en la variable distancia y los condicionales de hasta==PUNTOS.]

**Instrucciones del sistema:** Mantener la claridad y evitar la repetición de código para el consumo de dados.

**Uso:** Usada con modificaciones (Ajuste del consumo final de distancia).

**Archivo Final:** `backgammon/core/juego.py`

---

## 2025-10-24 — juego.py (Aplicación del Principio DIP/SRP)
**Herramienta:** Gemini Advanced

**Prompt:**
Necesito la clase Juego para coordinar el estado. Asegúrate de que los atributos principales (tablero, dados, jugadores) se inicialicen en el constructor para demostrar la Inversión de Dependencias (DIP) y se acceda a ellos mediante @property.

**Respuesta:**
[Generó el constructor inicial de Juego, incluyendo los atributos __tablero__, __dados__, y __jugadores__, y definió las propiedades correspondientes.]

**Instrucciones del sistema:** La clase debe ser el único punto de control del flujo principal.

**Uso:** Usada sin cambios.

**Archivo Final:** `backgammon/core/juego.py`

---

## 2025-10-25 — tablero.py (Lógica de Bloqueo)
**Herramienta:** Gemini Advanced

**Prompt:**
Escribe el método _bloqueado_por_oponente(jugador_id, punto) para Tablero. Debe verificar que, si hay fichas en el destino, el dueño de la primera ficha no sea jugador_id Y que la cantidad de fichas sea >= 2. La pila contiene objetos Checker.

**Respuesta:**
[Generó la lógica de validación con destino[0].owner_id y len(destino) >= 2.]

**Instrucciones del sistema:** El código debe ser eficiente y usar la propiedad owner_id de Checker.

**Uso:** Usada sin cambios.

**Archivo Final:** `backgammon/core/tablero.py`

---

## Resumen de Uso de IA en Desarrollo

**Total de prompts de desarrollo:** 26

**Distribución:**
- Estructura inicial y lógica core: 12 prompts
- Interfaz gráfica (Pygame): 3 prompts
- Correcciones de Pylint: 7 prompts
- CLI y configuración: 4 prompts

**Porcentaje de código generado por IA:** ~20%
- La lógica del juego fue desarrollada manualmente con ayuda de IA
- La IA se usó para correcciones de estilo, formato y refactorización

**Archivos modificados con ayuda de IA:**
- `backgammon/core/juego.py`
- `backgammon/core/tablero.py`
- `backgammon/core/jugador.py`
- `backgammon/core/checker.py`
- `backgammon/core/dados.py`
- `backgammon/pygame/pygame_ui.py`
- `backgammon/tests/test_tablero.py`
- `main.py`
- `.github/workflows/ci.yml`
- `Dockerfile`
- `.dockerignore`

## 2025-10-31 — Corrección Crítica: Dirección de Movimientos
**Herramienta:** Claude 3.7 Sonnet (Anthropic)

**Prompt:**
Arregla ese error. Dime si necesitas que te mande algun codigo para que lo puedas solucionar.
[Contexto: 17 tests fallando con error "el jugador debe moverse hacia adelante"]

**Respuesta:**
La IA identificó que la lógica de dirección estaba invertida en `_validar_movimiento`:
- Problema: J1 (impar) validaba `hasta >= desde` cuando debería ser `hasta <= desde`
- Problema: J2 (par) validaba `hasta <= desde` cuando debería ser `hasta >= desde`
- Corrección: J1 debe DECREMENTAR (23→0), J2 debe INCREMENTAR (0→23)
- También corrigió `es_ficha_mas_lejana` y `_validar_bearing_off`

**Instrucciones del sistema:** Ninguna.

**Uso:** Usada sin cambios.

**Archivo Final:** `backgammon/core/juego.py`

---

## 2025-10-31 — Implementación de Click en Barra Central
**Herramienta:** Claude 3.7 Sonnet (Anthropic)

**Prompt:**
LOS CIRCULOS CAPTURADOS SI SE MUESTRAN EN LA BARRA, PERO NO LOS PUEDO SACAR

**Respuesta:**
La IA implementó:
- Constante `BARRA_SELECCION = -1` para identificar selección de barra
- Actualización de `point_or_out_bar_from_xy` para detectar clicks en `bar_rect`
- Modificación de `dibujar_punto_seleccionado` para mostrar indicador en barra
- Actualización de `_manejar_click` para permitir seleccionar `BARRA_SELECCION`
- Modificación de `manejar_movimiento` para convertir `BARRA_SELECCION` a punto de entrada

**Instrucciones del sistema:** Ninguna.

**Uso:** Usada sin cambios.

**Archivo Final:** `backgammon/pygame/pygame_ui.py`

---

## 2025-10-31 — Corrección de puede_sacar_fichas
**Herramienta:** Claude 3.7 Sonnet (Anthropic)

**Prompt:**
AAAAAAA, CADA VEZ QUE TIRO DADOS CON BLANCAS ME DICE QUE NO HAY MOVIMIENTOS VALIDOS

**Respuesta:**
La IA identificó que `puede_sacar_fichas` en `tablero.py` tenía los rangos invertidos:
- J1 (impar): home en 0-5, debe revisar puntos 6-23 (antes revisaba 0-18)
- J2 (par): home en 18-23, debe revisar puntos 0-17 (antes revisaba 6-24)
- La inversión causaba que siempre fallara la validación de bearing off

**Instrucciones del sistema:** Ninguna.

**Uso:** Usada sin cambios.

**Archivo Final:** `backgammon/core/tablero.py`

---

## 2025-10-31 — Corrección de Dirección de Reingreso desde Barra
**Herramienta:** Claude 3.7 Sonnet (Anthropic)

**Prompt:**
Mismo problema, cada vez que tiro dados con blancas me dice que no hay movimientos disponibles y cambia de turno

**Respuesta:**
La IA corrigió la dirección de reingreso desde barra en tres funciones de `pygame_ui.py`:
- `dibujar_hints`: J1 incrementa desde 0 (0+3=3), J2 decrementa desde 23 (23-3=20)
- `manejar_evento_tirada`: Misma corrección para detección de movimientos válidos
- `_tiene_movimientos_validos`: Corrección de dirección en tablero vs barra

**Instrucciones del sistema:** Ninguna.

**Uso:** Usada sin cambios.

**Archivo Final:** `backgammon/pygame/pygame_ui.py`

---

## 2025-10-31 — Actualización de Tests de Bearing Off
**Herramienta:** Claude 3.7 Sonnet (Anthropic)

**Prompt:**
Arregla esto modificando los tests, no quiero que toques el resto
[Contexto: 6 tests de bearing off fallando]

**Respuesta:**
La IA corrigió los tests para reflejar la implementación correcta:
- `test_bearing_off_exacto_j1_consume_dado`: cambió punto 22 → 2
- `test_bearing_off_over_bearing_j1_consume_dado_mayor`: cambió punto 23 → 1
- `test_bearing_off_over_bearing_falla_si_hay_ficha_mas_lejana_j1`: cambió puntos 23,21 → 1,3
- `test_bearing_off_exacto_j2`: cambió punto 2 → 21
- `test_es_ficha_mas_lejana_j1_con_fichas_mas_cerca`: cambió puntos 23,20 → 1,4
- `test_es_ficha_mas_lejana_j2_con_fichas_mas_lejos`: cambió puntos 0,3 → 23,20

**Instrucciones del sistema:** Ninguna.

**Uso:** Usada con modificaciones (Ajuste del último test para manejar IDs dinámicos).

**Archivo Final:** `backgammon/tests/test_juego.py`

---

## 2025-10-31 — Corrección Final del Test de Over-Bearing
**Herramienta:** Claude 3.7 Sonnet (Anthropic)

**Prompt:**
[Último test fallando]

**Respuesta:**
La IA modificó `test_bearing_off_over_bearing_falla_si_hay_ficha_mas_lejana_j1` para:
- Detectar si el jugador actual es J1 o J2 dinámicamente
- Usar posiciones correctas según el jugador (J1: 1,3 o J2: 22,20)
- Resolver el problema de IDs de jugador no determinísticos en tests

**Instrucciones del sistema:** Ninguna.

**Uso:** Usada sin cambios.

**Archivo Final:** `backgammon/tests/test_juego.py`

---

## 2025-10-31 — Finalización del CHANGELOG.md
**Herramienta:** Claude 3.7 Sonnet (Anthropic)

**Prompt:**
Excelente ahora termina el changelog

**Respuesta:**
La IA completó el changelog agregando la versión 0.6.0 con:
- Added: Selección visual de barra, indicadores mejorados, numeración completa
- Changed: Corrección de dirección de movimientos, refactorización de validaciones
- Fixed: 6 bugs críticos corregidos (dirección, bearing off, reingreso, tests)
- Removed: Lógica obsoleta de detección de punto 0

**Instrucciones del sistema:** Ninguna.

**Uso:** Usada sin cambios.

**Archivo Final:** `CHANGELOG.md`

---

## 2025-10-31 — Actualización de Archivos de Prompts
**Herramienta:** Claude 3.7 Sonnet (Anthropic)

**Prompt:**
Ahora agrega algunos prompts aca y terminamos con el proyecto

**Respuesta:**
La IA generó la documentación de todos los prompts de la sesión de depuración final, incluyendo:
- Corrección de lógica de dirección
- Implementación de click en barra
- Corrección de validaciones de bearing off
- Actualización de tests
- Finalización de changelog

**Instrucciones del sistema:** Ninguna.

**Uso:** Usada sin cambios.

**Archivo Final:** `prompts/prompts-desarrollo.md`

---

## Resumen Final de Desarrollo

**Total de prompts en sesión final:** 7

**Bugs críticos corregidos:**
1. Dirección de movimientos invertida en core
2. Dirección de reingreso invertida en UI
3. Validación de home boards incorrecta
4. Detección de ficha más lejana incorrecta
5. Tests con posiciones erróneas
6. Click en barra no funcional

**Resultado:**
- ✅ 162/162 tests pasando (100%)
- ✅ Interfaz gráfica completamente funcional
- ✅ Reingreso desde barra implementado
- ✅ Bearing off funcionando correctamente
- ✅ Documentación completa