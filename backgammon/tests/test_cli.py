"""Tests completos para CLI - VERSIÓN FINAL SIN ERRORES."""
import unittest
from unittest.mock import patch
from io import StringIO
from backgammon.cli.main import (
    limpiar_pantalla,
    dibujar_tablero,
    obtener_nombre_jugador,
    obtener_punto,
    obtener_accion,
    obtener_movimiento,
    mostrar_info_jugador,
    mostrar_movimientos_posibles,
    mostrar_bienvenida,
    mostrar_reglas,
    mostrar_ganador,
    turno_juego,
    main,
)
from backgammon.core.juego import Juego
from backgammon.core.jugador import Jugador


class TestsFuncionesBasicas(unittest.TestCase):
    """Tests para funciones básicas de entrada."""

    def setUp(self):
        """Configurar captura de salida."""
        self.output = StringIO()
        self.patcher = patch('sys.stdout', new=self.output)
        self.patcher.start()

    def tearDown(self):
        """Restaurar salida."""
        self.patcher.stop()

    @patch('builtins.input', return_value='Alice')
    def test_obtener_nombre_valido(self, mock_input):
        """Test obtener nombre válido."""
        del mock_input
        resultado = obtener_nombre_jugador(1)
        self.assertEqual(resultado, 'Alice')

    @patch('builtins.input', side_effect=['', 'Bob'])
    def test_obtener_nombre_vacio_rechazado(self, mock_input):
        """Test rechazar nombre vacío."""
        del mock_input
        resultado = obtener_nombre_jugador(1)
        self.assertEqual(resultado, 'Bob')

    @patch('builtins.input', side_effect=['x' * 25, 'Joe'])
    def test_obtener_nombre_largo_rechazado(self, mock_input):
        """Test rechazar nombre muy largo."""
        del mock_input
        resultado = obtener_nombre_jugador(1)
        self.assertEqual(resultado, 'Joe')

    @patch('builtins.input', return_value='5')
    def test_obtener_punto_valido(self, mock_input):
        """Test obtener punto válido."""
        del mock_input
        resultado = obtener_punto()
        self.assertEqual(resultado, 5)

    @patch('builtins.input', return_value='0')
    def test_obtener_punto_cero(self, mock_input):
        """Test punto cero."""
        del mock_input
        resultado = obtener_punto()
        self.assertEqual(resultado, 0)

    @patch('builtins.input', return_value='23')
    def test_obtener_punto_veintitres(self, mock_input):
        """Test punto 23."""
        del mock_input
        resultado = obtener_punto()
        self.assertEqual(resultado, 23)

    @patch('builtins.input', return_value='24')
    def test_obtener_punto_veinticuatro(self, mock_input):
        """Test punto 24."""
        del mock_input
        resultado = obtener_punto()
        self.assertEqual(resultado, 24)

    @patch('builtins.input', return_value='S')
    def test_obtener_punto_salir(self, mock_input):
        """Test salir."""
        del mock_input
        resultado = obtener_punto()
        self.assertIsNone(resultado)

    @patch('builtins.input', return_value='FUERA')
    def test_obtener_punto_fuera(self, mock_input):
        """Test FUERA."""
        del mock_input
        resultado = obtener_punto()
        self.assertEqual(resultado, 24)

    @patch('builtins.input', side_effect=['abc', '10'])
    def test_obtener_punto_texto_invalido(self, mock_input):
        """Test rechazar texto."""
        del mock_input
        resultado = obtener_punto()
        self.assertEqual(resultado, 10)

    @patch('builtins.input', side_effect=['50', '15'])
    def test_obtener_punto_fuera_rango(self, mock_input):
        """Test rechazar fuera de rango."""
        del mock_input
        resultado = obtener_punto()
        self.assertEqual(resultado, 15)

    @patch('builtins.input', return_value='T')
    def test_obtener_accion_t(self, mock_input):
        """Test acción T."""
        del mock_input
        resultado = obtener_accion()
        self.assertEqual(resultado, 'T')

    @patch('builtins.input', return_value='V')
    def test_obtener_accion_v(self, mock_input):
        """Test acción V."""
        del mock_input
        resultado = obtener_accion()
        self.assertEqual(resultado, 'V')

    @patch('builtins.input', return_value='M')
    def test_obtener_accion_m(self, mock_input):
        """Test acción M."""
        del mock_input
        resultado = obtener_accion()
        self.assertEqual(resultado, 'M')

    @patch('builtins.input', return_value='P')
    def test_obtener_accion_p(self, mock_input):
        """Test acción P."""
        del mock_input
        resultado = obtener_accion()
        self.assertEqual(resultado, 'P')

    @patch('builtins.input', return_value='S')
    def test_obtener_accion_s(self, mock_input):
        """Test acción S."""
        del mock_input
        resultado = obtener_accion()
        self.assertEqual(resultado, 'S')

    @patch('builtins.input', side_effect=['X', 'T'])
    def test_obtener_accion_invalida(self, mock_input):
        """Test acción inválida."""
        del mock_input
        resultado = obtener_accion()
        self.assertEqual(resultado, 'T')


