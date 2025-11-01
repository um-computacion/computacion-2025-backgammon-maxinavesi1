"""Interfaz Gráfica de Backgammon utilizando Pygame

Muestra el tablero con la posición inicial estándar y permite movimientos, capturas
y bearing off (sacar fichas).

Teclas:
  ESC   → salir
  T     → tirar dados (solo una vez por turno)
  R     → reiniciar a la posición inicial estándar
  H     → mostrar/ocultar ayuda
  D     → deseleccionar ficha (o click en espacio vacío)
"""
import sys
import pygame
from backgammon.core.juego import Juego
from backgammon.core.jugador import Jugador
from backgammon.core.tablero import PUNTOS

ANCHO = 1000
ALTO = 750
FPS = 60

MARGEN_X = 40
MARGEN_Y_TABLERO = 120
MARGEN_Y_BOTTOM = 40

BG_COLOR = (245, 239, 230)
BOARD_COLOR = (230, 220, 200)
TRI_A = (170, 120, 90)
TRI_B = (210, 170, 130)
LINE = (60, 60, 60)

COLOR_TEXTO = (25, 25, 25)
COLOR_J1 = (245, 245, 245)
COLOR_J2 = (30, 30, 30)
COLOR_HINT = (90, 180, 90)
COLOR_SELECCION = (255, 215, 0)

MAX_VISIBLE_STACK = 5
OUT_BAR_W = 60
OUT_BAR_X_J1 = ANCHO - MARGEN_X - OUT_BAR_W
OUT_BAR_X_J2 = MARGEN_X

HUD_HEIGHT = 100

# Constante especial para indicar selección de barra
BARRA_SELECCION = -1


class BoardGeometry:
    """Geometría del tablero para evitar variables globales mutables."""

    def __init__(self):
        self.rect = None
        self.tri_width = 0
        self.bar_rect = None

    def get_rect(self) -> pygame.Rect:
        """Calcula y retorna el rectángulo del tablero interno con márgenes."""
        if self.rect is None:
            self.rect = pygame.Rect(
                MARGEN_X + OUT_BAR_W,
                MARGEN_Y_TABLERO + 20,
                ANCHO - 2 * MARGEN_X - 2 * OUT_BAR_W,
                ALTO - MARGEN_Y_TABLERO - MARGEN_Y_BOTTOM - 20
            )
            self.tri_width = self.rect.width / 12.0
        return self.rect

    def get_tri_width(self) -> float:
        """Retorna el ancho de cada triángulo."""
        if self.rect is None:
            self.get_rect()
        return self.tri_width

    def get_bar_rect(self) -> pygame.Rect:
        """Retorna el rectángulo de la barra central."""
        if self.bar_rect is None:
            board_rect = self.get_rect()
            bar_x = board_rect.centerx - 30
            self.bar_rect = pygame.Rect(bar_x, board_rect.top, 60, board_rect.height)
        return self.bar_rect


BOARD = BoardGeometry()


def point_index_to_display(idx: int) -> tuple[str, int]:
    """Mapea el índice lógico (0-23) al cuadrante y columna visual (0-11)."""
    if 0 <= idx <= 11:
        return 'top', 11 - idx
    return 'bottom', idx - 12


def point_center(idx: int) -> tuple[int, int]:
    """Calcula el centro horizontal de un punto para dibujar marcadores."""
    board_rect = BOARD.get_rect()
    row, col_vis = point_index_to_display(idx)
    x_pos = int(board_rect.left + col_vis * BOARD.get_tri_width() +
                BOARD.get_tri_width() / 2)
    y_pos = board_rect.top if row == 'top' else board_rect.bottom
    return x_pos, y_pos


def dibujar_triangulos(surface: pygame.Surface) -> None:
    """Dibuja los 24 triángulos (puntos) del tablero."""
    board_rect = BOARD.get_rect()
    tri_width = BOARD.get_tri_width()

    for col_vis in range(12):
        x_0 = board_rect.left + col_vis * tri_width
        x_1 = x_0 + tri_width
        x_m = (x_0 + x_1) / 2.0

        tip_y = board_rect.top + board_rect.height * 0.42
        pts = [(x_0, board_rect.top), (x_1, board_rect.top), (x_m, tip_y)]
        color = TRI_A if col_vis % 2 == 0 else TRI_B
        pygame.draw.polygon(surface, color, pts)

        tip_y = board_rect.bottom - board_rect.height * 0.42
        pts = [(x_0, board_rect.bottom), (x_1, board_rect.bottom), (x_m, tip_y)]
        color = TRI_B if col_vis % 2 == 0 else TRI_A
        pygame.draw.polygon(surface, color, pts)


