"""Coordinación del juego: tablero, dados, turno y estado simple."""

from backgammon.core.tablero import Tablero, PUNTOS
from backgammon.core.dados import Dados
from backgammon.core.jugador import Jugador


class Juego:
    """Coordina el estado del juego, los dados y el turno actual."""

    def __init__(self, jugador1, jugador2, indice_inicial=0):
        """Crea un juego con dos jugadores y un tablero nuevo."""
        self.__tablero__ = Tablero()
        self.__jugadores__ = [jugador1, jugador2]
        self.__dados__ = Dados()
        self.__indice_jugador_actual__ = 0 if indice_inicial not in (0, 1) else indice_inicial

        self.__barra__ = {jugador1.id: 0, jugador2.id: 0}

        self.__estado__ = "inicial"
        self.__movs_restantes__ = []

        self.__ultimo_error__ = ""

    @property
    def tablero(self):
        """Acceso de solo lectura al tablero (para UI/testing)."""
        return self.__tablero__

    @property
    def estado(self):
        """Devuelve el estado textual del juego."""
        return self.__estado__

    @property
    def jugador_actual(self):
        """Devuelve el jugador que tiene el turno."""
        return self.__jugadores__[self.__indice_jugador_actual__]

    def ultimo_error(self) -> str:
        """Último mensaje de error producido por una operación inválida."""
        return self.__ultimo_error__

    def _set_error(self, msg: str) -> None:
        self.__ultimo_error__ = msg


    def usar_semilla(self, semilla: int):
        """Fija la semilla de los dados (tiradas reproducibles)."""
        self.__dados__.fijar_semilla(semilla)

    def tirar(self):
        """Realiza una tirada de dados y la guarda como movimientos restantes."""
        d1, d2, movimientos = self.__dados__.tirar()
        self.__movs_restantes__ = list(movimientos)
        if self.__estado__ == "inicial":
            self.__estado__ = "en_curso"
        self._set_error("")  
        self._actualizar_estado()
        return d1, d2, movimientos

    def movimientos_disponibles(self):
        """Devuelve una copia de los movimientos que quedan por usar."""
        return list(self.__movs_restantes__)

    def aplicar_movimiento(self, desde: int, hasta: int) -> bool:
        """(Compat) Mueve una ficha si la distancia está disponible.
        No cambia el turno; sólo consume la distancia si el movimiento ocurre.
        """
        distancia = abs(hasta - desde)
        if distancia not in self.__movs_restantes__:
            return False

        ok = self.__tablero__.mover_ficha(self.jugador_actual.id, desde, hasta)
        if ok:
            self.__movs_restantes__.remove(distancia)
        return ok