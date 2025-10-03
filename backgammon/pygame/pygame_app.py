import sys
import pygame
from backgammon.core.juego import Juego
from backgammon.core.jugador import Jugador
from backgammon.core.tablero import PUNTOS

ANCHO = 960
ALTO = 480
MARGEN = 20
COLOR_FONDO = (240, 240, 240)
COLOR_TEXTO = (20, 20, 20)
COLOR_PUNTO = (200, 200, 200)
COLOR_A = (60, 120, 220)  
COLOR_B = (220, 120, 60)   

def _posicion_punto(idx):
    """Distribuye 24 puntos en dos filas de 12."""
    fila = 0 if idx < 12 else 1
    col = idx if idx < 12 else 23 - idx
    ancho_util = ANCHO - 2 * MARGEN
    esp = ancho_util // 12
    x = MARGEN + col * esp + esp // 2
    y = MARGEN + (ALTO - 2 * MARGEN) * (0.25 if fila == 0 else 0.75)
    return x, y, esp

def correr():
    pygame.init()
    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("Backgammon (demo UI)")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 24)

    j1 = Jugador("A")
    j2 = Jugador("B")
    juego = Juego(j1, j2)
    corriendo = True
    while corriendo:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                corriendo = False



