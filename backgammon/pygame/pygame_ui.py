"""Interfaz Gráfica de Backgammon utilizando Pygame

Muestra el tablero con la posición inicial estándar y permite movimientos, capturas
y bearing off (sacar fichas).

Teclas:
  ESC   → salir
  T     → tirar dados
  C     → cambiar turno
  R     → reiniciar a la posición inicial estándar
  H     → mostrar/ocultar ayuda
"""
import sys
import pygame
from backgammon.core.juego import Juego
from backgammon.core.jugador import Jugador
from backgammon.core.tablero import PUNTOS

ANCHO = 1000
ALTO = 700
FPS = 60

MARGEN_X = 40
MARGEN_Y = 40

BG_COLOR = (245, 239, 230)
BOARD_COLOR = (230, 220, 200)
TRI_A = (170, 120, 90)
TRI_B = (210, 170, 130)
LINE = (60, 60, 60)

COLOR_TEXTO = (25, 25, 25)
COLOR_J1 = (245, 245, 245)
COLOR_J2 = (30, 30, 30)
COLOR_HINT = (90, 180, 90)
COLOR_SELECCION = (255, 215, 0)  # Dorado para punto seleccionado

MAX_VISIBLE_STACK = 5
OUT_BAR_W = 60
OUT_BAR_X_J1 = ANCHO - MARGEN_X - OUT_BAR_W
OUT_BAR_X_J2 = MARGEN_X


class BoardGeometry:
    """Geometría del tablero para evitar variables globales mutables."""

    def __init__(self):
        self.rect = None
        self.tri_width = 0

    def get_rect(self) -> pygame.Rect:
        """Calcula y retorna el rectángulo del tablero interno con márgenes."""
        if self.rect is None:
            self.rect = pygame.Rect(
                MARGEN_X + OUT_BAR_W,
                MARGEN_Y + 20,
                ANCHO - 2 * MARGEN_X - 2 * OUT_BAR_W,
                ALTO - 2 * MARGEN_Y - 40
            )
            self.tri_width = self.rect.width / 12.0
        return self.rect

    def get_tri_width(self) -> float:
        """Retorna el ancho de cada triángulo."""
        if self.rect is None:
            self.get_rect()
        return self.tri_width


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


def dibujar_marco_y_labels(surface: pygame.Surface,
                           font: pygame.font.Font) -> None:
    """Dibuja el marco y la numeración 12..1 / 13..24."""
    board_rect = BOARD.get_rect()
    tri_width = BOARD.get_tri_width()

    pygame.draw.rect(surface, BOARD_COLOR, board_rect, border_radius=12)
    pygame.draw.rect(surface, LINE, board_rect, 2, border_radius=12)
    pygame.draw.line(
        surface, LINE,
        (board_rect.left, board_rect.centery),
        (board_rect.right, board_rect.centery), 1
    )

    top_labels = [str(i) for i in range(12, 0, -1)]
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
    pygame.draw.circle(surface, LINE, center, radius, 2)  # Borde más grueso
    if label:
        label_color = LINE if color_rgb == COLOR_J1 else COLOR_J1
        txt = font.render(str(label), True, label_color)
        surface.blit(txt, txt.get_rect(center=center))


def dibujar_punto_seleccionado(surface: pygame.Surface, idx: int | None) -> None:
    """Dibuja un indicador visual en el punto seleccionado."""
    if idx is None or idx == PUNTOS:
        return

    x_pos, y_pos = point_center(idx)
    # Círculo pulsante dorado
    pygame.draw.circle(surface, COLOR_SELECCION, (x_pos, y_pos), 35, 4)
    # Círculo interior para efecto de resplandor
    pygame.draw.circle(surface, (*COLOR_SELECCION[:3], 100), (x_pos, y_pos), 32, 2)


