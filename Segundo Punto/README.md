# 🎵 Sistema de Recomendación Spotify con Algoritmo de Colonias de Hormigas

## 📋 Descripción General

Este proyecto implementa un sistema de recomendación musical inteligente utilizando el algoritmo de colonias de hormigas. El sistema genera playlists personalizadas basadas en las preferencias del usuario, similitud musical y la "sabiduría colectiva" representada por feromonas.

## 🎯 Características Principales

###  🐜 Algoritmo de Colonias de Hormigas Completo

- UsuarioHormiga: Cada hormiga construye playlists basadas en feromonas y preferencias

- Evaluación de Transiciones: Combina feromonas, similitud musical y afinidad del usuario

- Actualización de Feromonas: Evaporación y deposición basada en la calidad de las playlists

### 🎵 Base de Datos Musical

- 10 canciones con características detalladas (rock, pop, jazz, energía, bailabilidad)

- 5 tipos de usuario predefinidos con preferencias específicas

### 🎨 Interfaz Visual Completa

- Selección de Tipo de Usuario: Rockero, PopLover, JazzFan, etc.

- Visualización de Canciones: Tabla con todas las características

- Gráfico de Evolución: Muestra cómo mejora la calidad de las recomendaciones

- Grafo de Recomendaciones: Visualiza conexiones entre canciones basadas en feromonas

## 🖼️ Visualización de la Interfaz

#### Estado Inicial - Iteración 0

1. Componentes visibles:

- Panel de configuración con selección de usuario

- Botones de control para ejecutar iteraciones

- Tabla de canciones con características detalladas

- Gráficos vacíos listos para mostrar evolución

![Interfaz Inicial](https://raw.githubusercontent.com/sharito2023s-oss/Taller_2/main/Images/InterfazSpotify.png)

#### Estado Evolucionado - Iteración 10

2. Mejoras observadas:
- Calidad mejorada de 0.00 a 0.2156

- Playlist optimizada generada automáticamente

- Grafo de recomendaciones mostrando conexiones fuertes

- Evolución visible en el gráfico de calidad

![Interfaz Inicial](https://raw.githubusercontent.com/sharito2023s-oss/Taller_2/main/Images/InterfazSpotify2.png)


## ⚙️ Configuración del Algoritmo

##### 🐜 Parámetros de la Colonia

```python

NUM_HORMIGAS = 10       # 10 hormigas por iteración
ITERACIONES = 50        # 50 iteraciones máximas
EVAPORACION = 0.3       # 30% de evaporación de feromonas
ALFA = 1.0              # Influencia de feromonas
BETA = 2.0              # Influencia de heurística
Q = 100                 # Constante de deposición
```


#### 👤 Tipos de Usuario Predefinidos

- Rockero: Prefiere rock (90%), alta energía

- PopLover: Enfocado en pop (90%), alta bailabilidad

- JazzFan: Amante del jazz (90%), energía media

- Energico: Busca alta energía (90%)

- Bailarin: Enfocado en bailabilidad (90%)

## 🧮 Sistema de Evaluación

### 📊 Métricas de Calidad

1. Similitud Musical

```python

def calcular_similitud(self, cancion1, cancion2):
    # Distancia euclidiana entre características
    distancia = 0
    for carac in caracteristicas1:
        distancia += (caracteristicas1[carac] - caracteristicas2[carac]) ** 2
    return 1 / (1 + math.sqrt(distancia))
```

2. Afinidad del Usuario

```python

def calcular_afinidad(self, cancion, preferencias_usuario):
    # Producto punto entre preferencias y características
    afinidad = 0
    for caracteristica, valor_pref in preferencias_usuario.items():
        valor_cancion = caracteristicas_cancion[caracteristica]
        afinidad += valor_pref * valor_cancion
    return afinidad / len(preferencias_usuario)
```

3. Probabilidad de Transición

```python

def evaluar_transicion(self, cancion_actual, siguiente_cancion, preferencias_usuario):
    similitud = self.calcular_similitud(cancion_actual, siguiente_cancion)
    afinidad = self.calcular_afinidad(siguiente_cancion, preferencias_usuario)
    feromona = self.feromonas[cancion_actual][siguiente_cancion]
    
    return (feromona ** ALFA) * ((similitud * afinidad) ** BETA)
```


## 🎪 Componentes de la Interfaz

### 🎛️ Panel de Control

- Tipo de Usuario: Selector de preferencias musicales

- Ejecutar 1 Iteración: Avanza la simulación paso a paso

- Ejecutar 10 Iteraciones: Ejecuta múltiples iteraciones

- Reiniciar: Vuelve al estado inicial

### 📊 Información en Tiempo Real

- Iteración actual: Número de iteración completada

- Mejor Calidad: Puntuación de la mejor playlist encontrada

- Playlist Actual: Secuencia de canciones recomendada

- Mejor Playlist Global: La mejor solución histórica

### 🎵 Tabla de Canciones

1. Muestra las características detalladas de cada canción:

- Rock/Pop/Jazz: Porcentajes de género musical

- Energía: Nivel de intensidad (0.0 - 1.0)

- Bailabilidad: Facilidad para bailar (0.0 - 1.0)

### 📈 Gráfico de Evolución

- Línea azul: Calidad de la mejor playlist por iteración

- Eje X: Número de iteración

- Eje Y: Calidad de recomendación (0.0 - 1.0)

### 🕸️ Grafo de Recomendaciones

- Nodos: Canciones individuales

- Aristas: Conexiones recomendadas entre canciones

- Grosor: Intensidad de las feromonas (preferencia colectiva)

- Flechas: Dirección de la recomendación

## 📊 Ejemplo de Resultados

#### Playlist Generada (Iteración 10)

text

song5 → song2 → song7 → song8 → song10 → song4 → song1 → song9



Calidad: 0.2156

#### Características de la Playlist Óptima

- ✅ Transiciones suaves entre canciones similares

- ✅ Alineación con preferencias del usuario

- ✅ Variedad musical balanceada

- ✅ Secuencia coherente desde el inicio al final

### 🔧 Personalización

#### Modificar Parámetros

```python

# Ajustar para más exploración o explotación
NUM_HORMIGAS = 15      # Más hormigas, más diversidad
EVAPORACION = 0.5      # Más evaporación, menos memoria
ALFA = 0.8             # Menos influencia de feromonas
BETA = 2.5             # Más influencia de heurística
```


#### Añadir Nuevos Usuarios

```python

self.tipos_usuario = {
    'Clasico': {'rock': 0.1, 'pop': 0.1, 'jazz': 0.1, 
               'energia': 0.3, 'bailabilidad': 0.2},
    # ... más tipos
}
```

## 🎯 Aplicaciones Prácticas

#### 🎵 Plataformas de Música

- Recomendación automática de playlists

- Descubrimiento de música personalizado

- Generación de radios temáticas

## 👥 Autores

#### 🧑‍💻 Contribuidores Principales

- *Carlos Andrés Suárez Torres* → [Carlos23Andres](https://github.com/Carlos23Andres)  

- *Saira Sharid Sanabria Muñoz* → [sharito202](https://github.com/sharito202)
