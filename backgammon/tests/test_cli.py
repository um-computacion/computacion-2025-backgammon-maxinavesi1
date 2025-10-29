"""Tests para el módulo CLI mejorado de Backgammon."""
import unittest
from unittest.mock import patch
from io import StringIO
from backgammon.cli.main import (
    obtener_nombre_jugador,
    obtener_punto,
    obtener_movimiento,
    obtener_accion,
    turno_juego,
    main,
)
from backgammon.core.juego import Juego
from backgammon.core.jugador import Jugador


class PruebasCLIMejorado(unittest.TestCase):
    """Pruebas para la interfaz CLI mejorada del juego de Backgammon."""

    def setUp(self):
        """Silenciar stdout para todos los tests."""
        self.held_output = StringIO()
        self.stdout_patcher = patch('sys.stdout', new=self.held_output)
        self.stdout_patcher.start()

    def tearDown(self):
        """Restaurar stdout después de cada test."""
        self.stdout_patcher.stop()

    @patch('builtins.input', return_value='Juan')
    def test_obtener_nombre_jugador_valido(self, _):
        """Verifica que obtener_nombre_jugador retorne nombre válido."""
        self.assertEqual(obtener_nombre_jugador(1), 'Juan')

    @patch('builtins.input', side_effect=['', 'Pedro'])
    def test_obtener_nombre_jugador_vacio(self, _):
        """Verifica que rechace nombres vacíos."""
        self.assertEqual(obtener_nombre_jugador(2), 'Pedro')

    @patch('builtins.input', side_effect=['NombreMuyLargoQueExcedeLimite', 'Maria'])
    def test_obtener_nombre_jugador_muy_largo(self, _):
        """Verifica que rechace nombres muy largos."""
        self.assertEqual(obtener_nombre_jugador(1), 'Maria')

    @patch('builtins.input', return_value='5')
    def test_obtener_punto_numero_valido(self, _):
        """Verifica que obtener_punto acepte número válido."""
        self.assertEqual(obtener_punto(), 5)

    @patch('builtins.input', return_value='FUERA')
    def test_obtener_punto_fuera(self, _):
        """Verifica que obtener_punto acepte 'FUERA' para sacar fichas."""
        self.assertEqual(obtener_punto(), 24)

    @patch('builtins.input', return_value='S')
    def test_obtener_punto_salir(self, _):
        """Verifica que obtener_punto retorne None al escribir 'S'."""
        self.assertIsNone(obtener_punto())

    @patch('builtins.input', side_effect=['ABC', '10'])
    def test_obtener_punto_texto_invalido(self, _):
        """Verifica que rechace texto en lugar de número."""
        self.assertEqual(obtener_punto(), 10)

    @patch('builtins.input', side_effect=['25', '15'])
    def test_obtener_punto_fuera_rango(self, _):
        """Verifica que rechace números > 24."""
        self.assertEqual(obtener_punto(), 15)

    @patch('builtins.input', return_value='T')
    def test_obtener_accion_tirar(self, _):
        """Verifica que obtener_accion acepte 'T' para tirar."""
        self.assertEqual(obtener_accion(), 'T')

    @patch('builtins.input', return_value='M')
    def test_obtener_accion_mover(self, _):
        """Verifica que obtener_accion acepte 'M' para mover."""
        self.assertEqual(obtener_accion(), 'M')

    @patch('builtins.input', return_value='P')
    def test_obtener_accion_pasar(self, _):
        """Verifica que obtener_accion acepte 'P' para pasar."""
        self.assertEqual(obtener_accion(), 'P')

    @patch('builtins.input', return_value='S')
    def test_obtener_accion_salir(self, _):
        """Verifica que obtener_accion acepte 'S' para salir."""
        self.assertEqual(obtener_accion(), 'S')

    @patch('builtins.input', return_value='V')
    def test_obtener_accion_ver(self, _):
        """Verifica que obtener_accion acepte 'V' para ver movimientos."""
        self.assertEqual(obtener_accion(), 'V')

    @patch('builtins.input', side_effect=['X', 'T'])
    def test_obtener_accion_invalido(self, _):
        """Verifica que rechace acciones inválidas."""
        self.assertEqual(obtener_accion(), 'T')

    @patch('builtins.input', side_effect=['5', '2'])
    def test_obtener_movimiento_normal(self, _):
        """Verifica obtener_movimiento con fichas normales."""
        juego = Juego(Jugador("A"), Jugador("B"))
        juego.tablero.colocar_ficha(juego.jugador_actual.id, 5)
        resultado = obtener_movimiento(juego)
        self.assertEqual(resultado, (5, 2))

    @patch('builtins.input', return_value='S')
    def test_obtener_movimiento_cancelar(self, _):
        """Verifica que obtener_movimiento permita cancelar."""
        juego = Juego(Jugador("A"), Jugador("B"))
        resultado = obtener_movimiento(juego)
        self.assertIsNone(resultado)

    @patch('backgammon.cli.main.dibujar_tablero')
    @patch('backgammon.cli.main.mostrar_info_jugador')
    @patch('backgammon.cli.main.obtener_accion', return_value='S')
    def test_turno_juego_salir(self, *_):
        """Verifica que turno_juego permita salir."""
        juego = Juego(Jugador("A"), Jugador("B"))
        resultado = turno_juego(juego)
        self.assertFalse(resultado)

    @patch('builtins.input', return_value='')
    @patch('backgammon.cli.main.dibujar_tablero')
    @patch('backgammon.cli.main.mostrar_info_jugador')
    @patch('backgammon.cli.main.mostrar_movimientos_posibles')
    @patch('backgammon.cli.main.obtener_accion', side_effect=['T', 'P'])
    def test_turno_juego_tirar_dados(self, mock_accion, *_):
        """Verifica que turno_juego permita tirar dados."""
        juego = Juego(Jugador("A"), Jugador("B"))
        resultado = turno_juego(juego)
        self.assertTrue(resultado)
        self.assertTrue(len(juego.movimientos_disponibles()) > 0)
        # Verificar que se llamó a obtener_accion dos veces
        self.assertEqual(mock_accion.call_count, 2)

    @patch('builtins.input', return_value='')
    @patch('backgammon.cli.main.dibujar_tablero')
    @patch('backgammon.cli.main.mostrar_info_jugador')
    @patch('backgammon.cli.main.obtener_movimiento', return_value=(5, 2))
    @patch('backgammon.cli.main.obtener_accion', return_value='M')
    def test_turno_juego_mover_exitoso(self, *_):
        """Verifica turno con movimiento exitoso."""
        juego = Juego(Jugador("A"), Jugador("B"))
        juego.tablero.colocar_ficha(juego.jugador_actual.id, 5)
        juego.__movs_restantes__ = [3]
        resultado = turno_juego(juego)
        self.assertTrue(resultado)

    @patch('builtins.input', return_value='')
    @patch('backgammon.cli.main.dibujar_tablero')
    @patch('backgammon.cli.main.mostrar_info_jugador')
    @patch('backgammon.cli.main.obtener_accion', side_effect=['P'])
    def test_turno_juego_pasar_sin_dados(self, *_):
        """Verifica pasar turno sin dados disponibles."""
        juego = Juego(Jugador("A"), Jugador("B"))
        jugador_inicial = juego.jugador_actual.nombre
        resultado = turno_juego(juego)
        self.assertTrue(resultado)
        self.assertNotEqual(juego.jugador_actual.nombre, jugador_inicial)

    @patch('builtins.input', return_value='')
    @patch('backgammon.cli.main.dibujar_tablero')
    @patch('backgammon.cli.main.mostrar_info_jugador')
    @patch('backgammon.cli.main.mostrar_movimientos_posibles')
    @patch('backgammon.cli.main.obtener_accion', side_effect=['V', 'P'])
    def test_turno_juego_ver_movimientos(self, mock_accion, *_):
        """Verifica que se puedan ver movimientos posibles."""
        juego = Juego(Jugador("A"), Jugador("B"))
        juego.__movs_restantes__ = [5, 3]
        resultado = turno_juego(juego)
        self.assertTrue(resultado)
        # Verificar que se llamó a obtener_accion dos veces
        self.assertEqual(mock_accion.call_count, 2)

    @patch('builtins.input', side_effect=['N', 'Alice', 'Bob', '', ''])
    @patch('backgammon.cli.main.turno_juego', return_value=False)
    @patch('backgammon.cli.main.limpiar_pantalla')
    @patch('backgammon.cli.main.dibujar_tablero')
    @patch('backgammon.cli.main.mostrar_info_jugador')
    def test_main_salir_inmediato(self, *_):
        """Verifica que main maneje salida inmediata."""
        main()

    @patch('builtins.input', side_effect=['S', '', 'Alice', 'Bob', '', ''])
    @patch('backgammon.cli.main.turno_juego', return_value=False)
    @patch('backgammon.cli.main.limpiar_pantalla')
    @patch('backgammon.cli.main.dibujar_tablero')
    @patch('backgammon.cli.main.mostrar_info_jugador')
    @patch('backgammon.cli.main.mostrar_reglas')
    def test_main_con_reglas(self, *_):
        """Verifica que main muestre reglas cuando se solicita."""
        main()

    @patch('builtins.input', return_value='0')
    def test_obtener_punto_cero(self, _):
        """Verifica que acepte el punto 0."""
        self.assertEqual(obtener_punto(), 0)

    @patch('builtins.input', return_value='23')
    def test_obtener_punto_veintitres(self, _):
        """Verifica que acepte el punto 23."""
        self.assertEqual(obtener_punto(), 23)

    @patch('builtins.input', return_value='24')
    def test_obtener_punto_veinticuatro(self, _):
        """Verifica que acepte el punto 24."""
        self.assertEqual(obtener_punto(), 24)


if __name__ == '__main__':
    unittest.main()