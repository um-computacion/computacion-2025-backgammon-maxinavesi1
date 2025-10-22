"""Módulo de la clase Checker, representa una ficha individual del juego Backgammon."""


class Checker:
    """
    Representa una ficha individual del juego Backgammon.
    Su única responsabilidad es mantener la identidad de su dueño.
    """

    def __init__(self, jugador_id: int):
        """
        Inicializa la ficha con el ID de su jugador propietario.

        Recibe:
            jugador_id (int): ID del jugador propietario.
        Devuelve:
            None
        """
        self.__pid__ = jugador_id

    @property
    def owner_id(self) -> int:
        """
        Devuelve el ID del jugador propietario de la ficha.
        """
        return self.__pid__

    def __eq__(self, other):
        """Permite comparar si dos Checkers son del mismo propietario (por ID)."""
        if isinstance(other, Checker):
            return self.owner_id == other.owner_id
        if isinstance(other, int):
            return self.owner_id == other
        return NotImplemented

    def __repr__(self) -> str:
        """Representación de string para debug."""
        return f"Checker(PID={self.__pid__})"