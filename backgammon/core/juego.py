from backgammon.core.tablero import Tablero
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
        self.__movs_restantes__ = []

    @property
    def jugador_actual(self):
        """Devuelve el jugador que tiene el turno."""
        return self.__jugadores__[self.__indice_jugador_actual__]


    def usar_semilla(self, semilla):
        """Fija la semilla de los dados (tiradas reproducibles)."""
        self.__dados__.fijar_semilla(semilla)

    def tirar(self):
        """Realiza una tirada de dados y guarda los movimientos posibles."""
        d1, d2, movimientos = self.__dados__.tirar()
        self.__movs_restantes__ = list(movimientos)  
        return d1, d2, movimientos

    def movimientos_disponibles(self):
        """Devuelve una copia de los movimientos que quedan por usar."""
        return list(self.__movs_restantes__)


    def aplicar_movimiento(self, desde, hasta):
        """Mueve una ficha del jugador actual si la distancia está disponible. """

        distancia = abs(hasta - desde)
        if distancia not in self.__movs_restantes__:
            return False

        ok = self.__tablero__.mover_ficha(self.jugador_actual.id, desde, hasta)
        if ok:
            
            self.__movs_restantes__.remove(distancia)
        return ok