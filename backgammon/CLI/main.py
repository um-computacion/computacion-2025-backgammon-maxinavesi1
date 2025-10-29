"""Interfaz de línea de comandos para el juego de Backgammon."""
from backgammon.core.juego import Juego
from backgammon.core.jugador import Jugador


def limpiar_pantalla():
    """Limpia la pantalla de la consola."""
    print("\n" * 50)


def dibujar_tablero(juego):
    """
    Dibuja el tablero de Backgammon de forma visual.

    Args:
        juego: Instancia del juego de Backgammon.
    """
    tablero = juego.tablero
    j1_id = juego.jugadores[0].id
    j2_id = juego.jugadores[1].id

    # Símbolos para las fichas
    simbolo_j1 = "●"  # Círculo lleno para jugador 1
    simbolo_j2 = "○"  # Círculo vacío para jugador 2

    print("\n" + "═" * 70)
    print("TABLERO DE BACKGAMMON".center(70))
    print("═" * 70)

    # Parte superior del tablero (puntos 12-23)
    print("\n┌" + "─" * 68 + "┐")

    # Números de puntos superiores
    print("│ ", end="")
    for i in range(12, 24):
        print(f"{i:2d} ", end="")
        if i == 17:
            print(" │ ", end="")
    print("│")

    # Mostrar fichas en puntos superiores (5 niveles)
    for nivel in range(5):
        print("│ ", end="")
        for punto in range(12, 24):
            fichas = tablero.punto(punto)
            if len(fichas) > nivel:
                simbolo = simbolo_j1 if fichas[nivel].owner_id == j1_id else simbolo_j2
                print(f" {simbolo} ", end="")
            else:
                print("   ", end="")
            if punto == 17:
                print(" │ ", end="")
        print("│")

    # Línea divisoria central con información de barra
    barra_j1 = tablero.fichas_en_barra(j1_id)
    barra_j2 = tablero.fichas_en_barra(j2_id)
    print("├" + "─" * 33 + "┤ BARRA ├" + "─" * 24 + "┤")
    print(
        f"│{' ' * 33}│ {simbolo_j1}×{barra_j1} {simbolo_j2}×{barra_j2} │{' ' * 24}│"
    )

    # Mostrar fichas en puntos inferiores (5 niveles)
    for nivel in range(4, -1, -1):
        print("│ ", end="")
        for punto in range(11, -1, -1):
            fichas = tablero.punto(punto)
            if len(fichas) > nivel:
                simbolo = simbolo_j1 if fichas[nivel].owner_id == j1_id else simbolo_j2
                print(f" {simbolo} ", end="")
            else:
                print("   ", end="")
            if punto == 6:
                print(" │ ", end="")
        print("│")

    # Números de puntos inferiores
    print("│ ", end="")
    for i in range(11, -1, -1):
        print(f"{i:2d} ", end="")
        if i == 6:
            print(" │ ", end="")
    print("│")

    print("└" + "─" * 68 + "┘")

    # Información de fichas sacadas
    salidas_j1 = tablero.fichas_salidas(j1_id)
    salidas_j2 = tablero.fichas_salidas(j2_id)
    print(f"\nFICHAS FUERA: {juego.jugadores[0].nombre} ({simbolo_j1}): {salidas_j1}/15"
          f"  |  {juego.jugadores[1].nombre} ({simbolo_j2}): {salidas_j2}/15")


def obtener_nombre_jugador(numero_jugador):
    """
    Solicita el nombre de un jugador.

    Args:
        numero_jugador (int): Número del jugador (1 o 2).

    Returns:
        str: Nombre del jugador ingresado.
    """
    while True:
        nombre = input(
            f"Ingresá el nombre del Jugador {numero_jugador}: "
        ).strip()
        if nombre and len(nombre) <= 20:
            return nombre
        if len(nombre) > 20:
            print("Error: El nombre no puede tener más de 20 caracteres.")
        else:
            print("Error: El nombre no puede estar vacío.")


