"""Tests para el módulo juego."""
import unittest
from backgammon.core.juego import Juego
from backgammon.core.jugador import Jugador
from backgammon.core.tablero import PUNTOS, FICHAS_POR_JUGADOR, Tablero, Checker


class TableroFalso:
    """Tablero simulado para testing de estados de fin de juego."""

    def __init__(self, ganador_id):
        """
        Inicializa el tablero falso con un ganador predefinido.

        Args:
            ganador_id (int): ID del jugador ganador.
        """
        self._gid = ganador_id

    def hay_ganador(self):
        """Retorna True indicando que hay un ganador."""
        return True

    def id_ganador(self):
        """Retorna el ID del ganador predefinido."""
        return self._gid


def preparar_bearing_off(juego: Juego, pid: int, pos_ficha: int):
    """
    Fuerza el estado para que 'juego' pueda sacar fichas.

    Args:
        juego (Juego): Instancia del juego.
        pid (int): ID del jugador.
        pos_ficha (int): Posición donde colocar la ficha.
    """
    juego.tablero.preparar_posicion_inicial()
    juego.tablero.__salidas__ = {pid: FICHAS_POR_JUGADOR - 1}
    juego.tablero.colocar_ficha(pid, pos_ficha)
    juego.__movs_restantes__ = []


