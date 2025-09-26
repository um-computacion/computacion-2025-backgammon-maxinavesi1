
class Jugador:
    """Representa a un jugador con nombre e id autoincremental."""
    _contador_ids = 1

    def __init__(self, nombre):
        """Guarda el nombre y asigna un id."""
        self.__nombre__ = nombre
        self.id = Jugador._contador_ids
        Jugador._contador_ids += 1

    @property
    def nombre(self):
        """Devuelve el nombre del jugador."""
        return self.__nombre__
