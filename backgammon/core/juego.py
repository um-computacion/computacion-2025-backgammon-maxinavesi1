from backgammon.core.tablero import Tablero, PUNTOS
from backgammon.core.dados import Dados
from backgammon.core.jugador import Jugador 

class Juego:
    """Coordina el estado del juego, los dados y el turno actual."""

    def __init__(self, jugador1, jugador2, indice_inicial=0):
        """Inicializa el juego con 2 jugadores."""
        self.__tablero__ = Tablero()
        self.__jugadores__ = [jugador1, jugador2]
        self.__dados__ = Dados()
        self.__indice_jugador_actual__ = 0 if indice_inicial not in (0, 1) else indice_inicial
        self.__barra__ = {jugador1.id: 0, jugador2.id: 0}
        self.__estado__ = "inicial"
        self.__movs_restantes__ = []
        self.__ultimo_error__ = None

    @property
    def tablero(self):
        """Devuelve la instancia del tablero de juego."""
        return self.__tablero__

    @property
    def estado(self):
        """Devuelve el estado actual del juego ("inicial", "en_curso", "terminado")."""
        return self.__estado__

    @property
    def jugador_actual(self):
        """Devuelve la instancia del jugador al que le toca mover."""
        return self.__jugadores__[self.__indice_jugador_actual__]
    
    @property
    def jugadores(self):
        """Devuelve la lista de instancias de Jugador."""
        return self.__jugadores__

    def ultimo_error(self):
        """Devuelve el mensaje del último error de movimiento."""
        return self.__ultimo_error__

    def _set_error(self, msg=None):
        """Establece el mensaje del último error."""
        self.__ultimo_error__ = msg

    def usar_semilla(self, semilla: int):
        """Fija la semilla para el generador de dados (para reproducibilidad)."""
        self.__dados__.fijar_semilla(semilla)

    def tirar(self):
        """Tira los dados, registra los movimientos disponibles y cambia el estado."""
        d1, d2, movimientos = self.__dados__.tirar()
        self.__movs_restantes__ = list(movimientos)
        if self.__estado__ == "inicial":
            self.__estado__ = "en_curso"
        self._set_error(None)
        self._actualizar_estado()
        return d1, d2, movimientos

    def movimientos_disponibles(self):
        """Devuelve una copia de la lista de movimientos de dados restantes."""
        return list(self.__movs_restantes__)

    def _dado_mayor_que(self, distancia_minima: int) -> int | None:
        """Busca el dado más pequeño disponible que sea >= distancia_minima."""
        movs_validos = sorted([m for m in self.__movs_restantes__ if m >= distancia_minima])
        return movs_validos[0] if movs_validos else None

    def es_ficha_mas_lejana(self, jugador_id: int, punto: int) -> bool:
        """Verifica si la ficha en 'punto' es la más lejana del home board."""
        
        if jugador_id % 2 != 0:
            puntos_relevantes = [i for i in range(18, punto) if jugador_id in self.__tablero__.punto(i)]
            return not puntos_relevantes
        else:
            puntos_relevantes = [i for i in range(punto + 1, 6) if jugador_id in self.__tablero__.punto(i)]
            return not puntos_relevantes
            
    def _entrada_para(self, pid: int) -> int:
        """Punto de entrada (desde la barra) para el jugador."""
        j1_id = self.__jugadores__[0].id
        return 0 if pid == j1_id else 23

    def _en_barra(self, pid: int) -> bool:
        """Verifica si el jugador tiene fichas en la barra."""
        return self.__tablero__.fichas_en_barra(pid) > 0

    def _validar_movimiento(self, desde: int, hasta: int) -> tuple[bool, int]:
        """Valida si el movimiento es legal, retorna (es_valido, distancia)."""
        pid = self.jugador_actual.id

        if not (0 <= desde < PUNTOS) or not (0 <= hasta <= PUNTOS):
            self._set_error(f"índices fuera de rango (0..{PUNTOS-1} o {PUNTOS} para sacar)")
            return False, 0
        
        if self._en_barra(pid):
            entrada = self._entrada_para(pid)
            if desde != entrada:
                self._set_error("tenés fichas en la barra: reingresá primero")
                return False, 0
            
            distancia = abs(hasta - entrada)
            
            if self.__tablero__._bloqueado_por_oponente(pid, hasta):
                 self._set_error("destino bloqueado por el oponente")
                 return False, distancia

        elif hasta == PUNTOS:
            if not self.__tablero__.puede_sacar_fichas(pid):
                self._set_error("solo podés sacar fichas si todas están en tu zona de salida")
                return False, 0
            
            if pid % 2 != 0:
                distancia = PUNTOS - desde
            else:
                distancia = desde + 1
            
            if distancia in self.__movs_restantes__:
                pass
            else:
                if self.es_ficha_mas_lejana(pid, desde):
                    dado_a_usar = self._dado_mayor_que(distancia)
                    if dado_a_usar is None:
                        self._set_error(f"la distancia {distancia} no está en movs {self.__movs_restantes__} ni se puede sobrepasar")
                        return False, distancia 
                    distancia = dado_a_usar
                else:
                    self._set_error("no se puede sobrepasar: hay fichas más lejos que requieren un dado menor")
                    return False, distancia
                
        else:
            distancia = abs(hasta - desde)
            if pid % 2 != 0:
                if hasta < desde:
                    self._set_error("el jugador debe moverse hacia adelante (de menor a mayor índice)")
                    return False, distancia
            else:
                if hasta > desde:
                    self._set_error("el jugador debe moverse hacia adelante (de mayor a menor índice)")
                    return False, distancia
            
            if pid not in self.__tablero__.punto(desde):
                self._set_error("no hay ficha del jugador en el origen")
                return False, distancia
            if self.__tablero__._bloqueado_por_oponente(pid, hasta):
                self._set_error("destino bloqueado por el oponente")
                return False, distancia

        if hasta != PUNTOS and distancia not in self.__movs_restantes__:
            self._set_error(f"la distancia {distancia} no está en movs {self.__movs_restantes__}")
            return False, distancia
        
        self._set_error(None)
        return True, distancia
    
    def aplicar_movimiento(self, desde: int, hasta: int) -> bool:
        """Aplica el movimiento (mover, reingresar o sacar) y consume el dado. No cambia el turno."""
        ok_pre, distancia = self._validar_movimiento(desde, hasta)
        if not ok_pre:
            return False

        pid = self.jugador_actual.id
        ok = False
        dado_consumido = distancia

        if hasta == PUNTOS:
            ok = self.__tablero__.sacar_ficha(pid, desde)
            if ok:
                distancia_a_salida = PUNTOS - desde if pid % 2 != 0 else desde + 1
                if distancia not in self.__movs_restantes__:
                    dado_consumido = self._dado_mayor_que(distancia_a_salida)
                
                if dado_consumido in self.__movs_restantes__:
                    self.__movs_restantes__.remove(dado_consumido)
                else:
                     ok = False 
            
        elif self._en_barra(pid):
            ok = self.__tablero__.reingresar_desde_barra(pid, hasta)
            if ok:
                self.__movs_restantes__.remove(distancia)
        else:
            ok = self.__tablero__.mover_ficha_seguro(pid, desde, hasta)
            if ok:
                self.__movs_restantes__.remove(distancia)

        if ok:
            self._set_error(None)
        else:
            self._set_error(self.__ultimo_error__ or "movimiento inválido") 
        
        self._actualizar_estado()
        return ok

    def mover_ficha(self, desde: int, hasta: int) -> bool:
        """Aplica el movimiento y si se consumen todos los dados, cambia el turno."""
        ok = self.aplicar_movimiento(desde, hasta)
        
        if ok and not self.__movs_restantes__:
            self.cambiar_turno()
        elif ok:
            self._actualizar_estado()
            
        return ok

    def colocar_ficha_en(self, punto: int) -> bool:
        """Coloca una ficha en un punto. Sólo para inicializar o pruebas."""
        pid = self.jugador_actual.id
        ok = self.__tablero__.colocar_ficha(pid, punto)
        if ok and self.__estado__ == "inicial":
            self.__estado__ = "en_curso"
        self._set_error(None if ok else "no se pudo colocar ficha")
        self._actualizar_estado()
        return ok

    def cambiar_turno(self):
        """Cambia el jugador actual, limpia los movimientos restantes y actualiza el estado."""
        self.__indice_jugador_actual__ = 1 - self.__indice_jugador_actual__
        self.__movs_restantes__.clear()
        self._set_error(None)
        self._actualizar_estado()

    def termino(self) -> bool:
        """Retorna True si el juego ha terminado (hay ganador)."""
        return self.__tablero__.hay_ganador()

    def ganador(self):
        """Devuelve el objeto Jugador que ganó, o None."""
        w = self.__tablero__.id_ganador()
        if w is None:
            return None
        for j in self.__jugadores__:
            if j.id == w:
                return j
        return None

    def estado_dict(self) -> dict:
        """Devuelve un diccionario con el estado completo del juego (útil para guardar y debug)."""
        puntos = [self.__tablero__.punto(i)[:] for i in range(PUNTOS)]
        barra = {pid: self.__tablero__.fichas_en_barra(pid) for pid in [j.id for j in self.__jugadores__]}
        salidas = {pid: self.__tablero__.fichas_salidas(pid) for pid in [j.id for j in self.__jugadores__]}
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
        """Devuelve una cadena de texto con el resumen del estado actual."""
        e = self.estado_dict()
        return (f"estado={e['estado']} | turno={e['jugador_actual']} "
                f"(id {e['jugador_actual_id']}) | movs={e['movs_restantes']}")

    def reiniciar(self):
        """Reinicia el tablero a la posición inicial estándar, movimientos y estado."""
        j1_id = self.__jugadores__[0].id
        j2_id = self.__jugadores__[1].id
        self.__tablero__.posicion_inicial_estandar(j1_id, j2_id)
        self.__movs_restantes__.clear()
        self.__indice_jugador_actual__ = 0
        self.__estado__ = "inicial" 
        self._set_error(None)
        self._actualizar_estado()

    def _actualizar_estado(self):
        """Revisa si el juego ha terminado y actualiza el estado interno."""
        if self.__tablero__.hay_ganador():
            self.__estado__ = "terminado"
        else:
            if self.__movs_restantes__:
                self.__estado__ = "en_curso"