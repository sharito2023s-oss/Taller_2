# 🏎️ Sistema de Control para Robot de Carreras - Algoritmos Híbridos

## 📋 Descripción General

Este proyecto implementa un sistema de control inteligente para un robot de carreras que combina tres algoritmos de inteligencia artificial:

- Algoritmo Genético - Evoluciona los parámetros del controlador

- Optimización por Enjambre de Partículas (PSO) - Optimiza decisiones de adelantamiento en tiempo real

- Algoritmo de Colonias de Hormigas - Aprende la mejor línea de carrera
## 🏎️ Componentes del Sistema

1. Controlador Genético (ControladorGenetico)

Parámetros evolucionados:

- agresividad (0-1): Tendencia a tomar riesgos

- conservador (0-1): Tendencia a mantener posiciones seguras

- adelantamiento (0-1): Habilidad para ejecutar adelantamientos

Funcionalidad:

- Decide acciones basadas en el estado de la carrera

- Se evalúa en múltiples escenarios (normal, adelantamiento, defensa, curvas)

-Evoluciona mediante selección, cruce y mutación

2. Controlador PSO (ControladorPSO)

Optimización en tiempo real:

- Espacio de búsqueda: [aceleración, dirección]

- Evalúa oportunidades de adelantamiento considerando:

    - Distancia a oponentes

    - Espacio disponible

    - Ventana de oportunidad

    - Influencia del controlador genético

3. Sistema de Hormigas (HormigaRacing)

Aprendizaje de trayectorias:

- Explora diferentes líneas en la pista

- Refuerza tramos con feromonas basadas en el tiempo

-Las feromonas guían a hormigas futuras hacia mejores trayectorias

## 🎯 Estados de Carrera

El sistema maneja cuatro estados principales:

- NORMAL: Conducción en rectas sin presión

- ADELANTAMIENTO: Oportunidad para pasar oponentes

- DEFENSA: Mantener posición bajo ataque

- CURVA: Navegación por secciones curvas

## 📊 Métricas de Evaluación
Controlador Genético:

- Fitness: Adecuación de decisiones en diferentes escenarios

- Estabilidad: Consistencia en el rendimiento

Algoritmo de Hormigas:

- Tiempo de vuelta: Tiempo total para completar la trayectoria

- Calidad de trayectoria: Eficiencia en el uso de la pista

PSO:

- Calidad de decisión: Efectividad en oportunidades de adelantamiento

## 🎮 Controles de la Interfaz
Estado Inicial de la Interfaz

La interfaz inicial muestra:

- Panel de Control: Botones para ejecutar los algoritmos individualmente o en conjunto

- Estado del Sistema: Métricas en cero esperando la primera ejecución

- Pista y Feromonas: Visualización inicial de la pista con dificultades uniformes

- Gráficos de Evolución: Áreas vacías listas para mostrar el progreso

Controles Disponibles:

- Ejecutar Gen. Genética: Una generación del algoritmo genético

- Ejecutar Hormigas: Una iteración del algoritmo de hormigas

- Ejecutar PSO: Una iteración de optimización PSO

- Ejecutar Todo 10 Iter: 10 iteraciones de cada algoritmo

- Reiniciar: Reinicia toda la simulación

Interfaz después de 10 Iteraciones

Después de ejecutar "Ejecutar Todo 10 Iter", la interfaz muestra:

Estado del Sistema Actualizado:

- Generación Genética: 10

- Iteración Hormigas: 10

- Mejor Fitness: 0.6821 (ejemplo)

- Mejor Tiempo: 3.14 (ejemplo)

- Parámetros del mejor controlador genético

Visualizaciones Evolucionadas:

- Pista y Feromonas: Distribución de feromonas que muestra las trayectorias preferidas

- Evolución del Algoritmo Genético: Gráfico que muestra la mejora del fitness a través de las generaciones

- Espacio de Búsqueda PSO: Partículas convergiendo hacia soluciones óptimas

## 📈 Visualización

La interfaz muestra en tiempo real:

- Estado del Sistema: Métricas actuales de rendimiento

- Pista y Feromonas: Dificultad de la pista y distribución de feromonas aprendida

- Evolución de Algoritmos: Progreso del aprendizaje de cada algoritmo

![Interfaz Inicial](https://raw.githubusercontent.com/sharito2023s-oss/Taller_2/main/Images/InterfazPista.png)


![Interfaz Inicial](https://raw.githubusercontent.com/sharito2023s-oss/Taller_2/main/Images/InterfazPista2.png)


## 🔧 Personalización

Parámetros Ajustables:

python

# Configuración de algoritmos
POBLACION_SIZE = 15
GENERACIONES = 50
MUTACION_PROB = 0.1
NUM_PARTICULAS = 20
NUM_HORMIGAS = 10
EVAPORACION = 0.1

Modificación de la Pista:

Editar el método crear_pista() en SistemaCarreras para cambiar:

- Número de tramos

- Dificultad de cada sección

- Tipos de curva

## 👥 Autores

#### 🧑‍💻 Contribuidores Principales

- **Carlos Andrés Suárez Torres** → [Carlos23Andres](https://github.com/Carlos23Andres)  

- **Saira Sharid Sanabria Muñoz** → [sharito202](https://github.com/sharito202)
