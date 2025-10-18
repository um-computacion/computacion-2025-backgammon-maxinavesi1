"""Demo Pygame con estado de juego + clicks para mover.

Teclas:
  ESC   → salir
  T     → tirar dados
  C     → cambiar turno
  R     → reset DEMO (2 fichas J1 en 0 y 2 fichas J2 en 23)

Clicks:
  • Click en un punto para seleccionarlo (origen).
  • Click en otro punto o en la barra de salida (laterales) para intentar mover/sacar (destino).
  • Si falla, se muestra el motivo (juego.ultimo_error()).

Ejecución:
    python -m backgammon.pygame.pygame_ui
"""
from __future__ import annotations
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
COLOR_SEL = (30, 30, 30)
COLOR_HINT = (90, 180, 90)

MAX_VISIBLE_STACK = 5   
OUT_BAR_W = 60 
OUT_BAR_X_J1 = ANCHO - MARGEN_X - OUT_BAR_W 
OUT_BAR_X_J2 = MARGEN_X 

_BOARD_RECT: pygame.Rect | None = None

def _board_rect() -> pygame.Rect:
    """Rectángulo del tablero interno con márgenes."""
    global _BOARD_RECT
    rect = pygame.Rect(
        MARGEN_X + OUT_BAR_W, 
        MARGEN_Y + 20,
        ANCHO - 2 * MARGEN_X - 2 * OUT_BAR_W,
        ALTO - 2 * MARGEN_Y - 40
    )
    _BOARD_RECT = rect
    return rect


def _tri_w() -> float:
    return _BOARD_RECT.width / 12.0  


def _point_index_to_display(idx: int) -> tuple[str, int]:
    """Mapeo 0..23 -> ('top'/'bottom', col_visual 0..11)."""
    if 0 <= idx <= 11:
        return 'top', 11 - idx       
    else:
        return 'bottom', idx - 12     


def _point_center(idx: int) -> tuple[int, int]:
    """Centro base de un punto para dibujar marcas/hints (no fichas apiladas)."""
    row, col_vis = _point_index_to_display(idx)
    x = int(_BOARD_RECT.left + col_vis * _tri_w() + _tri_w() / 2)
    y = _BOARD_RECT.top if row == 'top' else _BOARD_RECT.bottom
    return x, y


def _dibujar_triangulos(surface: pygame.Surface) -> None:
    """Triángulos alternados del tablero (arriba/abajo)."""
    if _BOARD_RECT is None:
        return
        
    for col_vis in range(12):
        x0 = _BOARD_RECT.left + col_vis * _tri_w()
        x1 = x0 + _tri_w()
        xm = (x0 + x1) / 2.0

        tip_y = _BOARD_RECT.top + _BOARD_RECT.height * 0.42
        pts = [(x0, _BOARD_RECT.top), (x1, _BOARD_RECT.top), (xm, tip_y)]
        pygame.draw.polygon(surface, TRI_A if col_vis % 2 == 0 else TRI_B, pts)

        tip_y = _BOARD_RECT.bottom - _BOARD_RECT.height * 0.42
        pts = [(x0, _BOARD_RECT.bottom), (x1, _BOARD_RECT.bottom), (xm, tip_y)]
        pygame.draw.polygon(surface, TRI_B if col_vis % 2 == 0 else TRI_A, pts)


def _dibujar_marco_y_labels(surface: pygame.Surface, font: pygame.font.Font) -> None:
    """Marco del tablero, línea central y numeración 12..1 / 13..24."""
    if _BOARD_RECT is None:
        return
        
    pygame.draw.rect(surface, BOARD_COLOR, _BOARD_RECT, border_radius=12)
    pygame.draw.rect(surface, LINE, _BOARD_RECT, 2, border_radius=12)

    pygame.draw.line(surface, LINE, (_BOARD_RECT.left, _BOARD_RECT.centery),
                     (_BOARD_RECT.right, _BOARD_RECT.centery), 1)

    triw = _tri_w()
    top_labels = [str(i) for i in range(12, 0, -1)]
    for col_vis, lbl in enumerate(top_labels):
        x = int(_BOARD_RECT.left + col_vis * triw + triw / 2)
        y = _BOARD_RECT.top - 14
        img = font.render(lbl, True, COLOR_TEXTO)
        surface.blit(img, img.get_rect(center=(x, y)))
    bottom_labels = [str(i) for i in range(13, 25)]
    for col_vis, lbl in enumerate(bottom_labels):
        x = int(_BOARD_RECT.left + col_vis * triw + triw / 2)
        y = _BOARD_RECT.bottom + 14
        img = font.render(lbl, True, COLOR_TEXTO)
        surface.blit(img, img.get_rect(center=(x, y)))


