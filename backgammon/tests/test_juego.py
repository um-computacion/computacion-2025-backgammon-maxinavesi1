import unittest
from backgammon.core.juego import Juego
from backgammon.core.jugador import Jugador


class _TableroFalso:
    def __init__(self, ganador_id):
        self._gid = ganador_id
    def hay_ganador(self):
        return True
    def id_ganador(self):
        return self._gid


class PruebasJuego(unittest.TestCase):
    def test_turno_inicial(self):
        g = Juego(Jugador("A"), Jugador("B"))
        self.assertEqual(g.jugador_actual.nombre, "A")

    def test_tirar_devuelve_3_valores(self):
        g = Juego(Jugador("A"), Jugador("B"))
        r = g.tirar()
        self.assertEqual(len(r), 3)

    def test_indice_inicial_valido_1(self):
        g = Juego(Jugador("A"), Jugador("B"), indice_inicial=1)
        self.assertEqual(g.jugador_actual.nombre, "B")

    def test_indice_inicial_invalido_se_normaliza_a_0(self):
        g = Juego(Jugador("A"), Jugador("B"), indice_inicial=9)
        self.assertEqual(g.jugador_actual.nombre, "A")

    def test_cambiar_turno(self):
        g = Juego(Jugador("A"), Jugador("B"))
        self.assertEqual(g.jugador_actual.nombre, "A")
        g.cambiar_turno()
        self.assertEqual(g.jugador_actual.nombre, "B")

    def test_termino_y_ganador_none(self):
        g = Juego(Jugador("A"), Jugador("B"))
        self.assertFalse(g.termino())
        self.assertIsNone(g.ganador())

    def test_ganador_devuelto(self):
        a = Jugador("A"); b = Jugador("B")
        g = Juego(a, b)
        g.__tablero__ = _TableroFalso(a.id)
        self.assertTrue(g.termino())
        self.assertEqual(g.ganador().id, a.id)

    def test_ganador_none_cuando_id_no_coincide(self):
        a = Jugador("A"); b = Jugador("B")
        g = Juego(a, b)
        g.__tablero__ = _TableroFalso(999)
        self.assertTrue(g.termino())
        self.assertIsNone(g.ganador())
    
if __name__ == "__main__":
    unittest.main()