# 🎮 Simulador de Evolución de Pokémon con Algoritmos Genéticos

## 📋 Descripción General

Este proyecto implementa un simulador de evolución de Pokémon utilizando algoritmos genéticos. El sistema simula cómo las características de los Pokémon (ataque, defensa, velocidad, vida) evolucionan a través de generaciones, aplicando principios de selección natural y genética.

## 🎯 Características Principales

###  🧬 Algoritmo Genético Completo

- Selección por ruleta: Los Pokémon con mejor fitness tienen mayor probabilidad de reproducirse

- Cruce de un punto: Combina características de dos Pokémon padres

- Mutación aleatoria: Introduce variabilidad genética

- Elitismo: Conserva los mejores individuos entre generaciones

### 🎨 Interfaz Gráfica Interactiva

- Controles en tiempo real: Ejecutar generaciones individuales o múltiples

- Visualización de datos: Gráficos de evolución del fitness

- Lista de Pokémon: Top 10 de la población actual

- Estadísticas detalladas: Mejor, promedio y peor fitness por generación

## 🏗️ Estructura del Proyecto

##### 🐍 Clase Pokemon

```python

class Pokemon:
    def __init__(self, ataque, defensa, velocidad, vida, tipo):
        self.ataque = ataque      # 0.0 - 1.0
        self.defensa = defensa    # 0.0 - 1.0  
        self.velocidad = velocidad # 0.0 - 1.0
        self.vida = vida          # 0.0 - 1.0
        self.tipo = tipo          # fuego, agua, planta, electrico, tierra
        self.fitness = 0
```

#### ⚙️ Sistema de Fitness

```python
def calcular_fitness(self):
    poder = (self.ataque * 0.3 +    # Ataque: 30% de importancia
            self.defensa * 0.2 +    # Defensa: 20% de importancia  
            self.velocidad * 0.25 + # Velocidad: 25% de importancia
            self.vida * 0.25)       # Vida: 25% de importancia
    
    # Bonus por tipo
    if self.tipo == 'fuego': poder *= 1.1    # +10% bonus
    elif self.tipo == 'agua': poder *= 1.05  # +5% bonus
    elif self.tipo == 'electrico': poder *= 1.03  # +3% bonus
```

## 🎮 Cómo Usar el Simulador

2. Controles disponibles:

- "Ejecutar Una Generación": Avanza una generación

- "Ejecutar 10 Generaciones": Avanza 10 generaciones automáticamente

- "Reiniciar Simulación": Comienza desde cero

## 📊 Interpretación de Resultados

Estado Inicial (Generación 0)

- Población diversa: Diferentes tipos y estadísticas

- Fitness variado: Desde 0.53 hasta 0.83

- Distribución aleatoria: Sin patrones evolutivos

Estado Evolucionado (Generación 10)

-Población optimizada: Pokémon tipo fuego dominan

- Fitness mejorado: Mejor fitness de 0.91

- Estadísticas equilibradas: Combinación óptima de características

## ⚙️ Parámetros Configurables
```python

# Configuración del algoritmo genético
POBLACION_SIZE = 20      # Número de Pokémon por generación
GENERACIONES = 50        # Máximo de generaciones
MUTACION_PROB = 0.1      # 10% probabilidad de mutación
ELITISMO = 2             # 2 mejores Pokémon conservados
```

### 🎯 Tipos de Pokémon y Bonificaciones

- 🔥 Fuego: +10% bonus (fitness × 1.1)

- 💧 Agua: +5% bonus (fitness × 1.05)

- ⚡ Eléctrico: +3% bonus (fitness × 1.03)

- 🌿 Planta: Sin bonus

- 🌍 Tierra: Sin bonus

## 📈 Análisis de la Evolución

### 🔍 Patrones Observados

- Dominancia del tipo fuego: Debido al bonus del 10%

- Optimización de defensa: Valores altos de defensa (0.97) son comunes

- Convergencia rápida: Mejora significativa en primeras generaciones

- Estancamiento evolutivo: Después de 10 generaciones, mejora marginal

## 📊 Métricas de Rendimiento

```text

Generación	Mejor Fitness	Promedio Fitness	Peor Fitness
0	        0.83	        ~0.65	            0.53
10	        0.91	        0.83	            0.54
Mejora	    +9.6%	        +27.7%	            +1.9%

```

## 🧪 Experimentación y Personalización

### 🔧 Modificar Parámetros

```python

# Para experimentar con diferentes configuraciones:
POBLACION_SIZE = 30     # Más diversidad genética
MUTACION_PROB = 0.05    # Menos mutaciones
ELITISMO = 5            # Conservar más individuos
```

### 🎯 Cambiar Sistema de Fitness

```python
# Modificar pesos de las características:
poder = (self.ataque * 0.4 +     # Más importancia al ataque
        self.defensa * 0.15 +    # Menos importancia a defensa
        self.velocidad * 0.25 + 
        self.vida * 0.2)
```

## 🖼️ Visualización de la Interfaz

#### Estado Inicial - Generación 0

1. Características visibles:

- Panel de control con botones de ejecución

- Información de generación en cero

- Gráfico vacío listo para mostrar evolución

- Tabla de población con Pokémon iniciales aleatorios

![Interfaz Inicial](https://raw.githubusercontent.com/sharito2023s-oss/Taller_2/main/Images/InterfazPokemon.png)

#### Estado Evolucionado - Generación 10

2. Mejoras observadas:

- Fitness mejorado de 0.00 a 0.91

- Gráfico de evolución mostrando progreso

- Pokémon histórico con estadísticas óptimas

- Población homogénea indicando convergencia

![Interfaz Inicial](https://raw.githubusercontent.com/sharito2023s-oss/Taller_2/main/Images/InterfazPokemon2.png)


## 👥 Autores

#### 🧑‍💻 Contribuidores Principales

- **Carlos Andrés Suárez Torres** → [Carlos23Andres](https://github.com/Carlos23Andres)  

- **Saira Sharid Sanabria Muñoz** → [sharito202](https://github.com/sharito202)
