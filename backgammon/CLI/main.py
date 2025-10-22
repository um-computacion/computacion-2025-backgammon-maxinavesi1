"""CLI para el juego de Backgammon con interfaz visual mejorada."""
import sys
from backgammon.core.juego import Juego
from backgammon.core.jugador import Jugador
from backgammon.core.tablero import PUNTOS


class Color:
    """Códigos de color ANSI para la terminal."""

    RESET = '\033[0m'
    BOLD = '\033[1m'

    # Colores de texto
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    GRAY = '\033[90m'

    # Colores de fondo
    BG_WHITE = '\033[107m'
    BG_GRAY = '\033[100m'


def ayuda():
    """Muestra ayuda simple de la CLI."""
    print(f"\n{Color.CYAN}{Color.BOLD}{'═' * 70}{Color.RESET}")
    print(f"{Color.YELLOW}{Color.BOLD}🎲 BACKGAMMON CLI 🎲{Color.RESET}")
    print(f"{Color.CYAN}{Color.BOLD}{'═' * 70}{Color.RESET}\n")

    comandos = [
        ("--tirar", "Tirar los dados"),
        ("--movs", "Ver movimientos disponibles"),
        ("--mover <desde> <hasta/24>", "Mover ficha (hasta=24 para sacar)"),
        ("--cambiar-turno", "Forzar el cambio de turno"),
        ("--semilla <n>", "Fijar semilla para tiradas reproducibles"),
        ("--ayuda | -h", "Mostrar esta ayuda"),
        ("--estado", "Ver un resumen del estado actual"),
        ("--tablero", "Ver el tablero de forma visual"),
        ("--dump-estado", "Volcar el estado completo (debug)"),
        ("--demo", "Cargar posición de práctica (debug)"),
    ]

    for cmd, desc in comandos:
        print(f"  {Color.GREEN}{cmd:30}{Color.RESET} "
              f"{Color.WHITE}{desc}{Color.RESET}")

    print(f"\n{Color.CYAN}{Color.BOLD}{'═' * 70}{Color.RESET}")
    print(f"{Color.YELLOW}Ejemplo de uso:{Color.RESET}")
    print(f"  {Color.GRAY}python -m backgammon.cli --semilla 42 "
          f"--tirar --mover 23 20{Color.RESET}")
    print(f"{Color.CYAN}{Color.BOLD}{'═' * 70}{Color.RESET}\n")


def ficha_visual(jugador_id, cantidad):
    """
    Retorna representación visual de las fichas.

    Args:
        jugador_id (int): ID del jugador propietario.
        cantidad (int): Cantidad de fichas.

    Returns:
        str: Representación visual coloreada de las fichas.
    """
    simbolo = "●"

    if jugador_id == 1:
        color = f"{Color.BG_WHITE}{Color.BOLD} "
    else:
        color = f"{Color.BG_GRAY}{Color.WHITE}{Color.BOLD} "

    if cantidad == 1:
        return f"{color}{simbolo}{Color.RESET}"
    if cantidad <= 5:
        return f"{color}{simbolo}×{cantidad}{Color.RESET}"
    return f"{color}{simbolo}×{cantidad:2}{Color.RESET}"