class TestsVisualizacion(unittest.TestCase):
    """Tests para funciones de visualización."""

    def setUp(self):
        """Configurar captura."""
        self.output = StringIO()
        self.patcher = patch('sys.stdout', new=self.output)
        self.patcher.start()

    def tearDown(self):
        """Restaurar."""
        self.patcher.stop()

    def test_limpiar_pantalla(self):
        """Test limpiar pantalla."""
        limpiar_pantalla()
        self.assertIn('\n', self.output.getvalue())

    def test_mostrar_bienvenida(self):
        """Test bienvenida."""
        mostrar_bienvenida()
        self.assertIn('BACKGAMMON', self.output.getvalue())

    @patch('builtins.input', return_value='')
    def test_mostrar_reglas(self, mock_input):
        """Test reglas."""
        del mock_input
        mostrar_reglas()
        self.assertIn('REGLAS', self.output.getvalue())

    def test_dibujar_tablero_vacio(self):
        """Test dibujar tablero vacío."""
        juego = Juego(Jugador("A"), Jugador("B"))
        dibujar_tablero(juego)
        output = self.output.getvalue()
        self.assertIn('TABLERO', output)
        self.assertIn('BARRA', output)

    def test_dibujar_tablero_con_fichas(self):
        """Test tablero con fichas."""
        juego = Juego(Jugador("A"), Jugador("B"))
        juego.tablero.posicion_inicial_estandar(
            juego.jugadores[0].id,
            juego.jugadores[1].id
        )
        dibujar_tablero(juego)
        self.assertIn('TABLERO', self.output.getvalue())

    def test_mostrar_info_sin_dados(self):
        """Test info sin dados."""
        juego = Juego(Jugador("Test"), Jugador("B"))
        mostrar_info_jugador(juego)
        output = self.output.getvalue()
        self.assertIn('Test', output)
        self.assertIn('No hay dados', output)

    def test_mostrar_info_con_dados(self):
        """Test info con dados."""
        juego = Juego(Jugador("A"), Jugador("B"))
        juego.usar_semilla(42)
        juego.tirar()
        mostrar_info_jugador(juego)
        self.assertIn('Dados disponibles', self.output.getvalue())

    def test_mostrar_info_con_barra(self):
        """Test info con fichas en barra."""
        juego = Juego(Jugador("A"), Jugador("B"))
        juego.tablero.enviar_a_barra(juego.jugador_actual.id)
        mostrar_info_jugador(juego)
        self.assertIn('BARRA', self.output.getvalue())

    def test_mostrar_ganador_sin_ganador(self):
        """Test sin ganador."""
        juego = Juego(Jugador("A"), Jugador("B"))
        mostrar_ganador(juego)
        self.assertIn('sin ganador', self.output.getvalue())

    def test_mostrar_ganador_con_ganador(self):
        """Test con ganador."""
        juego = Juego(Jugador("Winner"), Jugador("B"))
        for _ in range(15):
            juego.tablero.registrar_salida(juego.jugadores[0].id)
        mostrar_ganador(juego)
        output = self.output.getvalue()
        self.assertIn('Winner', output)
        self.assertIn('GANADOR', output)