def dibujar_marco_y_labels(
    surface: pygame.Surface,
    font: pygame.font.Font
) -> None:
    """Dibuja el marco y la numeración 12..0 / 13..24."""
    board_rect = BOARD.get_rect()
    tri_width = BOARD.get_tri_width()

    pygame.draw.rect(surface, BOARD_COLOR, board_rect, border_radius=12)
    pygame.draw.rect(surface, LINE, board_rect, 2, border_radius=12)
    pygame.draw.line(
        surface, LINE,
        (board_rect.left, board_rect.centery),
        (board_rect.right, board_rect.centery), 1
    )

    # CORRECCIÓN: Ahora incluye el punto 0
    top_labels = [str(i) for i in range(12, -1, -1)]  # 12, 11, 10... 1, 0
    for col_vis, lbl in enumerate(top_labels):
        x_pos = int(board_rect.left + col_vis * tri_width + tri_width / 2)
        y_pos = board_rect.top - 14
        img = font.render(lbl, True, COLOR_TEXTO)
        surface.blit(img, img.get_rect(center=(x_pos, y_pos)))

    bottom_labels = [str(i) for i in range(13, 25)]
    for col_vis, lbl in enumerate(bottom_labels):
        x_pos = int(board_rect.left + col_vis * tri_width + tri_width / 2)
        y_pos = board_rect.bottom + 14
        img = font.render(lbl, True, COLOR_TEXTO)
        surface.blit(img, img.get_rect(center=(x_pos, y_pos)))


def draw_checker(
    surface: pygame.Surface,
    center: tuple[int, int],
    radius: int,
    color_rgb: tuple[int, int, int],
    label: int | None,
    font: pygame.font.Font
) -> None:
    """Dibuja una ficha individual con su borde y etiqueta de stack si aplica."""
    pygame.draw.circle(surface, color_rgb, center, radius)
    pygame.draw.circle(surface, LINE, center, radius, 2)
    if label:
        label_color = LINE if color_rgb == COLOR_J1 else COLOR_J1
        txt = font.render(str(label), True, label_color)
        surface.blit(txt, txt.get_rect(center=center))


def dibujar_punto_seleccionado(
    surface: pygame.Surface,
    idx: int | None,
    juego: Juego
) -> None:
    """Dibuja un indicador visual en el punto seleccionado."""
    if idx is None or idx == PUNTOS:
        return

    # NUEVO: Indicador especial para barra seleccionada
    if idx == BARRA_SELECCION:
        bar_rect = BOARD.get_bar_rect()
        pygame.draw.rect(surface, COLOR_SELECCION, bar_rect, 5, border_radius=8)

        # Mostrar texto de ayuda
        font = pygame.font.Font(None, 20)
        pid = juego.jugador_actual.id
        entrada = juego._entrada_para(pid)
        txt = font.render(f"Click en punto {entrada} para entrar", True, (255, 140, 0))
        surface.blit(txt, (bar_rect.centerx - 100, bar_rect.centery - 10))
        return

    x_pos, y_pos = point_center(idx)
    pygame.draw.circle(surface, COLOR_SELECCION, (x_pos, y_pos), 35, 4)
    pygame.draw.circle(
        surface, (*COLOR_SELECCION[:3], 100), (x_pos, y_pos), 32, 2
    )