def obtener_punto(mensaje="Ingresá el número de punto (0-23)"):
    """
    Solicita un número de punto del tablero.

    Args:
        mensaje (str): Mensaje a mostrar al usuario.

    Returns:
        int: Número de punto válido o 24 para sacar ficha.
    """
    while True:
        try:
            entrada = input(f"{mensaje}: ").strip().upper()
            if entrada == 'SALIR' or entrada == 'S':
                return None
            if entrada == 'FUERA':
                return 24
            punto = int(entrada)
            if 0 <= punto <= 24:
                return punto
            print("Error: El punto debe estar entre 0 y 23 (o 24 para sacar).")
        except ValueError:
            print("Error: Ingresá un número, 'FUERA' para sacar o 'S' para salir.")


def obtener_movimiento(juego):
    """
    Solicita al jugador un movimiento completo.

    Args:
        juego: Instancia del juego.

    Returns:
        tuple: (origen, destino) o None si cancela.
    """
    pid = juego.jugador_actual.id

    # Verificar si hay fichas en la barra
    if juego.tablero.fichas_en_barra(pid) > 0:
        print("\n⚠️  Tenés fichas en la BARRA. Debés reingresarlas primero.")
        entrada = juego._entrada_para(pid)
        print(f"   Punto de entrada: {entrada}")
        destino = obtener_punto(f"Ingresá el dado a usar (destino desde {entrada})")
        if destino is None:
            return None
        return entrada, destino

    print("\n--- INGRESÁ TU MOVIMIENTO ---")
    print("(Ingresá 'S' para cancelar)")

    origen = obtener_punto("Punto ORIGEN")
    if origen is None:
        return None

    # Si origen es 24, no es válido como origen
    if origen == 24:
        print("Error: No podés usar 24 como origen. Usá el número del punto.")
        return None

    destino = obtener_punto("Punto DESTINO (o 'FUERA' para sacar)")
    if destino is None:
        return None

    return origen, destino


