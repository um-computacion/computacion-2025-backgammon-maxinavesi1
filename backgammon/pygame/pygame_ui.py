"""Ventana mínima con Pygame para ver algo en pantalla.

Uso (local):
    python -m backgammon.pygame_ui.ventana
"""

import pygame
import sys

ANCHO = 800
ALTO = 600
FPS = 60
COLOR_FONDO = (240, 240, 240)
COLOR_TEXTO = (30, 30, 30)
COLOR_PUNTO = (180, 120, 90)  

def dibujar_puntos(superficie):
    radio = 10
    margen = 40
    espacio = (ANCHO - 2 * margen) // 12
    y_sup = 100
    for i in range(12):
        x = margen + i * espacio + espacio // 2
        pygame.draw.circle(superficie, COLOR_PUNTO, (x, y_sup), radio)
    y_inf = ALTO - 100
    for i in range(12):
        x = margen + i * espacio + espacio // 2
        pygame.draw.circle(superficie, COLOR_PUNTO, (x, y_inf), radio)

def iniciar_ui(ancho=ANCHO, alto=ALTO):
    pygame.init()
    pygame.font.init()
    flags = pygame.SCALED if hasattr(pygame, "SCALED") else 0
    try:
        pantalla = pygame.display.set_mode((ancho, alto), flags=flags)
    except Exception as e:
        print("No se pudo crear la ventana de Pygame:", e)
        pygame.quit()
        sys.exit(1)

    pygame.display.set_caption("Backgammon — demo")
    reloj = pygame.time.Clock()
    fuente = pygame.font.Font(None, 24)
    texto = fuente.render("UI mínima — ESC para salir", True, COLOR_TEXTO)

    corriendo = True
    while corriendo:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                corriendo = False
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                corriendo = False

        pantalla.fill(COLOR_FONDO)
        dibujar_puntos(pantalla)
        pantalla.blit(texto, (20, 20))

        pygame.display.flip()
        reloj.tick(FPS)

    pygame.quit()
    sys.exit(0)

if __name__ == "__main__":
    iniciar_ui()
