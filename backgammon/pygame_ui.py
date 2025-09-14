import pygame
import sys

ANCHO = 800
ALTO = 600
FPS = 60
COLOR_FONDO = (240, 240, 240)
COLOR_TEXTO = (30, 30, 30)
COLOR_PUNTO = (180, 120, 90)  


def dibujar_puntos(superficie):
    """Dibuja 24 'puntos' como círculos simples, 12 arriba y 12 abajo."""
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