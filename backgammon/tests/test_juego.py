import unittest
from backgammon.core.juego import Juego
from backgammon.core.jugador import Jugador


class _TableroFalso:
    def __init__(self, ganador_id):
        self._gid = ganador_id
    def hay_ganador(self):
        return True
    def id_ganador(self):
        return self._gid


class PruebasJuego(unittest.TestCase):
    def test_turno_inicial(self):
        g = Juego(Jugador("A"), Jugador("B"))
        self.assertEqual(g.jugador_actual.nombre, "A")

    def test_tirar_devuelve_3_valores(self):
        g = Juego(Jugador("A"), Jugador("B"))
        r = g.tirar()
        self.assertEqual(len(r), 3)

    def test_indice_inicial_valido_1(self):
        g = Juego(Jugador("A"), Jugador("B"), indice_inicial=1)
        self.assertEqual(g.jugador_actual.nombre, "B")

    def test_indice_inicial_invalido_se_normaliza_a_0(self):
        g = Juego(Jugador("A"), Jugador("B"), indice_inicial=9)
        self.assertEqual(g.jugador_actual.nombre, "A")

    def test_cambiar_turno(self):
        g = Juego(Jugador("A"), Jugador("B"))
        self.assertEqual(g.jugador_actual.nombre, "A")
        g.cambiar_turno()
        self.assertEqual(g.jugador_actual.nombre, "B")

    def test_termino_y_ganador_none(self):
        g = Juego(Jugador("A"), Jugador("B"))
        self.assertFalse(g.termino())
        self.assertIsNone(g.ganador())

    def test_ganador_devuelto(self):
        a = Jugador("A"); b = Jugador("B")
        g = Juego(a, b)
        g.__tablero__ = _TableroFalso(a.id)
        self.assertTrue(g.termino())
        self.assertEqual(g.ganador().id, a.id)

    def test_ganador_none_cuando_id_no_coincide(self):
        a = Jugador("A"); b = Jugador("B")
        g = Juego(a, b)
        g.__tablero__ = _TableroFalso(999)
        self.assertTrue(g.termino())
        self.assertIsNone(g.ganador())

    def test_movimientos_quedan_guardados_y_son_copia(self):
        g = Juego(Jugador("A"), Jugador("B"))
        d1, d2, movs = g.tirar()
        self.assertEqual(sorted(g.movimientos_disponibles()), sorted(movs))
        copia = g.movimientos_disponibles()
        copia.clear()
        self.assertEqual(sorted(g.movimientos_disponibles()), sorted(movs))

    def test_movimientos_disponibles_y_aplicar(self):
        g = Juego(Jugador("A"), Jugador("B"))
        g.__movs_restantes__ = [3]
        pid = g.jugador_actual.id
        g.__tablero__.colocar_ficha(pid, 0)
        ok = g.aplicar_movimiento(0, 3)
        self.assertTrue(ok)
        self.assertEqual(g.movimientos_disponibles(), [])
        self.assertEqual(g.__tablero__.punto(0), [])
        self.assertEqual(g.__tablero__.punto(3), [pid])

    def test_aplicar_movimiento_distancia_invalida(self):
        g = Juego(Jugador("A"), Jugador("B"))
        g.__movs_restantes__ = [2]
        pid = g.jugador_actual.id
        g.__tablero__.colocar_ficha(pid, 0)
        ok = g.aplicar_movimiento(0, 3)
        self.assertFalse(ok)
        self.assertEqual(g.__tablero__.punto(0), [pid])
        self.assertEqual(g.__tablero__.punto(3), [])

    def test_juego_usar_semilla_reproduce(self):
        g = Juego(Jugador("A"), Jugador("B"))
        g.usar_semilla(9)
        a = g.tirar()
        g.usar_semilla(9)
        b = g.tirar()
        self.assertEqual(a, b)


    def test_tirar_cambia_estado_a_en_curso(self):
        g = Juego(Jugador("A"), Jugador("B"))
        self.assertEqual(g.estado, "inicial")
        g.tirar()
        self.assertEqual(g.estado, "en_curso")

    def test_colocar_cambia_estado_desde_inicial(self):
        g = Juego(Jugador("A"), Jugador("B"))
        self.assertEqual(g.estado, "inicial")
        self.assertTrue(g.colocar_ficha_en(0))
        self.assertEqual(g.estado, "en_curso")

    def test_cambiar_turno_limpia_movs(self):
        g = Juego(Jugador("A"), Jugador("B"))
        g.__movs_restantes__ = [2, 3]
        g.cambiar_turno()
        self.assertEqual(g.jugador_actual.nombre, "B")
        self.assertEqual(g.movimientos_disponibles(), [])

    def test_mover_ficha_consumo_y_cambio_turno(self):
        g = Juego(Jugador("A"), Jugador("B"))
        pid = g.jugador_actual.id
        g.__movs_restantes__ = [2]
        g.__tablero__.colocar_ficha(pid, 0)
        ok = g.mover_ficha(0, 2)
        self.assertTrue(ok)
        self.assertEqual(g.movimientos_disponibles(), [])
        self.assertEqual(g.jugador_actual.nombre, "B")  

    def test_mover_ficha_distancia_valida_pero_sin_ficha_no_mueve(self):
        g = Juego(Jugador("A"), Jugador("B"))
        g.__movs_restantes__ = [3]
        ok = g.mover_ficha(0, 3)  
        self.assertFalse(ok)
        self.assertEqual(g.movimientos_disponibles(), [3])

    def test_estado_dict_y_resumen_formato(self):
        g = Juego(Jugador("A"), Jugador("B"))
        e = g.estado_dict()
        self.assertIn("estado", e)
        self.assertIn("jugador_actual", e)
        self.assertIn("movs_restantes", e)
        s = g.resumen_estado()
        self.assertIsInstance(s, str)
        self.assertIn("estado=", s)
        self.assertIn("movs=", s)

    def test_reiniciar_restaurar_estado(self):
        g = Juego(Jugador("A"), Jugador("B"))
        g.__movs_restantes__ = [4]
        g.cambiar_turno()
        g.reiniciar()
        self.assertEqual(g.estado, "inicial")
        self.assertEqual(g.jugador_actual.nombre, "A")
        self.assertEqual(g.movimientos_disponibles(), [])

    def test_colocar_ficha_cambia_estado_a_en_curso(self):
        g = Juego(Jugador("A"), Jugador("B"))
        self.assertEqual(g.estado, "inicial")
        ok = g.colocar_ficha_en(0)
        self.assertTrue(ok)
        self.assertEqual(g.estado, "en_curso")

    def test_resumen_estado_y_estado_dict(self):
        g = Juego(Jugador("A"), Jugador("B"))
        g.usar_semilla(123)
        d1, d2, movs = g.tirar()
        snap = g.estado_dict()
        for k in ("estado", "jugador_actual", "jugador_actual_id",
                  "movs_restantes", "puntos", "barra", "salidas"):
            self.assertIn(k, snap)
        resumen = g.resumen_estado()
        self.assertIn("estado=", resumen)
        self.assertIn("movs=", resumen)

    def test_reiniciar_limpia_movs_y_vuelve_a_inicial(self):
        g = Juego(Jugador("A"), Jugador("B"))
        g.usar_semilla(1)
        g.tirar()
        self.assertEqual(g.estado, "en_curso")
        g.reiniciar()
        self.assertEqual(g.estado, "inicial")
        self.assertEqual(g.movimientos_disponibles(), [])
        self.assertEqual(g.jugador_actual.nombre, "A")

    def test_mover_ficha_consumo_distancia_y_cambio_turno(self):
        g = Juego(Jugador("A"), Jugador("B"))
        pid = g.jugador_actual.id
        g._Juego__tablero__.colocar_ficha(pid, 0)
        g._Juego__movs_restantes__ = [3]
        ok = g.mover_ficha(0, 3)
        self.assertTrue(ok)
        self.assertEqual(g.jugador_actual.nombre, "B")
        self.assertEqual(g.movimientos_disponibles(), [])

    def test_mover_ficha_falla_por_distancia_invalida(self):
        g = Juego(Jugador("A"), Jugador("B"))
        pid = g.jugador_actual.id
        g._Juego__tablero__.colocar_ficha(pid, 0)
        g._Juego__movs_restantes__ = [2]
        self.assertFalse(g.mover_ficha(0, 3))
        self.assertEqual(g.movimientos_disponibles(), [2])

    def test_aplicar_movimiento_sin_ficha_no_modifica(self):
        g = Juego(Jugador("A"), Jugador("B"))
        g._Juego__movs_restantes__ = [3]
        self.assertFalse(g.aplicar_movimiento(0, 3))
        self.assertEqual(g.movimientos_disponibles(), [3])

    def test_tablero_property_devuelve_instancia(self):
        g = Juego(Jugador("A"), Jugador("B"))
        self.assertIsNotNone(g.tablero.__class__)

    def test_usar_semilla_y_tirar_cubre_rama(self):
        g = Juego(Jugador("A"), Jugador("B"))
        g.usar_semilla(1234)                 
        r1 = g.tirar()
        g.usar_semilla(1234)
        r2 = g.tirar()
        self.assertEqual(r1, r2)

    def test_mover_ficha_consumo_parcial_sin_cambiar_turno(self):
        g = Juego(Jugador("A"), Jugador("B"))
        pid = g.jugador_actual.id
        g._Juego__tablero__.colocar_ficha(pid, 0)
        g._Juego__movs_restantes__ = [3, 2]
        ok = g.mover_ficha(0, 3)
        self.assertTrue(ok)
        self.assertEqual(g.jugador_actual.nombre, "A")   
        self.assertEqual(g.movimientos_disponibles(), [2])
        self.assertEqual(g.estado, "en_curso")          

    def test_estado_pasa_a_terminado_cuando_hay_ganador(self):
        from backgammon.core.tablero import FICHAS_POR_JUGADOR
        g = Juego(Jugador("A"), Jugador("B"))
        g.tablero._Tablero__salidas__ = {g.jugador_actual.id: FICHAS_POR_JUGADOR}
        g.cambiar_turno()                                
        self.assertEqual(g.estado, "terminado")

    def test_aplicar_movimiento_no_cambia_turno_pero_consumo(self):
        g = Juego(Jugador("A"), Jugador("B"))
        pid = g.jugador_actual.id
        g._Juego__tablero__.colocar_ficha(pid, 0)
        g._Juego__movs_restantes__ = [3, 4]
        ok = g.aplicar_movimiento(0, 3)                 
        self.assertTrue(ok)
        self.assertEqual(g.jugador_actual.nombre, "A")
        self.assertEqual(g.movimientos_disponibles(), [4])

    def test_reiniciar_cubre_todas_limpiezas(self):
        g = Juego(Jugador("A"), Jugador("B"))
        g.usar_semilla(7)
        g.tirar()
        g.colocar_ficha_en(0)
        g.reiniciar()
        self.assertEqual(g.estado, "inicial")
        self.assertEqual(g.movimientos_disponibles(), [])
        self.assertEqual(g.jugador_actual.nombre, "A")

    def test_juego_bloqueo_impide_mover_y_no_consumo(self):
        g = Juego(Jugador("A"), Jugador("B"))
        pid = g.jugador_actual.id
        g._Juego__tablero__.colocar_ficha(pid, 0)
        rival = 2 if pid == 1 else 1
        g._Juego__tablero__.colocar_ficha(rival, 3)
        g._Juego__tablero__.colocar_ficha(rival, 3)
        g._Juego__movs_restantes__ = [3]
        ok = g.mover_ficha(0, 3)
        self.assertFalse(ok)
        self.assertEqual(g.movimientos_disponibles(), [3])
        self.assertEqual(g.jugador_actual.id, pid)


    def test_juego_hit_envia_a_barra_y_cambia_turno_si_sin_movs(self):
        g = Juego(Jugador("A"), Jugador("B"))
        pid = g.jugador_actual.id
        rival = 2 if pid == 1 else 1
        g._Juego__tablero__.colocar_ficha(pid, 0)
        g._Juego__tablero__.colocar_ficha(rival, 3)  
        g._Juego__movs_restantes__ = [3]
        ok = g.mover_ficha(0, 3)
        self.assertTrue(ok)
        self.assertEqual(g.tablero.fichas_en_barra(rival), 1)
        self.assertEqual(g.tablero.punto(3), [pid])
        self.assertNotEqual(g.jugador_actual.id, pid)


    def test_alias_movs_restantes_espeja_en_getter(self):
        g = Juego(Jugador("A"), Jugador("B"))
        g._Juego__movs_restantes__ = [4, 1]
        self.assertEqual(g.movimientos_disponibles(), [4, 1])
        pid = g.jugador_actual.id
        g._Juego__tablero__.colocar_ficha(pid, 0)
        ok = g.aplicar_movimiento(0, 4)
        if not ok:
            g._Juego__tablero__.preparar_posicion_inicial()
            g._Juego__tablero__.colocar_ficha(pid, 0)
            g._Juego__movs_restantes__ = [1]
            ok = g.aplicar_movimiento(0, 1)
        self.assertTrue(ok)
        self.assertIn(len(g.movimientos_disponibles()), (0, 1))  


    def test_alias_reemplazo_de_tablero_dispara_estado_terminado(self):
        a = Jugador("A"); b = Jugador("B")
        g = Juego(a, b)
        from backgammon.core.tablero import Tablero, FICHAS_POR_JUGADOR
        t = Tablero()
        t._Tablero__salidas__ = {a.id: FICHAS_POR_JUGADOR}
        g._Juego__tablero__ = t
        g.cambiar_turno()
        self.assertEqual(g.estado, "terminado")



if __name__ == "__main__":
    unittest.main()
