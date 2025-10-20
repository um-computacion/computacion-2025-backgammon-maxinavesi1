import unittest
from backgammon.core.tablero import Tablero, PUNTOS, FICHAS_POR_JUGADOR
from backgammon.core.juego import Juego
from backgammon.core.jugador import Jugador
from backgammon.core.tablero import Checker

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
        t.__puntos__[5] = [Checker(2), Checker(2)] 
        self.assertTrue(t._bloqueado_por_oponente(1, 5))

    def test_bloqueado_por_oponente_false_vacio_o_una(self):
        t = Tablero()
        self.assertFalse(t._bloqueado_por_oponente(1, 7))
        t.__puntos__[7] = [Checker(2)]
        self.assertFalse(t._bloqueado_por_oponente(1, 7))

    def test_mover_ficha_seguro_ok(self):
        t = Tablero()
        t.__puntos__[0] = [Checker(1)]
        ok = t.mover_ficha_seguro(1, 0, 3)
        self.assertTrue(ok)
        self.assertEqual(t.punto(0), [])
        self.assertEqual(len(t.punto(3)), 1)
        self.assertEqual(t.punto(3)[0].owner_id, 1)

    def test_mover_ficha_seguro_falla_por_bloqueo(self):
        t = Tablero()
        t.__puntos__[0] = [Checker(1)]
        t.__puntos__[4] = [Checker(2), Checker(2)] 
        ok = t.mover_ficha_seguro(1, 0, 4)
        self.assertFalse(ok)
        self.assertEqual(t.punto(0)[0].owner_id, 1)
        self.assertEqual(t.punto(4)[0].owner_id, 2)

    def test_mover_ficha_seguro_falla_por_propiedad(self):
        t = Tablero()
        t.__puntos__[2] = [Checker(2)] 
        ok = t.mover_ficha_seguro(1, 2, 5)
        self.assertFalse(ok)
        self.assertEqual(t.punto(2)[0].owner_id, 2)
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
        t.__puntos__[4] = [Checker(rival), Checker(rival)]
        self.assertFalse(t.reingresar_desde_barra(pid, 4))
        self.assertEqual(t.fichas_en_barra(pid), 1)

    def test_reingresar_desde_barra_hit_si_una_rival(self):
        t = Tablero()
        pid = 1
        rival = 2
        t.enviar_a_barra(pid)
        t.__puntos__[5] = [Checker(rival)] 
        ok = t.reingresar_desde_barra(pid, 5)
        self.assertTrue(ok)
        self.assertEqual(t.fichas_en_barra(pid), 0)
        self.assertEqual(t.punto(5)[0].owner_id, pid)      
        self.assertEqual(t.fichas_en_barra(rival), 1)
    
    def test_posicion_inicial_estandar_coloca_fichas_correctamente(self):
        t = Tablero()
        j1_id = 1
        j2_id = 2
        t.posicion_inicial_estandar(j1_id, j2_id)
        total_fichas_j1 = sum(1 for p in t.__puntos__ for f in p if f.owner_id == j1_id) 
        total_fichas_j2 = sum(1 for p in t.__puntos__ for f in p if f.owner_id == j2_id)
        self.assertEqual(total_fichas_j1, FICHAS_POR_JUGADOR, "J1 debe tener 15 fichas en total.")
        self.assertEqual(total_fichas_j2, FICHAS_POR_JUGADOR, "J2 debe tener 15 fichas en total.")
        expected_j1 = {23: 2, 12: 5, 7: 3, 5: 5}
        expected_j2 = {0: 2, 11: 5, 16: 3, 18: 5}

        for punto, cantidad_esperada in expected_j1.items():
            fichas_en_punto = t.punto(punto)
            self.assertEqual(len(fichas_en_punto), cantidad_esperada, 
                             f"J1: Falla en punto {punto+1}. Esperado: {cantidad_esperada}, Obtenido: {len(fichas_en_punto)}")
            if fichas_en_punto:
                 self.assertTrue(all(f.owner_id == j1_id for f in fichas_en_punto),
                                 f"J1: El punto {punto+1} contiene fichas del oponente.")

        for punto, cantidad_esperada in expected_j2.items():
            fichas_en_punto = t.punto(punto)
            self.assertEqual(len(fichas_en_punto), cantidad_esperada,
                             f"J2: Falla en punto {punto+1}. Esperado: {cantidad_esperada}, Obtenido: {len(fichas_en_punto)}")
            if fichas_en_punto:
                 self.assertTrue(all(f.owner_id == j2_id for f in fichas_en_punto),
                                 f"J2: El punto {punto+1} contiene fichas del oponente.")

        puntos_ocupados = set(expected_j1.keys()) | set(expected_j2.keys())
        for i in range(PUNTOS):
            if i not in puntos_ocupados:
                self.assertEqual(len(t.punto(i)), 0, f"El punto {i+1} debería estar vacío.")


if __name__ == "__main__":
    unittest.main()