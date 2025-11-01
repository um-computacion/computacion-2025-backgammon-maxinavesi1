"""Módulo de la clase Jugador, responsable de la identidad de cada participante."""


class Jugador:
    """Representa a un jugador con nombre e id autoincremental."""
    _contador_ids = 1

    def __init__(self, nombre):
        """
        Guarda el nombre y asigna un id autoincremental.

        Recibe:
            nombre (str): Nombre del jugador.
        Devuelve:
            None
        """
        self.__nombre__ = nombre
        self.__id__ = Jugador._contador_ids
        Jugador._contador_ids += 1

    @property
    def nombre(self):
        """Devuelve el nombre del jugador."""
        return self.__nombre__

    @property
    def id(self):
        """Devuelve el ID único del jugador."""
        return self.__id__