def dibujar_fichas(
    surface: pygame.Surface,
    juego: Juego,
    font: pygame.font.Font
) -> None:
    """Dibuja las fichas apiladas en los puntos del tablero."""
    board_rect = BOARD.get_rect()
    tri_width = BOARD.get_tri_width()

    radius = int(tri_width * 0.38)
    radius = max(12, min(radius, 22))
    vgap = 4
    step = radius * 2 + vgap

    tablero = juego.tablero
    j1_id = juego.jugadores[0].id

    def color(pid):
        return COLOR_J1 if pid == j1_id else COLOR_J2

    for idx in range(PUNTOS):
        row, col_vis = point_index_to_display(idx)
        c_x = int(board_rect.left + col_vis * tri_width + tri_width / 2)

        pila = tablero.punto(idx)
        if not pila:
            continue

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


def dibujar_barra(
    surface: pygame.Surface,
    juego: Juego,
    font: pygame.font.Font
) -> None:
    """Muestra cuántas fichas tiene cada jugador en la barra central (Bar)."""
    board_rect = BOARD.get_rect()
    j1_id = juego.jugadores[0].id
    j2_id = juego.jugadores[1].id

    barra_1 = juego.tablero.fichas_en_barra(j1_id)
    barra_2 = juego.tablero.fichas_en_barra(j2_id)

    # Barra más ancha y visible
    bar_x = board_rect.centerx - 20  # Era 10
    bar_rect = pygame.Rect(bar_x, board_rect.top, 40, board_rect.height)  # Era 20
    pygame.draw.rect(surface, (200, 200, 200), bar_rect, border_radius=8)
    pygame.draw.rect(surface, LINE, bar_rect, 2, border_radius=8)

    if barra_1 > 0:
        cy_start = board_rect.top + 30
        cy_step = 25
        txt_color = COLOR_TEXTO if COLOR_J1 == (245, 245, 245) else COLOR_J1
        txt = font.render(str(barra_1), True, txt_color)
        for i in range(min(barra_1, 5)):
            c_y = cy_start + i * cy_step
            draw_checker(surface, (bar_rect.centerx, c_y), 12, COLOR_J1, None, font)
        txt_pos_y = cy_start + min(barra_1, 5) * cy_step
        surface.blit(txt, (bar_rect.centerx - 10, txt_pos_y))

    if barra_2 > 0:
        cy_start = board_rect.bottom - 30
        cy_step = 25
        txt_color = COLOR_TEXTO if COLOR_J2 == (30, 30, 30) else COLOR_J2
        txt = font.render(str(barra_2), True, txt_color)
        for i in range(min(barra_2, 5)):
            c_y = cy_start - i * cy_step
            draw_checker(surface, (bar_rect.centerx, c_y), 12, COLOR_J2, None, font)
        txt_pos_y = cy_start - min(barra_2, 5) * cy_step - 20
        surface.blit(txt, (bar_rect.centerx - 10, txt_pos_y))


def draw_bearing_off_bar(
    surface: pygame.Surface,
    juego: Juego,
    font: pygame.font.Font
) -> None:
    """Dibuja las barras laterales de Bearing Off (Salida) y el conteo."""
    j1_id = juego.jugadores[0].id
    j2_id = juego.jugadores[1].id

    j1_salidas = juego.tablero.fichas_salidas(j1_id)
    rect_j1 = pygame.Rect(OUT_BAR_X_J1, MARGEN_Y, OUT_BAR_W, ALTO - 2 * MARGEN_Y)
    pygame.draw.rect(surface, BOARD_COLOR, rect_j1, border_radius=8)
    pygame.draw.rect(surface, LINE, rect_j1, 2, border_radius=8)

    if j1_salidas > 0:
        txt = font.render("J1 OUT", True, COLOR_TEXTO)
        surface.blit(txt, txt.get_rect(center=(rect_j1.centerx, MARGEN_Y + 15)))
        num = font.render(str(j1_salidas), True, COLOR_TEXTO)
        surface.blit(num, num.get_rect(center=(rect_j1.centerx, MARGEN_Y + 35)))

    j2_salidas = juego.tablero.fichas_salidas(j2_id)
    rect_j2 = pygame.Rect(OUT_BAR_X_J2, MARGEN_Y, OUT_BAR_W, ALTO - 2 * MARGEN_Y)
    pygame.draw.rect(surface, BOARD_COLOR, rect_j2, border_radius=8)
    pygame.draw.rect(surface, LINE, rect_j2, 2, border_radius=8)

    if j2_salidas > 0:
        txt = font.render("J2 OUT", True, COLOR_TEXTO)
        surface.blit(txt, txt.get_rect(center=(rect_j2.centerx, MARGEN_Y + 15)))
        num = font.render(str(j2_salidas), True, COLOR_TEXTO)
        surface.blit(num, num.get_rect(center=(rect_j2.centerx, MARGEN_Y + 35)))