def mostrar_tablero(juego):
    """
    Muestra una representación visual mejorada del tablero.

    Args:
        juego (Juego): Instancia del juego actual.
    """
    j1_id = juego.jugadores[0].id
    j2_id = juego.jugadores[1].id

    print(f"\n{Color.CYAN}{Color.BOLD}{'═' * 90}{Color.RESET}")
    print(f"{Color.YELLOW}{Color.BOLD}  🎲 TABLERO DE BACKGAMMON 🎲"
          f"{Color.RESET}")
    print(f"{Color.CYAN}{Color.BOLD}{'═' * 90}{Color.RESET}")

    print(f"{Color.MAGENTA}{Color.BOLD}Turno:{Color.RESET} "
          f"{Color.WHITE}{juego.jugador_actual.nombre}{Color.RESET} "
          f"{Color.GRAY}(ID {juego.jugador_actual.id}){Color.RESET}")

    movs = juego.movimientos_disponibles()
    if movs:
        print(f"{Color.GREEN}{Color.BOLD}Dados disponibles:{Color.RESET} "
              f"{Color.YELLOW}{movs}{Color.RESET}")

    print(f"{Color.CYAN}{Color.BOLD}{'═' * 90}{Color.RESET}\n")

    # Parte superior del tablero (puntos 13-24)
    print(f"{Color.BLUE}{Color.BOLD}┌─────────────────────────────────┐ "
          f"BAR ┌─────────────────────────────────┐{Color.RESET}")

    # Números de puntos superiores
    linea_nums_sup = f"{Color.BLUE}│{Color.RESET} "
    for i in range(12, 18):
        linea_nums_sup += f"{Color.CYAN}{i:2d}{Color.RESET}  "
    linea_nums_sup += f"{Color.BLUE}│{Color.RESET} "
    linea_nums_sup += f"{Color.GRAY}BAR{Color.RESET} "
    linea_nums_sup += f"{Color.BLUE}│{Color.RESET} "
    for i in range(18, 24):
        linea_nums_sup += f"{Color.CYAN}{i:2d}{Color.RESET}  "
    linea_nums_sup += f"{Color.BLUE}│{Color.RESET}"
    print(linea_nums_sup)

    # Fichas en puntos superiores
    linea_fichas_sup = f"{Color.BLUE}│{Color.RESET} "
    for i in range(12, 18):
        fichas = juego.tablero.punto(i)
        if fichas:
            linea_fichas_sup += f"{ficha_visual(fichas[0].owner_id, len(fichas))}  "
        else:
            linea_fichas_sup += f"{Color.GRAY}───{Color.RESET} "

    linea_fichas_sup += f"{Color.BLUE}│{Color.RESET} "

    # Barra (centro)
    barra_j1 = juego.tablero.fichas_en_barra(j1_id)
    barra_j2 = juego.tablero.fichas_en_barra(j2_id)
    if barra_j1 > 0:
        linea_fichas_sup += f"{ficha_visual(j1_id, barra_j1)} "
    elif barra_j2 > 0:
        linea_fichas_sup += f"{ficha_visual(j2_id, barra_j2)} "
    else:
        linea_fichas_sup += f"{Color.GRAY}───{Color.RESET} "

    linea_fichas_sup += f"{Color.BLUE}│{Color.RESET} "

    for i in range(18, 24):
        fichas = juego.tablero.punto(i)
        if fichas:
            linea_fichas_sup += f"{ficha_visual(fichas[0].owner_id, len(fichas))}  "
        else:
            linea_fichas_sup += f"{Color.GRAY}───{Color.RESET} "
    linea_fichas_sup += f"{Color.BLUE}│{Color.RESET}"
    print(linea_fichas_sup)

    print(f"{Color.BLUE}{Color.BOLD}├─────────────────────────────────┤"
          f"     ├─────────────────────────────────┤{Color.RESET}")

    # Parte inferior del tablero (puntos 11-0)
    linea_fichas_inf = f"{Color.BLUE}│{Color.RESET} "
    for i in range(11, 5, -1):
        fichas = juego.tablero.punto(i)
        if fichas:
            linea_fichas_inf += f"{ficha_visual(fichas[0].owner_id, len(fichas))}  "
        else:
            linea_fichas_inf += f"{Color.GRAY}───{Color.RESET} "

    linea_fichas_inf += (f"{Color.BLUE}│{Color.RESET} {Color.GRAY}   {Color.RESET} "
                         f"{Color.BLUE}│{Color.RESET} ")

    for i in range(5, -1, -1):
        fichas = juego.tablero.punto(i)
        if fichas:
            linea_fichas_inf += f"{ficha_visual(fichas[0].owner_id, len(fichas))}  "
        else:
            linea_fichas_inf += f"{Color.GRAY}───{Color.RESET} "
    linea_fichas_inf += f"{Color.BLUE}│{Color.RESET}"
    print(linea_fichas_inf)

    # Números de puntos inferiores
    linea_nums_inf = f"{Color.BLUE}│{Color.RESET} "
    for i in range(11, 5, -1):
        linea_nums_inf += f"{Color.CYAN}{i:2d}{Color.RESET}  "
    linea_nums_inf += f"{Color.BLUE}│{Color.RESET}     {Color.BLUE}│{Color.RESET} "
    for i in range(5, -1, -1):
        linea_nums_inf += f"{Color.CYAN}{i:2d}{Color.RESET}  "
    linea_nums_inf += f"{Color.BLUE}│{Color.RESET}"
    print(linea_nums_inf)

    print(f"{Color.BLUE}{Color.BOLD}└─────────────────────────────────┘"
          f"     └─────────────────────────────────┘{Color.RESET}")

    # Información adicional
    print(f"\n{Color.CYAN}{'─' * 90}{Color.RESET}")

    # Mostrar fichas en barra
    print(f"{Color.YELLOW}{Color.BOLD}BARRA:{Color.RESET}", end=" ")
    if barra_j1 > 0:
        print(f"{ficha_visual(j1_id, barra_j1)} "
              f"{Color.WHITE}{juego.jugadores[0].nombre}{Color.RESET}", end="  ")
    if barra_j2 > 0:
        print(f"{ficha_visual(j2_id, barra_j2)} "
              f"{Color.WHITE}{juego.jugadores[1].nombre}{Color.RESET}", end="")
    if barra_j1 == 0 and barra_j2 == 0:
        print(f"{Color.GRAY}(vacía){Color.RESET}", end="")
    print()

    # Mostrar fichas que salieron
    salidas_j1 = juego.tablero.fichas_salidas(j1_id)
    salidas_j2 = juego.tablero.fichas_salidas(j2_id)

    print(f"{Color.YELLOW}{Color.BOLD}SALIDAS:{Color.RESET}", end=" ")
    print(f"{ficha_visual(j1_id, salidas_j1)} "
          f"{Color.WHITE}{juego.jugadores[0].nombre}: {salidas_j1}/15{Color.RESET}",
          end="  ")
    print(f"{ficha_visual(j2_id, salidas_j2)} "
          f"{Color.WHITE}{juego.jugadores[1].nombre}: {salidas_j2}/15{Color.RESET}")

    print(f"{Color.CYAN}{'─' * 90}{Color.RESET}\n")


