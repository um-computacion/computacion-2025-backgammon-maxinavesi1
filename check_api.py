from backgammon.core.juego import Juego
from backgammon.core.jugador import Jugador
g = Juego(Jugador("A"), Jugador("B"))
print("Tiene colocar_ficha_en:", hasattr(g, "colocar_ficha_en"))
print("Tiene mover_ficha:", hasattr(g, "mover_ficha"))
