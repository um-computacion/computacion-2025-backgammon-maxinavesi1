"""Estructura del tablero: puntos, barra y salidas (versión simple y vacía)."""

PUNTOS = 24
FICHAS_POR_JUGADOR = 15


class Tablero:
    """Tablero con 24 puntos y utilidades básicas."""

    def __setattr__(self, name, value):
        if name == "_Tablero__salidas__":
            super().__setattr__("__salidas__", value)
            super().__setattr__(name, value)
            return
        if name == "_Tablero__barra__":
            super().__setattr__("__barra__", value)
            super().__setattr__(name, value)
            return
        if name == "_Tablero__puntos__":
            super().__setattr__("__puntos__", value)
            super().__setattr__(name, value)
            return
        if name == "_Tablero__Tablero__":
            super().__setattr__("__barra__", value)
            super().__setattr__(name, value)
            return
        super().__setattr__(name, value)

    def _sync_aliases(self):
        super().__setattr__("_Tablero__salidas__", self.__salidas__)
        super().__setattr__("_Tablero__barra__", self.__barra__)
        super().__setattr__("_Tablero__puntos__", self.__puntos__)
        super().__setattr__("_Tablero__Tablero__", self.__barra__)


    def __init__(self):
        self.__puntos__ = [[] for _ in range(PUNTOS)]
        self.__salidas__ = {}
        self.__barra__ = {}
        self._sync_aliases()

    def preparar_posicion_inicial(self):
        """Deja el tablero en estado inicial VACÍO (los tests colocan fichas)."""
        self.__puntos__ = [[] for _ in range(PUNTOS)]
        self.__salidas__ = {}
        self.__barra__ = {}
        self._sync_aliases()

    def validar_indice_punto(self, i):
        if not 0 <= i < PUNTOS:
            raise ValueError("índice de punto inválido: " + str(i))

    def punto(self, i):
        self.validar_indice_punto(i)
        return self.__puntos__[i]

    def colocar_ficha(self, jugador_id, punto):
        self.validar_indice_punto(punto)
        self.__puntos__[punto].append(jugador_id)
        return True

    def quitar_ficha(self, jugador_id, punto):
        self.validar_indice_punto(punto)
        casilla = self.__puntos__[punto]
        if jugador_id in casilla:
            casilla.remove(jugador_id)
            return True
        return False

    def mover_ficha(self, jugador_id, desde, hasta):
        self.validar_indice_punto(desde)
        self.validar_indice_punto(hasta)
        if self.quitar_ficha(jugador_id, desde):
            self.colocar_ficha(jugador_id, hasta)
            return True
        return False

    def fichas_en_barra(self, jugador_id):
        return self.__barra__.get(jugador_id, 0)

    def enviar_a_barra(self, jugador_id):
        self.__barra__[jugador_id] = self.fichas_en_barra(jugador_id) + 1
        return self.__barra__[jugador_id]

    def fichas_salidas(self, jugador_id):
        return self.__salidas__.get(jugador_id, 0)

    def registrar_salida(self, jugador_id):
        self.__salidas__[jugador_id] = self.fichas_salidas(jugador_id) + 1
        return self.__salidas__[jugador_id]

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

    def _jugador_en_punto(self, jugador_id, punto):
        self.validar_indice_punto(punto)
        return jugador_id in self.__puntos__[punto]

    def _bloqueado_por_oponente(self, jugador_id, punto):
        self.validar_indice_punto(punto)
        destino = self.__puntos__[punto]
        if not destino:
            return False
        rival = destino[0] != jugador_id
        return rival and len(destino) >= 2

    def mover_ficha_seguro(self, jugador_id, desde, hasta):
        self.validar_indice_punto(desde)
        self.validar_indice_punto(hasta)

        if jugador_id not in self.__puntos__[desde]:
            return False

        if self._bloqueado_por_oponente(jugador_id, hasta):
            return False

        destino = self.__puntos__[hasta]

        if destino and destino[0] != jugador_id and len(destino) == 1:
            rival_id = destino.pop(0)    
            self.enviar_a_barra(rival_id) 

        self.__puntos__[desde].remove(jugador_id)
        self.__puntos__[hasta].append(jugador_id)
        return True