def mostrar_movimientos_posibles(juego):
    """
    Muestra todos los movimientos posibles que el jugador puede realizar.

    Args:
        juego: Instancia del juego de Backgammon.
    """
    jugador_id = juego.jugador_actual.id
    movimientos_dados = juego.movimientos_disponibles()

    if not movimientos_dados:
        print("\n⚠️  No hay dados disponibles. Tirá los dados primero (opción T).")
        return

    # Verificar si hay fichas en la barra
    if juego.tablero.fichas_en_barra(jugador_id) > 0:
        entrada = juego._entrada_para(jugador_id)
        print(f"\n🚨 MOVIMIENTOS POSIBLES (desde BARRA - punto {entrada}):")
        print("─" * 60)
        for dado in sorted(movimientos_dados, reverse=True):
            destino = entrada + dado if jugador_id % 2 == 0 else entrada - dado
            if 0 <= destino <= 23:
                # Verificar si el movimiento es válido
                punto_destino = juego.tablero.punto(destino)
                puede = len([f for f in punto_destino if f.owner_id != jugador_id]) <= 1
                estado = "✅" if puede else "❌"
                print(f"  {estado} Dado {dado}: Barra → Punto {destino}")
            else:
                print(f"  ❌ Dado {dado}: Fuera de rango")
        print("─" * 60)
        return

    # Buscar todos los puntos con fichas del jugador
    puntos_con_fichas = []
    for punto in range(24):
        fichas = juego.tablero.punto(punto)
        if fichas and fichas[0].owner_id == jugador_id:
            puntos_con_fichas.append((punto, len(fichas)))

    if not puntos_con_fichas:
        print("\n⚠️  No tenés fichas en el tablero.")
        return

    print("\n🎯 MOVIMIENTOS POSIBLES:")
    print("=" * 70)

    movimientos_validos = []

    # Verificar si puede hacer bearing off
    puede_bearing = juego._validar_bearing_off(jugador_id)

    for punto_origen, cantidad in puntos_con_fichas:
        for dado in sorted(movimientos_dados, reverse=True):
            # Calcular destino según dirección del jugador
            if jugador_id % 2 == 1:  # Jugador impar
                destino = punto_origen - dado
            else:  # Jugador par
                destino = punto_origen + dado

            # Verificar bearing off
            if puede_bearing:
                home_inicio = 0 if jugador_id % 2 == 1 else 18
                home_fin = 5 if jugador_id % 2 == 1 else 23
                en_home = home_inicio <= punto_origen <= home_fin

                if en_home and (destino < 0 or destino > 23):
                    # Bearing off exacto
                    movimientos_validos.append((
                        punto_origen,
                        "FUERA",
                        dado,
                        cantidad,
                        "✅ Bearing off"
                    ))
                    continue
                elif en_home and (
                    (jugador_id % 2 == 1 and destino < 0) or
                    (jugador_id % 2 == 0 and destino > 23)
                ):
                    # Over-bearing: verificar si es la más lejana
                    puntos_mas_lejos = [
                        p for p, _ in puntos_con_fichas
                        if (jugador_id % 2 == 1 and p > punto_origen) or
                           (jugador_id % 2 == 0 and p < punto_origen)
                    ]
                    if not puntos_mas_lejos:
                        movimientos_validos.append((
                            punto_origen,
                            "FUERA",
                            dado,
                            cantidad,
                            "✅ Over-bearing"
                        ))
                    continue

            # Movimiento normal
            if 0 <= destino <= 23:
                punto_destino = juego.tablero.punto(destino)
                fichas_enemigas = [f for f in punto_destino if f.owner_id != jugador_id]

                if len(fichas_enemigas) <= 1:
                    descripcion = "✅ OK"
                    if len(fichas_enemigas) == 1:
                        descripcion = "✅ Captura ficha enemiga"
                    elif len(punto_destino) > 0:
                        descripcion = "✅ Apila con tus fichas"

                    movimientos_validos.append((
                        punto_origen,
                        destino,
                        dado,
                        cantidad,
                        descripcion
                    ))

    # Mostrar movimientos agrupados por punto de origen
    if movimientos_validos:
        punto_actual = None
        for origen, destino, dado, cantidad, desc in sorted(movimientos_validos):
            if origen != punto_actual:
                if punto_actual is not None:
                    print()
                fichas_str = f"({cantidad} ficha{'s' if cantidad > 1 else ''})"
                print(f"📍 Desde PUNTO {origen} {fichas_str}:")
                punto_actual = origen

            destino_str = "FUERA (24)" if destino == "FUERA" else f"Punto {destino}"
            print(f"   • Dado {dado}: → {destino_str:12} {desc}")

        print("=" * 70)
        print(f"💡 Total: {len(movimientos_validos)} movimiento(s) posible(s)")
    else:
        print("❌ No hay movimientos válidos con estos dados.")
        print("   Deberás pasar el turno.")
        print("=" * 70)


def mostrar_info_jugador(juego):
    """
    Muestra información del jugador actual y sus movimientos.

    Args:
        juego: Instancia del juego de Backgammon.
    """
    jugador = juego.jugador_actual
    movimientos = juego.movimientos_disponibles()

    print("\n" + "┌" + "─" * 68 + "┐")
    print(f"│ 🎲 TURNO DE: {jugador.nombre} (Jugador {jugador.id})".ljust(70) + "│")

    if movimientos:
        movs_str = ", ".join(str(m) for m in sorted(movimientos, reverse=True))
        print(f"│ 📋 Dados disponibles: [{movs_str}]".ljust(70) + "│")
    else:
        print("│ ⚠️  No hay dados disponibles. Tirá los dados.".ljust(70) + "│")

    # Información adicional
    barra = juego.tablero.fichas_en_barra(jugador.id)
    if barra > 0:
        print(f"│ 🚨 Fichas en BARRA: {barra} (¡Debés reingresarlas!)".ljust(70) + "│")

    print("└" + "─" * 68 + "┘")


def obtener_accion():
    """
    Solicita al jugador qué acción quiere realizar.

    Returns:
        str: 'T' tirar dados, 'M' mover, 'V' ver movimientos, 'P' pasar, 'S' salir.
    """
    print("\n╔═══════════════════════════════════════╗")
    print("║           ACCIONES DISPONIBLES        ║")
    print("╠═══════════════════════════════════════╣")
    print("║  T - Tirar dados                      ║")
    print("║  V - Ver movimientos posibles         ║")
    print("║  M - Mover ficha                      ║")
    print("║  P - Pasar turno                      ║")
    print("║  S - Salir del juego                  ║")
    print("╚═══════════════════════════════════════╝")

    while True:
        accion = input("\n¿Qué querés hacer? (T/V/M/P/S): ").strip().upper()
        if accion in ('T', 'V', 'M', 'P', 'S'):
            return accion
        print("❌ Error: Ingresá T, V, M, P o S.")