def _dibujar_fichas_en_punto(
    surface: pygame.Surface,
    idx: int,
    pila: list,
    j1_id: int,
    board_rect: pygame.Rect,
    tri_width: float,
    font: pygame.font.Font
) -> None:
    """Dibuja las fichas de un punto específico."""
    radius = int(tri_width * 0.38)
    radius = max(12, min(radius, 22))
    vgap = 4
    step = radius * 2 + vgap

    def color(pid):
        return COLOR_J1 if pid == j1_id else COLOR_J2

    row, col_vis = point_index_to_display(idx)
    c_x = int(board_rect.left + col_vis * tri_width + tri_width / 2)

    visibles = min(len(pila), MAX_VISIBLE_STACK)
    extras = 0
    if len(pila) > MAX_VISIBLE_STACK:
        extras = max(0, len(pila) - (MAX_VISIBLE_STACK - 1))

    if row == 'top':
        c_y = int(board_rect.top + radius + 6)
        for i in range(visibles):
            pid = pila[i].owner_id
            lbl = extras if (extras and i == visibles - 1) else None
            draw_checker(
                surface, (c_x, c_y + i * step), radius, color(pid), lbl, font
            )
    else:
        c_y = int(board_rect.bottom - radius - 6)
        for i in range(visibles):
            pid = pila[i].owner_id
            lbl = extras if (extras and i == visibles - 1) else None
            draw_checker(
                surface, (c_x, c_y - i * step), radius, color(pid), lbl, font
            )


def dibujar_fichas(
    surface: pygame.Surface,
    juego: Juego,
    font: pygame.font.Font
) -> None:
    """Dibuja las fichas apiladas en los puntos del tablero."""
    board_rect = BOARD.get_rect()
    tri_width = BOARD.get_tri_width()
    tablero = juego.tablero
    j1_id = juego.jugadores[0].id

    for idx in range(PUNTOS):
        pila = tablero.punto(idx)
        if pila:
            _dibujar_fichas_en_punto(
                surface, idx, pila, j1_id, board_rect, tri_width, font
            )


def _dibujar_fichas_barra(
    surface: pygame.Surface,
    bar_rect: pygame.Rect,
    cantidad: int,
    color: tuple[int, int, int],
    desde_arriba: bool,
    font: pygame.font.Font
) -> None:
    """Dibuja fichas en la barra para un jugador."""
    if cantidad == 0:
        return

    board_rect = BOARD.get_rect()
    txt_color = COLOR_TEXTO if color == COLOR_J1 else COLOR_J1
    txt = font.render(str(cantidad), True, txt_color)

    if desde_arriba:
        cy_start = board_rect.top + 30
        cy_step = 25
        for i in range(min(cantidad, 5)):
            c_y = cy_start + i * cy_step
            draw_checker(
                surface, (bar_rect.centerx, c_y), 12, color, None, font
            )
        txt_pos_y = cy_start + min(cantidad, 5) * cy_step
        surface.blit(txt, (bar_rect.centerx - 10, txt_pos_y))
    else:
        cy_start = board_rect.bottom - 30
        cy_step = 25
        for i in range(min(cantidad, 5)):
            c_y = cy_start - i * cy_step
            draw_checker(
                surface, (bar_rect.centerx, c_y), 12, color, None, font
            )
        txt_pos_y = cy_start - min(cantidad, 5) * cy_step - 20
        surface.blit(txt, (bar_rect.centerx - 10, txt_pos_y))


def dibujar_barra(
    surface: pygame.Surface,
    juego: Juego,
    font: pygame.font.Font
) -> None:
    """Muestra cuántas fichas tiene cada jugador en la barra central (Bar)."""
    j1_id = juego.jugadores[0].id
    j2_id = juego.jugadores[1].id

    barra_1 = juego.tablero.fichas_en_barra(j1_id)
    barra_2 = juego.tablero.fichas_en_barra(j2_id)

    bar_rect = BOARD.get_bar_rect()
    pygame.draw.rect(surface, (200, 200, 200), bar_rect, border_radius=8)
    pygame.draw.rect(surface, LINE, bar_rect, 2, border_radius=8)

    _dibujar_fichas_barra(
        surface, bar_rect, barra_1, COLOR_J1, True, font
    )
    _dibujar_fichas_barra(
        surface, bar_rect, barra_2, COLOR_J2, False, font
    )


