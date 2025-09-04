"""CLI mínima para probar el juego.

Uso:
    python -m backgammon.cli.main
    python -m backgammon.cli.main --tirar
"""

import sys
from backgammon.core.juego import Juego
from backgammon.core.jugador import Jugador

def main():
    """Crea dos jugadores, instancia el juego y permite tirar dados con --tirar."""
    j1 = Jugador("Blancas")
    j2 = Jugador("Negras")
    juego = Juego(j1, j2)

    if len(sys.argv) > 1 and sys.argv[1] == "--tirar":
        d1, d2, movs = juego.tirar()
        print("Dados:", d1, "y", d2, "→ movimientos:", movs)
        return

    print("Backgammon CLI")
    print("Turno inicial:", juego.jugador_actual.nombre)

if __name__ == "__main__":
    main()

