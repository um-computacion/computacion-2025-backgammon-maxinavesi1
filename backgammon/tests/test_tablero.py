import unittest
from backgammon.core.tablero import Tablero, PUNTOS, FICHAS_POR_JUGADOR
from backgammon.core.juego import Juego
from backgammon.core.jugador import Jugador


class PruebasTablero(unittest.TestCase):

    def test_punto_valido(self):
        t = Tablero()
        self.assertIsInstance(t.punto(0), list)

    def test_punto_invalido(self):
        t = Tablero()
        with self.assertRaises(ValueError):
            t.punto(PUNTOS)

    def test_punto_ultimo_indice_valido(self):
        t = Tablero()
        self.assertIsInstance(t.punto(PUNTOS - 1), list)

    def test_indice_neativo(self):
        t = Tablero()
        with self.assertRaises(ValueError):
            t.punto(-1)

    def test_validar_indice_bordes_ok(self):
        t = Tablero()
        t.validar_indice_punto(0)
        t.validar_indice_punto(PUNTOS - 1)

    def test_validar_indice_fuera_rango(self):
        t = Tablero()
        with self.assertRaises(ValueError):
            t.validar_indice_punto(-1)
        with self.assertRaises(ValueError):
            t.validar_indice_punto(PUNTOS)

    def test_hay_ganador_false_e_id_none(self):
        t = Tablero()
        self.assertFalse(t.hay_ganador())
        self.assertIsNone(t.id_ganador())

    def test_hay_ganador_true_e_id(self):
        t = Tablero()
        t.__salidas__ = {7: FICHAS_POR_JUGADOR} 
        self.assertTrue(t.hay_ganador())
        self.assertEqual(t.id_ganador(), 7)

    def test_registrar_salida_hasta_ganar(self):
        t = Tablero()
        pid = 99
        self.assertEqual(t.fichas_salidas(pid), 0)
        for _ in range(FICHAS_POR_JUGADOR):
            t.registrar_salida(pid)
        self.assertTrue(t.hay_ganador())
        self.assertEqual(t.id_ganador(), pid)

    def test_colocar_y_quitar(self):
        t = Tablero()
        self.assertTrue(t.colocar_ficha(1, 0))
        self.assertEqual(t.punto(0), [1])
        self.assertTrue(t.quitar_ficha(1, 0))
        self.assertEqual(t.punto(0), [])

    def test_quitar_inexistente(self):
        t = Tablero()
        t.colocar_ficha(1, 0)
        self.assertFalse(t.quitar_ficha(2, 0))

    def test_mover_basico(self):
        t = Tablero()
        t.colocar_ficha(1, 0)
        ok = t.mover_ficha(1, 0, 3)
        self.assertTrue(ok)
        self.assertEqual(t.punto(0), [])
        self.assertEqual(t.punto(3), [1])

    def test_mover_ficha_sin_ficha_en_desde_devuelve_false(self):
        t = Tablero()
        self.assertFalse(t.mover_ficha(1, 0, 3))
        self.assertEqual(t.punto(0), [])
        self.assertEqual(t.punto(3), [])

    def test_mover_indices_invalidos(self):
        t = Tablero()
        with self.assertRaises(ValueError):
            t.mover_ficha(1, 0, PUNTOS)
        with self.assertRaises(ValueError):
            t.mover_ficha(1, -1, 0)

    def test_barra_helpers(self):
        t = Tablero()
        self.assertEqual(t.fichas_en_barra(1), 0)
        self.assertEqual(t.enviar_a_barra(1), 1)
        self.assertEqual(t.enviar_a_barra(1), 2)
        self.assertEqual(t.fichas_en_barra(1), 2)

    def test_salidas_helpers(self):
        t = Tablero()
        self.assertEqual(t.fichas_salidas(2), 0)
        self.assertEqual(t.registrar_salida(2), 1)
        self.assertEqual(t.registrar_salida(2), 2)
        self.assertEqual(t.fichas_salidas(2), 2)

    def test_posicion_inicial_demo_conteo(self):
        t = Tablero()
        t.colocar_ficha(1, 0); t.colocar_ficha(1, 0)
        t.colocar_ficha(2, PUNTOS - 1); t.colocar_ficha(2, PUNTOS - 1)
        self.assertEqual(t.punto(0), [1, 1])
        self.assertEqual(t.punto(PUNTOS - 1), [2, 2])
        vacios = all(len(t.punto(i)) == 0 for i in range(1, PUNTOS - 1))
        self.assertTrue(vacios)

    def test_preparar_posicion_inicial_limpia_todo(self):
        t = Tablero()
        t.__barra__ = {7: 3}
        t.__salidas__ = {7: 5}
        t.colocar_ficha(1, 0)
        t.colocar_ficha(2, 23)

        t.preparar_posicion_inicial()
        self.assertEqual(t.__barra__, {})
        self.assertEqual(t.__salidas__, {})
        self.assertTrue(all(len(t.punto(i)) == 0 for i in range(PUNTOS)))

