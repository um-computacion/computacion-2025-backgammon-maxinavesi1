"""Tests para el módulo dados."""
import unittest
from backgammon.core.dados import Dados


class PruebasDados(unittest.TestCase):
    """Pruebas para la clase Dados."""

    def test_formato_tirada(self):
        """Verifica que tirar() devuelva valores en el formato correcto."""
        dados = Dados(semilla=123)
        dado1, dado2, movimientos = dados.tirar()
        self.assertTrue(1 <= dado1 <= 6)
        self.assertTrue(1 <= dado2 <= 6)
        self.assertIn(len(movimientos), (2, 4))

    def test_rango_en_varias_tiradas(self):
        """Verifica que múltiples tiradas respeten el rango 1-6."""
        dados = Dados(semilla=42)
        for _ in range(200):
            dado1, dado2, _ = dados.tirar()
            self.assertTrue(1 <= dado1 <= 6)
            self.assertTrue(1 <= dado2 <= 6)

    def test_ultimo_tiro_actualiza(self):
        """Verifica que ultimo_tiro() se actualice correctamente."""
        dados = Dados(semilla=7)
        self.assertIsNone(dados.ultimo_tiro())
        dado1, dado2, movimientos = dados.tirar()
        self.assertEqual(dados.ultimo_tiro(), (dado1, dado2, movimientos))

    def test_tirar_con_doble_registra_cuatro_movimientos(self):
        """Verifica que un doble genere 4 movimientos."""
        dados = Dados(semilla=1)
        for _ in range(300):
            dado1, dado2, movimientos = dados.tirar()
            if dado1 == dado2:
                self.assertEqual(len(movimientos), 4)
                self.assertEqual(dados.ultimo_tiro(), (dado1, dado2, movimientos))
                return
        self.fail("No salió un doble en 300 tiradas")

    def test_tirar_sin_doble_registra_dos_movimientos(self):
        """Verifica que una tirada sin doble genere 2 movimientos."""
        dados = Dados(semilla=2)
        for _ in range(300):
            dado1, dado2, movimientos = dados.tirar()
            if dado1 != dado2:
                self.assertEqual(movimientos, [dado1, dado2])
                self.assertEqual(dados.ultimo_tiro(), (dado1, dado2, movimientos))
                return
        self.fail("Todas las tiradas fueron dobles en 300 intentos")

    def test_fijar_semilla_reproduce_y_resetea(self):
        """Verifica que fijar_semilla() reproduzca tiradas y resetee historial."""
        dados = Dados()
        dados.fijar_semilla(123)
        resultado1 = dados.tirar()
        dados.fijar_semilla(123)
        resultado2 = dados.tirar()
        self.assertEqual(resultado1, resultado2)
        dados.fijar_semilla(321)
        self.assertIsNone(dados.ultimo_tiro())

    def test_fijar_semilla_reproduce_tirada(self):
        """Verifica que fijar_semilla() produzca tiradas reproducibles."""
        dados = Dados()
        dados.fijar_semilla(5)
        tirada_a = dados.tirar()
        dados.fijar_semilla(5)
        tirada_b = dados.tirar()
        self.assertEqual(tirada_a, tirada_b)

    def test_ultimo_tiro_cambia_en_cada_tirada(self):
        """Verifica que ultimo_tiro() se actualice en cada tirada."""
        dados = Dados(semilla=10)
        resultado1 = dados.tirar()
        self.assertEqual(dados.ultimo_tiro(), resultado1)
        resultado2 = dados.tirar()
        self.assertEqual(dados.ultimo_tiro(), resultado2)
        self.assertNotEqual(resultado1, resultado2)

    def test_cambiar_semilla_cambia_secuencia_y_borra_historial(self):
        """Verifica que cambiar semilla modifique secuencia y borre historial."""
        dados = Dados()
        dados.fijar_semilla(11)
        tirada_a = dados.tirar()
        dados.fijar_semilla(12)
        self.assertIsNone(dados.ultimo_tiro())
        tirada_b = dados.tirar()
        self.assertNotEqual(tirada_a, tirada_b)

    def test_inicializar_con_semilla(self):
        """Verifica que se pueda inicializar con semilla."""
        dados1 = Dados(semilla=100)
        dados2 = Dados(semilla=100)
        tirada1 = dados1.tirar()
        tirada2 = dados2.tirar()
        self.assertEqual(tirada1, tirada2)

    def test_inicializar_sin_semilla(self):
        """Verifica que se pueda inicializar sin semilla."""
        dados = Dados()
        dado1, dado2, movimientos = dados.tirar()
        self.assertTrue(1 <= dado1 <= 6)
        self.assertTrue(1 <= dado2 <= 6)
        self.assertIsInstance(movimientos, list)


if __name__ == "__main__":
    unittest.main()