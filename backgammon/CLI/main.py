import sys
from backgammon.core.juego import Juego
from backgammon.core.jugador import Jugador

def _ayuda():
    print("Backgammon CLI")
    print("Uso:")
    print("  --tirar                     # tirar los dados")
    print("  --movs                      # ver movimientos disponibles")
    print("  --poner <p>                 # colocar ficha del jugador actual en el punto p")
    print("  --mover <desde> <hasta>     # mover ficha si la distancia está en los movimientos")

def main():
    j1 = Jugador("Blancas")
    j2 = Jugador("Negras")
    juego = Juego(j1, j2)

    args = sys.argv[1:]
    if not args:
        _ayuda()
        print("Turno inicial:", juego.jugador_actual.nombre)
        return

    cmd = args[0]