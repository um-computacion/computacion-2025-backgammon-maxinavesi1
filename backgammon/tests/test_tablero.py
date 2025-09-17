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

    def test_colocar_y_quitar(self):
        t = Tablero()
        self.assertTrue(t.colocar_ficha(1, 0))
        self.assertEqual(t.punto(0), [1])
        self.assertTrue(t.quitar_ficha(1, 0))
        self.assertEqual(t.punto(0), [])

    def test_quitar_inexistente(self):
        t = Tablero()
        t.colocar_ficha(1, 0)
        self.assertFalse(t.quitar_ficha(2, 0))  

    def test_mover_basico(self):
        t = Tablero()
        t.colocar_ficha(1, 0)
        ok = t.mover_ficha(1, 0, 3)
        self.assertTrue(ok)
        self.assertEqual(t.punto(0), [])
        self.assertEqual(t.punto(3), [1])

    def test_mover_indices_invalidos(self):
        t = Tablero()
        with self.assertRaises(ValueError):
            t.mover_ficha(1, 0, PUNTOS)
        with self.assertRaises(ValueError):
            t.mover_ficha(1, -1, 0)
            
if __name__ == "__main__":
    unittest.main()
