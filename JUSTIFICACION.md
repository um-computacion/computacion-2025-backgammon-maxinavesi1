# Justificación de Diseño - Backgammon

**Autor:** Maximiliano Navesi  
**Materia:** Computación 2025  
**Fecha:** Enero 2025

---

## 1. Resumen del Diseño General

El proyecto separa la **lógica del juego (core)** de las **interfaces de usuario (CLI y Pygame)**. Esta arquitectura permite que múltiples interfaces utilicen el mismo motor de juego sin duplicar código.

**Flujo de ejecución:**
1. Usuario elige interfaz (CLI o Pygame)
2. Se crea instancia de `Juego` con 2 jugadores
3. Bucle: tirar dados → mover fichas → validar → verificar victoria
4. El juego termina cuando un jugador saca sus 15 fichas

---

## 2. Justificación de Clases

### Jugador (`jugador.py`)
**Responsabilidad:** Representar la identidad de cada participante.

**Por qué:** Necesitamos identificar a quién pertenece cada ficha. El ID autoincremental garantiza unicidad.

**Atributos:**
- `__nombre__`: Identificación humana
- `__id__`: Identificación única numérica

---

### Checker (`checker.py`)
**Responsabilidad:** Representar una ficha individual.

**Por qué:** Encapsular el concepto de ficha como objeto facilita su manipulación y comparación.

**Atributos:**
- `__pid__`: ID del jugador propietario

---

### Dados (`dados.py`)
**Responsabilidad:** Generar tiradas y calcular movimientos disponibles.

**Por qué:** Centralizar la aleatoriedad permite reproducibilidad con semillas para testing.

**Atributos:**
- `__semilla__`: Para reproducibilidad
- `__rng__`: Generador aleatorio independiente
- `__ultimo_tiro__`: Registro de última tirada

**Regla especial:** Si sale doble (ej: 6-6), el jugador tiene 4 movimientos.

---

### Tablero (`tablero.py`)
**Responsabilidad:** Mantener el estado físico del juego (24 puntos, barra, salidas).

**Por qué:** Es la estructura de datos central. Todas las operaciones sobre fichas pasan por aquí.

**Atributos:**
- `__puntos__`: Lista de 24 listas (cada una con fichas de ese punto)
- `__barra__`: Diccionario {jugador_id: cantidad} para fichas capturadas
- `__salidas__`: Diccionario {jugador_id: cantidad} para fichas sacadas

**Métodos clave:**
- `mover_ficha_seguro()`: Aplica reglas físicas (bloqueos, capturas)
- `reingresar_desde_barra()`: Reingresa fichas capturadas
- `sacar_ficha()`: Bearing off (sacar del tablero)
- `puede_sacar_fichas()`: Verifica si todas las fichas están en home board

---

### Juego (`juego.py`)
**Responsabilidad:** Coordinar el flujo del juego y aplicar reglas de alto nivel.

**Por qué:** Es el controlador principal. Valida movimientos según las reglas de Backgammon y gestiona turnos.

**Atributos:**
- `__tablero__`: Estado físico del juego
- `__dados__`: Generador de movimientos
- `__jugadores__`: Lista con los 2 jugadores
- `__indice_jugador_actual__`: 0 o 1 (quién juega)
- `__estado__`: "inicial", "en_curso", "terminado"
- `__movs_restantes__`: Lista de dados disponibles para usar
- `__ultimo_error__`: Mensaje del último error (para UI)

**Métodos clave:**
- `_validar_movimiento()`: Verifica todas las reglas antes de mover
- `aplicar_movimiento()`: Ejecuta el movimiento y consume el dado
- `mover_ficha()`: Mueve y cambia turno si se acabaron los dados

---

## 3. Justificación de Atributos

**Convención `__atributo__`:**  
Todos los atributos usan doble guion bajo como prefijo y sufijo según requisito del proyecto. Esto indica que son privados y solo se accede mediante propiedades.

**Por qué cada atributo:**

| Clase | Atributo | Justificación |
|-------|----------|---------------|
| Juego | `__tablero__` | Delega gestión de posiciones |
| Juego | `__dados__` | Delega generación aleatoria |
| Juego | `__movs_restantes__` | Lista que se consume al mover |
| Juego | `__ultimo_error__` | Comunicación de errores a UI |
| Tablero | `__puntos__` | Estructura principal (24 pilas de fichas) |
| Tablero | `__barra__` | Fichas capturadas por jugador |
| Tablero | `__salidas__` | Fichas sacadas (cuenta hacia victoria) |

---

## 4. Decisiones de Diseño Relevantes

### 4.1 Separación Core / UI
**Decisión:** La lógica del juego no conoce las interfaces.

**Alternativas descartadas:**
- Lógica mezclada con Pygame → No testeable ni reutilizable
- Lógica en CLI → Dificulta agregar Pygame después

**Ventaja elegida:** Permite múltiples interfaces sin duplicar lógica.

---

### 4.2 Validación Centralizada
**Decisión:** Toda validación en `Juego._validar_movimiento()`.

**Por qué:** Una sola fuente de verdad. Fácil de probar y modificar.

---

### 4.3 Bearing Off con Dado Mayor
**Regla de Backgammon:** Si no puedes usar el número exacto, puedes sacar una ficha más lejana con un dado mayor.

**Implementación:**
```python
def es_ficha_mas_lejana(self, jugador_id: int, punto: int) -> bool:
    # Verifica si hay fichas más atrás que 'punto'
    
def _dado_mayor_que(self, distancia_minima: int) -> int | None:
    # Busca el menor dado disponible >= distancia
```

