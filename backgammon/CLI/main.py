"""CLI mínima para probar el juego.

Uso:
    python -m backgammon.cli.main
    python -m backgammon.cli.main --tirar
    python -m backgammon.cli.main --tirar --semilla 123
"""

import sys
from backgammon.core.juego import Juego
from backgammon.core.jugador import Jugador

def main():
    """Crea dos jugadores, instancia el juego y permite tirar dados con --tirar."""
    # argumentos muy simples (sin argparse para no complicar)
    args = sys.argv[1:]
    usar_tirar = "--tirar" in args
    semilla = None
    if "--semilla" in args:
        try:
            i = args.index("--semilla")
            semilla = int(args[i + 1])
        except Exception:
            print("Uso de --semilla: --semilla <entero>")

    j1 = Jugador("Blancas")
    j2 = Jugador("Negras")
    juego = Juego(j1, j2)
    if semilla is not None:
        juego.usar_semilla(semilla)

    if usar_tirar:
        d1, d2, movs = juego.tirar()
        print("Dados:", d1, "y", d2, "→ movimientos:", movs)
        return

    print("Backgammon CLI")
    print("Turno inicial:", juego.jugador_actual.nombre)

if __name__ == "__main__":
    main()
