from backgammon.core.tablero import Tablero
from backgammon.core.dados import Dados
from backgammon.core.jugador import Jugador

class Juego:
    def __init__(self, jugador1, jugador2, indice_inicial=0):
        self.__tablero__ = Tablero()
        self.__jugadores__ = [jugador1, jugador2]
        self.__dados__ = Dados()
        
        self.__indice_jugador_actual__ = 0 if indice_inicial not in (0, 1) else indice_inicial
        self.__barra__ = {jugador1.id: 0, jugador2.id: 0}

    @property
    def jugador_actual(self):
        return self.__jugadores__[self.__indice_jugador_actual__]

    def tirar(self):
        
        return self.__dados__.tirar()

    def cambiar_turno(self):
        
        self.__indice_jugador_actual__ = 1 - self.__indice_jugador_actual__

    def termino(self):
        return self.__tablero__.hay_ganador()

    def ganador(self):
        w = self.__tablero__.id_ganador()
        if w is None:
            return None
        for j in self.__jugadores__:
            if j.id == w:
                return j
        return None
