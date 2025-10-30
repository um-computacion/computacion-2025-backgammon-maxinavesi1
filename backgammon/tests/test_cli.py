"""Tests adicionales para aumentar coverage de main.py."""
import unittest
from unittest.mock import patch
from io import StringIO
from backgammon.cli.main import (
    obtener_punto,
    obtener_accion,
    obtener_nombre_jugador,
    obtener_movimiento,
    turno_juego,
    main,
    limpiar_pantalla,
    mostrar_bienvenida,
    mostrar_reglas,
    mostrar_ganador,
    dibujar_tablero,
    mostrar_info_jugador,
    mostrar_movimientos_posibles,
)
from backgammon.core.juego import Juego
from backgammon.core.jugador import Jugador


class TestsCompletos(unittest.TestCase):
    """Tests que ejecutan TODO el código."""

    def setUp(self):
        """Capturar stdout."""
        self.held_output = StringIO()
        self.stdout_patcher = patch('sys.stdout', new=self.held_output)
        self.stdout_patcher.start()

    def tearDown(self):
        """Restaurar stdout."""
        self.stdout_patcher.stop()

    # ========== TESTS BÁSICOS ==========
    @patch('builtins.input', return_value='5')
    def test_obtener_punto_basico(self, mock_input):
        """Test obtener punto básico."""
        del mock_input
        self.assertEqual(obtener_punto(), 5)

    @patch('builtins.input', return_value='T')
    def test_obtener_accion_basica(self, mock_input):
        """Test obtener acción básica."""
        del mock_input
        self.assertEqual(obtener_accion(), 'T')

    @patch('builtins.input', return_value='Jugador1')
    def test_obtener_nombre_basico(self, mock_input):
        """Test obtener nombre básico."""
        del mock_input
        self.assertEqual(obtener_nombre_jugador(1), 'Jugador1')

    def test_limpiar_pantalla(self):
        """Test limpiar pantalla."""
        limpiar_pantalla()
        output = self.held_output.getvalue()
        self.assertGreater(len(output), 0)

    def test_mostrar_bienvenida(self):
        """Test mostrar bienvenida."""
        mostrar_bienvenida()
        self.assertIn('BACKGAMMON', self.held_output.getvalue())

    @patch('builtins.input', return_value='')
    def test_mostrar_reglas(self, mock_input):
        """Test mostrar reglas."""
        del mock_input
        mostrar_reglas()
        self.assertIn('REGLAS', self.held_output.getvalue())

    # ========== TESTS DE TABLERO ==========
    def test_dibujar_tablero_vacio(self):
        """Test dibujar tablero vacío."""
        juego = Juego(Jugador("A"), Jugador("B"))
        dibujar_tablero(juego)
        self.assertIn('TABLERO', self.held_output.getvalue())

    def test_dibujar_tablero_con_fichas(self):
        """Test dibujar tablero con fichas."""
        juego = Juego(Jugador("A"), Jugador("B"))
        juego.tablero.posicion_inicial_estandar(
            juego.jugadores[0].id,
            juego.jugadores[1].id
        )
        dibujar_tablero(juego)
        self.assertIn('TABLERO', self.held_output.getvalue())

    def test_mostrar_info_jugador_sin_dados(self):
        """Test mostrar info sin dados."""
        juego = Juego(Jugador("Test"), Jugador("B"))
        mostrar_info_jugador(juego)
        self.assertIn('Test', self.held_output.getvalue())

    def test_mostrar_info_jugador_con_dados(self):
        """Test mostrar info con dados."""
        juego = Juego(Jugador("A"), Jugador("B"))
        juego.usar_semilla(42)
        juego.tirar()
        mostrar_info_jugador(juego)
        self.assertIn('Dados', self.held_output.getvalue())

    def test_mostrar_movimientos_sin_dados(self):
        """Test mostrar movimientos sin dados."""
        juego = Juego(Jugador("A"), Jugador("B"))
        mostrar_movimientos_posibles(juego)
        self.assertIn('dados', self.held_output.getvalue())

    def test_mostrar_movimientos_con_dados(self):
        """Test mostrar movimientos con dados."""
        juego = Juego(Jugador("A"), Jugador("B"))
        juego.tablero.posicion_inicial_estandar(
            juego.jugadores[0].id,
            juego.jugadores[1].id
        )
        juego.usar_semilla(42)
        juego.tirar()
        mostrar_movimientos_posibles(juego)
        self.assertIn('MOVIMIENTOS', self.held_output.getvalue())

    def test_mostrar_ganador_sin_ganador(self):
        """Test mostrar sin ganador."""
        juego = Juego(Jugador("A"), Jugador("B"))
        mostrar_ganador(juego)
        self.assertIn('sin ganador', self.held_output.getvalue())

    def test_mostrar_ganador_con_ganador(self):
        """Test mostrar con ganador."""
        juego = Juego(Jugador("Ganador"), Jugador("Perdedor"))
        for _ in range(15):
            juego.tablero.registrar_salida(juego.jugadores[0].id)
        mostrar_ganador(juego)
        self.assertIn('Ganador', self.held_output.getvalue())

    # ========== TESTS DE OBTENER_MOVIMIENTO ==========
    @patch('builtins.input', side_effect=['5', '2'])
    def test_obtener_movimiento_normal(self, mock_input):
        """Test obtener movimiento normal."""
        del mock_input
        juego = Juego(Jugador("A"), Jugador("B"))
        juego.tablero.colocar_ficha(juego.jugador_actual.id, 5)
        resultado = obtener_movimiento(juego)
        self.assertEqual(resultado, (5, 2))

    @patch('builtins.input', return_value='S')
    def test_obtener_movimiento_cancelar(self, mock_input):
        """Test cancelar movimiento."""
        del mock_input
        juego = Juego(Jugador("A"), Jugador("B"))
        self.assertIsNone(obtener_movimiento(juego))

    @patch('builtins.input', side_effect=['3'])
    def test_obtener_movimiento_desde_barra(self, mock_input):
        """Test movimiento desde barra."""
        del mock_input
        juego = Juego(Jugador("A"), Jugador("B"))
        juego.tablero.enviar_a_barra(juego.jugador_actual.id)
        resultado = obtener_movimiento(juego)
        self.assertIsNotNone(resultado)

    # ========== TESTS DE TURNO_JUEGO (COMPLETOS) ==========
    @patch('builtins.input', return_value='')
    @patch('backgammon.cli.main.obtener_accion', return_value='S')
    @patch('backgammon.cli.main.limpiar_pantalla')
    @patch('backgammon.cli.main.dibujar_tablero')
    @patch('backgammon.cli.main.mostrar_info_jugador')
    def test_turno_salir(self, *mocks):
        """Test salir del turno."""
        del mocks
        juego = Juego(Jugador("A"), Jugador("B"))
        self.assertFalse(turno_juego(juego))

    @patch('builtins.input', side_effect=['', '', ''])
    @patch('backgammon.cli.main.obtener_accion', side_effect=['T', 'P'])
    @patch('backgammon.cli.main.limpiar_pantalla')
    @patch('backgammon.cli.main.dibujar_tablero')
    @patch('backgammon.cli.main.mostrar_info_jugador')
    @patch('backgammon.cli.main.mostrar_movimientos_posibles')
    def test_turno_tirar_dados(self, *mocks):
        """Test tirar dados en turno."""
        del mocks
        juego = Juego(Jugador("A"), Jugador("B"))
        juego.usar_semilla(42)
        self.assertTrue(turno_juego(juego))

    @patch('builtins.input', side_effect=['', '', ''])
    @patch('backgammon.cli.main.obtener_accion', side_effect=['T', 'T', 'P'])
    @patch('backgammon.cli.main.limpiar_pantalla')
    @patch('backgammon.cli.main.dibujar_tablero')
    @patch('backgammon.cli.main.mostrar_info_jugador')
    @patch('backgammon.cli.main.mostrar_movimientos_posibles')
    def test_turno_tirar_con_dados_ya_disponibles(self, *mocks):
        """Test intentar tirar con dados disponibles."""
        del mocks
        juego = Juego(Jugador("A"), Jugador("B"))
        juego.usar_semilla(42)
        juego.tirar()
        self.assertTrue(turno_juego(juego))

    @patch('builtins.input', side_effect=['', ''])
    @patch('backgammon.cli.main.obtener_accion', side_effect=['V', 'P'])
    @patch('backgammon.cli.main.limpiar_pantalla')
    @patch('backgammon.cli.main.dibujar_tablero')
    @patch('backgammon.cli.main.mostrar_info_jugador')
    @patch('backgammon.cli.main.mostrar_movimientos_posibles')
    def test_turno_ver_movimientos_sin_dados(self, *mocks):
        """Test ver movimientos sin dados."""
        del mocks
        juego = Juego(Jugador("A"), Jugador("B"))
        self.assertTrue(turno_juego(juego))

    @patch('builtins.input', side_effect=['', '', ''])
    @patch('backgammon.cli.main.obtener_accion', side_effect=['V', 'P'])
    @patch('backgammon.cli.main.limpiar_pantalla')
    @patch('backgammon.cli.main.dibujar_tablero')
    @patch('backgammon.cli.main.mostrar_info_jugador')
    @patch('backgammon.cli.main.mostrar_movimientos_posibles')
    def test_turno_ver_movimientos_con_dados(self, *mocks):
        """Test ver movimientos con dados."""
        del mocks
        juego = Juego(Jugador("A"), Jugador("B"))
        juego.usar_semilla(42)
        juego.tirar()
        self.assertTrue(turno_juego(juego))

    @patch('builtins.input', side_effect=['', ''])
    @patch('backgammon.cli.main.obtener_accion', side_effect=['M', 'P'])
    @patch('backgammon.cli.main.limpiar_pantalla')
    @patch('backgammon.cli.main.dibujar_tablero')
    @patch('backgammon.cli.main.mostrar_info_jugador')
    def test_turno_mover_sin_dados(self, *mocks):
        """Test intentar mover sin dados."""
        del mocks
        juego = Juego(Jugador("A"), Jugador("B"))
        self.assertTrue(turno_juego(juego))

    @patch('builtins.input', side_effect=['', '', '', ''])
    @patch('backgammon.cli.main.obtener_accion', side_effect=['M', 'P'])
    @patch('backgammon.cli.main.obtener_movimiento', return_value=None)
    @patch('backgammon.cli.main.limpiar_pantalla')
    @patch('backgammon.cli.main.dibujar_tablero')
    @patch('backgammon.cli.main.mostrar_info_jugador')
    def test_turno_mover_cancelado(self, *mocks):
        """Test movimiento cancelado."""
        del mocks
        juego = Juego(Jugador("A"), Jugador("B"))
        juego.usar_semilla(42)
        juego.tirar()
        self.assertTrue(turno_juego(juego))

    @patch('builtins.input', side_effect=['', '', '', ''])
    @patch('backgammon.cli.main.obtener_accion', side_effect=['M', 'P'])
    @patch('backgammon.cli.main.obtener_movimiento', return_value=(5, 2))
    @patch('backgammon.cli.main.limpiar_pantalla')
    @patch('backgammon.cli.main.dibujar_tablero')
    @patch('backgammon.cli.main.mostrar_info_jugador')
    def test_turno_mover_exitoso(self, *mocks):
        """Test movimiento exitoso."""
        del mocks
        juego = Juego(Jugador("A"), Jugador("B"))
        juego.tablero.colocar_ficha(juego.jugador_actual.id, 5)
        juego.__movs_restantes__ = [3]
        self.assertTrue(turno_juego(juego))

    @patch('builtins.input', side_effect=['', ''])
    @patch('backgammon.cli.main.obtener_accion', side_effect=['P', 'P'])
    @patch('backgammon.cli.main.limpiar_pantalla')
    @patch('backgammon.cli.main.dibujar_tablero')
    @patch('backgammon.cli.main.mostrar_info_jugador')
    def test_turno_pasar_sin_dados(self, *mocks):
        """Test pasar turno sin dados."""
        del mocks
        juego = Juego(Jugador("A"), Jugador("B"))
        self.assertTrue(turno_juego(juego))

    @patch('builtins.input', side_effect=['', 'S', ''])
    @patch('backgammon.cli.main.obtener_accion', side_effect=['P', 'P'])
    @patch('backgammon.cli.main.limpiar_pantalla')
    @patch('backgammon.cli.main.dibujar_tablero')
    @patch('backgammon.cli.main.mostrar_info_jugador')
    def test_turno_pasar_con_dados_confirmado(self, *mocks):
        """Test pasar con dados confirmado."""
        del mocks
        juego = Juego(Jugador("A"), Jugador("B"))
        juego.__movs_restantes__ = [3, 5]
        self.assertTrue(turno_juego(juego))

    @patch('builtins.input', side_effect=['', 'N', '', ''])
    @patch('backgammon.cli.main.obtener_accion', side_effect=['P', 'P', 'P'])
    @patch('backgammon.cli.main.limpiar_pantalla')
    @patch('backgammon.cli.main.dibujar_tablero')
    @patch('backgammon.cli.main.mostrar_info_jugador')
    def test_turno_pasar_con_dados_rechazado(self, *mocks):
        """Test pasar con dados rechazado."""
        del mocks
        juego = Juego(Jugador("A"), Jugador("B"))
        juego.__movs_restantes__ = [3]
        self.assertTrue(turno_juego(juego))

    # ========== TESTS DE MAIN (COMPLETOS) ==========
    @patch('builtins.input', side_effect=['N', 'Alice', 'Bob', ''])
    @patch('backgammon.cli.main.turno_juego', return_value=False)
    @patch('backgammon.cli.main.limpiar_pantalla')
    @patch('backgammon.cli.main.mostrar_bienvenida')
    @patch('backgammon.cli.main.dibujar_tablero')
    @patch('backgammon.cli.main.mostrar_info_jugador')
    def test_main_sin_reglas(self, *mocks):
        """Test main sin reglas."""
        del mocks
        main()

    @patch('builtins.input', side_effect=['S', '', 'Alice', 'Bob', ''])
    @patch('backgammon.cli.main.turno_juego', return_value=False)
    @patch('backgammon.cli.main.limpiar_pantalla')
    @patch('backgammon.cli.main.mostrar_bienvenida')
    @patch('backgammon.cli.main.mostrar_reglas')
    @patch('backgammon.cli.main.dibujar_tablero')
    @patch('backgammon.cli.main.mostrar_info_jugador')
    def test_main_con_reglas(self, *mocks):
        """Test main con reglas."""
        del mocks
        main()

    @patch('builtins.input', side_effect=['N', 'P1', 'P2', ''])
    @patch('backgammon.cli.main.limpiar_pantalla')
    @patch('backgammon.cli.main.mostrar_bienvenida')
    @patch('backgammon.cli.main.dibujar_tablero')
    @patch('backgammon.cli.main.mostrar_info_jugador')
    @patch('backgammon.cli.main.mostrar_ganador')
    def test_main_hasta_victoria(self, *mocks):
        """Test main hasta victoria."""
        del mocks

        def turno_ganador(juego):
            for _ in range(15):
                juego.tablero.registrar_salida(juego.jugadores[0].id)
            return True

        with patch('backgammon.cli.main.turno_juego', side_effect=turno_ganador):
            main()


if __name__ == '__main__':
    unittest.main()