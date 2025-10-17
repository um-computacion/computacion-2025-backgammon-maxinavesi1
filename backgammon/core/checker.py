class Checker:
    """
    Representa una ficha individual del juego Backgammon.
    Una ficha tiene un propietario (Jugador ID).
    """

    def __init__(self, jugador_id: int):
        """
        Inicializa la ficha.
        
        Recibe:
            jugador_id (int): ID del jugador propietario de esta ficha.
        Devuelve:
            None
        """
        self._pid_ = jugador_id 
        
    @property
    def owner_id(self) -> int:
        """
        Devuelve el ID del jugador propietario de la ficha.
        """
        return self._pid_

    def __eq__(self, other):
        """Permite comparar si dos Checkers son del mismo propietario (por ID)."""
        if isinstance(other, Checker):
            return self.owner_id == other.owner_id
        if isinstance(other, int):
            return self.owner_id == other
        return NotImplemented

    def __repr__(self) -> str:
        """Representación de string para debug."""
        return f"Checker(PID={self._pid_})"