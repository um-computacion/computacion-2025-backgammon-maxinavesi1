import sys
from backgammon.core.juego import Juego
from backgammon.core.jugador import Jugador

def _ayuda():
    """Muestra ayuda simple de la CLI."""
    print("Backgammon CLI")
    print("Uso:")
    print("  --tirar                     # tirar los dados")
    print("  --movs                      # ver movimientos disponibles")
    print("  --poner <p>                 # colocar ficha del jugador actual en el punto p")
    print("  --mover <desde> <hasta>     # mover ficha si la distancia está en los movimientos")
    print("  --semilla <n>               # fija semilla para tiradas reproducibles")
    print("  --ayuda | -h                # mostrar esta ayuda")
    print("  --estado                    # ver un resumen del estado actual")
    print("  --dump-estado               # volcar el estado completo (debug)")
    print("  --demo                      # cargar posición de práctica (no oficial)")

def main():
    args = sys.argv[1:]
    if not args or args[0] in ("--ayuda", "-h"):
        _ayuda()
        return

    j1 = Jugador("Blancas")
    j2 = Jugador("Negras")
    juego = Juego(j1, j2)

    i = 0
    while i < len(args):
        cmd = args[i]

        if cmd == "--semilla":
            if i + 1 >= len(args):
                print("Falta <n> para --semilla"); return
            try:
                n = int(args[i + 1])
            except ValueError:
                print("Semilla inválida:", args[i + 1]); return
            juego.usar_semilla(n)
            print("Semilla fija en", n)
            i += 2
            continue

        if cmd == "--tirar":
            d1, d2, movs = juego.tirar()
            print("Dados:", d1, "y", d2, "→ movs:", movs)
            i += 1
            continue

        if cmd == "--movs":
            print("Movimientos disponibles:", juego.movimientos_disponibles())
            i += 1
            continue

        if cmd == "--poner":
            if i + 1 >= len(args):
                print("Falta <p> para --poner"); return
            try:
                p = int(args[i + 1])
            except ValueError:
                print("Punto inválido:", args[i + 1]); return
            ok = juego.colocar_ficha_en(p)
            print(f"Se colocó una ficha en {p}" if ok else "No se pudo colocar la ficha")
            i += 2
            continue

        if cmd == "--mover":
            if i + 2 >= len(args):
                print("Faltan <desde> <hasta> para --mover"); return
            try:
                desde = int(args[i + 1]); hasta = int(args[i + 2])
            except ValueError:
                print("Parámetros inválidos. Ej: --mover 0 3"); return
            ok = juego.mover_ficha(desde, hasta)
            print("Movimiento:", "OK" if ok else "NO se pudo")
            print("Movs restantes:", juego.movimientos_disponibles())
            i += 3
            continue

        if cmd == "--estado":
            print(juego.resumen_estado())
            i += 1
            continue

        if cmd == "--dump-estado":
            est = juego.estado_dict()
            print("estado:", est["estado"])
            print("turno:", est["jugador_actual"], "(id", est["jugador_actual_id"], ")")
            print("movs_restantes:", est["movs_restantes"])
            for idx, fichas in enumerate(est["puntos"]):
                if fichas:
                    print(f"punto {idx}: {fichas} (n={len(fichas)})")
            if est["barra"]:
                print("barra:", est["barra"])
            if est["salidas"]:
                print("salidas:", est["salidas"])
            i += 1
            continue
        if cmd == "--demo":
            juego.reiniciar()  
            pid_a = juego.jugador_actual.id
            pid_b = juego._Juego__jugadores__[1].id
            juego._Juego__tablero__.colocar_ficha(pid_a, 0)
            juego._Juego__tablero__.colocar_ficha(pid_a, 0)
            juego._Juego__tablero__.colocar_ficha(pid_b, 23)
            juego._Juego__tablero__.colocar_ficha(pid_b, 23)

            print("Demo: [A,A] en 0 y [B,B] en 23 (posición de práctica)")
            i += 1
            continue

        print("Comando no reconocido:", cmd)
        _ayuda()
        return

if __name__ == "__main__":
    main()
