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
     
    def test_movimientos_quedan_guardados_y_son_copia(self):
        g = Juego(Jugador("A"), Jugador("B"))
        d1, d2, movs = g.tirar()
        self.assertEqual(sorted(g.movimientos_disponibles()), sorted(movs))
        copia = g.movimientos_disponibles()
        copia.clear()
        self.assertEqual(sorted(g.movimientos_disponibles()), sorted(movs))

    def test_movimientos_disponibles_y_aplicar(self):
        g = Juego(Jugador("A"), Jugador("B"))
        g.__movs_restantes__ = [3]
        pid = g.jugador_actual.id
        g.__tablero__.colocar_ficha(pid, 0)
        ok = g.aplicar_movimiento(0, 3)
        self.assertTrue(ok)
        self.assertEqual(g.movimientos_disponibles(), [])
        self.assertEqual(g.__tablero__.punto(0), [])
        self.assertEqual(g.__tablero__.punto(3), [pid])

    def test_aplicar_movimiento_distancia_invalida(self):
        g = Juego(Jugador("A"), Jugador("B"))
        g.__movs_restantes__ = [2]
        pid = g.jugador_actual.id
        g.__tablero__.colocar_ficha(pid, 0)
        ok = g.aplicar_movimiento(0, 3)
        self.assertFalse(ok)
        self.assertEqual(g.__tablero__.punto(0), [pid])
        self.assertEqual(g.__tablero__.punto(3), [])

    def test_juego_usar_semilla_reproduce(self):
        g = Juego(Jugador("A"), Jugador("B"))
        g.usar_semilla(9)
        a = g.tirar()
        g.usar_semilla(9)
        b = g.tirar()
        self.assertEqual(a, b)

if __name__ == "__main__":
    unittest.main() 