# Changelog
Formato basado en [Keep a Changelog 1.1.0] y [SemVer].  

## [Unreleased] — cierra 2025-10-15
### Added
- CLI: **secuencia de comandos** (encadenar `--tirar --poner 0 --mover 0 3`, etc.).
- CLI: **`--semilla <n>`** para tiradas reproducibles (y tests asociados).
- Ajustes de tablero para **demo vacía** y helpers simples de movimiento.

### Changed
- CLI migrado a **API pública de `Juego`** (sin tocar atributos internos).
- Pequeñas mejoras en mensajes y prompts de documentación.

### Fixed
- Correcciones de tests de tablero/CLI para reflejar el comportamiento actual.

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
- Clases base en `core`:
  - `Jugador` (nombre + id autoincremental),
  - `Dados` (tiradas, manejo de dobles),
  - `Tablero` (24 puntos, validación de índices, barra y salidas),
  - `Juego` (turnos, tirar, ganador).
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