"""Demo Pygame con estado de juego + clicks para mover.

Teclas:
  ESC  → salir
  T    → tirar dados (muestra movs)
  C    → cambiar turno
  R    → reset DEMO (2 fichas J1 en 0 y 2 fichas J2 en 23)

Clicks:
  • Click en un punto para seleccionarlo (origen).
  • Click en otro punto para intentar mover (destino).
  • Si el movimiento falla, se muestra un motivo genérico.

Ejecución:
    python -m backgammon.pygame.pygame_ui
"""

from __future__ import annotations

import sys
import pygame

from backgammon.core.juego import Juego
from backgammon.core.jugador import Jugador
from backgammon.core.tablero import PUNTOS


ANCHO = 900
ALTO = 560
FPS = 60

COLOR_FONDO = (242, 242, 242)
COLOR_TEXTO = (30, 30, 30)
COLOR_PUNTO = (196, 144, 110)
COLOR_J1 = (60, 120, 220)
COLOR_J2 = (220, 120, 60)
COLOR_SEL = (30, 30, 30)
COLOR_HINT = (90, 180, 90)

MARGEN = 36
Y_SUP = 110
Y_INF = ALTO - 110
RADIO_PUNTO = 9
RADIO_FICHA = 12
SEP_FICHA = 5


def _col_w() -> int:
    """Ancho de cada columna (12 por fila)."""
    ancho_util = ANCHO - 2 * MARGEN
    return ancho_util // 12


def _xy_punto(idx: int) -> tuple[int, int, int, int]:
    """(x_centro, y_base, ancho_col, dir). dir = -1 (arriba) o +1 (abajo)."""
    fila_sup = (idx < 12)
    col = idx if fila_sup else (23 - idx)
    colw = _col_w()
    x = MARGEN + col * colw + colw // 2
    y = Y_SUP if fila_sup else Y_INF
    return x, y, colw, (-1 if fila_sup else 1)


def _punto_desde_xy(x: int, y: int) -> int | None:
    """Mapea un clic (x,y) al índice de punto [0..23] o None si está fuera."""
    colw = _col_w()

    if y < (ALTO // 2):
        fila_sup = True
        base_y = Y_SUP
    else:
        fila_sup = False
        base_y = Y_INF

    if x < MARGEN or x >= (ANCHO - MARGEN):
        return None

    col = (x - MARGEN) // colw
    if not (0 <= col <= 11):
        return None
    if abs(y - base_y) > 40:
        return None

    if fila_sup:
        idx = col
    else:
        idx = 23 - col
    return idx


def _dibujar_puntos(surface: pygame.Surface, seleccionado: int | None) -> None:
    for i in range(24):
        x, y, _, _ = _xy_punto(i)
        pygame.draw.circle(surface, COLOR_PUNTO, (x, y), RADIO_PUNTO)
        if seleccionado == i:
            pygame.draw.circle(surface, COLOR_SEL, (x, y), RADIO_PUNTO + 3, width=2)


def _dibujar_fichas(surface: pygame.Surface, juego: Juego) -> None:
    """Dibuja las fichas apiladas leyendo el tablero público (sin tocar privados)."""
    t = juego.tablero
    j1_id = 1  

    for i in range(PUNTOS):
        x, y_base, _, dire = _xy_punto(i)
        pila = t.punto(i)
        for n, pid in enumerate(pila):
            dy = (RADIO_FICHA * 2 + SEP_FICHA) * n * dire
            color = COLOR_J1 if pid == j1_id else COLOR_J2
            pygame.draw.circle(surface, color, (x, y_base + dy), RADIO_FICHA)


def _dibujar_hints(surface: pygame.Surface, origen: int | None, movs: list[int]) -> None:
    """Dibuja pistas (puntitos) en destinos posibles desde 'origen' según 'movs'."""
    if origen is None or not movs:
        return
    posibles = set()
    for d in movs:
        a = origen + d
        b = origen - d
        if 0 <= a < PUNTOS:
            posibles.add(a)
        if 0 <= b < PUNTOS:
            posibles.add(b)
    for idx in posibles:
        x, y, _, _ = _xy_punto(idx)
        pygame.draw.circle(surface, COLOR_HINT, (x, y), RADIO_PUNTO // 2)


def _demo_reset(juego: Juego) -> None:
    """Tablero vacío + 2 fichas del jugador actual en 0 y 2 del otro en 23."""
    t = juego.tablero
    t.preparar_posicion_inicial()
    j1 = juego.jugador_actual
    otro = 1 if j1.id != 1 else 2
    t.colocar_ficha(j1.id, 0)
    t.colocar_ficha(j1.id, 0)
    t.colocar_ficha(otro, 23)
    t.colocar_ficha(otro, 23)


def iniciar_ui(ancho: int = ANCHO, alto: int = ALTO) -> None:
    pygame.init()
    pygame.font.init()

    flags = pygame.SCALED if hasattr(pygame, "SCALED") else 0
    screen = pygame.display.set_mode((ancho, alto), flags=flags)
    pygame.display.set_caption("Backgammon — demo")

    clock = pygame.time.Clock()
    f28 = pygame.font.Font(None, 28)
    f20 = pygame.font.Font(None, 22)

    j1 = Jugador("Blancas")
    j2 = Jugador("Negras")
    juego = Juego(j1, j2)
    _demo_reset(juego)

    ultimo_txt = None
    seleccionado: int | None = None  

    corriendo = True
    while corriendo:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                corriendo = False

            elif ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_ESCAPE:
                    corriendo = False
                elif ev.key == pygame.K_t:
                    d1, d2, movs = juego.tirar()
                    ultimo_txt = f20.render(
                        f"Tirada: {d1} y {d2} → movs: {movs}", True, COLOR_TEXTO
                    )
                elif ev.key == pygame.K_c:
                    juego.cambiar_turno()
                    seleccionado = None
                elif ev.key == pygame.K_r:
                    _demo_reset(juego)
                    ultimo_txt = None
                    seleccionado = None

            elif ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                x, y = ev.pos
                idx = _punto_desde_xy(x, y)
                if idx is None:
                    seleccionado = None
                else:
                    if seleccionado is None:
                        seleccionado = idx
                    else:
                        if idx == seleccionado:
                            seleccionado = None
                        else:
                            if not juego.movimientos_disponibles():
                                msg = "No hay movimientos: presioná T para tirar los dados."
                                ultimo_txt = f20.render(msg, True, COLOR_TEXTO)
                                seleccionado = None
                                continue

                            ok = juego.mover_ficha(seleccionado, idx)
                            if ok:
                                msg = (
                                    f"Movimiento {seleccionado}→{idx} OK. "
                                    f"Restantes: {juego.movimientos_disponibles()}"
                                )
                                seleccionado = None
                            else:
                                msg = (
                                    f"NO se pudo mover {seleccionado}→{idx}. "
                                    f"Motivo: {juego.ultimo_error() or 'movimiento inválido'}"
                                )
                            ultimo_txt = f20.render(msg, True, COLOR_TEXTO)

        screen.fill(COLOR_FONDO)
        _dibujar_puntos(screen, seleccionado)
        _dibujar_hints(screen, seleccionado, juego.movimientos_disponibles())
        _dibujar_fichas(screen, juego)

        estado = (
            f"estado={juego.estado} | turno={juego.jugador_actual.nombre} "
            f"(id {juego.jugador_actual.id}) | movs={juego.movimientos_disponibles()}"
        )
        titulo = f28.render(
            "UI mínima — ESC: salir | T: tirar | C: cambiar turno | R: reset demo",
            True, COLOR_TEXTO,
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
