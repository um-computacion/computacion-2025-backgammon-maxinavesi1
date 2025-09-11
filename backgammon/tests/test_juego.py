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

    def test_cambiar_turno(self):
        g = Juego(Jugador("A"), Jugador("B"))
        self.assertEqual(g.jugador_actual.nombre, "A")
        g.cambiar_turno()
        self.assertEqual(g.jugador_actual.nombre, "B")

    def test_termino_y_ganador_none(self):
        g = Juego(Jugador("A"), Jugador("B"))
        self.assertFalse(g.termino())
        self.assertIsNone(g.ganador())

class _TableroFalso:
    
    def __init__(self, ganador_id):
        self._gid = ganador_id
    def hay_ganador(self):
        return True
    def id_ganador(self):
        return self._gid

def test_ganador_devuelto(self):
    a = Jugador("A"); b = Jugador("B")
    g = Juego(a, b)
    g._Juego__tablero__ = _TableroFalso(a.id)
    self.assertTrue(g.termino())
    self.assertEqual(g.ganador().id, a.id)

if __name__ == "__main__":
    unittest.main()