def _dibujar_bearing_off_single(
    surface: pygame.Surface,
    rect: pygame.Rect,
    salidas: int,
    label: str,
    font: pygame.font.Font
) -> None:
    """Dibuja una barra de bearing off para un jugador."""
    pygame.draw.rect(surface, BOARD_COLOR, rect, border_radius=8)
    pygame.draw.rect(surface, LINE, rect, 2, border_radius=8)

    if salidas > 0:
        txt = font.render(label, True, COLOR_TEXTO)
        rect_top = rect.top - MARGEN_Y_TABLERO + HUD_HEIGHT
        surface.blit(
            txt, txt.get_rect(center=(rect.centerx, rect_top + 15))
        )
        num = font.render(str(salidas), True, COLOR_TEXTO)
        surface.blit(
            num, num.get_rect(center=(rect.centerx, rect_top + 35))
        )


def draw_bearing_off_bar(
    surface: pygame.Surface,
    juego: Juego,
    font: pygame.font.Font
) -> None:
    """Dibuja las barras laterales de Bearing Off (Salida) y el conteo."""
    board_rect = BOARD.get_rect()
    j1_id = juego.jugadores[0].id
    j2_id = juego.jugadores[1].id

    j1_salidas = juego.tablero.fichas_salidas(j1_id)
    rect_j1 = pygame.Rect(
        OUT_BAR_X_J1,
        board_rect.top,
        OUT_BAR_W,
        board_rect.height
    )
    _dibujar_bearing_off_single(surface, rect_j1, j1_salidas, "J1 OUT", font)

    j2_salidas = juego.tablero.fichas_salidas(j2_id)
    rect_j2 = pygame.Rect(
        OUT_BAR_X_J2,
        board_rect.top,
        OUT_BAR_W,
        board_rect.height
    )
    _dibujar_bearing_off_single(surface, rect_j2, j2_salidas, "J2 OUT", font)


def _tiene_movimientos_validos(juego: Juego, punto: int) -> bool:
    """Verifica si un punto tiene movimientos válidos."""
    movs = juego.movimientos_disponibles()
    if not movs:
        return False

    pid = juego.jugador_actual.id

    if juego.tablero.fichas_en_barra(pid) > 0:
        entrada = juego._entrada_para(pid)
        return punto == entrada

    for mov in movs:
 #J1 (impar) decrementa, J2 (par) incrementa
        destino = (punto - mov) if pid % 2 != 0 else (punto + mov)

        if 0 <= destino < PUNTOS:
            ok, _ = juego._validar_movimiento(punto, destino)
            if ok:
                return True

        if juego.tablero.puede_sacar_fichas(pid):
            ok, _ = juego._validar_movimiento(punto, PUNTOS)
            if ok:
                return True

    return False


def dibujar_hints(
    surface: pygame.Surface,
    origen: int | None,
    movs: list[int],
    juego: Juego
) -> None:
    """Dibuja pistas visuales (puntos verdes) en los destinos posibles."""
    if not movs:
        return

    board_rect = BOARD.get_rect()
    pid = juego.jugador_actual.id
    posibles = set()

    fichas_barra = juego.tablero.fichas_en_barra(pid)

    # NUEVO: Si seleccionó la barra, mostrar punto de entrada
    if origen == BARRA_SELECCION and fichas_barra > 0:
        entrada = juego._entrada_para(pid)

        # Mostrar hints en todos los puntos posibles desde la entrada
        for mov in movs:
            # ✅ CORRECCIÓN: desde barra, J1 incrementa desde 0, J2 decrementa desde 23
            destino = entrada + mov if pid % 2 != 0 else entrada - mov
            if 0 <= destino < PUNTOS:
                ok, _ = juego._validar_movimiento(entrada, destino)
                if ok:
                    posibles.add(destino)

        # Dibujar los hints
        for idx in posibles:
            x_pos, y_pos = point_center(idx)
            pygame.draw.circle(surface, COLOR_HINT, (x_pos, y_pos), 10)
            pygame.draw.circle(surface, (50, 150, 50), (x_pos, y_pos), 10, 2)
        return

    # Si tiene fichas en barra pero NO seleccionó nada, mostrar advertencia
    if fichas_barra > 0 and origen is None:
        entrada = juego._entrada_para(pid)
        bar_rect = BOARD.get_bar_rect()

        # Destacar la barra
        pygame.draw.rect(surface, (255, 140, 0), bar_rect, 4, border_radius=8)

        # Mostrar mensaje
        font = pygame.font.Font(None, 18)
        txt = font.render("¡Click en BARRA!", True, (255, 100, 0))
        surface.blit(txt, (bar_rect.centerx - 60, bar_rect.top - 20))
        return

    if origen is None:
        return

    for distancia in movs:
        # J1 (impar) decrementa en tablero, J2 (par) incrementa en tablero
        if pid % 2 != 0:
            destino_fwd = origen - distancia
        else:
            destino_fwd = origen + distancia

        if 0 <= destino_fwd < PUNTOS:
            ok_mov, _ = juego._validar_movimiento(origen, destino_fwd)
            if ok_mov:
                posibles.add(destino_fwd)

        if juego.tablero.puede_sacar_fichas(pid):
            ok_sacar, _ = juego._validar_movimiento(origen, PUNTOS)
            if ok_sacar:
                posibles.add(PUNTOS)

    for idx in posibles:
        if idx == PUNTOS:
            out_x = OUT_BAR_X_J1 if pid % 2 != 0 else OUT_BAR_X_J2
            rect = pygame.Rect(
                out_x + 10, board_rect.centery - 15, OUT_BAR_W - 20, 30
            )
            pygame.draw.rect(surface, COLOR_HINT, rect, border_radius=8)
        else:
            x_pos, y_pos = point_center(idx)
            pygame.draw.circle(surface, COLOR_HINT, (x_pos, y_pos), 8)
            pygame.draw.circle(surface, (50, 100, 50), (x_pos, y_pos), 8, 2)


