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
    def test_ultimo_tiro_actualiza(self):
        d = Dados(semilla=7)
        self.assertIsNone(d.ultimo_tiro())
        d1, d2, movs = d.tirar()
        self.assertEqual(d.ultimo_tiro(), (d1, d2, movs))

class _RNGFijo:
    def __init__(self, vals):
        self._it = iter(vals)
    def randint(self, a, b):
        return next(self._it)

def test_tirar_doble_actualiza_ultimo():
    d = Dados()
    d._Dados__rng__ = _RNGFijo([5, 5])   
    d1, d2, movs = d.tirar()
    assert movs == [5, 5, 5, 5]
    assert d.ultimo_tiro() == (5, 5, [5, 5, 5, 5])

def test_tirar_no_doble_actualiza_ultimo():
    d = Dados()
    d._Dados__rng__ = _RNGFijo([2, 6])
    d1, d2, movs = d.tirar()
    assert movs == [2, 6]
    assert d.ultimo_tiro() == (2, 6, [2, 6])


if __name__ == "__main__":
    unittest.main()
