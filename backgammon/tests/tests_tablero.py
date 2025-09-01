import unittest
from backgammon.core.tablero import Tablero, PUNTOS

class PruebasTablero(unittest.TestCase):
    def test_punto_valido(self):
        t = Tablero()
        self.assertIsInstance(t.punto(0), list)

    def test_punto_invalido(self):
        t = Tablero()
        with self.assertRaises(ValueError):
            t.punto(PUNTOS)

if __name__ == "__main__":
    unittest.main()