def turno_juego(juego):
    """
    Ejecuta un turno completo del juego.

    Args:
        juego: Instancia del juego de Backgammon.

    Returns:
        bool: False si el usuario quiere salir, True en otro caso.
    """
    # Mostrar tablero al inicio del turno
    limpiar_pantalla()
    dibujar_tablero(juego)
    mostrar_info_jugador(juego)

    while True:
        accion = obtener_accion()

        if accion == 'S':
            return False

        if accion == 'T':
            if juego.movimientos_disponibles():
                print("\n⚠️  Ya tenés dados disponibles. Usá M para mover o V para ver opciones.")
                input("\n[Presioná ENTER para continuar]")
            else:
                dado1, dado2, movs = juego.tirar()
                print(f"\n🎲 ¡Tiraste! Dados: {dado1} y {dado2}")
                if dado1 == dado2:
                    print(f"   🎉 ¡DOBLES! Podés mover 4 veces con {dado1}")
                else:
                    movs_str = ", ".join(str(m) for m in sorted(movs, reverse=True))
                    print(f"   Movimientos disponibles: [{movs_str}]")

                input("\n[Presioná ENTER para ver movimientos posibles]")

                # Actualizar pantalla y mostrar movimientos posibles automáticamente
                limpiar_pantalla()
                dibujar_tablero(juego)
                mostrar_info_jugador(juego)
                mostrar_movimientos_posibles(juego)
                input("\n[Presioná ENTER para continuar]")

        elif accion == 'V':
            if not juego.movimientos_disponibles():
                print("\n❌ No tenés dados disponibles. Tirá primero (opción T).")
                input("\n[Presioná ENTER para continuar]")
            else:
                mostrar_movimientos_posibles(juego)
                input("\n[Presioná ENTER para continuar]")

        elif accion == 'M':
            if not juego.movimientos_disponibles():
                print("\n❌ No tenés dados disponibles. Tirá primero (opción T).")
                input("\n[Presioná ENTER para continuar]")
                continue

            movimiento = obtener_movimiento(juego)
            if movimiento is None:
                print("\n↩️  Movimiento cancelado.")
                input("\n[Presioná ENTER para continuar]")
                continue

            origen, destino = movimiento

            try:
                resultado = juego.mover_ficha(origen, destino)
                if resultado:
                    print("\n✅ ¡Movimiento exitoso!")

                    # Actualizar tablero inmediatamente después del movimiento
                    limpiar_pantalla()
                    dibujar_tablero(juego)
                    mostrar_info_jugador(juego)

                    # Verificar si quedan movimientos
                    if not juego.movimientos_disponibles():
                        print("\n   ℹ️  No te quedan más movimientos. El turno pasa "
                              "automáticamente.")
                        input("\n[Presioná ENTER para continuar]")
                        return True
                    else:
                        movs_str = ", ".join(
                            str(m) for m in sorted(
                                juego.movimientos_disponibles(), reverse=True
                            )
                        )
                        print(f"\n   📋 Te quedan dados: [{movs_str}]")
                        print("   💡 Usá V para ver movimientos posibles")
                        input("\n[Presioná ENTER para continuar]")
                        # Continuar en el loop para permitir más movimientos
                        continue
                else:
                    print(f"\n❌ Movimiento inválido: {juego.ultimo_error()}")

                input("\n[Presioná ENTER para continuar]")
            except (ValueError, AttributeError, TypeError, KeyError) as error:
                print(f"\n❌ Error al procesar movimiento: {error}")
                input("\n[Presioná ENTER para continuar]")

        elif accion == 'P':
            if juego.movimientos_disponibles():
                confirmacion = input(
                    "\n⚠️  Todavía tenés dados. ¿Seguro que querés pasar? (S/N): "
                ).strip().upper()
                if confirmacion != 'S':
                    continue

            print("\n➡️  Pasaste el turno.")
            juego.cambiar_turno()
            input("\n[Presioná ENTER para continuar]")
            return True

        # Actualizar pantalla después de cada acción (excepto movimientos que ya actualizan)
        if accion in ('T', 'V', 'P'):
            limpiar_pantalla()
            dibujar_tablero(juego)
            mostrar_info_jugador(juego)


