"""Estructura del tablero: puntos, barra y salidas."""

PUNTOS = 24
FICHAS_POR_JUGADOR = 15

class Tablero:
    """Tablero con 24 puntos y utilidades básicas."""

    def __init__(self):
        """Crea la estructura vacía del tablero."""
        self.__puntos__ = [[] for _ in range(PUNTOS)]
        self.__salidas__ = {}
        self.__barra__ = {}
        self.preparar_posicion_inicial()

    def preparar_posicion_inicial(self):
        """Deja preparada la posición inicial (pendiente de completar)."""
        pass

    def validar_indice_punto(self, i):
        """Valida que i esté en [0, PUNTOS). Lanza ValueError si no."""
        if not 0 <= i < PUNTOS:
            raise ValueError("índice de punto inválido: " + str(i))

    def punto(self, i):
        """Devuelve la lista de fichas del punto i."""
        self.validar_indice_punto(i)
        return self.__puntos__[i]

    def hay_ganador(self):
        """Indica si algún jugador sacó todas sus fichas."""
        for cantidad in self.__salidas__.values():
            if cantidad == FICHAS_POR_JUGADOR:
                return True
        return False

    def id_ganador(self):
        """Devuelve el id del jugador ganador o None."""
        for pid, cantidad in self.__salidas__.items():
            if cantidad == FICHAS_POR_JUGADOR:
                return pid
        return None
