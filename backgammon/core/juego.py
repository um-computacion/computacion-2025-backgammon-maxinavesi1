# backgammon/core/juego.py
from backgammon.core.tablero import Tablero, PUNTOS
from backgammon.core.dados import Dados
from backgammon.core.jugador import Jugador  # noqa: F401  (lo usan tests)

class Juego:
    """Coordina el estado del juego, los dados y el turno actual."""

    # ---- PUENTE con los nombres que usan los tests (name-mangling) ----
    def __setattr__(self, name, value):
        # Si los tests asignan directamente al alias, reflejar en el real
        if name == "_Juego__movs_restantes__":
            super().__setattr__("__movs_restantes__", value)
            super().__setattr__(name, value)
            return
        if name == "_Juego__tablero__":
            super().__setattr__("__tablero__", value)
            super().__setattr__(name, value)
            return
        super().__setattr__(name, value)

    def __init__(self, jugador1, jugador2, indice_inicial=0):
        self.__tablero__ = Tablero()
        self.__jugadores__ = [jugador1, jugador2]
        self.__dados__ = Dados()
        self.__indice_jugador_actual__ = 0 if indice_inicial not in (0, 1) else indice_inicial
        self.__barra__ = {jugador1.id: 0, jugador2.id: 0}

        self.__estado__ = "inicial"
        self.__movs_restantes__ = []

        self._sync_aliases()

    # Mantener alias consistentes (para lectura desde los tests)
    def _sync_aliases(self):
        super().__setattr__("_Juego__tablero__", self.__tablero__)
        super().__setattr__("_Juego__movs_restantes__", self.__movs_restantes__)

    @property
    def tablero(self):
        return self.__tablero__

    @property
    def estado(self):
        return self.__estado__

    @property
    def jugador_actual(self):
        return self.__jugadores__[self.__indice_jugador_actual__]

    def usar_semilla(self, semilla: int):
        self.__dados__.fijar_semilla(semilla)

    def tirar(self):
        d1, d2, movimientos = self.__dados__.tirar()
        # ¡OJO! Reasignamos la lista -> actualizar alias
        self.__movs_restantes__ = list(movimientos)
        self._sync_aliases()
        if self.__estado__ == "inicial":
            self.__estado__ = "en_curso"
        self._actualizar_estado()
        return d1, d2, movimientos

    def movimientos_disponibles(self):
        return list(self.__movs_restantes__)

    def aplicar_movimiento(self, desde: int, hasta: int) -> bool:
        distancia = abs(hasta - desde)
        if distancia not in self.__movs_restantes__:
            return False
        ok = self.__tablero__.mover_ficha(self.jugador_actual.id, desde, hasta)
        if ok:
            self.__movs_restantes__.remove(distancia)
            # NO cambia el turno: los tests esperan que solo consuma
        return ok

    def mover_ficha(self, desde: int, hasta: int) -> bool:
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
        pid = self.jugador_actual.id
        ok = self.__tablero__.colocar_ficha(pid, punto)
        if ok and self.__estado__ == "inicial":
            self.__estado__ = "en_curso"
        self._actualizar_estado()
        return ok

    def cambiar_turno(self):
        self.__indice_jugador_actual__ = 1 - self.__indice_jugador_actual__
        self.__movs_restantes__.clear()
        # no reasignamos la lista -> alias sigue válido
        self._actualizar_estado()

    def termino(self) -> bool:
        return self.__tablero__.hay_ganador()

    def ganador(self):
        w = self.__tablero__.id_ganador()
        if w is None:
            return None
        for j in self.__jugadores__:
            if j.id == w:
                return j
        return None

    def estado_dict(self) -> dict:
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
        e = self.estado_dict()
        return (f"estado={e['estado']} | turno={e['jugador_actual']} "
                f"(id {e['jugador_actual_id']}) | movs={e['movs_restantes']}")

    def reiniciar(self):
        self.__tablero__.preparar_posicion_inicial()
        self.__movs_restantes__.clear()
        self.__indice_jugador_actual__ = 0
        self.__estado__ = "inicial"
        self._actualizar_estado()

    def _actualizar_estado(self):
        if self.__tablero__.hay_ganador():
            self.__estado__ = "terminado"
        else:
            if self.__movs_restantes__:
                self.__estado__ = "en_curso"