class TestsObtenerMovimiento(unittest.TestCase):
    """Tests para obtener_movimiento."""

    def setUp(self):
        """Configurar."""
        self.output = StringIO()
        self.patcher = patch('sys.stdout', new=self.output)
        self.patcher.start()

    def tearDown(self):
        """Restaurar."""
        self.patcher.stop()

    @patch('builtins.input', return_value='S')
    def test_movimiento_cancelar_origen(self, mock_input):
        """Test cancelar en origen."""
        del mock_input
        juego = Juego(Jugador("A"), Jugador("B"))
        resultado = obtener_movimiento(juego)
        self.assertIsNone(resultado)

    @patch('builtins.input', side_effect=['5', 'S'])
    def test_movimiento_cancelar_destino(self, mock_input):
        """Test cancelar en destino."""
        del mock_input
        juego = Juego(Jugador("A"), Jugador("B"))
        resultado = obtener_movimiento(juego)
        self.assertIsNone(resultado)

    @patch('builtins.input', side_effect=['10', '7'])
    def test_movimiento_normal(self, mock_input):
        """Test movimiento normal."""
        del mock_input
        juego = Juego(Jugador("A"), Jugador("B"))
        resultado = obtener_movimiento(juego)
        self.assertEqual(resultado, (10, 7))

    @patch('builtins.input', side_effect=['5', 'FUERA'])
    def test_movimiento_fuera(self, mock_input):
        """Test mover FUERA."""
        del mock_input
        juego = Juego(Jugador("A"), Jugador("B"))
        resultado = obtener_movimiento(juego)
        self.assertEqual(resultado, (5, 24))

    @patch('builtins.input', side_effect=['24', '10'])
    def test_movimiento_origen_24_invalido(self, mock_input):
        """Test origen 24 inválido."""
        del mock_input
        juego = Juego(Jugador("A"), Jugador("B"))
        resultado = obtener_movimiento(juego)
        self.assertIsNone(resultado)

    @patch('builtins.input', return_value='5')
    def test_movimiento_desde_barra(self, mock_input):
        """Test desde barra."""
        del mock_input
        juego = Juego(Jugador("A"), Jugador("B"))
        juego.tablero.enviar_a_barra(juego.jugador_actual.id)
        resultado = obtener_movimiento(juego)
        self.assertIsNotNone(resultado)


class TestsMostrarMovimientos(unittest.TestCase):
    """Tests para mostrar_movimientos_posibles."""

    def setUp(self):
        """Configurar."""
        self.output = StringIO()
        self.patcher = patch('sys.stdout', new=self.output)
        self.patcher.start()

    def tearDown(self):
        """Restaurar."""
        self.patcher.stop()

    def test_movimientos_sin_dados(self):
        """Test sin dados."""
        juego = Juego(Jugador("A"), Jugador("B"))
        mostrar_movimientos_posibles(juego)
        self.assertIn('No hay dados', self.output.getvalue())

    def test_movimientos_con_dados(self):
        """Test con dados."""
        juego = Juego(Jugador("A"), Jugador("B"))
        juego.tablero.posicion_inicial_estandar(
            juego.jugadores[0].id,
            juego.jugadores[1].id
        )
        juego.__movs_restantes__ = [3, 5]
        mostrar_movimientos_posibles(juego)
        self.assertIn('MOVIMIENTOS POSIBLES', self.output.getvalue())

    def test_movimientos_desde_barra(self):
        """Test desde barra."""
        juego = Juego(Jugador("A"), Jugador("B"))
        juego.tablero.enviar_a_barra(juego.jugador_actual.id)
        juego.__movs_restantes__ = [3, 5]
        mostrar_movimientos_posibles(juego)
        self.assertIn('BARRA', self.output.getvalue())

    def test_movimientos_sin_fichas(self):
        """Test sin fichas en tablero."""
        juego = Juego(Jugador("A"), Jugador("B"))
        juego.__movs_restantes__ = [3]
        mostrar_movimientos_posibles(juego)
        self.assertIn('No tenés fichas', self.output.getvalue())