def _draw_checker(surface: pygame.Surface, center: tuple[int, int], radius: int,
                  color_rgb: tuple[int, int, int], label: int | None,
                  font: pygame.font.Font) -> None:
    pygame.draw.circle(surface, color_rgb, center, radius)
    pygame.draw.circle(surface, LINE, center, radius, 1)
    if label:
        txt = font.render(str(label), True, LINE if color_rgb == COLOR_J1 else COLOR_J1)
        surface.blit(txt, txt.get_rect(center=center))


def _dibujar_fichas(surface: pygame.Surface, juego: Juego, font: pygame.font.Font) -> None:
    """Dibuja las fichas apiladas con contador en la última si hay overflow."""
    if _BOARD_RECT is None:
        return
        
    triw = _tri_w()
    radius = int(triw * 0.38)
    radius = max(12, min(radius, 22))
    vgap = 4
    step = radius * 2 + vgap

    t = juego.tablero
    j1_id = juego.jugadores[0].id  

    def color(pid): return COLOR_J1 if pid == j1_id else COLOR_J2

    for idx in range(PUNTOS):
        row, col_vis = _point_index_to_display(idx)
        cx = int(_BOARD_RECT.left + col_vis * triw + triw / 2)

        pila = t.punto(idx)
        if not pila:
            continue

        visibles = min(len(pila), MAX_VISIBLE_STACK)
        extras = max(0, len(pila) - (MAX_VISIBLE_STACK - 1)) if len(pila) > MAX_VISIBLE_STACK else 0

        if row == 'top':
            cy = int(_BOARD_RECT.top + radius + 6)
            for i in range(visibles):
                pid = pila[i].owner_id
                lbl = extras if (extras and i == visibles - 1) else None
                _draw_checker(surface, (cx, cy + i * step), radius, color(pid), lbl, font)
        else:
            cy = int(_BOARD_RECT.bottom - radius - 6)
            for i in range(visibles):
                pid = pila[i].owner_id
                lbl = extras if (extras and i == visibles - 1) else None
                _draw_checker(surface, (cx, cy - i * step), radius, color(pid), lbl, font)


def _dibujar_barra(surface: pygame.Surface, juego: Juego, font: pygame.font.Font) -> None:
    """Muestra cuántas fichas tiene cada jugador en la barra central."""
    if _BOARD_RECT is None:
        return
        
    j1_id = juego.jugadores[0].id
    j2_id = juego.jugadores[1].id
    
    b1 = juego.tablero.fichas_en_barra(j1_id)
    b2 = juego.tablero.fichas_en_barra(j2_id)
    
    bar_rect = pygame.Rect(_BOARD_RECT.centerx - 10, _BOARD_RECT.top, 20, _BOARD_RECT.height)

    if b1 > 0:
        cy_start = _BOARD_RECT.top + 30
        cy_step = 25
        txt = font.render(str(b1), True, COLOR_TEXTO if COLOR_J1 == (245, 245, 245) else COLOR_J1)
        for i in range(min(b1, 5)):
             _draw_checker(surface, (bar_rect.centerx, cy_start + i * cy_step), 10, COLOR_J1, None, font)
        surface.blit(txt, (bar_rect.centerx - 10, cy_start + min(b1, 5) * cy_step)) # Contador

    if b2 > 0:
        cy_start = _BOARD_RECT.bottom - 30
        cy_step = 25
        txt = font.render(str(b2), True, COLOR_TEXTO if COLOR_J2 == (30, 30, 30) else COLOR_J2)
        for i in range(min(b2, 5)):
             _draw_checker(surface, (bar_rect.centerx, cy_start - i * cy_step), 10, COLOR_J2, None, font)
        surface.blit(txt, (bar_rect.centerx - 10, cy_start - min(b2, 5) * cy_step - 20)) # Contador


