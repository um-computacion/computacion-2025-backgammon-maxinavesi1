class Jugador:
    _contador_ids = 1  

    def __init__(self, nombre):
        self.__nombre__ = nombre
        self.id = Jugador._contador_ids
        Jugador._contador_ids += 1

    @property
    def nombre(self):
        return self.__nombre__
