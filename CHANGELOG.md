# Changelog
Formato basado en [Keep a Changelog 1.1.0] y [SemVer]. 

## [0.6.0] — 2025-10-31 *(Sprint 6: 2025-10-30 → 2025-10-31)*
### Added
- **Selección visual de barra:** Implementación de la constante `BARRA_SELECCION` para permitir seleccionar fichas capturadas mediante click en la barra central.
- **Indicadores visuales mejorados:** Hints verdes que muestran movimientos válidos desde la barra y puntos de reingreso.
- **Numeración completa del tablero:** Inclusión del punto 0 en las etiquetas visuales del tablero.
- **Detección de clicks en barra:** Función `point_or_out_bar_from_xy` actualizada para detectar clicks en la barra central.

### Changed
- **Corrección de dirección de movimientos:** 
  - J1 (Blancas, ID impar) ahora decrementa correctamente (23→0) en movimientos de tablero.
  - J2 (Negras, ID par) ahora incrementa correctamente (0→23) en movimientos de tablero.
  - Reingreso desde barra: J1 incrementa desde punto 0, J2 decrementa desde punto 23.
- **Refactorización de `puede_sacar_fichas`:** Corrección de la lógica de validación de home boards (J1: 0-5, J2: 18-23).
- **Actualización de `es_ficha_mas_lejana`:** Corrección de la detección de fichas más lejanas para bearing off correcto.
- **Funciones de hints en pygame_ui:** `dibujar_hints`, `_tiene_movimientos_validos` y `manejar_evento_tirada` actualizadas con lógica de dirección correcta.

### Fixed
- **Bug crítico de dirección:** Corrección de lógica invertida en `_validar_movimiento` que impedía movimientos válidos para J1.
- **Cálculo de distancias en bearing off:** Corrección de fórmulas de distancia (J1: `desde + 1`, J2: `24 - desde`).
- **Tests de bearing off:** Actualización de 6 tests con posiciones correctas según home boards reales:
  - `test_bearing_off_exacto_j1_consume_dado`
  - `test_bearing_off_over_bearing_j1_consume_dado_mayor`
  - `test_bearing_off_over_bearing_falla_si_hay_ficha_mas_lejana_j1`
  - `test_bearing_off_exacto_j2`
  - `test_es_ficha_mas_lejana_j1_con_fichas_mas_cerca`
  - `test_es_ficha_mas_lejana_j2_con_fichas_mas_lejos`
- **Reingreso desde barra:** Corrección completa del flujo de reingreso con detección de clicks, validación y movimiento.
- **Warnings de Pylint:** Eliminación de variable sin usar `board_rect` en `dibujar_barra`.

### Removed
- Lógica obsoleta de detección de punto 0 que causaba confusión en la interfaz.

---

## [0.5.0] — 2025-10-31 *(Sprint 5: 2025-10-15 → 2025-10-29)*
### Added
- **Clase `Checker`:** Implementación del objeto ficha (`core/checker.py`) para el diseño orientado a objetos.
- **Lógica de Bearing Off:** Implementación de `puede_sacar_fichas` y `sacar_ficha` en `Tablero`.
- **Regla de Over-Bearing:** Lógica para usar dados mayores si la ficha está en el punto más lejano (implementada en `core/juego.py`).
- **Posición Inicial Estándar:** Implementación de la función `posicion_inicial_estandar` y test de validación.
- **Archivos de Prompts:** Creación de los archivos de registro de IA obligatorios (`prompts/`).

### Changed
- **Refactorización Core:** Migración completa de `Tablero` y `Juego` para manejar instancias de `Checker` en lugar de IDs de jugador (`int`).
- **Pygame UI:** Finalización de la interfaz gráfica con soporte para el *Bearing Off* (movimiento a 24) y carga de la posición inicial estándar.

### Fixed
- Corrección de *tests* que fallaban al migrar a la clase `Checker` (resolviendo `AttributeError`).
- Solución de problemas de la tubería de CI para asegurar la visibilidad del reporte de Pylint.

---

## [0.4.0] — 2025-10-20 *(Sprint 4: 2025-10-01 → 2025-10-15)*
### Added
- **Movimientos en CLI**: Soporte para encadenar comandos (`--mover 0 3`).
- **Lógica de Reingreso:** Implementación de la función auxiliar `_entrada_para` para el reingreso desde la barra.
- **Tests Adicionales:** Tests exhaustivos para validar el consumo parcial de dados y los movimientos inversos.

### Changed
- **Pygame UI:** Implementación de la visualización de la barra de salida (Home Bar).

### Fixed
- Corrección de *tests* de tablero/CLI para reflejar el comportamiento actual de captura.

---

## [0.3.0] — 2025-10-01  *(Sprint 3: 2025-09-18 → 2025-10-01)*
### Added
- **Movimientos en CLI**: `--mover <desde> <hasta>` y **`--movs`** para listar movimientos disponibles.  
- **Tests extra** (tablero/juego/dados) → objetivo de **>90% de coverage**.
- **SonarCloud** en CI y **Pylint** con `.pylintrc`.
- **Helpers** en `core` para facilitar operaciones del tablero.

### Changed
- CLI: refactor y salidas más legibles.  
- Reorganización y nombres de archivos en `tests/`.

### Fixed
- Acceso indebido a `tablero` desde el exterior (ahora vía métodos públicos).
- Ajustes de tests que no coincidían con el comportamiento real.

---

## [0.2.0] — 2025-09-17  *(Sprint 2: 2025-09-04 → 2025-09-17)*
### Added
- **UI mínima con Pygame** (ventana, rótulo, puntos y tecla **T** para tirar y mostrar dados).  
- **Ayuda del CLI** (`--ayuda`/`-h`) con uso y ejemplos.
- **Soporte de semillas** en `Dados` y exposición desde el CLI.
- **Entorno virtual** documentado y usado en desarrollo.
- **Coverage** configurado y primeros reportes.

### Changed
- Docstrings y estilo en módulos de `core`.  
- Primeros pasos de integración del CLI con `Juego` y `Tablero`.

### Fixed
- Correcciones en tests y estructura de paquetes de pruebas.

---

## [0.1.0] — 2025-09-03  *(Sprint 1: 2025-08-20 → 2025-09-03)*
### Added
- **Estructura inicial** del proyecto (`backgammon/` y `tests/`).  
- Clases base en `core`: `Jugador`, `Dados`, `Tablero`, `Juego`.
- **CLI inicial** con comando `--tirar`.
- **Tests iniciales** de `dados`, `tablero` y `juego`.
- **Docstrings** mínimos.
- **Dockerfile** y `.dockerignore`.

### Changed
- Ajustes de setup y estructura de carpetas.
- Mejoras simples en `juego` y `tablero`.

### Fixed
- Primeros fixes post-setup (importaciones/rutas y detalles menores).

---

[Keep a Changelog 1.1.0]: https://keepachangelog.com/es-ES/1.1.0/
[SemVer]: https://semver.org/lang/es/