class TestsTurnoJuego(unittest.TestCase):
    """Tests para turno_juego."""

    def setUp(self):
        """Configurar."""
        self.output = StringIO()
        self.patcher = patch('sys.stdout', new=self.output)
        self.patcher.start()

    def tearDown(self):
        """Restaurar."""
        self.patcher.stop()

    @patch('builtins.input', return_value='')
    @patch('backgammon.cli.main.obtener_accion', return_value='S')
    def test_salir(self, mock_accion, mock_input):
        """Test salir."""
        del mock_accion, mock_input
        juego = Juego(Jugador("A"), Jugador("B"))
        resultado = turno_juego(juego)
        self.assertFalse(resultado)

    @patch('builtins.input', side_effect=['', '', 'S', ''])
    @patch('backgammon.cli.main.obtener_accion', side_effect=['T', 'P'])
    def test_tirar_pasar(self, mock_accion, mock_input):
        """Test tirar y pasar."""
        del mock_accion, mock_input
        juego = Juego(Jugador("A"), Jugador("B"))
        juego.usar_semilla(42)
        resultado = turno_juego(juego)
        self.assertTrue(resultado)

    @patch('builtins.input', side_effect=[''] * 200)
    @patch('backgammon.cli.main.obtener_accion', side_effect=['V'] + ['P'] * 100)
    def test_ver_sin_dados(self, mock_accion, mock_input):
        """Test ver sin dados."""
        del mock_accion, mock_input
        juego = Juego(Jugador("A"), Jugador("B"))
        resultado = turno_juego(juego)
        self.assertTrue(resultado)

    @patch('builtins.input', side_effect=[''] * 200)
    @patch('backgammon.cli.main.obtener_accion', side_effect=['M'] + ['P'] * 100)
    def test_mover_sin_dados(self, mock_accion, mock_input):
        """Test mover sin dados."""
        del mock_accion, mock_input
        juego = Juego(Jugador("A"), Jugador("B"))
        resultado = turno_juego(juego)
        self.assertTrue(resultado)

    @patch('builtins.input', side_effect=[''] * 200)
    @patch('backgammon.cli.main.obtener_accion', side_effect=['P'] * 100)
    def test_pasar_sin_dados(self, mock_accion, mock_input):
        """Test pasar sin dados."""
        del mock_accion, mock_input
        juego = Juego(Jugador("A"), Jugador("B"))
        resultado = turno_juego(juego)
        self.assertTrue(resultado)

    @patch('builtins.input', side_effect=['', 'S'] + [''] * 200)
    @patch('backgammon.cli.main.obtener_accion', side_effect=['P'] * 100)
    def test_pasar_con_dados_confirmar(self, mock_accion, mock_input):
        """Test pasar confirmando."""
        del mock_accion, mock_input
        juego = Juego(Jugador("A"), Jugador("B"))
        juego.__movs_restantes__ = [3]
        resultado = turno_juego(juego)
        self.assertTrue(resultado)

    @patch('builtins.input', side_effect=['N', 'S', ''])
    @patch('backgammon.cli.main.obtener_accion', side_effect=['P', 'P'])
    def test_pasar_con_dados_rechazar(self, mock_accion, mock_input):
        """Test pasar rechazando."""
        del mock_accion, mock_input
        juego = Juego(Jugador("A"), Jugador("B"))
        juego.__movs_restantes__ = [3]
        resultado = turno_juego(juego)
        self.assertTrue(resultado)

    @patch('builtins.input', side_effect=[''] * 200)
    @patch('backgammon.cli.main.obtener_movimiento', return_value=(5, 2))
    @patch('backgammon.cli.main.obtener_accion', side_effect=['M'] + ['P'] * 100)
    def test_mover_exitoso(self, mock_accion, mock_mov, mock_input):
        """Test mover exitoso."""
        del mock_accion, mock_mov, mock_input
        juego = Juego(Jugador("A"), Jugador("B"))
        pid = juego.jugador_actual.id
        juego.tablero.colocar_ficha(pid, 5)
        juego.__movs_restantes__ = [3]
        resultado = turno_juego(juego)
        self.assertTrue(resultado)

    @patch('builtins.input', side_effect=['', 'S', ''])
    @patch('backgammon.cli.main.obtener_movimiento', return_value=None)
    @patch('backgammon.cli.main.obtener_accion', side_effect=['M', 'P'])
    def test_mover_cancelado(self, mock_accion, mock_mov, mock_input):
        """Test mover cancelado."""
        del mock_accion, mock_mov, mock_input
        juego = Juego(Jugador("A"), Jugador("B"))
        juego.__movs_restantes__ = [3]
        resultado = turno_juego(juego)
        self.assertTrue(resultado)


class TestsMain(unittest.TestCase):
    """Tests para main."""

    def setUp(self):
        """Configurar."""
        self.output = StringIO()
        self.patcher = patch('sys.stdout', new=self.output)
        self.patcher.start()

    def tearDown(self):
        """Restaurar."""
        self.patcher.stop()

    @patch('builtins.input', side_effect=['N', 'Alice', 'Bob', ''])
    @patch('backgammon.cli.main.turno_juego', return_value=False)
    def test_main_sin_reglas(self, mock_turno, mock_input):
        """Test main sin reglas."""
        del mock_turno, mock_input
        main()

    @patch('builtins.input', side_effect=['S', '', 'Alice', 'Bob', ''])
    @patch('backgammon.cli.main.turno_juego', return_value=False)
    def test_main_con_reglas(self, mock_turno, mock_input):
        """Test main con reglas."""
        del mock_turno, mock_input
        main()

    @patch('builtins.input', side_effect=['N', 'P1', 'P2', ''])
    def test_main_victoria(self, mock_input):
        """Test main con victoria."""
        del mock_input

        contador = [0]

        def turno_ganador(juego):
            """Mock ganador."""
            contador[0] += 1
            if contador[0] == 1:
                for _ in range(15):
                    juego.tablero.registrar_salida(juego.jugadores[0].id)
            return True

        with patch('backgammon.cli.main.turno_juego', side_effect=turno_ganador):
            main()


if __name__ == '__main__':
    unittest.main()