class PruebasTableroExtra(unittest.TestCase): 
    
    def test_bloqueado_por_oponente_true(self):
        t = Tablero()
        t.__puntos__[5] = [2, 2] 
        self.assertTrue(t._bloqueado_por_oponente(1, 5))

    def test_bloqueado_por_oponente_false_vacio_o_una(self):
        t = Tablero()
        self.assertFalse(t._bloqueado_por_oponente(1, 7))
        t.__puntos__[7] = [2]
        self.assertFalse(t._bloqueado_por_oponente(1, 7))

    def test_mover_ficha_seguro_ok(self):
        t = Tablero()
        t.__puntos__[0] = [1]
        ok = t.mover_ficha_seguro(1, 0, 3)
        self.assertTrue(ok)
        self.assertEqual(t.punto(0), [])
        self.assertEqual(t.punto(3), [1])

    def test_mover_ficha_seguro_falla_por_bloqueo(self):
        t = Tablero()
        t.__puntos__[0] = [1]
        t.__puntos__[4] = [2, 2] 
        ok = t.mover_ficha_seguro(1, 0, 4)
        self.assertFalse(ok)
        self.assertEqual(t.punto(0), [1])
        self.assertEqual(t.punto(4), [2, 2])

    def test_mover_ficha_seguro_falla_por_propiedad(self):
        t = Tablero()
        t.__puntos__[2] = [2] 
        ok = t.mover_ficha_seguro(1, 2, 5)
        self.assertFalse(ok)
        self.assertEqual(t.punto(2), [2])
        self.assertEqual(t.punto(5), [])

    def test_hit_envia_a_barra_y_ocupa(self):
        t = Tablero()
        t.colocar_ficha(1, 0)
        t.colocar_ficha(2, 3)
        
        ok = t.mover_ficha_seguro(1, 0, 3)
        
        self.assertTrue(ok)
        self.assertEqual(t.punto(3), [1])
        self.assertEqual(t.fichas_en_barra(2), 1)

    def test_aliases_de_barra_y_salidas_se_reflejan(self):
        t = Tablero()
        t.__barra__ = {7: 2}
        self.assertEqual(t.fichas_en_barra(7), 2)

        t.__salidas__ = {5: FICHAS_POR_JUGADOR}
        self.assertTrue(t.hay_ganador())
        self.assertEqual(t.id_ganador(), 5)

    def test_mover_ficha_seguro_bloqueado_por_oponente(self):
        t = Tablero()
        t.colocar_ficha(1, 0)
        t.colocar_ficha(2, 4)
        t.colocar_ficha(2, 4)
        ok = t.mover_ficha_seguro(1, 0, 4)
        self.assertFalse(ok)
        self.assertEqual(t.punto(0), [1])
        self.assertEqual(t.punto(4), [2, 2])

    def test_mover_ficha_seguro_exitoso_desde_juego(self):
        g = Juego(Jugador("A"), Jugador("B"))
        pid = g.jugador_actual.id
        g.tablero.colocar_ficha(pid, 0)
        g.__movs_restantes__ = [3]
        ok = g.mover_ficha(0, 3)
        self.assertTrue(ok)
        self.assertEqual(g.jugador_actual.nombre, "B")

    def test_reingresar_desde_barra_falla_si_bloqueado(self):
        t = Tablero()
        pid = 1
        rival = 2
        t.enviar_a_barra(pid)
        t.__puntos__[4] = [rival, rival]
        self.assertFalse(t.reingresar_desde_barra(pid, 4))
        self.assertEqual(t.fichas_en_barra(pid), 1)

    def test_reingresar_desde_barra_hit_si_una_rival(self):
        t = Tablero()
        pid = 1
        rival = 2
        t.enviar_a_barra(pid)
        t.__puntos__[5] = [rival] 
        ok = t.reingresar_desde_barra(pid, 5)
        self.assertTrue(ok)
        self.assertEqual(t.fichas_en_barra(pid), 0)
        self.assertEqual(t.punto(5), [pid])      
        self.assertEqual(t.fichas_en_barra(rival), 1) 


if __name__ == "__main__":
    unittest.main()