def mostrar_ayuda(surface: pygame.Surface, font: pygame.font.Font) -> None:
    """Muestra overlay con controles e instrucciones."""
    overlay = pygame.Surface((ANCHO, ALTO))
    overlay.set_alpha(220)
    overlay.fill((0, 0, 0))
    surface.blit(overlay, (0, 0))

    titulo_font = pygame.font.Font(None, 48)
    titulo = titulo_font.render("AYUDA", True, (255, 215, 0))
    surface.blit(titulo, titulo.get_rect(center=(ANCHO // 2, 150)))

    textos = [
        "",
        "CONTROLES:",
        "T - Tirar dados (una vez por turno)",
        "D o ESC - Deseleccionar ficha",
        "R - Reiniciar juego",
        "H - Mostrar/Ocultar ayuda",
        "",
        "JUGABILIDAD:",
        "• Click en un punto para seleccionar tu ficha",
        "• Si tienes fichas capturadas, click en la BARRA CENTRAL",
        "• Click en otro punto para moverla",
        "• Los puntos verdes muestran movimientos válidos",
        "• Click en la barra lateral para sacar fichas",
        "• El turno cambia automáticamente al usar todos los dados",
        "",
        "Presiona H para cerrar"
    ]

    y_inicial = 190
    for i, txt in enumerate(textos):
        color = (255, 255, 0) if txt.endswith(":") else (255, 255, 255)
        render = font.render(txt, True, color)
        surface.blit(render, (ANCHO // 2 - 280, y_inicial + i * 26))


def punto_desde_xy(x_pos: int, y_pos: int) -> int | None:
    """Mapear click a índice 0..23 en el tablero central."""
    board_rect = BOARD.get_rect()
    tri_width = BOARD.get_tri_width()

    fila_sup = y_pos < board_rect.centery
    base_y = board_rect.top if fila_sup else board_rect.bottom

    if x_pos < board_rect.left or x_pos >= board_rect.right:
        return None

    col = int((x_pos - board_rect.left) // tri_width)
    if not 0 <= col <= 11:
        return None

    if abs(y_pos - base_y) > (board_rect.height * 0.5):
        return None

    if fila_sup:
        idx = 11 - col
    else:
        idx = 12 + col
    return idx


def point_or_out_bar_from_xy(x_pos: int, y_pos: int, juego: Juego) -> int | None:
    """Mapear click a índice 0..23, BARRA_SELECCION, o PUNTOS (Bearing Off)."""
    # NUEVO: Detectar click en barra central
    bar_rect = BOARD.get_bar_rect()
    if bar_rect.collidepoint(x_pos, y_pos):
        # Solo permitir seleccionar la barra si el jugador tiene fichas ahí
        pid = juego.jugador_actual.id
        if juego.tablero.fichas_en_barra(pid) > 0:
            return BARRA_SELECCION
        return None

    idx = punto_desde_xy(x_pos, y_pos)
    if idx is not None:
        return idx

    board_rect = BOARD.get_rect()
    rect_out_j1 = pygame.Rect(
        OUT_BAR_X_J1, board_rect.top, OUT_BAR_W, board_rect.height
    )
    rect_out_j2 = pygame.Rect(
        OUT_BAR_X_J2, board_rect.top, OUT_BAR_W, board_rect.height
    )

    if (rect_out_j1.collidepoint(x_pos, y_pos) or
            rect_out_j2.collidepoint(x_pos, y_pos)):
        return PUNTOS

    return None


def manejar_evento_tirada(juego: Juego, font: pygame.font.Font):
    """Maneja el evento de tirar dados."""
    if juego.movimientos_disponibles():
        return font.render(
            "❌ Ya tiraste los dados. Usá tus movimientos primero.",
            True,
            (200, 50, 50)
        )

    dado1, dado2, movs = juego.tirar()

    pid = juego.jugador_actual.id
    tiene_movimientos = False

    if juego.tablero.fichas_en_barra(pid) > 0:
        entrada = juego._entrada_para(pid)
        for mov in movs:
            # ✅ CORRECCIÓN: desde barra, J1 incrementa desde 0, J2 decrementa desde 23
            destino = entrada + mov if pid % 2 != 0 else entrada - mov
            if 0 <= destino < PUNTOS:
                ok, _ = juego._validar_movimiento(entrada, destino)
                if ok:
                    tiene_movimientos = True
                    break
    else:
        for punto in range(PUNTOS):
            fichas = juego.tablero.punto(punto)
            if fichas and fichas[0].owner_id == pid:
                for mov in movs:
                    # J1 (impar) decrementa en tablero, J2 (par) incrementa en tablero
                    destino = (punto - mov) if pid % 2 != 0 else (punto + mov)
                    if 0 <= destino < PUNTOS:
                        ok, _ = juego._validar_movimiento(punto, destino)
                        if ok:
                            tiene_movimientos = True
                            break
                    if juego.tablero.puede_sacar_fichas(pid):
                        ok, _ = juego._validar_movimiento(punto, PUNTOS)
                        if ok:
                            tiene_movimientos = True
                            break
                if tiene_movimientos:
                    break

    if not tiene_movimientos:
        mensaje = f"🎲 {dado1}-{dado2} → ❌ Sin movimientos válidos"
        juego.cambiar_turno()
        mensaje += f" | Turno: {juego.jugador_actual.nombre}"
    else:
        mensaje = f"🎲 Dados: {dado1} y {dado2} → {movs}"
        if dado1 == dado2:
            mensaje = f"🎲 ¡DOBLES! {dado1}-{dado1} (×4)"

    return font.render(mensaje, True, COLOR_TEXTO)


def manejar_movimiento(
    juego: Juego,
    sel: int,
    idx: int,
    font: pygame.font.Font
):
    """Maneja el intento de movimiento de una ficha."""
    # NUEVO: Si seleccionó la barra, obtener el punto de entrada
    if sel == BARRA_SELECCION:
        pid = juego.jugador_actual.id
        sel = juego._entrada_para(pid)

    resultado = juego.mover_ficha(sel, idx)

    if resultado:
        movs_restantes = juego.movimientos_disponibles()

        if idx == PUNTOS:
            msg = f"✓ Sacada {sel}. "
        else:
            msg = f"✓ {sel}→{idx}. "

        if not movs_restantes:
            msg += f"✅ Turno: {juego.jugador_actual.nombre}"
        else:
            msg += f"Quedan: {movs_restantes}"

        if juego.termino():
            msg = f"🏆 ¡{juego.ganador().nombre} GANÓ!"
    else:
        error = juego.ultimo_error() or 'inválido'
        msg = f"❌ {sel}→{idx}: {error}"

    return resultado, font.render(msg, True, COLOR_TEXTO)


def _validar_seleccion(
    seleccionado: int | None,
    juego: Juego
) -> int | None:
    """Valida que la selección actual sea válida para el jugador actual."""
    if seleccionado is None or seleccionado == PUNTOS or seleccionado == BARRA_SELECCION:
        return seleccionado

    pid = juego.jugador_actual.id
    fichas_en_punto = juego.tablero.punto(seleccionado)
    if not any(f.owner_id == pid for f in fichas_en_punto):
        return None
    return seleccionado


def _manejar_tecla(
    tecla: int,
    juego: Juego,
    font: pygame.font.Font
) -> tuple[bool, pygame.Surface | None, int | None, bool]:
    """Maneja eventos de teclado."""
    if tecla == pygame.K_ESCAPE:
        return False, None, None, False

    if tecla == pygame.K_t:
        txt = manejar_evento_tirada(juego, font)
        return True, txt, None, False

    if tecla == pygame.K_d:
        txt = font.render("↩️ Deseleccionado", True, COLOR_TEXTO)
        return True, txt, None, False

    if tecla == pygame.K_r:
        juego.reiniciar()
        txt = font.render("♻️ Reiniciado", True, COLOR_TEXTO)
        return True, txt, None, False

    return True, None, None, None


def _manejar_click(
    pos: tuple[int, int],
    seleccionado: int | None,
    juego: Juego,
    font: pygame.font.Font
) -> tuple[int | None, pygame.Surface | None]:
    """Maneja eventos de click del mouse."""
    idx = point_or_out_bar_from_xy(*pos, juego)

    if idx is None:
        if seleccionado is not None:
            txt = font.render("↩️ Deseleccionado", True, COLOR_TEXTO)
            return None, txt
        return None, None

    if seleccionado is None:
        # NUEVO: Permitir seleccionar la barra
        if idx == BARRA_SELECCION:
            return BARRA_SELECCION, None

        if idx == PUNTOS:
            return None, None

        pid = juego.jugador_actual.id
        fichas_barra = juego.tablero.fichas_en_barra(pid)

        if fichas_barra > 0:
            msg = "❌ Primero reingresa tus fichas de la BARRA (click en barra central)"
            return None, font.render(msg, True, (200, 50, 50))

        fichas = juego.tablero.punto(idx)
        if not any(f.owner_id == pid for f in fichas):
            msg = "❌ No tienes fichas en ese punto."
            return None, font.render(msg, True, (200, 50, 50))

        if not _tiene_movimientos_validos(juego, idx):
            msg = f"❌ Punto {idx}: sin movimientos válidos"
            return None, font.render(msg, True, (200, 50, 50))

        return idx, None

    if idx == seleccionado:
        txt = font.render("↩️ Deseleccionado", True, COLOR_TEXTO)
        return None, txt

    ok_mov, ultimo_txt = manejar_movimiento(juego, seleccionado, idx, font)
    if ok_mov:
        return None, ultimo_txt
    return seleccionado, ultimo_txt


def _dibujar_hud(
    surface: pygame.Surface,
    juego: Juego,
    ultimo_txt: pygame.Surface | None,
    f24: pygame.font.Font,
    f16: pygame.font.Font
) -> None:
    """Dibuja el HUD en la barra superior (fuera del tablero)."""
    hud_rect = pygame.Rect(0, 0, ANCHO, HUD_HEIGHT)
    pygame.draw.rect(surface, (220, 215, 210), hud_rect)
    pygame.draw.line(surface, LINE, (0, HUD_HEIGHT), (ANCHO, HUD_HEIGHT), 2)

    movs = juego.movimientos_disponibles()

    titulo = f24.render("🎲 Backgammon", True, COLOR_TEXTO)
    surface.blit(titulo, (15, 12))

    controles = "[T:tirar] [D:deselec] [R:reiniciar] [H:ayuda]"
    ctrl_render = f16.render(controles, True, (100, 100, 100))
    surface.blit(ctrl_render, (15, 42))

    estado = f"{juego.estado} | Turnos automáticos"
    estado_render = f16.render(estado, True, (120, 120, 120))
    surface.blit(estado_render, (15, 64))

    turno_color = COLOR_J1 if juego.jugador_actual.id % 2 != 0 else COLOR_J2
    turno_bg = (100, 180, 100) if movs else (180, 100, 100)

    turno_rect = pygame.Rect(ANCHO - 320, 10, 305, 80)
    pygame.draw.rect(surface, turno_bg, turno_rect, border_radius=12)
    pygame.draw.rect(surface, LINE, turno_rect, 3, border_radius=12)

    simbolo = "●" if juego.jugador_actual.id % 2 != 0 else "○"
    nombre_font = pygame.font.Font(None, 32)
    nombre = nombre_font.render(
        f"{simbolo} {juego.jugador_actual.nombre}",
        True,
        turno_color
    )
    surface.blit(nombre, (turno_rect.x + 15, turno_rect.y + 12))

    if movs:
        movs_txt = f"Dados: {movs}"
    else:
        movs_txt = "Presiona T para tirar"

    dados_render = f16.render(movs_txt, True, COLOR_TEXTO)
    surface.blit(dados_render, (turno_rect.x + 15, turno_rect.y + 50))

    if ultimo_txt:
        msg_y = HUD_HEIGHT + 5
        msg_rect = pygame.Rect(
            15, msg_y, ultimo_txt.get_width() + 20, 30
        )
        pygame.draw.rect(surface, (240, 240, 240), msg_rect, border_radius=8)
        pygame.draw.rect(surface, LINE, msg_rect, 2, border_radius=8)
        surface.blit(ultimo_txt, (25, msg_y + 7))


def iniciar_ui(ancho: int = ANCHO, alto: int = ALTO) -> None:
    """Función principal que inicia la interfaz gráfica del juego."""
    pygame.init()
    pygame.font.init()

    flags = pygame.SCALED if hasattr(pygame, "SCALED") else 0
    screen = pygame.display.set_mode((ancho, alto), flags=flags)
    pygame.display.set_caption("Backgammon — Computación 2025")
    clock = pygame.time.Clock()

    f24 = pygame.font.Font(None, 24)
    f20 = pygame.font.Font(None, 20)
    f18 = pygame.font.Font(None, 18)
    f16 = pygame.font.Font(None, 16)

    jugador1 = Jugador("Blancas")
    jugador2 = Jugador("Negras")
    juego = Juego(jugador1, jugador2)
    juego.reiniciar()

    ultimo_txt = None
    seleccionado: int | None = None
    mostrar_ayuda_flag = False

    corriendo = True
    while corriendo:
        BOARD.get_rect()
        seleccionado = _validar_seleccion(seleccionado, juego)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                corriendo = False

            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_h:
                    mostrar_ayuda_flag = not mostrar_ayuda_flag
                elif evento.key == pygame.K_ESCAPE and mostrar_ayuda_flag:
                    mostrar_ayuda_flag = False
                elif evento.key == pygame.K_ESCAPE and seleccionado is not None:
                    seleccionado = None
                    ultimo_txt = f18.render("↩️ Deseleccionado", True, COLOR_TEXTO)
                else:
                    cont, txt, sel, ayuda = _manejar_tecla(
                        evento.key, juego, f18
                    )
                    if not cont:
                        corriendo = False
                    if txt:
                        ultimo_txt = txt
                    if sel is not None:
                        seleccionado = sel
                    if ayuda is not None:
                        mostrar_ayuda_flag = ayuda

            elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                if not mostrar_ayuda_flag:
                    nuevo_sel, txt = _manejar_click(
                        evento.pos, seleccionado, juego, f18
                    )
                    if txt:
                        ultimo_txt = txt
                    if nuevo_sel is not None or txt:
                        seleccionado = nuevo_sel

        screen.fill(BG_COLOR)
        _dibujar_hud(screen, juego, ultimo_txt, f24, f16)
        draw_bearing_off_bar(screen, juego, f20)
        dibujar_marco_y_labels(screen, f20)
        dibujar_triangulos(screen)
        dibujar_punto_seleccionado(screen, seleccionado, juego)
        dibujar_hints(
            screen, seleccionado, juego.movimientos_disponibles(), juego
        )
        dibujar_fichas(screen, juego, f20)
        dibujar_barra(screen, juego, f20)

        if mostrar_ayuda_flag:
            mostrar_ayuda(screen, f18)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit(0)


if __name__ == "__main__":
    iniciar_ui()