def mostrar_bienvenida():
    """Muestra la pantalla de bienvenida."""
    print("\n" + "╔" + "═" * 68 + "╗")
    print("║" + "BACKGAMMON".center(68) + "║")
    print("║" + "Juego de mesa clásico para 2 jugadores".center(68) + "║")
    print("╚" + "═" * 68 + "╝")


def mostrar_reglas():
    """Muestra las reglas básicas del juego."""
    print("\n╔═══════════════════════════════════════════════════════════════════╗")
    print("║                         REGLAS BÁSICAS                            ║")
    print("╠═══════════════════════════════════════════════════════════════════╣")
    print("║ • Cada jugador tiene 15 fichas que debe mover alrededor del      ║")
    print("║   tablero y sacarlas antes que su oponente.                      ║")
    print("║                                                                   ║")
    print("║ • Jugador 1 (●) mueve de punto 23 → 0                           ║")
    print("║ • Jugador 2 (○) mueve de punto 0 → 23                           ║")
    print("║                                                                   ║")
    print("║ • Tirás dos dados y movés la cantidad indicada.                  ║")
    print("║ • Si sacás DOBLES, movés 4 veces ese número.                     ║")
    print("║                                                                   ║")
    print("║ • Podés capturar fichas solitarias del oponente.                 ║")
    print("║ • Si te capturan, tu ficha va a la BARRA y debés reingresarla.  ║")
    print("║                                                                   ║")
    print("║ • Para sacar fichas, todas deben estar en tu HOME (últimos 6).   ║")
    print("║ • ¡El primero en sacar todas sus 15 fichas GANA!                 ║")
    print("╚═══════════════════════════════════════════════════════════════════╝")

    input("\n[Presioná ENTER para comenzar]")


def mostrar_ganador(juego):
    """
    Muestra la pantalla de victoria.

    Args:
        juego: Instancia del juego de Backgammon.
    """
    ganador = juego.ganador()
    if ganador:
        print("\n" + "╔" + "═" * 68 + "╗")
        print("║" + "¡JUEGO TERMINADO!".center(68) + "║")
        print("╠" + "═" * 68 + "╣")
        print("║" + " ".center(68) + "║")
        print("║" + f"🏆 ¡GANADOR: {ganador.nombre}! 🏆".center(68) + "║")
        print("║" + " ".center(68) + "║")
        print("╚" + "═" * 68 + "╝")
    else:
        print("\n╔═══════════════════════════════════════╗")
        print("║   Juego terminado sin ganador         ║")
        print("╚═══════════════════════════════════════╝")


def main():
    """Función principal que ejecuta el juego de Backgammon."""
    limpiar_pantalla()
    mostrar_bienvenida()

    print("\n¿Querés ver las reglas? (S/N): ", end="")
    if input().strip().upper() == 'S':
        mostrar_reglas()

    print("\n")
    nombre1 = obtener_nombre_jugador(1)
    nombre2 = obtener_nombre_jugador(2)

    jugador1 = Jugador(nombre1)
    jugador2 = Jugador(nombre2)

    juego = Juego(jugador1, jugador2)

    # Configurar posición inicial estándar
    juego.tablero.posicion_inicial_estandar(jugador1.id, jugador2.id)

    print("\n¡Que comience el juego!")
    print(f"{nombre1} (●) vs {nombre2} (○)")
    input("\n[Presioná ENTER para comenzar]")

    # Loop principal del juego
    while not juego.termino():
        continuar = turno_juego(juego)
        if not continuar:
            print("\n👋 Saliendo del juego...")
            return

    # Mostrar resultado final
    limpiar_pantalla()
    dibujar_tablero(juego)
    mostrar_ganador(juego)


if __name__ == "__main__":
    main()