---

### 4.4 Movimientos como Lista Mutable
**Decisión:** `__movs_restantes__` es una lista que se modifica con `remove()`.

**Por qué:** Simple y soporta dobles naturalmente (ej: [6,6,6,6]).

---

### 4.5 Dirección por Jugador
**Regla:** Jugador 1 (impar) se mueve 0→23, Jugador 2 (par) se mueve 23→0.

**Implementación:**
```python
if pid % 2 != 0:  # Jugador 1
    valido = hasta > desde
else:  # Jugador 2
    valido = hasta < desde
```

---

## 5. Excepciones y Manejo de Errores

### 5.1 Excepciones Definidas

**Solo se usa `ValueError` para errores de programación:**
```python
def validar_indice_punto(self, i):
    if not 0 <= i < PUNTOS:
        raise ValueError(f"índice de punto inválido: {i}")
```

**Por qué solo ValueError:**
- Errores de índices son bugs del programador
- Errores de juego (movimiento inválido) retornan `False` con mensaje

---

### 5.2 Estrategia

**Errores de programación → Exception**
- Índice fuera de rango (0-23)
- Parámetros inválidos

**Errores de juego → Return False + mensaje**
- Movimiento inválido
- Punto bloqueado
- Dado no disponible

**Ventaja:** La UI no necesita try/except para manejar movimientos del usuario.

---

## 6. Estrategias de Testing y Cobertura

### 6.1 Qué se probó

**Tests de Tablero (core):**
- Colocar y quitar fichas
- Movimientos básicos
- Bloqueo por oponente (2+ fichas)
- Capturas (hits)
- Reingresos desde barra
- Bearing off
- Detección de victoria

**Tests de Juego:**
- Validación de dirección por jugador
- Consumo de dados al mover
- Cambio de turnos
- Bearing off con dado mayor
- Prioridad de reingresos

---

### 6.2 Por qué estos tests

**Tablero:** Es la estructura crítica. Errores aquí rompen el juego.  
**Juego:** Coordina todo. Los tests verifican que las reglas se aplican correctamente.

**Cobertura alcanzada:**
- Lógica core: >90%
- CLI: ~50% (comandos básicos)
- Pygame: ~30% (manual, difícil automatizar UI)

**Por qué no 100% en UI:** Las interfaces gráficas requieren interacción humana.

---

### 6.3 Testing Determinístico

**Decisión:** Tests de dados usan semilla fija.

```python
dados = Dados(semilla=42)
d1, d2, movs = dados.tirar()
# Siempre retorna los mismos valores
```

**Ventaja:** Tests reproducibles y confiables en CI/CD.

---

## 7. Principios SOLID

### Single Responsibility (SRP)
✅ Cada clase tiene una responsabilidad:
- `Jugador`: Solo identidad
- `Dados`: Solo generar tiradas
- `Tablero`: Solo estado físico
- `Juego`: Solo coordinar flujo

---

### Open/Closed (OCP)
✅ Extensible sin modificar código:
- Agregar nueva UI no requiere cambiar `Juego` ni `Tablero`
- Ejemplo: Se puede crear `WebUI` sin tocar el core

---

### Liskov Substitution (LSP)
✅ Las interfaces son intercambiables:
- `CLI` y `PygameUI` usan la misma API de `Juego`
- Ambas funcionan idénticamente desde el punto de vista del usuario

---

### Interface Segregation (ISP)
✅ Interfaces mínimas y cohesivas:
- `Juego` expone solo lo necesario: `tirar()`, `mover_ficha()`, `estado`
- No expone detalles internos del tablero

---

### Dependency Inversion (DIP)
✅ Dependencias hacia abstracciones:
- UI depende de `Juego` (abstracción), no de implementación del `Tablero`
- Fácil de testear con mocks

---

## 8. Anexos: Diagrama UML de Clases

```
                    ┌─────────────────┐
                    │      Juego      │
                    ├─────────────────┤
                    │ -__tablero__    │───────┐
                    │ -__dados__      │───┐   │
                    │ -__jugadores__  │─┐ │   │
                    │ -__movs_rest__  │ │ │   │
                    ├─────────────────┤ │ │   │
                    │ +tirar()        │ │ │   │
                    │ +mover_ficha()  │ │ │   │
                    │ +termino()      │ │ │   │
                    └─────────────────┘ │ │   │
                              ┌─────────┘ │   │
                              │           │   │
                    ┌─────────▼──┐   ┌────▼────┐   ┌──────────────┐
                    │  Jugador   │   │  Dados  │   │   Tablero    │
                    ├────────────┤   ├─────────┤   ├──────────────┤
                    │ -__id__    │   │ -__rng__│   │ -__puntos__  │──┐
                    │ -__nombre__│   ├─────────┤   │ -__barra__   │  │
                    ├────────────┤   │+tirar() │   │ -__salidas__ │  │
                    │ +id        │   └─────────┘   ├──────────────┤  │
                    │ +nombre    │                 │ +mover()     │  │
                    └────────────┘                 │ +sacar()     │  │
                                                   └──────────────┘  │
                                                                     │
                                                   ┌──────────────┐  │
                                                   │   Checker    │◄─┘
                                                   ├──────────────┤
                                                   │ -__pid__     │
                                                   ├──────────────┤
                                                   │ +owner_id    │
                                                   └──────────────┘
```

**Relaciones:**
- Juego **tiene-un** Tablero, Dados, y 2 Jugadores (composición)
- Tablero **contiene** múltiples Checkers (agregación)
- Checker **pertenece-a** un Jugador (asociación)
