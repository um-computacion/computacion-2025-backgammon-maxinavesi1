Herramienta usada: Copilot


Prompt: Ya tengo test_juego.py con dos pruebas (test_turno_inicial y test_tirar_devuelve_3_valores). Necesito solo el bloque para agregar una tercera prueba llamada test_cambiar_turno que cree un juego con dos jugadores, llame cambiar_turno() una vez y verifique que el jugador actual cambió de "A" a "B". No reescribas todo el archivo, no pongas imports ni el if __name__ == "__main__". Dame únicamente la nueva función de test, corta y en español.


Resultado: def test_cambiar_turno(self):
    g = Juego(Jugador("A"), Jugador("B"))
    self.assertEqual(g.jugador_actual.nombre, "A")
    g.cambiar_turno()
    self.assertEqual(g.jugador_actual.nombre, "B")