class PruebasJuego(unittest.TestCase):
    """Pruebas para la clase Juego."""

    def test_turno_inicial(self):
        """Verifica que el turno inicial sea el jugador A."""
        juego = Juego(Jugador("A"), Jugador("B"))
        self.assertEqual(juego.jugador_actual.nombre, "A")

    def test_tirar_devuelve_3_valores(self):
        """Verifica que tirar() devuelva 3 valores."""
        juego = Juego(Jugador("A"), Jugador("B"))
        resultado = juego.tirar()
        self.assertEqual(len(resultado), 3)

    def test_indice_inicial_valido_1(self):
        """Verifica que el índice inicial 1 inicie con jugador B."""
        juego = Juego(Jugador("A"), Jugador("B"), indice_inicial=1)
        self.assertEqual(juego.jugador_actual.nombre, "B")

    def test_indice_inicial_invalido_se_normaliza_a_0(self):
        """Verifica que índice inválido se normalice a 0."""
        juego = Juego(Jugador("A"), Jugador("B"), indice_inicial=9)
        self.assertEqual(juego.jugador_actual.nombre, "A")

    def test_cambiar_turno(self):
        """Verifica que cambiar_turno() alterne entre jugadores."""
        juego = Juego(Jugador("A"), Jugador("B"))
        self.assertEqual(juego.jugador_actual.nombre, "A")
        juego.cambiar_turno()
        self.assertEqual(juego.jugador_actual.nombre, "B")

    def test_termino_y_ganador_none(self):
        """Verifica estado inicial sin ganador."""
        juego = Juego(Jugador("A"), Jugador("B"))
        self.assertFalse(juego.termino())
        self.assertIsNone(juego.ganador())

    def test_ganador_devuelto(self):
        """Verifica que se devuelva el ganador correcto."""
        jugador_a = Jugador("A")
        jugador_b = Jugador("B")
        juego = Juego(jugador_a, jugador_b)
        juego.__tablero__ = TableroFalso(jugador_a.id)
        self.assertTrue(juego.termino())
        self.assertEqual(juego.ganador().id, jugador_a.id)

    def test_ganador_none_cuando_id_no_coincide(self):
        """Verifica que ganador() retorne None si ID no coincide."""
        jugador_a = Jugador("A")
        jugador_b = Jugador("B")
        juego = Juego(jugador_a, jugador_b)
        juego.__tablero__ = TableroFalso(999)
        self.assertTrue(juego.termino())
        self.assertIsNone(juego.ganador())

    def test_movimientos_quedan_guardados_y_son_copia(self):
        """Verifica que movimientos_disponibles() devuelva una copia."""
        juego = Juego(Jugador("A"), Jugador("B"))
        _, _, movs = juego.tirar()
        self.assertEqual(sorted(juego.movimientos_disponibles()), sorted(movs))
        copia = juego.movimientos_disponibles()
        copia.clear()
        self.assertEqual(sorted(juego.movimientos_disponibles()), sorted(movs))

    def test_movimientos_disponibles_y_aplicar(self):
        """Verifica que aplicar_movimiento() consuma movimientos."""
        juego = Juego(Jugador("A"), Jugador("B"))
        juego.__movs_restantes__ = [3]
        pid = juego.jugador_actual.id
        juego.tablero.colocar_ficha(pid, 5)
        resultado = juego.aplicar_movimiento(5, 2)
        self.assertTrue(resultado)
        self.assertEqual(juego.movimientos_disponibles(), [])
        self.assertEqual(juego.tablero.punto(5), [])
        self.assertEqual(len(juego.tablero.punto(2)), 1)

    def test_aplicar_movimiento_distancia_invalida(self):
        """Verifica que movimiento con distancia inválida falle."""
        juego = Juego(Jugador("A"), Jugador("B"))
        juego.__movs_restantes__ = [2]
        pid = juego.jugador_actual.id
        juego.tablero.colocar_ficha(pid, 5)
        resultado = juego.aplicar_movimiento(5, 2)
        self.assertFalse(resultado)
        self.assertEqual(len(juego.tablero.punto(5)), 1)
        self.assertEqual(juego.tablero.punto(2), [])

    def test_juego_usar_semilla_reproduce(self):
        """Verifica que usar_semilla() produzca tiradas reproducibles."""
        juego = Juego(Jugador("A"), Jugador("B"))
        juego.usar_semilla(9)
        tirada_a = juego.tirar()
        juego.usar_semilla(9)
        tirada_b = juego.tirar()
        self.assertEqual(tirada_a, tirada_b)

    def test_tirar_cambia_estado_a_en_curso(self):
        """Verifica que tirar() cambie estado a 'en_curso'."""
        juego = Juego(Jugador("A"), Jugador("B"))
        self.assertEqual(juego.estado, "inicial")
        juego.tirar()
        self.assertEqual(juego.estado, "en_curso")

    def test_colocar_cambia_estado_desde_inicial(self):
        """Verifica que colocar_ficha_en() cambie estado desde inicial."""
        juego = Juego(Jugador("A"), Jugador("B"))
        self.assertEqual(juego.estado, "inicial")
        self.assertTrue(juego.colocar_ficha_en(5))
        self.assertEqual(juego.estado, "en_curso")

    def test_cambiar_turno_limpia_movs(self):
        """Verifica que cambiar_turno() limpie movimientos."""
        juego = Juego(Jugador("A"), Jugador("B"))
        juego.__movs_restantes__ = [2, 3]
        juego.cambiar_turno()
        self.assertEqual(juego.jugador_actual.nombre, "B")
        self.assertEqual(juego.movimientos_disponibles(), [])

    def test_mover_ficha_consumo_y_cambio_turno(self):
        """Verifica que mover_ficha() cambie turno al consumir todos los dados."""
        juego = Juego(Jugador("A"), Jugador("B"))
        pid = juego.jugador_actual.id
        juego.__movs_restantes__ = [2]
        juego.tablero.colocar_ficha(pid, 5)
        resultado = juego.mover_ficha(5, 3)
        self.assertTrue(resultado)
        self.assertEqual(juego.movimientos_disponibles(), [])
        self.assertEqual(juego.jugador_actual.nombre, "B")

    def test_mover_ficha_distancia_valida_pero_sin_ficha_no_mueve(self):
        """Verifica que mover sin ficha en origen falle."""
        juego = Juego(Jugador("A"), Jugador("B"))
        juego.__movs_restantes__ = [3]
        resultado = juego.mover_ficha(5, 2)
        self.assertFalse(resultado)
        self.assertEqual(juego.movimientos_disponibles(), [3])
        self.assertIn("no hay ficha", juego.ultimo_error() or "")

    def test_estado_dict_y_resumen_formato(self):
        """Verifica que estado_dict() y resumen_estado() tengan formato correcto."""
        juego = Juego(Jugador("A"), Jugador("B"))
        estado = juego.estado_dict()
        self.assertIn("estado", estado)
        self.assertIn("jugador_actual", estado)
        self.assertIn("movs_restantes", estado)
        resumen = juego.resumen_estado()
        self.assertIsInstance(resumen, str)
        self.assertIn("estado=", resumen)
        self.assertIn("movs=", resumen)

    def test_reiniciar_restaurar_estado(self):
        """Verifica que reiniciar() restaure el estado inicial."""
        juego = Juego(Jugador("A"), Jugador("B"))
        juego.__movs_restantes__ = [4]
        juego.cambiar_turno()
        juego.reiniciar()
        self.assertEqual(juego.estado, "inicial")
        self.assertEqual(juego.jugador_actual.nombre, "A")
        self.assertEqual(juego.movimientos_disponibles(), [])

    def test_colocar_ficha_cambia_estado_a_en_curso(self):
        """Verifica que colocar ficha cambie el estado a 'en_curso'."""
        juego = Juego(Jugador("A"), Jugador("B"))
        self.assertEqual(juego.estado, "inicial")
        resultado = juego.colocar_ficha_en(5)
        self.assertTrue(resultado)
        self.assertEqual(juego.estado, "en_curso")

    def test_resumen_estado_y_estado_dict(self):
        """Verifica contenido de estado_dict() y resumen_estado()."""
        juego = Juego(Jugador("A"), Jugador("B"))
        juego.usar_semilla(123)
        _, _, _ = juego.tirar()
        snap = juego.estado_dict()
        for clave in ("estado", "jugador_actual", "jugador_actual_id",
                      "movs_restantes", "puntos", "barra", "salidas"):
            self.assertIn(clave, snap)
        resumen = juego.resumen_estado()
        self.assertIn("estado=", resumen)
        self.assertIn("movs=", resumen)

    def test_reiniciar_limpia_movs_y_vuelve_a_inicial(self):
        """Verifica que reiniciar() limpie movimientos y vuelva a inicial."""
        juego = Juego(Jugador("A"), Jugador("B"))
        juego.usar_semilla(1)
        juego.tirar()
        self.assertEqual(juego.estado, "en_curso")
        juego.reiniciar()
        self.assertEqual(juego.estado, "inicial")
        self.assertEqual(juego.movimientos_disponibles(), [])
        self.assertEqual(juego.jugador_actual.nombre, "A")

    def test_mover_ficha_consumo_distancia_y_cambio_turno(self):
        """Verifica consumo de distancia y cambio de turno."""
        juego = Juego(Jugador("A"), Jugador("B"))
        pid = juego.jugador_actual.id
        juego.tablero.colocar_ficha(pid, 5)
        juego.__movs_restantes__ = [3]
        resultado = juego.mover_ficha(5, 2)
        self.assertTrue(resultado)
        self.assertEqual(juego.jugador_actual.nombre, "B")
        self.assertEqual(juego.movimientos_disponibles(), [])

    def test_mover_ficha_falla_por_distancia_invalida(self):
        """Verifica que falle con distancia no disponible."""
        juego = Juego(Jugador("A"), Jugador("B"))
        pid = juego.jugador_actual.id
        juego.tablero.colocar_ficha(pid, 5)
        juego.__movs_restantes__ = [3]
        resultado = juego.mover_ficha(5, 1)
        self.assertFalse(resultado)
        self.assertIn("distancia", juego.ultimo_error() or "")

    def test_mover_ficha_consumo_parcial_sin_cambiar_turno(self):
        """Verifica que consumo parcial no cambie turno."""
        juego = Juego(Jugador("A"), Jugador("B"))
        pid = juego.jugador_actual.id
        juego.tablero.colocar_ficha(pid, 5)
        juego.__movs_restantes__ = [2, 4]
        resultado = juego.mover_ficha(5, 3)
        self.assertTrue(resultado)
        self.assertEqual(juego.jugador_actual.nombre, "A")
        self.assertEqual(juego.movimientos_disponibles(), [4])

    def test_aplicar_movimiento_no_cambia_turno_pero_consumo(self):
        """Verifica que aplicar_movimiento() no cambie turno."""
        juego = Juego(Jugador("A"), Jugador("B"))
        pid = juego.jugador_actual.id
        juego.tablero.colocar_ficha(pid, 5)
        juego.__movs_restantes__ = [1]
        resultado = juego.aplicar_movimiento(5, 4)
        self.assertTrue(resultado)
        self.assertIn(len(juego.movimientos_disponibles()), (0, 1))

    def test_juego_hit_envia_a_barra_y_cambia_turno_si_sin_movs(self):
        """Verifica que hit envíe a barra y cambie turno."""
        juego = Juego(Jugador("A"), Jugador("B"))
        pid = juego.jugador_actual.id
        rival = 2 if pid == 1 else 1
        juego.tablero.colocar_ficha(pid, 5)
        juego.tablero.colocar_ficha(rival, 2)
        juego.__movs_restantes__ = [3]
        resultado = juego.mover_ficha(5, 2)
        self.assertTrue(resultado)
        self.assertEqual(juego.tablero.fichas_en_barra(rival), 1)
        self.assertEqual(juego.jugador_actual.nombre, "B")

    def test_alias_movs_restantes_espeja_en_getter(self):
        """Verifica que movimientos_disponibles() refleje cambios internos."""
        juego = Juego(Jugador("A"), Jugador("B"))
        pid = juego.jugador_actual.id
        juego.tablero.colocar_ficha(pid, 5)
        juego.__movs_restantes__ = [1]
        resultado = juego.aplicar_movimiento(5, 4)
        self.assertTrue(resultado)
        self.assertIn(len(juego.movimientos_disponibles()), (0, 1))

    def test_alias_reemplazo_de_tablero_dispara_estado_terminado(self):
        """Verifica que reemplazar tablero actualice el estado."""
        jugador_a = Jugador("A")
        jugador_b = Jugador("B")
        juego = Juego(jugador_a, jugador_b)

        tablero = Tablero()
        tablero.__salidas__ = {jugador_a.id: FICHAS_POR_JUGADOR}
        juego.__tablero__ = tablero

        juego._actualizar_estado()
        self.assertEqual(juego.estado, "terminado")

    def test_mover_ficha_falla_por_bloqueo_registra_error(self):
        """Verifica que bloqueo registre error apropiado."""
        juego = Juego(Jugador("A"), Jugador("B"))
        pid = juego.jugador_actual.id
        rival = 2 if pid == 1 else 1
        juego.tablero.colocar_ficha(pid, 5)
        juego.tablero.__puntos__[1] = [Checker(rival), Checker(rival)]
        juego.__movs_restantes__ = [4]
        resultado = juego.mover_ficha(5, 1)
        self.assertFalse(resultado)
        self.assertIn("bloqueado", juego.ultimo_error() or "")

    def test_mover_ficha_distancia_no_disponible_registra_error(self):
        """Verifica error por distancia no disponible."""
        juego = Juego(Jugador("A"), Jugador("B"))
        pid = juego.jugador_actual.id
        juego.tablero.colocar_ficha(pid, 5)
        juego.__movs_restantes__ = [3]
        resultado = juego.mover_ficha(5, 3)
        self.assertFalse(resultado)
        self.assertIn("distancia 2", juego.ultimo_error() or "")

    def test_aplicar_mov_distancia_no_disponible_registra_error(self):
        """Verifica error en aplicar_movimiento() por distancia."""
        juego = Juego(Jugador("A"), Jugador("B"))
        pid = juego.jugador_actual.id
        juego.tablero.colocar_ficha(pid, 5)
        juego.__movs_restantes__ = [3]
        resultado = juego.aplicar_movimiento(5, 3)
        self.assertFalse(resultado)
        self.assertIn("distancia 2", juego.ultimo_error() or "")

    def test_aplicar_mov_indices_fuera_de_rango_registra_error(self):
        """Verifica error por índices fuera de rango."""
        juego = Juego(Jugador("A"), Jugador("B"))
        juego.__movs_restantes__ = [3]
        resultado = juego.aplicar_movimiento(-1, 2)
        self.assertFalse(resultado)
        self.assertIn("fuera de rango", juego.ultimo_error() or "")

    def test_aplicar_mov_sin_ficha_en_origen_registra_error(self):
        """Verifica error cuando no hay ficha en origen."""
        juego = Juego(Jugador("A"), Jugador("B"))
        juego.__movs_restantes__ = [3]
        resultado = juego.aplicar_movimiento(5, 2)
        self.assertFalse(resultado)
        self.assertIn("no hay ficha", juego.ultimo_error() or "")

    def test_aplicar_mov_bloqueado_por_oponente_registra_error(self):
        """Verifica error por punto bloqueado en aplicar_movimiento()."""
        juego = Juego(Jugador("A"), Jugador("B"))
        pid = juego.jugador_actual.id
        rival = 2 if pid == 1 else 1
        juego.tablero.colocar_ficha(pid, 5)
        juego.tablero.__puntos__[1] = [Checker(rival), Checker(rival)]
        juego.__movs_restantes__ = [4]
        resultado = juego.aplicar_movimiento(5, 1)
        self.assertFalse(resultado)
        self.assertIn("bloqueado", juego.ultimo_error() or "")

    def test_mover_indices_fuera_de_rango_registra_error(self):
        """Verifica error en mover_ficha() por índices fuera de rango."""
        juego = Juego(Jugador("A"), Jugador("B"))
        juego.__movs_restantes__ = [3]
        resultado = juego.mover_ficha(5, 99)
        self.assertFalse(resultado)
        self.assertIn("fuera de rango", juego.ultimo_error() or "")

    def test_mover_sin_ficha_en_origen_registra_error(self):
        """Verifica error en mover_ficha() sin ficha en origen."""
        juego = Juego(Jugador("A"), Jugador("B"))
        juego.__movs_restantes__ = [3]
        resultado = juego.mover_ficha(5, 2)
        self.assertFalse(resultado)
        self.assertIn("no hay ficha", juego.ultimo_error() or "")

    def test_mover_bloqueado_por_oponente_registra_error(self):
        """Verifica error por punto bloqueado en mover_ficha()."""
        juego = Juego(Jugador("A"), Jugador("B"))
        pid = juego.jugador_actual.id
        rival = 2 if pid == 1 else 1
        juego.tablero.colocar_ficha(pid, 5)
        juego.tablero.__puntos__[1] = [Checker(rival), Checker(rival)]
        juego.__movs_restantes__ = [4]
        resultado = juego.mover_ficha(5, 1)
        self.assertFalse(resultado)
        self.assertIn("bloqueado", juego.ultimo_error() or "")

    def test_tirar_limpia_ultimo_error(self):
        """Verifica que tirar() limpie el último error."""
        juego = Juego(Jugador("A"), Jugador("B"))
        juego.__movs_restantes__ = [3]
        _ = juego.mover_ficha(5, 3)
        self.assertIsNotNone(juego.ultimo_error())
        juego.tirar()
        self.assertIsNone(juego.ultimo_error())

    def test_no_permite_mover_si_hay_barra_y_origen_distinto_a_entrada(self):
        """Verifica que con fichas en barra solo se pueda reingresar."""
        juego = Juego(Jugador("A"), Jugador("B"))
        pid = juego.jugador_actual.id
        juego.tablero.enviar_a_barra(pid)
        juego.__movs_restantes__ = [3]
        origen_mal = 5
        resultado = juego.mover_ficha(origen_mal, 8)
        self.assertFalse(resultado)
        self.assertIn("barra", juego.ultimo_error() or "")

    def test_reingreso_desde_barra_consumo_y_quita_de_barra(self):
        """Verifica que reingreso consuma dado y quite ficha de barra."""
        juego = Juego(Jugador("A"), Jugador("B"))
        pid = juego.jugador_actual.id
        juego.tablero.enviar_a_barra(pid)
        juego.__movs_restantes__ = [3]
        resultado = juego.mover_ficha(0, 3)
        self.assertTrue(resultado)
        self.assertEqual(juego.tablero.fichas_en_barra(pid), 0)
        self.assertEqual(juego.movimientos_disponibles(), [])

    def test_bearing_off_exacto_j1_consume_dado(self):
        """J1 saca ficha usando dado exacto."""
        juego = Juego(Jugador("A"), Jugador("B"))
        pid = juego.jugador_actual.id
        pos_ficha = 22
        preparar_bearing_off(juego, pid, pos_ficha)
        juego.__movs_restantes__ = [2, 6]

        resultado = juego.mover_ficha(pos_ficha, PUNTOS)

        self.assertTrue(resultado)
        self.assertEqual(juego.tablero.fichas_salidas(pid), FICHAS_POR_JUGADOR)
        self.assertEqual(juego.movimientos_disponibles(), [6])

    def test_bearing_off_over_bearing_j1_consume_dado_mayor(self):
        """J1 saca ficha con over-bearing usando dado mayor."""
        juego = Juego(Jugador("A"), Jugador("B"))
        pid = juego.jugador_actual.id
        pos_ficha = 23
        preparar_bearing_off(juego, pid, pos_ficha)
        juego.__movs_restantes__ = [5, 6]

        resultado = juego.mover_ficha(pos_ficha, PUNTOS)

        self.assertTrue(resultado)
        self.assertEqual(juego.tablero.fichas_salidas(pid), FICHAS_POR_JUGADOR)
        self.assertEqual(juego.movimientos_disponibles(), [6])

    def test_bearing_off_over_bearing_falla_si_hay_ficha_mas_lejana_j1(self):
        """J1 no puede usar dado mayor si hay ficha más lejana."""
        juego = Juego(Jugador("A"), Jugador("B"))
        pid = juego.jugador_actual.id
        juego.tablero.preparar_posicion_inicial()
        juego.tablero.__salidas__ = {pid: FICHAS_POR_JUGADOR - 2}
        juego.tablero.colocar_ficha(pid, 23)
        juego.tablero.colocar_ficha(pid, 21)
        juego.__movs_restantes__ = [5, 6]

        resultado = juego.mover_ficha(23, PUNTOS)

        self.assertFalse(resultado)
        self.assertIn("más lejos que requieren un dado menor",
                      juego.ultimo_error() or "")
        self.assertEqual(juego.movimientos_disponibles(), [5, 6])
        self.assertEqual(juego.tablero.fichas_salidas(pid),
                        FICHAS_POR_JUGADOR - 2)

    def test_bearing_off_falla_si_no_puede_sacar_fichas(self):
        """Falla si no se cumple condición de home board."""
        juego = Juego(Jugador("A"), Jugador("B"))
        pid = juego.jugador_actual.id
        juego.tablero.colocar_ficha(pid, 17)
        juego.__movs_restantes__ = [6]

        resultado = juego.mover_ficha(17, PUNTOS)

        self.assertFalse(resultado)
        self.assertIn("solo podés sacar fichas", juego.ultimo_error() or "")
        self.assertEqual(juego.movimientos_disponibles(), [6])

    def test_bearing_off_exacto_j2(self):
        """J2 saca ficha usando dado exacto."""
        juego = Juego(Jugador("A"), Jugador("B"), indice_inicial=1)
        pid = juego.jugador_actual.id
        pos_ficha = 2
        preparar_bearing_off(juego, pid, pos_ficha)
        juego.__movs_restantes__ = [3]

        resultado = juego.mover_ficha(pos_ficha, PUNTOS)

        self.assertTrue(resultado)
        self.assertEqual(juego.tablero.fichas_salidas(pid), FICHAS_POR_JUGADOR)
        self.assertEqual(juego.movimientos_disponibles(), [])

    def test_usar_semilla_fija_comportamiento(self):
        """Verifica que usar_semilla fije el comportamiento de los dados."""
        juego = Juego(Jugador("A"), Jugador("B"))
        juego.usar_semilla(42)
        tirada1 = juego.tirar()
        juego.usar_semilla(42)
        tirada2 = juego.tirar()
        self.assertEqual(tirada1, tirada2)

    def test_dado_mayor_que_retorna_none_si_no_hay(self):
        """Verifica que _dado_mayor_que retorne None si no hay dados válidos."""
        juego = Juego(Jugador("A"), Jugador("B"))
        juego.__movs_restantes__ = [1, 2]
        resultado = juego._dado_mayor_que(5)
        self.assertIsNone(resultado)

    def test_dado_mayor_que_retorna_menor_disponible(self):
        """Verifica que _dado_mayor_que retorne el menor dado >= distancia."""
        juego = Juego(Jugador("A"), Jugador("B"))
        juego.__movs_restantes__ = [2, 4, 6]
        resultado = juego._dado_mayor_que(3)
        self.assertEqual(resultado, 4)

    def test_es_ficha_mas_lejana_j1_con_fichas_mas_cerca(self):
        """Verifica que es_ficha_mas_lejana detecte fichas más lejos para J1."""
        juego = Juego(Jugador("A"), Jugador("B"))
        pid = juego.jugador_actual.id
        if pid % 2 != 0:  # Solo si es J1
            juego.tablero.preparar_posicion_inicial()
            juego.tablero.colocar_ficha(pid, 23)
            juego.tablero.colocar_ficha(pid, 20)
            resultado = juego.es_ficha_mas_lejana(pid, 23)
            self.assertFalse(resultado)

    def test_es_ficha_mas_lejana_j2_con_fichas_mas_lejos(self):
        """Verifica que es_ficha_mas_lejana detecte fichas más lejos para J2."""
        juego = Juego(Jugador("A"), Jugador("B"), indice_inicial=1)
        pid = juego.jugador_actual.id
        if pid % 2 == 0:  # Solo si es J2
            juego.tablero.preparar_posicion_inicial()
            juego.tablero.colocar_ficha(pid, 0)
            juego.tablero.colocar_ficha(pid, 3)
            resultado = juego.es_ficha_mas_lejana(pid, 0)
            self.assertFalse(resultado)

    def test_validar_bearing_off_sin_dado_ni_sobrepasar(self):
        """Verifica que bearing off falle sin dado exacto ni sobrepasar."""
        juego = Juego(Jugador("A"), Jugador("B"))
        pid = juego.jugador_actual.id
        juego.tablero.preparar_posicion_inicial()
        juego.tablero.__salidas__ = {pid: FICHAS_POR_JUGADOR - 2}
        juego.tablero.colocar_ficha(pid, 23)
        juego.tablero.colocar_ficha(pid, 21)
        juego.__movs_restantes__ = [2]
        resultado = juego.mover_ficha(23, PUNTOS)
        self.assertFalse(resultado)

    def test_entrada_para_j1(self):
        """Verifica que _entrada_para retorne 0 para J1."""
        juego = Juego(Jugador("A"), Jugador("B"))
        j1_id = juego.jugadores[0].id
        entrada = juego._entrada_para(j1_id)
        self.assertEqual(entrada, 0)

    def test_entrada_para_j2(self):
        """Verifica que _entrada_para retorne 23 para J2."""
        juego = Juego(Jugador("A"), Jugador("B"))
        j2_id = juego.jugadores[1].id
        entrada = juego._entrada_para(j2_id)
        self.assertEqual(entrada, 23)

    def test_en_barra_true(self):
        """Verifica que _en_barra retorne True si hay fichas en barra."""
        juego = Juego(Jugador("A"), Jugador("B"))
        pid = juego.jugador_actual.id
        juego.tablero.enviar_a_barra(pid)
        self.assertTrue(juego._en_barra(pid))

    def test_en_barra_false(self):
        """Verifica que _en_barra retorne False si no hay fichas en barra."""
        juego = Juego(Jugador("A"), Jugador("B"))
        pid = juego.jugador_actual.id
        self.assertFalse(juego._en_barra(pid))

    def test_colocar_ficha_en_retorna_true(self):
        """Verifica que colocar_ficha_en retorne True exitosamente."""
        juego = Juego(Jugador("A"), Jugador("B"))
        resultado = juego.colocar_ficha_en(5)
        self.assertTrue(resultado)


if __name__ == "__main__":
    unittest.main()