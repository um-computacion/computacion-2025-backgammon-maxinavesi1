## 2025-08-28 — tablero.py (versión inicial)

 herramienta usada: ChatGPT (GPT-5 Thinking)

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
        self.__salidas__ = {}  # fichas que salieron por jugador
        self.__barra__ = {}    # fichas en la barra por jugador
        self.preparar_posicion_inicial()

    def preparar_posicion_inicial(self):
        # TODO: más adelante poner la posición inicial real
        pass

    def validar_indice_punto(self, i):
        if not 0 <= i < PUNTOS:
            raise ValueError("índice de punto inválido: " + str(i))

    def punto(self, i):
        self.validar_indice_punto(i)
        return self.__puntos__[i]