def dibujar_hints(
    surface: pygame.Surface,
    origen: int | None,
    movs: list[int],
    juego: Juego
) -> None:
    """Dibuja pistas visuales (puntos verdes) en los destinos posibles."""
    if origen is None or not movs:
        return

    board_rect = BOARD.get_rect()
    pid = juego.jugador_actual.id
    posibles = set()

    for distancia in movs:
        if pid % 2 != 0:
            destino_fwd = origen - distancia  # J1 va hacia la izquierda
        else:
            destino_fwd = origen + distancia  # J2 va hacia la derecha

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
    surface.blit(titulo, titulo.get_rect(center=(ANCHO // 2, 100)))

    textos = [
        "",
        "CONTROLES:",
        "T - Tirar dados",
        "C - Cambiar turno (si no hay movimientos)",
        "R - Reiniciar juego",
        "H - Mostrar/Ocultar ayuda",
        "ESC - Salir",
        "",
        "JUGABILIDAD:",
        "• Click en un punto para seleccionar tu ficha",
        "• Click en otro punto para moverla",
        "• Los puntos verdes muestran movimientos válidos",
        "• Click en la barra lateral para sacar fichas",
        "",
        "Presiona H para cerrar"
    ]

    y_inicial = 180
    for i, txt in enumerate(textos):
        color = (255, 255, 0) if txt.endswith(":") else (255, 255, 255)
        render = font.render(txt, True, color)
        surface.blit(render, (ANCHO // 2 - 200, y_inicial + i * 28))


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


def point_or_out_bar_from_xy(x_pos: int, y_pos: int) -> int | None:
    """Mapear click a índice 0..23 o al índice 24 (Salida/Bearing Off)."""
    idx = punto_desde_xy(x_pos, y_pos)
    if idx is not None:
        return idx

    rect_out_j1 = pygame.Rect(
        OUT_BAR_X_J1, MARGEN_Y, OUT_BAR_W, ALTO - 2 * MARGEN_Y
    )
    rect_out_j2 = pygame.Rect(
        OUT_BAR_X_J2, MARGEN_Y, OUT_BAR_W, ALTO - 2 * MARGEN_Y
    )

    if rect_out_j1.collidepoint(x_pos, y_pos) or rect_out_j2.collidepoint(x_pos, y_pos):
        return PUNTOS

    return None


def manejar_evento_tirada(juego: Juego, font: pygame.font.Font):
    """Maneja el evento de tirar dados."""
    dado1, dado2, movs = juego.tirar()
    mensaje = f"🎲 Tirada: {dado1} y {dado2} → movs: {movs}"
    return font.render(mensaje, True, COLOR_TEXTO)


def manejar_movimiento(
    juego: Juego,
    sel: int,
    idx: int,
    font: pygame.font.Font
):
    """Maneja el intento de movimiento de una ficha."""
    resultado = juego.mover_ficha(sel, idx)

    if resultado:
        if idx == PUNTOS:
            msg = (
                f"✓ Ficha sacada desde {sel}. "
                f"Restantes: {juego.movimientos_disponibles()}"
            )
        else:
            msg = (
                f"✓ Movimiento {sel}→{idx}. "
                f"Restantes: {juego.movimientos_disponibles()}"
            )

        if juego.termino():
            msg += f" | 🏆 ¡{juego.ganador().nombre} ha ganado!"
    else:
        error = juego.ultimo_error() or 'movimiento inválido'
        msg = f"❌ No se pudo mover {sel}→{idx}. Motivo: {error}"

    return resultado, font.render(msg, True, COLOR_TEXTO)


def iniciar_ui(ancho: int = ANCHO, alto: int = ALTO) -> None:
    """Función principal que inicia la interfaz gráfica del juego."""
    pygame.init()
    pygame.font.init()

    flags = pygame.SCALED if hasattr(pygame, "SCALED") else 0
    screen = pygame.display.set_mode((ancho, alto), flags=flags)
    pygame.display.set_caption("Backgammon — Computación 2025")
    clock = pygame.time.Clock()

    f28 = pygame.font.Font(None, 28)
    f20 = pygame.font.Font(None, 20)
    f18 = pygame.font.Font(None, 18)

    jugador1 = Jugador("Blancas")
    jugador2 = Jugador("Negras")
    juego = Juego(jugador1, jugador2)
    juego.reiniciar()

    ultimo_txt = None
    seleccionado: int | None = None
    mostrar_ayuda_flag = False

    corriendo = True
    while corriendo:
        BOARD.get_rect()  # Inicializar geometría

        # Validar selección actual
        if seleccionado is not None and seleccionado != PUNTOS:
            pid = juego.jugador_actual.id
            fichas_en_punto = juego.tablero.punto(seleccionado)
            if not any(f.owner_id == pid for f in fichas_en_punto):
                seleccionado = None

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                corriendo = False
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    corriendo = False
                elif evento.key == pygame.K_t:
                    ultimo_txt = manejar_evento_tirada(juego, f20)
                    seleccionado = None
                elif evento.key == pygame.K_c:
                    juego.cambiar_turno()
                    seleccionado = None
                    ultimo_txt = f20.render("🔄 Turno cambiado", True, COLOR_TEXTO)
                elif evento.key == pygame.K_r:
                    juego.reiniciar()
                    ultimo_txt = f20.render("♻️ Juego reiniciado", True, COLOR_TEXTO)
                    seleccionado = None
                elif evento.key == pygame.K_h:
                    mostrar_ayuda_flag = not mostrar_ayuda_flag
            elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                if mostrar_ayuda_flag:
                    continue

                idx = point_or_out_bar_from_xy(*evento.pos)

                if idx is None:
                    seleccionado = None
                elif seleccionado is None:
                    if idx != PUNTOS:
                        seleccionado = idx
                elif idx == seleccionado:
                    seleccionado = None
                else:
                    ok_mov, ultimo_txt = manejar_movimiento(juego, seleccionado, idx, f20)
                    if ok_mov:
                        seleccionado = None

        # Dibujo
        screen.fill(BG_COLOR)

        draw_bearing_off_bar(screen, juego, f20)
        dibujar_marco_y_labels(screen, f20)
        dibujar_triangulos(screen)

        dibujar_punto_seleccionado(screen, seleccionado)
        dibujar_hints(screen, seleccionado, juego.movimientos_disponibles(), juego)
        dibujar_fichas(screen, juego, f20)
        dibujar_barra(screen, juego, f20)

        # HUD
        movs = juego.movimientos_disponibles()
        estado = (
            f"Estado: {juego.estado} | Turno: {juego.jugador_actual.nombre} "
            f"(ID {juego.jugador_actual.id}) | Movs: {movs}"
        )
        titulo_texto = (
            "Backgammon — [ESC: salir] [T: tirar] [C: turno] [R: reiniciar] [H: ayuda]"
        )
        titulo = f28.render(titulo_texto, True, COLOR_TEXTO)
        info = f18.render(estado, True, COLOR_TEXTO)

        screen.blit(titulo, (20, 20))
        screen.blit(info, (20, 52))
        if ultimo_txt:
            screen.blit(ultimo_txt, (20, 78))

        if mostrar_ayuda_flag:
            mostrar_ayuda(screen, f20)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit(0)


if __name__ == "__main__":
    iniciar_ui()