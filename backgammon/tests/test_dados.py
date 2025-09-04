import unittest
from backgammon.core.dados import Dados

class PruebasDados(unittest.TestCase):
    """"Maneja tiradas de dados."""
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

if __name__ == "__main__":
    unittest.main()
