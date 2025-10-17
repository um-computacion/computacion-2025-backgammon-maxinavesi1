"""Estructura del tablero: puntos, barra y salidas (versión simple y vacía)."""

PUNTOS = 24
FICHAS_POR_JUGADOR = 15
HOME_BOARD_J1 = range(18, 24) 
HOME_BOARD_J2 = range(0, 6)   


class Tablero:
    """Tablero con 24 puntos, barra y utilidades de movimiento y fin de juego."""



    def __init__(self):
        """Inicializa un tablero vacío."""
        self.__puntos__ = [[] for _ in range(PUNTOS)]
        self.__salidas__ = {}
        self.__barra__ = {}

    def preparar_posicion_inicial(self):
        """Deja el tablero en estado inicial VACÍO (los tests colocan fichas)."""
        self.__puntos__ = [[] for _ in range(PUNTOS)]
        self.__salidas__ = {}
        self.__barra__ = {}

    def validar_indice_punto(self, i):
        """Valida si el índice de punto está dentro del rango 0..23."""
        if not 0 <= i < PUNTOS:
            raise ValueError("índice de punto inválido: " + str(i))

    def punto(self, i):
        """Devuelve la lista de fichas en un punto del tablero."""
        self.validar_indice_punto(i)
        return self.__puntos__[i]

    def colocar_ficha(self, jugador_id, punto):
        """Coloca una ficha de un jugador en un punto."""
        self.validar_indice_punto(punto)
        self.__puntos__[punto].append(jugador_id)
        return True

    def quitar_ficha(self, jugador_id, punto):
        """Quita una ficha de un jugador de un punto."""
        self.validar_indice_punto(punto)
        casilla = self.__puntos__[punto]
        if jugador_id in casilla:
            casilla.remove(jugador_id)
            return True
        return False

    def mover_ficha(self, jugador_id, desde, hasta):
        """Mueve una ficha SIN validación de bloqueo ni de hit. Usar mover_ficha_seguro."""
        self.validar_indice_punto(desde)
        self.validar_indice_punto(hasta)
        if self.quitar_ficha(jugador_id, desde):
            self.colocar_ficha(jugador_id, hasta)
            return True
        return False

    def fichas_en_barra(self, jugador_id):
        """Devuelve el número de fichas del jugador en la barra."""
        return self.__barra__.get(jugador_id, 0)

    def enviar_a_barra(self, jugador_id):
        """Incrementa el contador de fichas en la barra para un jugador."""
        self.__barra__[jugador_id] = self.fichas_en_barra(jugador_id) + 1
        return self.__barra__[jugador_id]

    def fichas_salidas(self, jugador_id):
        """Devuelve el número de fichas que el jugador ha sacado."""
        return self.__salidas__.get(jugador_id, 0)

    def registrar_salida(self, jugador_id):
        """Incrementa el contador de fichas fuera del tablero (Bearing Off)."""
        self.__salidas__[jugador_id] = self.fichas_salidas(jugador_id) + 1
        return self.__salidas__[jugador_id]

    def hay_ganador(self):
        """Retorna True si algún jugador ha sacado todas sus fichas."""
        for cantidad in self.__salidas__.values():
            if cantidad == FICHAS_POR_JUGADOR:
                return True
        return False

    def id_ganador(self):
        """Retorna el ID del jugador que ha sacado todas sus fichas, o None."""
        for pid, cantidad in self.__salidas__.items():
            if cantidad == FICHAS_POR_JUGADOR:
                return pid
        return None

    def _jugador_en_punto(self, jugador_id, punto):
        """Verifica si el jugador tiene fichas en el punto."""
        self.validar_indice_punto(punto)
        return jugador_id in self.__puntos__[punto]

    def _bloqueado_por_oponente(self, jugador_id, punto):
        """Verifica si el punto está bloqueado (dos o más fichas rivales)."""
        self.validar_indice_punto(punto)
        destino = self.__puntos__[punto]
        if not destino:
            return False
        rival = destino[0] != jugador_id
        return rival and len(destino) >= 2

    def mover_ficha_seguro(self, jugador_id, desde, hasta):
        """Mueve una ficha, aplicando reglas de hit/bloqueo, sin reingreso de barra."""
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
    
    def reingresar_desde_barra(self, jugador_id: int, hasta: int) -> bool:
        """Si el jugador tiene fichas en barra, intenta reingresar una ficha a 'hasta'."""
        self.validar_indice_punto(hasta)
        if self.fichas_en_barra(jugador_id) <= 0:
            return False

        if self._bloqueado_por_oponente(jugador_id, hasta):
            return False

        destino = self.__puntos__[hasta]

        if destino and destino[0] != jugador_id and len(destino) == 1:
            rival_id = destino.pop(0)
            self.enviar_a_barra(rival_id)

        self.__barra__[jugador_id] = self.fichas_en_barra(jugador_id) - 1
        self.__puntos__[hasta].append(jugador_id)
        return True

    def puede_sacar_fichas(self, jugador_id: int) -> bool:
        """
        Verifica si el jugador tiene todas sus fichas restantes en su home board """
        fichas_fuera_home_board = 0

        if jugador_id % 2 != 0: 
            home_board = HOME_BOARD_J1
            puntos_a_revisar = range(0, 18) 
        else: 
            home_board = HOME_BOARD_J2
            puntos_a_revisar = range(6, 24)

        if self.fichas_en_barra(jugador_id) > 0:
            return False

        for i in puntos_a_revisar:
            if jugador_id in self.__puntos__[i]:
                fichas_fuera_home_board += 1
                return False 

        return True

    def sacar_ficha(self, jugador_id: int, desde: int) -> bool:
        """Intenta sacar una ficha (bearing off) desde 'desde'."""
        if not self.puede_sacar_fichas(jugador_id):
            return False

        if jugador_id not in self.punto(desde):
            return False

        if self.quitar_ficha(jugador_id, desde):
            self.registrar_salida(jugador_id)
            return True
            
        return False