import unittest
from backgammon.core.dados import Dados


class PruebasDados(unittest.TestCase):

    def test_formato_tirada(self):
        d = Dados(semilla=123)
        d1, d2, movs = d.tirar()
        self.assertTrue(1 <= d1 <= 6)
        self.assertTrue(1 <= d2 <= 6)
        self.assertIn(len(movs), (2, 4))

    def test_rango_en_varias_tiradas(self):
        d = Dados(semilla=42)
        for _ in range(200):
            d1, d2, _ = d.tirar()
            self.assertTrue(1 <= d1 <= 6)
            self.assertTrue(1 <= d2 <= 6)

    def test_ultimo_tiro_actualiza(self):
        d = Dados(semilla=7)
        self.assertIsNone(d.ultimo_tiro())  
        d1, d2, movs = d.tirar()
        self.assertEqual(d.ultimo_tiro(), (d1, d2, movs))

    def test_tirar_con_doble_registra_cuatro_movimientos(self):
        d = Dados(semilla=1)
        for _ in range(300):           
            d1, d2, movs = d.tirar()
            if d1 == d2:
                self.assertEqual(len(movs), 4)
                self.assertEqual(d.ultimo_tiro(), (d1, d2, movs))
                return
        self.fail("No salió un doble en 300 tiradas")

    def test_tirar_sin_doble_registra_dos_movimientos(self):
        d = Dados(semilla=2)
        for _ in range(300):
            d1, d2, movs = d.tirar()
            if d1 != d2:
                self.assertEqual(movs, [d1, d2])
                self.assertEqual(d.ultimo_tiro(), (d1, d2, movs))
                return
        self.fail("Todas las tiradas fueron dobles en 300 intentos (muy improbable)")

    def test_fijar_semilla_reproduce_y_resetea(self):
        d = Dados()
        d.fijar_semilla(123)
        r1 = d.tirar()
        d.fijar_semilla(123)
        r2 = d.tirar()
        self.assertEqual(r1, r2)
        d.fijar_semilla(321)
        self.assertIsNone(d.ultimo_tiro())

if __name__ == "__main__":
    unittest.main()

