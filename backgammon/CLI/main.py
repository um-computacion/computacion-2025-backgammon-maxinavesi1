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
    print("  --mover <desde> <hasta>     # mover ficha si la distancia está en los movimientos")
    print("  --ayuda | -h                # mostrar esta ayuda")
    
    args = sys.argv[1:]
    if args and args[0] in ("--ayuda", "-h"):
        _ayuda()
        return
    if not args:
        _ayuda()
        return

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

    if cmd == "--tirar":
        d1, d2, movs = juego.tirar()
        print("Dados:", d1, "y", d2, "→ movs:", movs)
        return

    if cmd == "--movs":
        print("Movimientos disponibles:", juego.movimientos_disponibles())
        return

    if cmd == "--poner" and len(args) >= 2:
        try:
            p = int(args[1])
        except ValueError:
            print("Punto inválido:", args[1]); return
        pid = juego.jugador_actual.id
        juego._Juego__tablero__.colocar_ficha(pid, p)  
        print(f"Se colocó una ficha en el punto {p} para {juego.jugador_actual.nombre}")
        return

    if cmd == "--mover" and len(args) >= 3:
        try:
            desde = int(args[1]); hasta = int(args[2])
        except ValueError:
            print("Parámetros inválidos. Ej: --mover 0 3"); return
        ok = juego.aplicar_movimiento(desde, hasta)
        print("Movimiento:", "OK" if ok else "NO se pudo")
        print("Movs restantes:", juego.movimientos_disponibles())
        return

    print("Comando no reconocido.")
    _ayuda()

    if cmd == "--poner" and len(args) >= 2:
        try:
            p = int(args[1])
        except ValueError:
            print("Punto inválido:", args[1])
            return
        pid = juego.jugador_actual.id
        juego.__tablero__.colocar_ficha(pid, p)
        print(f"Se colocó una ficha en el punto {p} para {juego.jugador_actual.nombre}")
        return
    
    if cmd == "--mover" and len(args) >= 3:
        try:
            desde = int(args[1]); hasta = int(args[2])
        except ValueError:
            print("Parámetros inválidos. Ej: --mover 0 3")
            return
        ok = juego.aplicar_movimiento(desde, hasta)
        print("Movimiento:", "OK" if ok else "NO se pudo")
        print("Movs restantes:", juego.movimientos_disponibles())
        return


if __name__ == "__main__":
    main()