def procesar_semilla(args, i, juego):
    """
    Procesa el comando --semilla.

    Args:
        args (list): Lista de argumentos.
        i (int): Índice actual.
        juego (Juego): Instancia del juego.

    Returns:
        tuple: (continuar, nuevo_indice)
    """
    if i + 1 >= len(args):
        print(f"{Color.RED}❌ Error: Falta <n> para --semilla{Color.RESET}")
        return False, i
    try:
        semilla = int(args[i + 1])
    except ValueError:
        print(f"{Color.RED}❌ Error: Semilla inválida: {args[i + 1]}{Color.RESET}")
        return False, i
    juego.usar_semilla(semilla)
    print(f"{Color.GREEN}✓ Semilla fijada en {semilla}{Color.RESET}")
    return True, i + 2


def procesar_mover(args, i, juego):
    """
    Procesa el comando --mover.

    Args:
        args (list): Lista de argumentos.
        i (int): Índice actual.
        juego (Juego): Instancia del juego.

    Returns:
        tuple: (continuar, nuevo_indice)
    """
    if i + 2 >= len(args):
        print(f"{Color.RED}❌ Error: Faltan <desde> <hasta> para --mover{Color.RESET}")
        return False, i

    try:
        desde = int(args[i + 1])
        hasta = int(args[i + 2])
    except ValueError:
        print(f"{Color.RED}❌ Error: Parámetros inválidos. "
              f"Ej: --mover 0 3 o --mover 22 24{Color.RESET}")
        return False, i

    # Validación adicional
    if desde < 0 or desde >= PUNTOS:
        print(f"{Color.RED}❌ Error: 'desde' fuera de rango (0-{PUNTOS-1}){Color.RESET}")
        return False, i
    if hasta < 0 or hasta > PUNTOS:
        print(f"{Color.RED}❌ Error: 'hasta' fuera de rango (0-{PUNTOS}){Color.RESET}")
        return False, i

    ok = juego.mover_ficha(desde, hasta)
    if ok:
        print(f"{Color.GREEN}✓ Movimiento exitoso:{Color.RESET} "
              f"{Color.CYAN}{desde}{Color.RESET} {Color.WHITE}→{Color.RESET} "
              f"{Color.CYAN}{hasta}{Color.RESET}")
        movs_restantes = juego.movimientos_disponibles()
        if movs_restantes:
            print(f"{Color.YELLOW}📋 Movimientos restantes: "
                  f"{movs_restantes}{Color.RESET}")
        else:
            print(f"{Color.MAGENTA}🔄 Turno cambiado a: "
                  f"{Color.BOLD}{juego.jugador_actual.nombre}{Color.RESET}")
    else:
        motivo = juego.ultimo_error() or "movimiento inválido"
        print(f"{Color.RED}❌ Movimiento rechazado:{Color.RESET} "
              f"{Color.YELLOW}{motivo}{Color.RESET}")

    return True, i + 3


