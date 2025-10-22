# Changelog
Formato basado en [Keep a Changelog 1.1.0] y [SemVer]. 

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

## [0.3.0] — 2025-10-01  *(Sprint 3: 2025-09-18 → 2025-10-01)*
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

## [0.2.0] — 2025-09-17  *(Sprint 2: 2025-09-04 → 2025-09-17)*
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

## [0.1.0] — 2025-09-03  *(Sprint 1: 2025-08-20 → 2025-09-03)*
### Added
- **Estructura inicial** del proyecto (`backgammon/` y `tests/`).  
- [cite_start]Clases base en `core`: `Jugador`, `Dados`, `Tablero`, `Juego` [cite: 107-109].
- **CLI inicial** con comando `--tirar`.
- **Tests iniciales** de `dados`, `tablero` y `juego`.
- **Docstrings** mínimos.
- **Dockerfile** y `.dockerignore`.

### Changed
- Ajustes de setup y estructura de carpetas.
- Mejoras simples en `juego` y `tablero`.

### Fixed
- Primeros fixes post-setup (importaciones/rutas y detalles menores).