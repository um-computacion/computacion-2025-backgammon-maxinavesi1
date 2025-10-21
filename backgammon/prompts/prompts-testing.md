
# Registro de Prompts de IA: Testing

## 2025-09-04 — test_juego.py (Hit y Turno)
**Herramienta:** ChatGPT 

Prompt:
Crea un test para juego.py que verifique lo siguiente: el jugador A (id 1) mueve su ficha al punto 3. En el punto 3, hay exactamente una ficha del jugador B (id 2). El movimiento debe resultar en la captura (hit), enviar la ficha de B a la barra, y consumir el dado. Si el dado es el último disponible, el turno debe cambiar a B.

Respuesta:
[Generó el test completo, incluyendo el setup de la barra y la aserción final del cambio de turno y la barra.]
**Instrucciones del sistema:** El test debe simular el consumo total del dado para verificar el cambio de turno.
**Uso:** Usada con modificaciones (Se adaptó el acceso a atributos internos para el setup).
**Archivo Final:** tests/test_juego.py

## 2025-10-18 — test_tablero.py (Posición Inicial)
**Herramienta:** Gemini Advanced 

Prompt:
Genera un test para test_tablero.py que valide la función posicion_inicial_estandar. Debe verificar que cada punto de inicio (2, 5, 7, 12, 18, 23) tiene la cantidad correcta de fichas y la propiedad correcta, y que el total es 15 fichas por jugador.

Respuesta:
[Generó la estructura de bucles y aserciones para los puntos fijos, y la lógica de sum(1 for p in ...) para el conteo total por ID.]
**Instrucciones del sistema:** Asegúrate de que el conteo final verifique que el número total de fichas sea exactamente 15 por ID de jugador.
**Uso:** Usada con modificaciones (Se corrigió la aserción total de fichas de 30 a 15 por jugador y se adaptó para usar objetos Checker).
**Archivo Final:** tests/test_tablero.py

## 2025-10-19 — test_juego.py (Error de Bloqueo)
**Herramienta:** ChatGPT 

Prompt:
Tengo un bug donde mi _validar_movimiento no registra el error de 'destino bloqueado' si el destino tiene 2 fichas del oponente. Crea un test para juego.py que intente mover una ficha al punto 4, donde ya hay [B, B], y verifique que el movimiento falla y registra el error "destino bloqueado por el oponente".

Respuesta:
[Generó el test que hace el setup de las dos fichas rivales y chequea el último error.]
**Instrucciones del sistema:** Ninguna.
**Uso:** Usada sin cambios.
**Archivo Final:** tests/test_juego.py

## 2025-10-22 — test_juego.py (Cobertura: Movimiento Inverso)
**Herramienta:** Gemini Advanced 

Prompt:
Tengo una rama faltante en mi método _validar_movimiento de juego.py: la validación que impide al jugador mover hacia atrás si está moviendo normalmente (no reingreso, no bearing off). Escribe un test que fuerce el error "el jugador debe moverse hacia adelante" para el Jugador 1.

Respuesta:
[Generó un test que intenta llamar a mover_ficha(5, 4) para el Jugador 1, verificando que el último error coincida.]
**Instrucciones del sistema:** El test debe simular que hay fichas en el origen para que la validación avance.
**Uso:** Usada con modificaciones (Ajuste del mensaje de error exacto).
**Archivo Final:** tests/test_juego.py

## 2025-10-22 — test_juego.py (Cobertura: Mover con Barra)
**Herramienta:** ChatGPT 

Prompt:
Escribe un test para juego.py que demuestre que el jugador 1 no puede mover su ficha del punto 5 al punto 8 si tiene 1 ficha en la barra, aunque la distancia 3 sea un dado disponible. El error debe ser: "tenés fichas en la barra: reingresá primero".

Respuesta:
[Generó el test que hace el setup de la barra, pone una ficha en el punto 5, y luego intenta mover, verificando el error de bloqueo de reingreso.]
**Instrucciones del sistema:** Ninguna.
**Uso:** Usada sin cambios.
**Archivo Final:** tests/test_juego.py

## 2025-10-22 — test_tablero.py (Cobertura: Quitar Ficha Fallida)
**Herramienta:** Gemini Advanced 

Prompt:
Necesito un test para tablero.py que verifique que el método quitar_ficha() devuelve False si el jugador_id especificado no tiene ninguna ficha en el punto dado. Esto debe cubrir una rama faltante.

Respuesta:
[Generó el test que intenta quitar la ficha del jugador 2 del punto 0, donde solo hay fichas del jugador 1, y verifica que retorna False.]
**Instrucciones del sistema:** El test debe ser simple y conciso.
**Uso:** Usada sin cambios.
**Archivo Final:** tests/test_tablero.py

## 2025-10-26 — test_juego.py (Cobertura: Distancia No Disponible)
**Herramienta:** ChatGPT 