def procesar_poner(args, i, juego):
    """
    Procesa el comando --poner.

    Args:
        args (list): Lista de argumentos.
        i (int): Índice actual.
        juego (Juego): Instancia del juego.

    Returns:
        tuple: (continuar, nuevo_indice)
    """
    if i + 1 >= len(args):
        print(f"{Color.RED}❌ Error: Falta <p> para --poner{Color.RESET}")
        return False, i
    try:
        punto = int(args[i + 1])
    except ValueError:
        print(f"{Color.RED}❌ Error: Punto inválido: {args[i + 1]}{Color.RESET}")
        return False, i

    if punto < 0 or punto >= PUNTOS:
        print(f"{Color.RED}❌ Error: Punto fuera de rango (0-{PUNTOS-1}){Color.RESET}")
        return False, i

    ok = juego.colocar_ficha_en(punto)
    if ok:
        print(f"{Color.GREEN}✓ Ficha colocada en punto {punto}{Color.RESET}")
    else:
        print(f"{Color.RED}❌ No se pudo colocar la ficha{Color.RESET}")
    return True, i + 2


def procesar_dump_estado(juego):
    """
    Muestra el volcado completo del estado del juego.

    Args:
        juego (Juego): Instancia del juego.
    """
    est = juego.estado_dict()
    print(f"\n{Color.CYAN}{Color.BOLD}{'═' * 70}{Color.RESET}")
    print(f"{Color.YELLOW}{Color.BOLD}DUMP DEL ESTADO COMPLETO{Color.RESET}")
    print(f"{Color.CYAN}{Color.BOLD}{'═' * 70}{Color.RESET}")
    print(f"{Color.WHITE}Estado:{Color.RESET} {est['estado']}")
    print(f"{Color.WHITE}Turno:{Color.RESET} {est['jugador_actual']} "
          f"{Color.GRAY}(id {est['jugador_actual_id']}){Color.RESET}")
    print(f"{Color.WHITE}Movimientos restantes:{Color.RESET} "
          f"{est['movs_restantes']}")
    print(f"\n{Color.YELLOW}PUNTOS CON FICHAS:{Color.RESET}")
    for idx, fichas in enumerate(est["puntos"]):
        if fichas:
            fichas_str = [f.owner_id for f in fichas]
            print(f"  {Color.CYAN}Punto {idx}:{Color.RESET} {fichas_str} "
                  f"{Color.GRAY}(n={len(fichas)}){Color.RESET}")
    if est["barra"]:
        print(f"\n{Color.YELLOW}BARRA:{Color.RESET} {est['barra']}")
    if est["salidas"]:
        print(f"{Color.YELLOW}SALIDAS:{Color.RESET} {est['salidas']}")
    print(f"{Color.CYAN}{Color.BOLD}{'═' * 70}{Color.RESET}\n")


