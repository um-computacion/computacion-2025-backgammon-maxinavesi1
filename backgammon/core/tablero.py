PUNTOS = 24
FICHAS_POR_JUGADOR = 15


class Tablero:


    def __init__(self):
        self.__puntos__ = [[] for _ in range(PUNTOS)]  
        self.__salidas__ = {}  
        self.__barra__ = {}    
        self.preparar_posicion_inicial()

    def preparar_posicion_inicial(self):
       
        pass

    def validar_indice_punto(self, i):
        if not 0 <= i < PUNTOS:
            raise ValueError("índice de punto inválido: " + str(i))

    def punto(self, i):
        self.validar_indice_punto(i)
        return self.__puntos__[i]

    def hay_ganador(self):
        for cantidad in self.__salidas__.values():
            if cantidad == FICHAS_POR_JUGADOR:
                return True
        return False

    def id_ganador(self):
        for pid, cantidad in self.__salidas__.items():
            if cantidad == FICHAS_POR_JUGADOR:
                return pid
        return None