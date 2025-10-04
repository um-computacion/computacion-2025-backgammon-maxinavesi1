"""Módulo de dados del juego."""

import random

class Dados:
    """Maneja tiradas de dados."""

    def __init__(self, semilla=None):
        """Inicializa el generador de números aleatorios."""
        self.__semilla__ = semilla
        self.__rng__ = random.Random(semilla)
        self.__ultimo_tiro__ = None

    def tirar(self):
        """Tira dos dados y calcula los movimientos.
        Returns:
            tuple[int, int, list[int]]: d1, d2 y lista de movimientos.
        """
        d1 = self.__rng__.randint(1, 6)
        d2 = self.__rng__.randint(1, 6)
        if d1 == d2:
            movimientos = [d1, d1, d1, d1]
        else:
            movimientos = [d1, d2]
        self.__ultimo_tiro__ = (d1, d2, movimientos)
        return d1, d2, movimientos

    def ultimo_tiro(self):
        """Devuelve el último tiro registrado (o None si no hubo)."""
        return self.__ultimo_tiro__
    
    def test_ultimo_tiro_actualiza(self):
        d = Dados(semilla=7)
        assert d.ultimo_tiro() is None
        d1, d2, movs = d.tirar()
        assert d.ultimo_tiro() == (d1, d2, movs)

    def fijar_semilla(self, semilla):
        import random  
        self.__semilla__ = semilla
        self.__rng__ = random.Random(semilla)
        self.__ultimo_tiro__ = None