def main():
    """Función principal de la CLI que parsea los argumentos y ejecuta comandos."""
    args = sys.argv[1:]

    if not args or args[0] in ("--ayuda", "-h"):
        ayuda()
        return

    jugador1 = Jugador("Blancas")
    jugador2 = Jugador("Negras")
    juego = Juego(jugador1, jugador2)

    juego.reiniciar()

    print(f"\n{Color.CYAN}{Color.BOLD}{'═' * 70}{Color.RESET}")
    print(f"{Color.YELLOW}{Color.BOLD}🎲 BACKGAMMON - Juego Inicializado 🎲"
          f"{Color.RESET}")
    print(f"{Color.CYAN}{Color.BOLD}{'═' * 70}{Color.RESET}")
    print(f"{Color.WHITE}Jugador 1:{Color.RESET} "
          f"{ficha_visual(jugador1.id, 1)} {Color.BOLD}{jugador1.nombre}{Color.RESET} "
          f"{Color.GRAY}(ID {jugador1.id}){Color.RESET}")
    print(f"{Color.WHITE}Jugador 2:{Color.RESET} "
          f"{ficha_visual(jugador2.id, 1)} {Color.BOLD}{jugador2.nombre}{Color.RESET} "
          f"{Color.GRAY}(ID {jugador2.id}){Color.RESET}")
    print(f"{Color.CYAN}{Color.BOLD}{'═' * 70}{Color.RESET}\n")

    i = 0
    while i < len(args):
        cmd = args[i]

        if cmd == "--semilla":
            continuar, i = procesar_semilla(args, i, juego)
            if not continuar:
                return
            continue

        if cmd == "--tirar":
            dado1, dado2, movs = juego.tirar()
            print(f"{Color.YELLOW}{Color.BOLD}🎲 Dados:{Color.RESET} "
                  f"{Color.WHITE}{dado1}{Color.RESET} y "
                  f"{Color.WHITE}{dado2}{Color.RESET} "
                  f"{Color.GREEN}→ Movimientos: {movs}{Color.RESET}")
            i += 1
            continue

        if cmd == "--movs":
            movs = juego.movimientos_disponibles()
            print(f"{Color.CYAN}📋 Movimientos disponibles:{Color.RESET} "
                  f"{Color.YELLOW}{movs}{Color.RESET}")
            i += 1
            continue

        if cmd == "--cambiar-turno":
            juego.cambiar_turno()
            print(f"{Color.MAGENTA}🔄 Turno cambiado a:{Color.RESET} "
                  f"{Color.BOLD}{juego.jugador_actual.nombre}{Color.RESET}")
            i += 1
            continue

        if cmd == "--poner":
            continuar, i = procesar_poner(args, i, juego)
            if not continuar:
                return
            continue

        if cmd == "--mover":
            continuar, i = procesar_mover(args, i, juego)
            if not continuar:
                return
            continue

        if cmd == "--estado":
            resumen = juego.resumen_estado()
            print(f"{Color.CYAN}📊 {resumen}{Color.RESET}")
            i += 1
            continue

        if cmd == "--tablero":
            mostrar_tablero(juego)
            i += 1
            continue

        if cmd == "--dump-estado":
            procesar_dump_estado(juego)
            i += 1
            continue

        if cmd == "--demo":
            juego.reiniciar()
            pid_a = juego.jugador_actual.id
            pid_b = jugador2.id
            juego.tablero.colocar_ficha(pid_a, 0)
            juego.tablero.colocar_ficha(pid_a, 0)
            juego.tablero.colocar_ficha(pid_b, PUNTOS - 1)
            juego.tablero.colocar_ficha(pid_b, PUNTOS - 1)
            print(f"{Color.GREEN}✓ Demo cargada: 2 fichas de cada jugador "
                  f"en extremos opuestos{Color.RESET}")
            mostrar_tablero(juego)
            i += 1
            continue

        print(f"{Color.RED}❌ Comando no reconocido:{Color.RESET} {cmd}")
        ayuda()
        return

    # Al finalizar todos los comandos, verificar si hay ganador
    if juego.termino():
        ganador = juego.ganador()
        print(f"\n{Color.YELLOW}{Color.BOLD}{'═' * 70}{Color.RESET}")
        print(f"{Color.GREEN}{Color.BOLD}🏆 ¡JUEGO TERMINADO! 🏆{Color.RESET}")
        print(f"{Color.YELLOW}{Color.BOLD}Ganador: {ganador.nombre} "
              f"(ID {ganador.id}){Color.RESET}")
        print(f"{Color.YELLOW}{Color.BOLD}{'═' * 70}{Color.RESET}\n")


if __name__ == "__main__":
    main()