def __dibujar_bearing_off_bar__(surface: pygame.Surface, juego: Juego, font: pygame.font.Font) -> None:
    """Dibuja las barras laterales de Bearing Off (Salida) y el conteo."""
    j1_id = juego.jugadores[0].id
    j2_id = juego.jugadores[1].id
    j1_salidas = juego.tablero.fichas_salidas(j1_id)
    rect_j1 = pygame.Rect(OUT_BAR_X_J1, MARGEN_Y, OUT_BAR_W, ALTO - 2 * MARGEN_Y)
    pygame.draw.rect(surface, BOARD_COLOR, rect_j1)
    pygame.draw.rect(surface, LINE, rect_j1, 1)

    if j1_salidas > 0:
        txt = font.render(f"J1 OUT: {j1_salidas}", True, COLOR_TEXTO)
        surface.blit(txt, txt.get_rect(center=(rect_j1.centerx, MARGEN_Y + 10)))

    j2_salidas = juego.tablero.fichas_salidas(j2_id)
    rect_j2 = pygame.Rect(OUT_BAR_X_J2, MARGEN_Y, OUT_BAR_W, ALTO - 2 * MARGEN_Y)
    pygame.draw.rect(surface, BOARD_COLOR, rect_j2)
    pygame.draw.rect(surface, LINE, rect_j2, 1)

    if j2_salidas > 0:
        txt = font.render(f"J2 OUT: {j2_salidas}", True, COLOR_TEXTO)
        surface.blit(txt, txt.get_rect(center=(rect_j2.centerx, MARGEN_Y + 10)))


def _dibujar_hints(surface: pygame.Surface, origen: int | None, movs: list[int], juego: Juego) -> None:
    """Pistas (puntitos) en destinos posibles desde 'origen' según los dados."""
    if origen is None or not movs:
        return
        
    pid = juego.jugador_actual.id
    posibles = set()
    
    for d in movs:
        destino_potencial = 0
        if origen == 0 and juego._en_barra(pid):
            if pid % 2 != 0: destino_potencial = origen + d
            
        elif origen == 23 and juego._en_barra(pid):
            if pid % 2 == 0: destino_potencial = origen - d
            
        elif pid % 2 != 0: 
            destino_potencial = origen + d
        else:
            destino_potencial = origen - d

        if 0 <= destino_potencial < PUNTOS:
            ok, _ = juego._validar_movimiento(origen, destino_potencial)
            if ok:
                posibles.add(destino_potencial)

        if juego.tablero.puede_sacar_fichas(pid):
            dist_req = PUNTOS - origen if pid % 2 != 0 else origen + 1
            if d >= dist_req:
                 posibles.add(PUNTOS)

    for idx in posibles:
        if idx == PUNTOS:
            rect = pygame.Rect(OUT_BAR_X_J1 if pid % 2 != 0 else OUT_BAR_X_J2, _BOARD_RECT.centery - 10, OUT_BAR_W, 20)
            pygame.draw.rect(surface, COLOR_HINT, rect, border_radius=6)
        else:
            x, y = _point_center(idx)
            pygame.draw.circle(surface, COLOR_HINT, (x, y), 6)


