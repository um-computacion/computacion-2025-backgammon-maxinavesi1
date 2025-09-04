from backgammon.core.tablero import Tablero
from backgammon.core.dados import Dados
from backgammon.core.jugador import Jugador

class Juego:
    """Coordina el estado del juego y el turno actual."""

    def __init__(self, jugador1, jugador2, indice_inicial=0):
        """Crea un juego con dos jugadores y un tablero nuevo."""
        self.__tablero__ = Tablero()
        self.__jugadores__ = [jugador1, jugador2]
        self.__dados__ = Dados()
        self.__indice_jugador_actual__ = 0 if indice_inicial not in (0, 1) else indice_inicial
        self.__barra__ = {jugador1.id: 0, jugador2.id: 0}

    @property
    def jugador_actual(self):
        """Devuelve el jugador que tiene el turno."""
        return self.__jugadores__[self.__indice_jugador_actual__]

    def tirar(self):
        """Realiza una tirada de dados y la devuelve."""
    d1, d2, movimientos = self.__dados__.tirar()
    return d1, d2  


    def cambiar_turno(self):
        """Alterna el turno entre 0 y 1."""
        self.__indice_jugador_actual__ = 1 - self.__indice_jugador_actual__

    def termino(self):
        """Indica si el juego terminó (hay ganador)."""
        return self.__tablero__.hay_ganador()

    def ganador(self):
        """Devuelve el Jugador ganador o None si no hay."""
        w = self.__tablero__.id_ganador()
        if w is None:
            return None
        for j in self.__jugadores__:
            if j.id == w:
                return j
        return None

