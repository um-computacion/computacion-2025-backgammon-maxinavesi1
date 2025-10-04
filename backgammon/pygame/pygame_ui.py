"""Demo Pygame con estado de juego.

Teclas:
  ESC  → salir
  T    → tirar dados (muestra movs)
  C    → cambiar turno
  R    → reset DEMO (2 fichas J1 en 0 y 2 fichas J2 en 23)

Ejecución:
    python -m backgammon.pygame.pygame_ui
"""

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


def _xy_punto(idx: int) -> tuple[int, int, int, int]:
    """(x_centro, y_base, ancho_col, dir), dir = -1 (arriba) o +1 (abajo)."""
    fila_sup = (idx < 12)
    col = idx if fila_sup else (23 - idx)
    margen = 36
    ancho_util = ANCHO - 2 * margen
    col_w = ancho_util // 12
    x = margen + col * col_w + col_w // 2
    y = 110 if fila_sup else (ALTO - 110)
    return x, y, col_w, (-1 if fila_sup else 1)

def _dibujar_puntos(surface: pygame.Surface) -> None:
    radio = 9
    for i in range(24):
        x, y, _, _ = _xy_punto(i)
        pygame.draw.circle(surface, COLOR_PUNTO, (x, y), radio)

def _dibujar_fichas(surface: pygame.Surface, juego: Juego) -> None:
    """Dibuja las fichas apiladas leyendo el tablero público (sin tocar privados)."""
    t = juego.tablero
    radio = 12
    sep = 5
    j1_id = 1  
    for i in range(PUNTOS):
        x, y_base, _, dire = _xy_punto(i)
        pila = t.punto(i)  
        for n, pid in enumerate(pila):
            dy = (radio * 2 + sep) * n * dire
            color = COLOR_J1 if pid == j1_id else COLOR_J2
            pygame.draw.circle(surface, color, (x, y_base + dy), radio)

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

    # Juego de demo
    j1 = Jugador("Blancas")
    j2 = Jugador("Negras")
    juego = Juego(j1, j2)
    _demo_reset(juego)

    ultimo_txt = None  

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
                    ultimo_txt = f20.render(f"Tirada: {d1} y {d2} → movs: {movs}", True, COLOR_TEXTO)
                elif ev.key == pygame.K_c:
                    juego.cambiar_turno()
                elif ev.key == pygame.K_r:
                    _demo_reset(juego)
                    ultimo_txt = None

        screen.fill(COLOR_FONDO)
        _dibujar_puntos(screen)
        _dibujar_fichas(screen, juego)

        estado = f"estado={juego.estado} | turno={juego.jugador_actual.nombre} (id {juego.jugador_actual.id}) | movs={juego.movimientos_disponibles()}"
        titulo = f28.render("UI mínima — ESC: salir | T: tirar | C: cambiar turno | R: reset demo", True, COLOR_TEXTO)
        info = f20.render(estado, True, COLOR_TEXTO)

        screen.blit(titulo, (20, 20))
        screen.blit(info,   (20, 52))
        if ultimo_txt:
            screen.blit(ultimo_txt, (20, 78))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit(0)

if __name__ == "__main__":
    iniciar_ui()
