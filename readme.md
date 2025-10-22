# Backgammon - Computación 2025

Implementación completa del juego de Backgammon en Python con interfaz de línea de comandos (CLI) y interfaz gráfica usando Pygame.

![Python](https://img.shields.io/badge/python-3.10+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Coverage](https://img.shields.io/badge/coverage-90%25-brightgreen.svg)

## 📋 Tabla de Contenidos

- [Descripción](#descripción)
- [Características](#características)
- [Requisitos](#requisitos)
- [Instalación](#instalación)
- [Uso](#uso)
- [Testing](#testing)
- [Docker](#docker)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Contribución](#contribución)

## 📖 Descripción

Este proyecto implementa el juego clásico de Backgammon siguiendo las reglas tradicionales. El diseño separa completamente la lógica del juego (core) de las interfaces de usuario, permitiendo múltiples formas de interacción.

**Reglas del juego:** [Wikipedia - Backgammon](https://es.wikipedia.org/wiki/Backgammon)

## ✨ Características

- ✅ Lógica completa del juego de Backgammon
- ✅ Interfaz de línea de comandos (CLI)
- ✅ Interfaz gráfica con Pygame
- ✅ Movimientos válidos, capturas y bearing off
- ✅ Reingresos desde la barra
- ✅ Detección automática de victoria
- ✅ Tests unitarios con >90% de cobertura
- ✅ Integración continua con GitHub Actions
- ✅ Análisis de calidad de código con Pylint

## 🔧 Requisitos

- Python 3.10 o superior
- pip (gestor de paquetes de Python)
- Docker (opcional, para ejecución en contenedor)

## 📥 Instalación

### Instalación Local

1. **Clonar el repositorio:**
```bash
git clone https://github.com/tu-usuario/computacion-2025-backgammon-maxinavesi1.git
cd computacion-2025-backgammon-maxinavesi1
```

2. **Crear entorno virtual:**
```bash
python -m venv .venv
```

3. **Activar entorno virtual:**

**Windows:**
```bash
.venv\Scripts\activate
```

**Linux/Mac:**
```bash
source .venv/bin/activate
```

4. **Instalar dependencias:**
```bash
pip install -r requirements.txt
```

## 🎮 Uso

### Modo Interfaz Gráfica (Pygame)

Ejecutar la interfaz gráfica:

```bash
python -m backgammon.pygame.pygame_ui
```

**Controles:**
- **T** - Tirar dados
- **C** - Cambiar turno
- **R** - Reiniciar juego
- **ESC** - Salir
- **Click** - Seleccionar y mover fichas

### Modo Línea de Comandos (CLI)

Ejecutar la CLI:

```bash
python main.py --ayuda
```

**Comandos disponibles:**

```bash
# Ver ayuda
python main.py --ayuda

# Tirar dados
python main.py --tirar

# Mover ficha
python main.py --mover 0 3

# Ver estado del juego
python main.py --estado

# Usar semilla fija para reproducibilidad
python main.py --semilla 42 --tirar --mover 0 3
```

**Ejemplo de partida completa:**

```bash
python main.py --semilla 123 --tirar --mover 23 21 --mover 12 10 --estado
```

## 🧪 Testing

### Ejecutar Tests Localmente

```bash
# Ejecutar todos los tests
python -m unittest discover

# Ejecutar tests de un módulo específico
python -m unittest backgammon.tests.test_tablero

# Ejecutar con coverage
coverage run -m unittest discover
coverage report -m
coverage html  # Genera reporte HTML en htmlcov/
```

### Cobertura de Código

El proyecto mantiene una cobertura de código superior al 90% como requisito mínimo.

```bash
# Ver reporte de cobertura
coverage report -m

# Ver reporte detallado en el navegador
coverage html
open htmlcov/index.html  # Linux/Mac
start htmlcov/index.html # Windows
```

## 🐳 Docker

### Modo Juego (Interfaz Gráfica)

```bash
# Construir imagen
docker build -t backgammon-game .

# Ejecutar (requiere X11 en Linux/Mac o XServer en Windows)
docker run -it --rm \
  -e DISPLAY=$DISPLAY \
  -v /tmp/.X11-unix:/tmp/.X11-unix \
  backgammon-game
```

**Windows con XServer:**
1. Instalar [VcXsrv](https://sourceforge.net/projects/vcxsrv/)
2. Iniciar XLaunch con "Disable access control"
3. Ejecutar:
```bash
docker run -it --rm -e DISPLAY=host.docker.internal:0 backgammon-game
```

### Modo Testing

```bash
# Ejecutar tests en Docker
docker build -t backgammon-test -f Dockerfile.test .
docker run --rm backgammon-test

# Ver cobertura
docker run --rm backgammon-test coverage report -m
```

### Docker Compose

```bash
# Ejecutar ambiente completo
docker-compose up

# Ejecutar solo tests
docker-compose run test

# Limpiar
docker-compose down
```

## 📁 Estructura del Proyecto

```
computacion-2025-backgammon-maxinavesi1/
├── backgammon/
│   ├── core/              # Lógica del juego
│   │   ├── __init__.py
│   │   ├── juego.py       # Clase principal Juego
│   │   ├── tablero.py     # Tablero con 24 puntos
│   │   ├── jugador.py     # Clase Jugador
│   │   ├── dados.py       # Lógica de dados
│   │   └── checker.py     # Ficha individual
│   ├── cli/               # Interfaz de línea de comandos
│   ├── pygame/            # Interfaz gráfica
│   │   └── pygame_ui.py
│   └── tests/             # Tests unitarios
│       └── test_tablero.py
├── .github/
│   └── workflows/
│       └── ci.yml         # CI/CD con GitHub Actions
├── main.py                # Punto de entrada CLI
├── requirements.txt       # Dependencias
├── Dockerfile             # Imagen para juego
├── Dockerfile.test        # Imagen para testing
├── docker-compose.yml     # Orquestación
├── .pylintrc              # Configuración Pylint
├── README.md              # Este archivo
├── CHANGELOG.md           # Historial de cambios
└── JUSTIFICACION.md       # Justificación de diseño
```

## 🏗️ Arquitectura

El proyecto sigue el principio de **separación de responsabilidades**:

- **core/**: Lógica pura del juego, independiente de la UI
- **cli/**: Interfaz de texto que consume core/
- **pygame/**: Interfaz gráfica que consume core/

**Principios SOLID aplicados:**
- **S**ingle Responsibility: Cada clase tiene una única responsabilidad
- **O**pen/Closed: Extensible sin modificar código existente
- **L**iskov Substitution: Las interfaces son intercambiables
- **I**nterface Segregation: Interfaces específicas y cohesivas
- **D**ependency Inversion: Dependencias hacia abstracciones

### Desarrollo

```bash
# Instalar dependencias de desarrollo
pip install -r requirements-dev.txt

# Ejecutar linter
pylint backgammon/


# Ejecutar tests antes de commit
python -m unittest discover
```