Prompt:
Crea un test para juego.py llamado test_mover_ficha_distancia_no_disponible_registra_error. El test debe poner una ficha del Jugador 1 en 0, darles solo el dado [2], e intentar mover 3 espacios (0 a 3). Debe verificar que el movimiento falla y que el error registrado es "la distancia 3 no está en movs [2]".

Respuesta:
[Generó el test que establece los movimientos restantes y verifica la aserción de error.]
**Instrucciones del sistema:** El test debe simular que hay fichas en el origen para que la validación avance al chequeo del dado.
**Uso:** Usada sin cambios.
**Archivo Final:** tests/test_juego.py

## 2025-10-26 — test_juego.py (Cobertura: Consumo de Dados)
**Herramienta:** Gemini Advanced 

Prompt:
Escribe un test unitario para juego.py que demuestre el consumo parcial de dados. El Jugador 1 debe tener movimientos [4, 2]. Debe mover 4 (0 a 4), y la lista de movimientos restantes debe ser [2]. El turno no debe cambiar.

Respuesta:
[Generó el test que verifica la lista de movimientos restantes ([2]) y que el jugador actual sigue siendo J1.]
**Instrucciones del sistema:** Ninguna.
**Uso:** Usada sin cambios.
**Archivo Final:** tests/test_juego.py

## 2025-10-27 — test_tablero.py (Cobertura: Quitar Ficha Inexistente)
**Herramienta:** ChatGPT 

Prompt:
Crea un test en test_tablero.py para cubrir el caso donde se intenta quitar una ficha de un jugador (ID 2) de un punto (0) donde el único dueño es otro jugador (ID 1). El método quitar_ficha debe retornar False.

Respuesta:
[Generó el test que coloca una ficha de J1 en 0, intenta quitar una de J2, y verifica que retorna False.]
**Instrucciones del sistema:** Asegúrate de que el test sea claro sobre qué IDs están involucrados.
**Uso:** Usada con modificaciones (Ajuste para usar el método colocar_ficha).
**Archivo Final:** tests/test_tablero.py

## 2025-10-26 — test_juego.py (Cobertura: Distancia No Disponible)
**Herramienta:** ChatGPT 

Prompt:
Crea un test para juego.py llamado test_mover_ficha_distancia_no_disponible_registra_error. El test debe poner una ficha del Jugador 1 en 0, darle solo el dado [2], e intentar mover 3 espacios (0 a 3). Debe verificar que el movimiento falla y que el error registrado es "la distancia 3 no está en movs [2]".

Respuesta:
[Generó el test que establece los movimientos restantes y verifica la aserción de error.]
**Instrucciones del sistema:** El test debe simular que hay fichas en el origen para que la validación avance al chequeo del dado.
**Uso:** Usada sin cambios.
**Archivo Final:** tests/test_juego.py

## 2025-10-26 — test_juego.py (Cobertura: Consumo de Dados)
**Herramienta:** Gemini Advanced 

Prompt:
Escribe un test unitario para juego.py que demuestre el consumo parcial de dados. El Jugador 1 debe tener movimientos [4, 2]. Debe mover 4 (0 a 4), y la lista de movimientos restantes debe ser [2]. El turno no debe cambiar.

Respuesta:
[Generó el test que verifica la lista de movimientos restantes ([2]) y que el jugador actual sigue siendo J1.]
**Instrucciones del sistema:** Ninguna.
**Uso:** Usada sin cambios.
**Archivo Final:** tests/test_juego.py

## 2025-10-26 — test_tablero.py (Cobertura: Quitar Ficha Inexistente)
**Herramienta:** ChatGPT 

Prompt:
Crea un test en test_tablero.py para cubrir el caso donde se intenta quitar una ficha de un jugador (ID 2) de un punto (0) donde el único dueño es otro jugador (ID 1). El método quitar_ficha debe retornar False.

Respuesta:
[Generó el test que coloca una ficha de J1 en 0, intenta quitar una de J2, y verifica que retorna False.]
**Instrucciones del sistema:** Asegúrate de que el test sea claro sobre qué IDs están involucrados.
**Uso:** Usada con modificaciones (Ajuste para usar el método colocar_ficha).
**Archivo Final:** tests/test_tablero.py

## 2025-10-30 — test_juego.py (Cobertura: Falla de Reingreso por Bloqueo)
**Herramienta:** Gemini Advanced 

Prompt:
Crea un test para juego.py que simule un escenario donde el Jugador 1 tiene 1 ficha en la barra, tira un [4], e intenta reingresar al punto 4, pero el punto 4 está bloqueado por dos fichas del oponente. El movimiento debe fallar, y el dado [4] no debe consumirse.

