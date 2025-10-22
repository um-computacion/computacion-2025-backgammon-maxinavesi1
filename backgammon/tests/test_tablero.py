"""Tests para el módulo tablero."""
import unittest
from backgammon.core.tablero import Tablero, PUNTOS, FICHAS_POR_JUGADOR
from backgammon.core.juego import Juego
from backgammon.core.jugador import Jugador
from backgammon.core.checker import Checker


class PruebasTablero(unittest.TestCase):
    """Pruebas básicas de la clase Tablero."""

    def test_punto_valido(self):
        """Verifica que se pueda acceder a un punto válido."""
        tablero = Tablero()
        self.assertIsInstance(tablero.punto(0), list)

    def test_punto_invalido(self):
        """Verifica que lanzar excepción para punto inválido."""
        tablero = Tablero()
        with self.assertRaises(ValueError):
            tablero.punto(PUNTOS)

    def test_punto_ultimo_indice_valido(self):
        """Verifica que el último índice sea válido."""
        tablero = Tablero()
        self.assertIsInstance(tablero.punto(PUNTOS - 1), list)

    def test_indice_negativo(self):
        """Verifica que índices negativos lancen excepción."""
        tablero = Tablero()
        with self.assertRaises(ValueError):
            tablero.punto(-1)

    def test_validar_indice_bordes_ok(self):
        """Verifica validación en los bordes del rango."""
        tablero = Tablero()
        tablero.validar_indice_punto(0)
        tablero.validar_indice_punto(PUNTOS - 1)

    def test_validar_indice_fuera_rango(self):
        """Verifica que índices fuera de rango lancen excepción."""
        tablero = Tablero()
        with self.assertRaises(ValueError):
            tablero.validar_indice_punto(-1)
        with self.assertRaises(ValueError):
            tablero.validar_indice_punto(PUNTOS)

    def test_hay_ganador_false_e_id_none(self):
        """Verifica estado inicial sin ganador."""
        tablero = Tablero()
        self.assertFalse(tablero.hay_ganador())
        self.assertIsNone(tablero.id_ganador())

    def test_hay_ganador_true_e_id(self):
        """Verifica detección de ganador."""
        tablero = Tablero()
        tablero.__salidas__ = {7: FICHAS_POR_JUGADOR}
        self.assertTrue(tablero.hay_ganador())
        self.assertEqual(tablero.id_ganador(), 7)

    def test_registrar_salida_hasta_ganar(self):
        """Verifica que registrar 15 salidas marca victoria."""
        tablero = Tablero()
        pid = 99
        self.assertEqual(tablero.fichas_salidas(pid), 0)
        for _ in range(FICHAS_POR_JUGADOR):
            tablero.registrar_salida(pid)
        self.assertTrue(tablero.hay_ganador())
        self.assertEqual(tablero.id_ganador(), pid)

    def test_colocar_y_quitar(self):
        """Verifica colocar y quitar fichas."""
        tablero = Tablero()
        self.assertTrue(tablero.colocar_ficha(1, 0))
        fichas = [f.owner_id for f in tablero.punto(0)]
        self.assertEqual(fichas, [1])
        self.assertTrue(tablero.quitar_ficha(1, 0))
        self.assertEqual(tablero.punto(0), [])

    def test_quitar_inexistente(self):
        """Verifica que no se pueda quitar ficha inexistente."""
        tablero = Tablero()
        tablero.colocar_ficha(1, 0)
        self.assertFalse(tablero.quitar_ficha(2, 0))

    def test_mover_basico(self):
        """Verifica movimiento básico."""
        tablero = Tablero()
        tablero.colocar_ficha(1, 0)
        resultado = tablero.mover_ficha(1, 0, 3)
        self.assertTrue(resultado)
        self.assertEqual(tablero.punto(0), [])
        self.assertEqual([f.owner_id for f in tablero.punto(3)], [1])

    def test_mover_ficha_sin_ficha_en_desde_devuelve_false(self):
        """Verifica que mover sin ficha retorne False."""
        tablero = Tablero()
        self.assertFalse(tablero.mover_ficha(1, 0, 3))
        self.assertEqual(tablero.punto(0), [])
        self.assertEqual(tablero.punto(3), [])

    def test_mover_indices_invalidos(self):
        """Verifica que índices inválidos lancen excepción."""
        tablero = Tablero()
        with self.assertRaises(ValueError):
            tablero.mover_ficha(1, 0, PUNTOS)
        with self.assertRaises(ValueError):
            tablero.mover_ficha(1, -1, 0)

    def test_barra_helpers(self):
        """Verifica funciones auxiliares de la barra."""
        tablero = Tablero()
        self.assertEqual(tablero.fichas_en_barra(1), 0)
        self.assertEqual(tablero.enviar_a_barra(1), 1)
        self.assertEqual(tablero.enviar_a_barra(1), 2)
        self.assertEqual(tablero.fichas_en_barra(1), 2)

    def test_salidas_helpers(self):
        """Verifica funciones auxiliares de salidas."""
        tablero = Tablero()
        self.assertEqual(tablero.fichas_salidas(2), 0)
        self.assertEqual(tablero.registrar_salida(2), 1)
        self.assertEqual(tablero.registrar_salida(2), 2)
        self.assertEqual(tablero.fichas_salidas(2), 2)

    def test_posicion_inicial_demo_conteo(self):
        """Verifica posición de demostración."""
        tablero = Tablero()
        tablero.colocar_ficha(1, 0)
        tablero.colocar_ficha(1, 0)
        tablero.colocar_ficha(2, PUNTOS - 1)
        tablero.colocar_ficha(2, PUNTOS - 1)
        fichas_0 = [f.owner_id for f in tablero.punto(0)]
        fichas_23 = [f.owner_id for f in tablero.punto(PUNTOS - 1)]
        self.assertEqual(fichas_0, [1, 1])
        self.assertEqual(fichas_23, [2, 2])
        vacios = all(len(tablero.punto(i)) == 0 for i in range(1, PUNTOS - 1))
        self.assertTrue(vacios)

    def test_preparar_posicion_inicial_limpia_todo(self):
        """Verifica que preparar posición inicial limpie todo."""
        tablero = Tablero()
        tablero.__barra__ = {7: 3}
        tablero.__salidas__ = {7: 5}
        tablero.colocar_ficha(1, 0)
        tablero.colocar_ficha(2, 23)

        tablero.preparar_posicion_inicial()
        self.assertEqual(tablero.__barra__, {})
        self.assertEqual(tablero.__salidas__, {})
        self.assertTrue(all(len(tablero.punto(i)) == 0 for i in range(PUNTOS)))