def _punto_desde_xy(x: int, y: int) -> int | None:
    """Mapear click a índice 0..23 en función de columnas y mitad superior/inferior."""
    if _BOARD_RECT is None:
        return None
        
    triw = _tri_w()
    fila_sup = y < _BOARD_RECT.centery
    base_y = _BOARD_RECT.top if fila_sup else _BOARD_RECT.bottom

    if x < _BOARD_RECT.left or x >= _BOARD_RECT.right:
        return None
        
    col = int((x - _BOARD_RECT.left) // triw)
    if not (0 <= col <= 11):
        return None
        
    if abs(y - base_y) > (_BOARD_RECT.height * 0.5):
        return None

    if fila_sup:
        idx = 11 - col  
    else:
        idx = 12 + col  
    return idx


def _point_or_out_bar_from_xy(x: int, y: int) -> int | None:
    """Mapear click a índice 0..23 o al índice 24 (Salida/Bearing Off)."""

    idx = _punto_desde_xy(x, y)
    if idx is not None:
        return idx

    rect_out_j1 = pygame.Rect(OUT_BAR_X_J1, MARGEN_Y, OUT_BAR_W, ALTO - 2 * MARGEN_Y)
    rect_out_j2 = pygame.Rect(OUT_BAR_X_J2, MARGEN_Y, OUT_BAR_W, ALTO - 2 * MARGEN_Y)

    if rect_out_j1.collidepoint(x, y) or rect_out_j2.collidepoint(x, y):
        return PUNTOS 
    
    return None


def _demo_reset(juego: Juego) -> None:
    """Tablero vacío + 2 fichas del jugador actual en 0 y 2 del otro en 23."""
    t = juego.tablero
    t.preparar_posicion_inicial()
    j1 = juego.jugadores[0].id
    j2 = juego.jugadores[1].id
    t.colocar_ficha(j1, 0); t.colocar_ficha(j1, 0)
    t.colocar_ficha(j2, 23); t.colocar_ficha(j2, 23)


def iniciar_ui(ancho: int = ANCHO, alto: int = ALTO) -> None:
    pygame.init()
    pygame.font.init()

    flags = pygame.SCALED if hasattr(pygame, "SCALED") else 0
    screen = pygame.display.set_mode((ancho, alto), flags=flags)
    pygame.display.set_caption("Backgammon — demo")
    clock = pygame.time.Clock()

    f28 = pygame.font.Font(None, 28)
    f20 = pygame.font.Font(None, 20)

    j1 = Jugador("Blancas"); j2 = Jugador("Negras")
    juego = Juego(j1, j2)
    _demo_reset(juego)

    ultimo_txt = None
    seleccionado: int | None = None

    corriendo = True
    while corriendo:
        _board_rect()

        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                corriendo = False
            elif ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_ESCAPE:
                    corriendo = False
                elif ev.key == pygame.K_t:
                    d1, d2, movs = juego.tirar()
                    ultimo_txt = f20.render(f"Tirada: {d1} y {d2} → movs: {movs}", True, COLOR_TEXTO)
                elif ev.key == pygame.K_c:
                    juego.cambiar_turno(); seleccionado = None
                elif ev.key == pygame.K_r:
                    _demo_reset(juego); ultimo_txt = None; seleccionado = None
            elif ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                idx = _point_or_out_bar_from_xy(*ev.pos)
                
                if idx is None:
                    seleccionado = None
                else:
                    if seleccionado is None:
                        if idx != PUNTOS:
                            seleccionado = idx
                    else:
                        if idx == seleccionado:
                            seleccionado = None
                        else:
                            ok = juego.mover_ficha(seleccionado, idx)
                            
                            if ok:
                                if idx == PUNTOS:
                                    msg = f"Ficha sacada (Bearing Off) desde {seleccionado} OK. Restantes: {juego.movimientos_disponibles()}"
                                else:
                                    msg = f"Movimiento {seleccionado}→{idx} OK. Restantes: {juego.movimientos_disponibles()}"
                                
                                if juego.termino():
                                    msg += f" - ¡{juego.ganador().nombre} ha ganado!"
                                    
                                seleccionado = None
                            else:
                                msg = (f"NO se pudo mover {seleccionado}→{idx}. "
                                       f"Motivo: {juego.ultimo_error() or 'movimiento inválido'}")
                            ultimo_txt = f20.render(msg, True, COLOR_TEXTO)

        screen.fill(BG_COLOR)

        __dibujar_bearing_off_bar__(screen, juego, f20)
        _dibujar_marco_y_labels(screen, f20)
        _dibujar_triangulos(screen)
        _dibujar_hints(screen, seleccionado, juego.movimientos_disponibles(), juego) 
        _dibujar_fichas(screen, juego, f20)
        _dibujar_barra(screen, juego, f20)

        estado = (f"estado={juego.estado} | turno={juego.jugador_actual.nombre} "
                  f"(id {juego.jugador_actual.id}) | movs={juego.movimientos_disponibles()}")
        titulo = f28.render(
            "UI mínima — ESC: salir | T: tirar | C: cambiar turno | R: reset demo", True, COLOR_TEXTO
        )
        info = f20.render(estado, True, COLOR_TEXTO)

        screen.blit(titulo, (20, 20))
        screen.blit(info, (20, 52))
        if ultimo_txt:
            screen.blit(ultimo_txt, (20, 78))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit(0)


if __name__ == "__main__":
    iniciar_ui()