import unittest
from backgammon.core.juego import Juego
from backgammon.core.jugador import Jugador

class PruebasJuego(unittest.TestCase):
    def test_turno_inicial(self):
        g = Juego(Jugador("A"), Jugador("B"))
        self.assertEqual(g.jugador_actual.nombre, "A")

    def test_tirar_devuelve_3_valores(self):
        g = Juego(Jugador("A"), Jugador("B"))
        r = g.tirar()
        self.assertEqual(len(r), 3)  

if __name__ == "__main__":
    unittest.main()