Respuesta:
[Generó el test con el setup de la barra, la colocación de [Rival, Rival] en el punto 4, y verificó la lista de movimientos restantes.]
**Instrucciones del sistema:** Asegúrate de que el test verifique el estado final de la barra (debe seguir en 1) y los movimientos restantes.
**Uso:** Usada sin cambios.
**Archivo Final:** tests/test_juego.py

## 2025-10-30 — test_juego.py (Cobertura: Reingreso con Hit)
**Herramienta:** ChatGPT 

Prompt:
Necesito un test para juego.py que cubra el reingreso con captura (hit). El Jugador 1 reingresa al punto 5 con un [5]. En el punto 5 solo hay una ficha de B. La ficha de B debe terminar en la barra, y la ficha de A en el punto 5.

Respuesta:
[Generó el test que hace el setup de la barra para A, coloca una ficha de B en 5, y verifica que la barra de B se incremente.]
**Instrucciones del sistema:** La aserción final debe verificar tanto la barra como el punto de destino.
**Uso:** Usada sin cambios.
**Archivo Final:** tests/test_juego.py

## 2025-10-30 — test_tablero.py (Cobertura: Falla al Quitar Ficha)
**Herramienta:** Gemini Advanced 

Prompt:
Escribe un test conciso para test_tablero.py que valide la rama del método quitar_ficha() que retorna False. Esto debe ocurrir cuando el índice del punto es válido, pero el jugador_id no es dueño de ninguna ficha en esa ubicación.

Respuesta:
[Generó el test que coloca la ficha del jugador 1 en 0, y luego intenta llamar a quitar_ficha(2, 0), esperando False.]
**Instrucciones del sistema:** Ninguna.
**Uso:** Usada con modificaciones (Asegurar la claridad del setup de los IDs).
**Archivo Final:** tests/test_tablero.py

## 2025-10-30 — test_tablero.py (Cobertura: Movimiento Simple sin Ficha)
**Herramienta:** ChatGPT 

Prompt:
Crea un test para tablero.py que verifique que mover_ficha(1, 10, 13) devuelve False si el punto 10 está vacío. Esto debe cubrir una rama simple de fallo.

Respuesta:
[Generó el test que verifica el valor de retorno False y que los puntos de origen y destino permanecen vacíos.]
**Instrucciones del sistema:** Ninguna.
**Uso:** Usada sin cambios.
**Archivo Final:** tests/test_tablero.py

## 2025-10-31 — test_juego.py (Caso Borde: Movimiento Inválido)
**Herramienta:** Gemini Advanced 

Prompt:
Crea un test para juego.py que cubra el chequeo de rango inválido de destino. El test debe intentar llamar a mover_ficha(0, 24) y verificar que el error registrado es "índices fuera de rango". (Nota: hasta=24 es solo válido para sacar ficha).

Respuesta:
[Generó el test que llama a mover_ficha(0, PUNTOS) para forzar el chequeo de rango inicial en el core, ya que el valor 24 (PUNTOS) es un índice inválido para un movimiento normal de punto a punto.]
**Instrucciones del sistema:** El test debe fallar antes de la validación de bearing off.
**Uso:** Usada con modificaciones (Ajuste del mensaje de error).
**Archivo Final:** tests/test_juego.py

## 2025-10-31 — test_juego.py (Caso Borde: Doble y Consumo Parcial)
**Herramienta:** ChatGPT 

Prompt:
Crea un test para juego.py que use una tirada doble (ej. [3, 3, 3, 3]). El Jugador 1 solo debe tener fichas para hacer dos movimientos de 3. El test debe verificar que, después de esos dos movimientos, la lista de movimientos restantes sigue siendo [3, 3] y el turno NO cambia.

Respuesta:
[Generó el test que configura 4 movimientos de 3, ejecuta 2 movimientos de 3, y verifica que el turno sigue siendo el mismo y que sobran [3, 3].]
**Instrucciones del sistema:** Asegúrate de que el setup use colocar_ficha() y que los movimientos se ejecuten correctamente.
**Uso:** Usada sin cambios.
**Archivo Final:** tests/test_juego.py

## 2025-10-31 — test_tablero.py (Caso Borde: Reingreso Falla Bloqueo)
**Herramienta:** Gemini Advanced 

Prompt:
Escribe un test para test_tablero.py que simule que el Jugador 1 tiene 1 ficha en la barra. El reingreso al punto 3 debe fallar porque el punto 3 está ocupado por [Checker(2), Checker(2)]. Verifica que el método reingresar_desde_barra() retorna False y que el conteo de la barra no cambia.

Respuesta:
[Generó el test que establece el bloqueo y el conteo de la barra, verificando el retorno False.]
**Instrucciones del sistema:** El test debe usar los objetos Checker para el bloqueo.
**Uso:** Usada sin cambios.
**Archivo Final:** tests/test_tablero.py