class PruebasTableroExtra(unittest.TestCase):
    """Pruebas avanzadas de Tablero."""

    def test_bloqueado_por_oponente_true(self):
        """Verifica detección de punto bloqueado."""
        tablero = Tablero()
        tablero.__puntos__[5] = [Checker(2), Checker(2)]
        self.assertTrue(tablero._bloqueado_por_oponente(1, 5))

    def test_bloqueado_por_oponente_false_vacio_o_una(self):
        """Verifica que punto con 0 o 1 ficha no bloquee."""
        tablero = Tablero()
        self.assertFalse(tablero._bloqueado_por_oponente(1, 7))
        tablero.__puntos__[7] = [Checker(2)]
        self.assertFalse(tablero._bloqueado_por_oponente(1, 7))

    def test_mover_ficha_seguro_ok(self):
        """Verifica movimiento seguro exitoso."""
        tablero = Tablero()
        tablero.__puntos__[0] = [Checker(1)]
        resultado = tablero.mover_ficha_seguro(1, 0, 3)
        self.assertTrue(resultado)
        self.assertEqual(tablero.punto(0), [])
        self.assertEqual(len(tablero.punto(3)), 1)
        self.assertEqual(tablero.punto(3)[0].owner_id, 1)

    def test_mover_ficha_seguro_falla_por_bloqueo(self):
        """Verifica que movimiento seguro falle por bloqueo."""
        tablero = Tablero()
        tablero.__puntos__[0] = [Checker(1)]
        tablero.__puntos__[4] = [Checker(2), Checker(2)]
        resultado = tablero.mover_ficha_seguro(1, 0, 4)
        self.assertFalse(resultado)
        self.assertEqual(tablero.punto(0)[0].owner_id, 1)
        self.assertEqual(tablero.punto(4)[0].owner_id, 2)

    def test_mover_ficha_seguro_falla_por_propiedad(self):
        """Verifica que no se pueda mover ficha de otro jugador."""
        tablero = Tablero()
        tablero.__puntos__[2] = [Checker(2)]
        resultado = tablero.mover_ficha_seguro(1, 2, 5)
        self.assertFalse(resultado)
        self.assertEqual(tablero.punto(2)[0].owner_id, 2)
        self.assertEqual(tablero.punto(5), [])

    def test_hit_envia_a_barra_y_ocupa(self):
        """Verifica que hacer hit envíe ficha rival a la barra."""
        tablero = Tablero()
        tablero.colocar_ficha(1, 0)
        tablero.colocar_ficha(2, 3)

        resultado = tablero.mover_ficha_seguro(1, 0, 3)

        self.assertTrue(resultado)
        self.assertEqual([f.owner_id for f in tablero.punto(3)], [1])
        self.assertEqual(tablero.fichas_en_barra(2), 1)

    def test_aliases_de_barra_y_salidas_se_reflejan(self):
        """Verifica que las estructuras internas se reflejen correctamente."""
        tablero = Tablero()
        tablero.__barra__ = {7: 2}
        self.assertEqual(tablero.fichas_en_barra(7), 2)

        tablero.__salidas__ = {5: FICHAS_POR_JUGADOR}
        self.assertTrue(tablero.hay_ganador())
        self.assertEqual(tablero.id_ganador(), 5)

    def test_mover_ficha_seguro_bloqueado_por_oponente(self):
        """Verifica que movimiento seguro respete bloqueos."""
        tablero = Tablero()
        tablero.colocar_ficha(1, 0)
        tablero.colocar_ficha(2, 4)
        tablero.colocar_ficha(2, 4)
        resultado = tablero.mover_ficha_seguro(1, 0, 4)
        self.assertFalse(resultado)
        self.assertEqual([f.owner_id for f in tablero.punto(0)], [1])
        self.assertEqual([f.owner_id for f in tablero.punto(4)], [2, 2])

    def test_mover_ficha_seguro_exitoso_desde_juego(self):
        """Verifica movimiento seguro desde clase Juego."""
        juego = Juego(Jugador("A"), Jugador("B"))
        pid = juego.jugador_actual.id

        # Determinar movimiento correcto según el ID del jugador
        if pid % 2 != 0:  # Jugador impar: mueve de mayor a menor (23→0)
            origen = 5
            destino = 2
        else:  # Jugador par: mueve de menor a mayor (0→23)
            origen = 2
            destino = 5

        juego.tablero.colocar_ficha(pid, origen)
        juego.__movs_restantes__ = [3]
        resultado = juego.mover_ficha(origen, destino)
        self.assertTrue(resultado)
        self.assertEqual(juego.jugador_actual.nombre, "B")

    def test_reingresar_desde_barra_falla_si_bloqueado(self):
        """Verifica que reingreso falle si punto está bloqueado."""
        tablero = Tablero()
        pid = 1
        rival = 2
        tablero.enviar_a_barra(pid)
        tablero.__puntos__[4] = [Checker(rival), Checker(rival)]
        self.assertFalse(tablero.reingresar_desde_barra(pid, 4))
        self.assertEqual(tablero.fichas_en_barra(pid), 1)

    def test_reingresar_desde_barra_hit_si_una_rival(self):
        """Verifica que reingreso haga hit si hay una ficha rival."""
        tablero = Tablero()
        pid = 1
        rival = 2
        tablero.enviar_a_barra(pid)
        tablero.__puntos__[5] = [Checker(rival)]
        resultado = tablero.reingresar_desde_barra(pid, 5)
        self.assertTrue(resultado)
        self.assertEqual(tablero.fichas_en_barra(pid), 0)
        self.assertEqual(tablero.punto(5)[0].owner_id, pid)
        self.assertEqual(tablero.fichas_en_barra(rival), 1)

    def test_posicion_inicial_estandar_coloca_fichas_correctamente(self):
        """Verifica que posición inicial estándar sea correcta."""
        tablero = Tablero()
        j1_id = 1
        j2_id = 2
        tablero.posicion_inicial_estandar(j1_id, j2_id)
        total_j1 = sum(
            1 for punto in tablero.__puntos__ for ficha in punto
            if ficha.owner_id == j1_id
        )
        total_j2 = sum(
            1 for punto in tablero.__puntos__ for ficha in punto
            if ficha.owner_id == j2_id
        )
        self.assertEqual(total_j1, FICHAS_POR_JUGADOR, "J1 debe tener 15 fichas")
        self.assertEqual(total_j2, FICHAS_POR_JUGADOR, "J2 debe tener 15 fichas")
        expected_j1 = {23: 2, 12: 5, 7: 3, 5: 5}
        expected_j2 = {0: 2, 11: 5, 16: 3, 18: 5}

        for punto, cantidad_esperada in expected_j1.items():
            fichas_en_punto = tablero.punto(punto)
            self.assertEqual(
                len(fichas_en_punto),
                cantidad_esperada,
                f"J1: Falla en punto {punto+1}"
            )
            if fichas_en_punto:
                self.assertTrue(
                    all(ficha.owner_id == j1_id for ficha in fichas_en_punto),
                    f"J1: El punto {punto+1} contiene fichas del oponente"
                )

        for punto, cantidad_esperada in expected_j2.items():
            fichas_en_punto = tablero.punto(punto)
            self.assertEqual(
                len(fichas_en_punto),
                cantidad_esperada,
                f"J2: Falla en punto {punto+1}"
            )
            if fichas_en_punto:
                self.assertTrue(
                    all(ficha.owner_id == j2_id for ficha in fichas_en_punto),
                    f"J2: El punto {punto+1} contiene fichas del oponente"
                )

        puntos_ocupados = set(expected_j1.keys()) | set(expected_j2.keys())
        for i in range(PUNTOS):
            if i not in puntos_ocupados:
                self.assertEqual(
                    len(tablero.punto(i)), 0,
                    f"El punto {i+1} debe estar vacío"
                )


if __name__ == "__main__":
    unittest.main()