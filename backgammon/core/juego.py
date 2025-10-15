from backgammon.core.tablero import Tablero, PUNTOS
from backgammon.core.dados import Dados
from backgammon.core.jugador import Jugador 

class Juego:
    """Coordina el estado del juego, los dados y el turno actual."""

    def __setattr__(self, name, value):
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
        self.__ultimo_error__ = None

        self._sync_aliases()

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
    
    @property
    def jugadores(self):
        return self.__jugadores__

    def ultimo_error(self):
        return self.__ultimo_error__

    def _set_error(self, msg=None):
        self.__ultimo_error__ = msg

    def usar_semilla(self, semilla: int):
        self.__dados__.fijar_semilla(semilla)

    def tirar(self):
        d1, d2, movimientos = self.__dados__.tirar()
        self.__movs_restantes__ = list(movimientos)
        self._sync_aliases()
        if self.__estado__ == "inicial":
            self.__estado__ = "en_curso"
        self._set_error(None)
        self._actualizar_estado()
        return d1, d2, movimientos

    def movimientos_disponibles(self):
        return list(self.__movs_restantes__)

    def _validar_movimiento(self, desde: int, hasta: int) -> tuple[bool, int]:
        pid = self.jugador_actual.id

        if not (0 <= desde < PUNTOS) or not (0 <= hasta < PUNTOS):
            self._set_error(f"índices fuera de rango (0..{PUNTOS-1})")
            return False, 0

        entrada = self._entrada_para(pid)
        if self._en_barra(pid) and desde != entrada:
            self._set_error("tenés fichas en la barra: reingresá primero")
            return False, 0

        distancia = abs(hasta - desde if not self._en_barra(pid) else hasta - entrada)
        distancia = abs(distancia)

        if distancia not in self.__movs_restantes__:
            self._set_error(f"la distancia {distancia} no está en movs {self.__movs_restantes__}")
            return False, distancia

        if not self._en_barra(pid):
            if pid not in self.__tablero__.punto(desde):
                self._set_error("no hay ficha del jugador en el origen")
                return False, distancia
            if self.__tablero__._bloqueado_por_oponente(pid, hasta):
                self._set_error("destino bloqueado por el oponente")
                return False, distancia

        self._set_error(None)
        return True, distancia


    def aplicar_movimiento(self, desde: int, hasta: int) -> bool:
        ok_pre, distancia = self._validar_movimiento(desde, hasta)
        if not ok_pre:
            return False

        pid = self.jugador_actual.id
        if self._en_barra(pid):
            ok = self.__tablero__.reingresar_desde_barra(pid, hasta)
        else:
            ok = self.__tablero__.mover_ficha_seguro(pid, desde, hasta)

        if ok:
            self.__movs_restantes__.remove(distancia)
            self._set_error(None)
        else:
            self._set_error("movimiento inválido")
        return ok


    def mover_ficha(self, desde: int, hasta: int) -> bool:
        ok_pre, distancia = self._validar_movimiento(desde, hasta)
        if not ok_pre:
            return False

        pid = self.jugador_actual.id
        if self._en_barra(pid):
            ok = self.__tablero__.reingresar_desde_barra(pid, hasta)
        else:
            ok = self.__tablero__.mover_ficha_seguro(pid, desde, hasta)

        if not ok:
            self._set_error("movimiento inválido")
            return False

        self.__movs_restantes__.remove(distancia)
        self._set_error(None)
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
        self._set_error(None if ok else "no se pudo colocar ficha")
        self._actualizar_estado()
        return ok

    def cambiar_turno(self):
        self.__indice_jugador_actual__ = 1 - self.__indice_jugador_actual__
        self.__movs_restantes__.clear()
        self._set_error(None)
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
        self._set_error(None)
        self._actualizar_estado()

    def _actualizar_estado(self):
        if self.__tablero__.hay_ganador():
            self.__estado__ = "terminado"
        else:
            if self.__movs_restantes__:
                self.__estado__ = "en_curso"
    
    def _entrada_para(self, pid: int) -> int:
        j1_id = self.__jugadores__[0].id
        return 0 if pid == j1_id else 23

    def _en_barra(self, pid: int) -> bool:
        return self.__tablero__.fichas_en_barra(pid) > 0

