import unittest
from backgammon.core.tablero import Tablero, PUNTOS, FICHAS_POR_JUGADOR


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

    def test_indice_negativo(self):
        t = Tablero()
        with self.assertRaises(ValueError):
            t.punto(-1)

    def test_hay_ganador_false_e_id_none(self):
        t = Tablero()
        self.assertFalse(t.hay_ganador())
        self.assertIsNone(t.id_ganador())

    def test_hay_ganador_true_e_id(self):
        t = Tablero()
        t.__salidas__ = {7: FICHAS_POR_JUGADOR}
        self.assertTrue(t.hay_ganador())
        self.assertEqual(t.id_ganador(), 7)


if __name__ == "__main__":
    unittest.main()
