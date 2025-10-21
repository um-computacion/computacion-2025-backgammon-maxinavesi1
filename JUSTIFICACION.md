## 1. Diseño Arquitectónico: Principios SOLID y Abstracción

El proyecto de Backgammon fue diseñado bajo una **Arquitectura de Tres Capas (Core - Abstracción - Presentación)**. Esta estructura es la base para el cumplimiento riguroso de los principios SOLID.

### 1.1. Principio de Responsabilidad Única (SRP)

Cada módulo y clase en la capa `core/` tiene una única razón para cambiar, maximizando la cohesión.

| Clase | Responsabilidad Única | Justificación de la Decisión |
| :--- | :--- | :--- |
| **`Tablero`** | **Estructura de Datos:** Modelado de los 24 puntos, barra y salidas. Gestiona las reglas de **colocación, captura y bloqueo**. | No tiene conocimiento de turnos ni consumo de dados. |
| **`Juego`** | **Coordinador de Flujo:** Gestiona el estado de la partida, turnos, y la **validación compleja de reglas** (ej: *over-bearing*, reingreso, consumo de dados). | Delega la estructura al `Tablero` y la aleatoriedad a `Dados`. |
| **`Checker`** | **Identidad de Ficha:** Encapsula la propiedad (`__pid__`). Su existencia mejora la POO, ya que `Tablero` maneja objetos, no IDs primitivos. | [cite_start]Su implementación fue un requisito de diseño fundamental[cite: 110]. |
| **`Dados`** | **Aleatoriedad:** Generación de tiradas y aplicación inmediata de la regla de dobles (4 movimientos). | |

### 1.2. Principio de Inversión de Dependencias (DIP)

El módulo de alto nivel (`Juego`) no depende de las implementaciones concretas, sino de abstracciones:

* **Inyección de Dependencias:** El constructor de `Juego` recibe instancias de `Tablero` y `Dados`. Esto permite reemplazar el `Tablero` fácilmente por un *Mock* durante el testing, garantizando que probamos la lógica de `Juego` de forma aislada.
* **Propiedades:** El acceso a los atributos internos (ej., `self.__tablero__`) se realiza únicamente a través de *getters* (`@property tablero`), desacoplando el uso externo del almacenamiento interno.

---

## 2. Lógica de Negocio y Justificación de Atributos

### 2.1. Justificación de Atributos Internos

Todos los atributos de instancia se definen con doble guion bajo (`self.__atributo__`) para asegurar el **máximo encapsulamiento**, impidiendo la manipulación externa y forzando el acceso a través de los métodos públicos definidos por el desarrollador.

| Clase | Atributos Clave (Ejemplos) | Justificación de la Elección |
| :--- | :--- | :--- |
| **`Tablero`** | `__puntos__`, `__barra__`, `__salidas__` | Utilización de estructuras de Python nativas (`list[list[Checker]]` y `dict[int, int]`) para una alta velocidad de acceso y manipulación por índice. |
| **`Juego`** | `__movs_restantes__` | Almacena la lista de dados disponibles. Al ser una lista, permite la remoción secuencial de valores tras cada movimiento, crucial para la regla de consumo de dados. |
| **`Dados`** | `__rng__` | Instancia de `random.Random` para permitir la **fijación de semillas** y la reproducibilidad de las tiradas, esencial para el testing automatizado. |

### 2.2. Decisiones de Diseño de Reglas

* **Bearing Off Complejo:** La lógica de *over-bearing* (usar un dado de 5 para sacar una ficha en el punto 23 (distancia 1)) se implementó en `Juego` mediante la función `_dado_mayor_que`, que permite consumir el dado más grande disponible si la ficha es la más lejana en el *home board*.
* **Estrategia de Movimiento:** Se usa el valor especial `PUNTOS` (`24`) como índice de destino para representar el acto de "sacar la ficha fuera del tablero", simplificando la interfaz del método `mover_ficha(desde, hasta)`.

---

## 3. Estrategia de Calidad y Trazabilidad

### 3.1. Testing y Cobertura (Requisito >90%)

La estrategia se centró en lograr una alta **cobertura de ramas** para garantizar la fiabilidad del `core/`.

* **Cobertura Lograda:** El proyecto alcanzó la meta de **$\ge 90\%$ de cobertura de código** en la lógica central, como lo demuestran los reportes automatizados.
* **Pruebas de Reglas de Borde:** Se implementaron *tests* específicos para:
    * **Bloqueo/Reingreso:** Verificación de que el jugador con fichas en la barra **no puede** mover ninguna otra ficha del tablero, y que el reingreso con *hit* funciona correctamente.
    * **Consumo de Dados:** *Tests* que aseguran que la lista `__movs_restantes__` se actualiza correctamente tras movimientos simples, dobles y *bearing off*.

### 3.2. Trazabilidad de la Documentación (IA Prompts)

Se utilizó la documentación de *prompts* para la trazabilidad y justificación de las decisiones complejas de refactorización y *testing*. Los archivos en la carpeta `prompts/` actúan como el historial de QA y diseño, cumpliendo con el requisito de documentación de la cátedra.