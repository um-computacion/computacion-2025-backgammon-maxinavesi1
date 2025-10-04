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


    def usar_semilla(self, semilla: int):
        """Fija la semilla de los dados (tiradas reproducibles)."""
        self.__dados__.fijar_semilla(semilla)

    def tirar(self):
        """Realiza una tirada de dados y la guarda como movimientos restantes."""
        d1, d2, movimientos = self.__dados__.tirar()
        self.__movs_restantes__ = list(movimientos)
        if self.__estado__ == "inicial":
            self.__estado__ = "en_curso"
        self._actualizar_estado()
        return d1, d2, movimientos

    def movimientos_disponibles(self):
        """Devuelve una copia de los movimientos que quedan por usar."""
        return list(self.__movs_restantes__)

    def aplicar_movimiento(self, desde: int, hasta: int) -> bool:
        """Mueve una ficha del jugador actual si la distancia está disponible.
        No cambia el turno; sólo consume la distancia si el movimiento ocurre.
        """
        distancia = abs(hasta - desde)
        if distancia not in self.__movs_restantes__:
            return False

        ok = self.__tablero__.mover_ficha(self.jugador_actual.id, desde, hasta)
        if ok:
            self.__movs_restantes__.remove(distancia)
        return ok

    def mover_ficha(self, desde: int, hasta: int) -> bool:
        """Mueve una ficha si la distancia está en los movimientos restantes.
        Consume la distancia y, si no quedan, cambia el turno.
        """
        pid = self.jugador_actual.id
        distancia = abs(hasta - desde)
        if distancia not in self.__movs_restantes__:
            return False

        ok = self.__tablero__.mover_ficha(pid, desde, hasta)
        if not ok:
            return False

        self.__movs_restantes__.remove(distancia)
        if not self.__movs_restantes__:
            self.cambiar_turno()
        else:
            self._actualizar_estado()
        return True

    def colocar_ficha_en(self, punto: int) -> bool:
        """Coloca una ficha del jugador actual en 'punto'."""
        pid = self.jugador_actual.id
        ok = self.__tablero__.colocar_ficha(pid, punto)
        if ok and self.__estado__ == "inicial":
            self.__estado__ = "en_curso"
        self._actualizar_estado()
        return ok

    def cambiar_turno(self):
        """Alterna el turno entre 0 y 1 y limpia movimientos pendientes."""
        self.__indice_jugador_actual__ = 1 - self.__indice_jugador_actual__
        self.__movs_restantes__.clear()
        self._actualizar_estado()

    def termino(self) -> bool:
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

    def estado_dict(self) -> dict:
        """Devuelve un snapshot del juego en un diccionario simple."""
        puntos = [self.__tablero__.punto(i)[:] for i in range(PUNTOS)]
        barra = {pid: self.__tablero__.fichas_en_barra(pid) for pid in self.__barra__.keys()}
        salidas = {pid: self.__tablero__.fichas_salidas(pid) for pid in self.__barra__.keys()}
        return {
            "estado": self.__estado__,
            "jugador_actual": self.jugador_actual.nombre,
            "jugador_actual_id": self.jugador_actual.id,
            "movs_restantes": self.__movs_restantes__[:],
            "puntos": puntos,
            "barra": barra,
            "salidas": salidas,
        }

    def resumen_estado(self) -> str:
        """String corto para imprimir en CLI o logs."""
        e = self.estado_dict()
        return (f"estado={e['estado']} | turno={e['jugador_actual']} "
                f"(id {e['jugador_actual_id']}) | movs={e['movs_restantes']}")

    def reiniciar(self):
        """Pone tablero limpio, sin movs y turno del primer jugador."""
        self.__tablero__.preparar_posicion_inicial()
        self.__movs_restantes__.clear()
        self.__indice_jugador_actual__ = 0
        self.__estado__ = "inicial"

    def _actualizar_estado(self):
        """Actualiza 'terminado' si hay ganador; si no, 'en_curso' cuando corresponda."""
        if self.__tablero__.hay_ganador():
            self.__estado__ = "terminado"
        else:
            if self.__movs_restantes__ and self.__estado__ != "inicial":
                self.__estado__ = "en_curso"
