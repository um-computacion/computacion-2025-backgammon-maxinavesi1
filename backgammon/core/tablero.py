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
        
    def colocar_ficha(self, jugador_id, punto):
        """Pone una ficha del jugador en el punto dado. Devuelve True."""
        self.validar_indice_punto(punto)
        self.__puntos__[punto].append(jugador_id)
        return True

    def quitar_ficha(self, jugador_id, punto):
        """Saca una ficha del jugador de ese punto. Devuelve True si pudo."""
        self.validar_indice_punto(punto)
        casilla = self.__puntos__[punto]
        if jugador_id in casilla:
            casilla.remove(jugador_id)  
            return True
        return False

    def mover_ficha(self, jugador_id, desde, hasta):
        """Mueve una ficha del jugador desde -> hasta. True si se pudo."""
        self.validar_indice_punto(desde)
        self.validar_indice_punto(hasta)
        if self.quitar_ficha(jugador_id, desde):
            self.colocar_ficha(jugador_id, hasta)
            return True
        return False
    
    def fichas_en_barra(self, jugador_id):
        """Cantidad de fichas del jugador en la barra."""
        return self.__barra__.get(jugador_id, 0)

    def enviar_a_barra(self, jugador_id):
        """Suma 1 ficha a la barra del jugador."""
        self.__barra__[jugador_id] = self.fichas_en_barra(jugador_id) + 1
        return self.__barra__[jugador_id]

    def fichas_salidas(self, jugador_id):
        """Cantidad de fichas que ya salieron del tablero."""
        return self.__salidas__.get(jugador_id, 0)

    def registrar_salida(self, jugador_id):
        """Suma 1 ficha a las salidas del jugador."""
        self.__salidas__[jugador_id] = self.fichas_salidas(jugador_id) + 1
        return self.__salidas__[jugador_id]