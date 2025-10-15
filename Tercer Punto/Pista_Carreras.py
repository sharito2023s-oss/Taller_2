import random
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import ttk
import math
from enum import Enum

# Configuración de algoritmos
POBLACION_SIZE = 15
GENERACIONES = 50
MUTACION_PROB = 0.1
NUM_PARTICULAS = 20
NUM_HORMIGAS = 10
EVAPORACION = 0.1

class EstadoCarrera(Enum):
    NORMAL = "Normal"
    ADELANTAMIENTO = "Adelantamiento"
    DEFENSA = "Defensa"
    CURVA = "Curva"

class ControladorGenetico:
    def __init__(self, agresividad=None, conservador=None, adelantamiento=None):
        self.agresividad = agresividad if agresividad is not None else random.random()
        self.conservador = conservador if conservador is not None else random.random()
        self.adelantamiento = adelantamiento if adelantamiento is not None else random.random()
        self.fitness = 0
        
        # Normalizar para que sumen 1
        total = self.agresividad + self.conservador + self.adelantamiento
        self.agresividad /= total
        self.conservador /= total
        self.adelantamiento /= total
        
    def decidir_accion(self, estado, distancia_oponente, tipo_curva):
        """Decide la acción basada en los parámetros genéticos"""
        if estado == EstadoCarrera.ADELANTAMIENTO:
            return self.agresividad * 0.7 + self.adelantamiento * 0.3
        elif estado == EstadoCarrera.DEFENSA:
            return self.conservador * 0.8 + self.agresividad * 0.2
        elif estado == EstadoCarrera.CURVA:
            return self.conservador * 0.6 + self.agresividad * 0.4
        else:  # NORMAL
            return self.agresividad * 0.5 + self.conservador * 0.5
            
    def __str__(self):
        return f"Agresividad: {self.agresividad:.2f}, Conservador: {self.conservador:.2f}, Adelantamiento: {self.adelantamiento:.2f}"

class Particula:
    def __init__(self, id_particula):
        self.id = id_particula
        self.posicion = np.array([random.uniform(0, 1), random.uniform(0, 1)])  # [aceleracion, direccion]
        self.velocidad = np.array([random.uniform(-0.1, 0.1), random.uniform(-0.1, 0.1)])
        self.mejor_posicion = self.posicion.copy()
        self.mejor_fitness = float('-inf')
        
    def actualizar_velocidad(self, mejor_global, w=0.7, c1=1.4, c2=1.4):
        """Actualiza la velocidad según PSO"""
        r1, r2 = random.random(), random.random()
        
        inercia = w * self.velocidad
        cognitivo = c1 * r1 * (self.mejor_posicion - self.posicion)
        social = c2 * r2 * (mejor_global - self.posicion)
        
        self.velocidad = inercia + cognitivo + social
        # Limitar velocidad
        self.velocidad = np.clip(self.velocidad, -0.2, 0.2)
        
    def actualizar_posicion(self):
        """Actualiza la posición de la partícula"""
        self.posicion += self.velocidad
        self.posicion = np.clip(self.posicion, 0, 1)

class ControladorPSO:
    def __init__(self):
        self.particulas = [Particula(i) for i in range(NUM_PARTICULAS)]
        self.mejor_global = np.array([0.5, 0.5])
        self.mejor_global_fitness = float('-inf')
        
    def decidir_adelantamiento(self, oponentes, pista, controlador_genetico):
        """Decide el mejor momento para adelantar usando PSO"""
        # Evaluar todas las partículas
        for particula in self.particulas:
            fitness = self.evaluar_adelantamiento(particula.posicion, oponentes, pista, controlador_genetico)
            
            if fitness > particula.mejor_fitness:
                particula.mejor_fitness = fitness
                particula.mejor_posicion = particula.posicion.copy()
                
            if fitness > self.mejor_global_fitness:
                self.mejor_global_fitness = fitness
                self.mejor_global = particula.posicion.copy()
        
        # Actualizar partículas
        for particula in self.particulas:
            particula.actualizar_velocidad(self.mejor_global)
            particula.actualizar_posicion()
            
        return self.mejor_global
    
    def evaluar_adelantamiento(self, decision, oponentes, pista, controlador_genetico):
        """Evalúa la calidad de una decisión de adelantamiento"""
        aceleracion, direccion = decision
        
        # Factores de evaluación
        distancia_segura = min(oponentes) if oponentes else 10
        espacio_suficiente = 1.0 / (1 + math.exp(-distancia_segura + 2))
        
        # Ventana de oportunidad basada en posición de oponentes
        ventana_oportunidad = 1.0 if len([o for o in oponentes if o > 3]) >= 2 else 0.5
        
        # Influencia del controlador genético
        influencia_genetica = controlador_genetico.adelantamiento
        
        fitness = (aceleracion * 0.4 + 
                  espacio_suficiente * 0.3 + 
                  ventana_oportunidad * 0.2 + 
                  influencia_genetica * 0.1)
        
        return fitness

class HormigaRacing:
    def __init__(self, id_hormiga):
        self.id = id_hormiga
        self.trayectoria = []
        self.tiempo_total = 0
        
    def explorar_trayectoria(self, pista, feromonas):
        """Explora una trayectoria en la pista"""
        self.trayectoria = []
        self.tiempo_total = 0
        
        tramos = len(pista)
        tramo_actual = 0
        
        while tramo_actual < tramos:
            # Decidir siguiente movimiento basado en feromonas y heurística
            siguiente_tramo = self.elegir_siguiente_tramo(tramo_actual, pista, feromonas)
            self.trayectoria.append(siguiente_tramo)
            
            # Calcular tiempo en este tramo (inversamente proporcional a feromonas)
            tiempo_tramo = pista[siguiente_tramo]['dificultad'] / (feromonas[siguiente_tramo] + 0.1)
            self.tiempo_total += tiempo_tramo
            
            tramo_actual = siguiente_tramo
            
            # Posibilidad de terminar anticipadamente
            if random.random() < 0.1 and tramo_actual > tramos * 0.7:
                break
                
        return self.trayectoria, self.tiempo_total
    
    def elegir_siguiente_tramo(self, tramo_actual, pista, feromonas):
        """Elige el siguiente tramo basado en probabilidades"""
        tramos_posibles = list(range(tramo_actual + 1, min(tramo_actual + 4, len(pista))))
        
        if not tramos_posibles:
            return tramo_actual
            
        probabilidades = []
        for tramo in tramos_posibles:
            # Combinar feromonas y heurística (dificultad inversa)
            heuristica = 1.0 / pista[tramo]['dificultad']
            prob = feromonas[tramo] * heuristica
            probabilidades.append(prob)
            
        # Normalizar
        total = sum(probabilidades)
        if total == 0:
            return random.choice(tramos_posibles)
            
        probabilidades = [p / total for p in probabilidades]
        return random.choices(tramos_posibles, weights=probabilidades)[0]

class SistemaCarreras:
    def __init__(self):
        # Pista con tramos de diferente dificultad
        self.pista = self.crear_pista()
        self.feromonas = [1.0] * len(self.pista)  # Feromonas iniciales
        
        # Algoritmos
        self.controladores_geneticos = []
        self.mejor_controlador = None
        self.controlador_pso = ControladorPSO()
        self.hormigas = [HormigaRacing(i) for i in range(NUM_HORMIGAS)]
        
        # Historial
        self.historial_fitness = []
        self.mejor_trayectoria = None
        self.mejor_tiempo = float('inf')
        
    def crear_pista(self):
        """Crea una pista con tramos de diferente dificultad"""
        pista = []
        tramos = 20
        
        for i in range(tramos):
            # Dificultad varía sinusoidalmente para simular curvas y rectas
            dificultad = 0.5 + 0.4 * math.sin(i * 0.5)
            tipo = "Recta" if dificultad < 0.6 else "Curva suave" if dificultad < 0.8 else "Curva cerrada"
            
            pista.append({
                'id': i,
                'dificultad': dificultad,
                'tipo': tipo,
                'longitud': random.uniform(0.8, 1.2)
            })
            
        return pista
    
    def inicializar_poblacion_genetica(self):
        """Inicializa la población de controladores genéticos"""
        self.controladores_geneticos = [ControladorGenetico() for _ in range(POBLACION_SIZE)]
        
    def evaluar_controlador(self, controlador):
        """Evalúa un controlador en una simulación de carrera"""
        # Simular diferentes escenarios
        escenarios = [
            (EstadoCarrera.NORMAL, [5, 8], "Recta"),
            (EstadoCarrera.ADELANTAMIENTO, [2, 4], "Recta"),
            (EstadoCarrera.DEFENSA, [1, 3], "Curva"),
            (EstadoCarrera.CURVA, [6, 9], "Curva cerrada")
        ]
        
        puntuacion_total = 0
        
        for estado, oponentes, tipo_pista in escenarios:
            decision = controlador.decidir_accion(estado, min(oponentes), tipo_pista)
            
            # Puntuación basada en la adecuación de la decisión
            if estado == EstadoCarrera.ADELANTAMIENTO:
                puntuacion = decision  # Más agresivo mejor
            elif estado == EstadoCarrera.DEFENSA:
                puntuacion = 1 - decision  # Más conservador mejor
            elif estado == EstadoCarrera.CURVA:
                puntuacion = 0.5 + (0.5 - abs(0.7 - decision))  # Punto óptimo alrededor de 0.7
            else:  # NORMAL
                puntuacion = 0.5 + (0.5 - abs(0.5 - decision))  # Punto óptimo alrededor de 0.5
                
            puntuacion_total += puntuacion
            
        controlador.fitness = puntuacion_total / len(escenarios)
        return controlador.fitness
    
    def ejecutar_generacion_genetica(self):
        """Ejecuta una generación del algoritmo genético"""
        # Evaluar población
        for controlador in self.controladores_geneticos:
            self.evaluar_controlador(controlador)
            
        # Ordenar por fitness
        self.controladores_geneticos.sort(key=lambda x: x.fitness, reverse=True)
        
        # Guardar mejor controlador
        if self.mejor_controlador is None or self.controladores_geneticos[0].fitness > self.mejor_controlador.fitness:
            self.mejor_controlador = ControladorGenetico(
                self.controladores_geneticos[0].agresividad,
                self.controladores_geneticos[0].conservador,
                self.controladores_geneticos[0].adelantamiento
            )
            self.mejor_controlador.fitness = self.controladores_geneticos[0].fitness
            
        # Crear nueva población (elitismo + cruce + mutación)
        nueva_poblacion = self.controladores_geneticos[:2]  # Elitismo
        
        while len(nueva_poblacion) < POBLACION_SIZE:
            padre1 = self.seleccion_ruleta()
            padre2 = self.seleccion_ruleta()
            hijo = self.cruce(padre1, padre2)
            self.mutacion(hijo)
            nueva_poblacion.append(hijo)
            
        self.controladores_geneticos = nueva_poblacion
        self.historial_fitness.append(self.controladores_geneticos[0].fitness)
        
        return self.controladores_geneticos[0].fitness
    
    def seleccion_ruleta(self):
        """Selección por método de ruleta"""
        total_fitness = sum(c.fitness for c in self.controladores_geneticos)
        if total_fitness == 0:
            return random.choice(self.controladores_geneticos)
            
        r = random.uniform(0, total_fitness)
        acumulado = 0
        for controlador in self.controladores_geneticos:
            acumulado += controlador.fitness
            if acumulado >= r:
                return controlador
        return self.controladores_geneticos[-1]
    
    def cruce(self, padre1, padre2):
        """Cruce de dos controladores"""
        return ControladorGenetico(
            (padre1.agresividad + padre2.agresividad) / 2,
            (padre1.conservador + padre2.conservador) / 2,
            (padre1.adelantamiento + padre2.adelantamiento) / 2
        )
    
    def mutacion(self, controlador):
        """Aplica mutación a un controlador"""
        if random.random() < MUTACION_PROB:
            gen = random.randint(1, 3)
            if gen == 1:
                controlador.agresividad = random.random()
            elif gen == 2:
                controlador.conservador = random.random()
            else:
                controlador.adelantamiento = random.random()
            
            # Renormalizar
            total = controlador.agresividad + controlador.conservador + controlador.adelantamiento
            controlador.agresividad /= total
            controlador.conservador /= total
            controlador.adelantamiento /= total
    
    def ejecutar_hormigas(self):
        """Ejecuta una iteración del algoritmo de hormigas"""
        mejor_tiempo_iteracion = float('inf')
        mejor_trayectoria_iteracion = None
        
        for hormiga in self.hormigas:
            trayectoria, tiempo = hormiga.explorar_trayectoria(self.pista, self.feromonas)
            
            if tiempo < mejor_tiempo_iteracion:
                mejor_tiempo_iteracion = tiempo
                mejor_trayectoria_iteracion = trayectoria
                
            if tiempo < self.mejor_tiempo:
                self.mejor_tiempo = tiempo
                self.mejor_trayectoria = trayectoria.copy()
        
        # Actualizar feromonas (evaporación)
        for i in range(len(self.feromonas)):
            self.feromonas[i] *= (1 - EVAPORACION)
            
        # Reforzar mejor trayectoria
        if mejor_trayectoria_iteracion:
            for tramo in mejor_trayectoria_iteracion:
                self.feromonas[tramo] += 1.0 / mejor_tiempo_iteracion
                
        return mejor_tiempo_iteracion, mejor_trayectoria_iteracion

class VisualizadorCarreras:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Sistema de Control para Robot de Carreras - Algoritmos Híbridos")
        self.root.geometry("1400x900")
        
        self.sistema = SistemaCarreras()
        self.sistema.inicializar_poblacion_genetica()
        
        self.generacion_actual = 0
        self.iteracion_hormigas = 0
        
        self.setup_ui()
        self.actualizar_ui()
        
    def setup_ui(self):
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configurar grid
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # Panel de control
        control_frame = ttk.LabelFrame(main_frame, text="Control de Simulación", padding="5")
        control_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Button(control_frame, text="Ejecutar Gen. Genética", 
                  command=self.ejecutar_generacion_genetica).grid(row=0, column=0, padx=5)
        ttk.Button(control_frame, text="Ejecutar Hormigas", 
                  command=self.ejecutar_hormigas).grid(row=0, column=1, padx=5)
        ttk.Button(control_frame, text="Ejecutar PSO", 
                  command=self.ejecutar_pso).grid(row=0, column=2, padx=5)
        ttk.Button(control_frame, text="Ejecutar Todo 10 Iter", 
                  command=self.ejecutar_todo).grid(row=0, column=3, padx=5)
        ttk.Button(control_frame, text="Reiniciar", 
                  command=self.reiniciar).grid(row=0, column=4, padx=5)
        
        # Información del sistema
        info_frame = ttk.LabelFrame(main_frame, text="Estado del Sistema", padding="5")
        info_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        
        self.lbl_generacion = ttk.Label(info_frame, text="Generación Genética: 0")
        self.lbl_generacion.grid(row=0, column=0, sticky=tk.W, pady=2)
        
        self.lbl_iteracion_hormigas = ttk.Label(info_frame, text="Iteración Hormigas: 0")
        self.lbl_iteracion_hormigas.grid(row=1, column=0, sticky=tk.W, pady=2)
        
        self.lbl_mejor_fitness = ttk.Label(info_frame, text="Mejor Fitness: 0.00")
        self.lbl_mejor_fitness.grid(row=2, column=0, sticky=tk.W, pady=2)
        
        self.lbl_mejor_tiempo = ttk.Label(info_frame, text="Mejor Tiempo: ∞")
        self.lbl_mejor_tiempo.grid(row=3, column=0, sticky=tk.W, pady=2)
        
        # Mejor controlador genético
        controlador_frame = ttk.LabelFrame(info_frame, text="Mejor Controlador Genético", padding="5")
        controlador_frame.grid(row=4, column=0, sticky=(tk.W, tk.E), pady=(10, 0))
        
        self.lbl_mejor_controlador = ttk.Label(controlador_frame, text="Agresividad: -, Conservador: -, Adelantamiento: -")
        self.lbl_mejor_controlador.grid(row=0, column=0, sticky=tk.W, pady=2)
        
        # Mejor trayectoria
        trayectoria_frame = ttk.LabelFrame(info_frame, text="Mejor Trayectoria", padding="5")
        trayectoria_frame.grid(row=5, column=0, sticky=(tk.W, tk.E), pady=(10, 0))
        
        self.lbl_mejor_trayectoria = ttk.Label(trayectoria_frame, text="Trayectoria: -", wraplength=300)
        self.lbl_mejor_trayectoria.grid(row=0, column=0, sticky=tk.W, pady=2)
        
        # Pista y feromonas
        pista_frame = ttk.LabelFrame(main_frame, text="Pista y Feromonas", padding="5")
        pista_frame.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10), pady=(10, 0))
        
        self.fig_pista, (self.ax_pista, self.ax_feromonas) = plt.subplots(2, 1, figsize=(8, 6))
        self.canvas_pista = FigureCanvasTkAgg(self.fig_pista, master=pista_frame)
        self.canvas_pista.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Gráficos de evolución
        graficos_frame = ttk.LabelFrame(main_frame, text="Evolución de Algoritmos", padding="5")
        graficos_frame.grid(row=1, column=1, rowspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.fig_evolucion, (self.ax_genetico, self.ax_hormigas) = plt.subplots(2, 1, figsize=(8, 6))
        self.canvas_evolucion = FigureCanvasTkAgg(self.fig_evolucion, master=graficos_frame)
        self.canvas_evolucion.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Configurar pesos de grid
        main_frame.rowconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
    def ejecutar_generacion_genetica(self):
        """Ejecuta una generación del algoritmo genético"""
        fitness = self.sistema.ejecutar_generacion_genetica()
        self.generacion_actual += 1
        self.actualizar_ui()
        
    def ejecutar_hormigas(self):
        """Ejecuta una iteración del algoritmo de hormigas"""
        tiempo, trayectoria = self.sistema.ejecutar_hormigas()
        self.iteracion_hormigas += 1
        self.actualizar_ui()
        
    def ejecutar_pso(self):
        """Ejecuta una iteración de PSO"""
        # Simular escenario de adelantamiento
        oponentes = [random.uniform(1, 10) for _ in range(3)]
        decision = self.sistema.controlador_pso.decidir_adelantamiento(
            oponentes, self.sistema.pista, self.sistema.mejor_controlador
        )
        self.actualizar_ui()
        
    def ejecutar_todo(self):
        """Ejecuta 10 iteraciones de cada algoritmo"""
        for _ in range(10):
            self.ejecutar_generacion_genetica()
            self.ejecutar_hormigas()
            self.ejecutar_pso()
            self.root.update()
            
    def reiniciar(self):
        """Reinicia la simulación"""
        self.sistema = SistemaCarreras()
        self.sistema.inicializar_poblacion_genetica()
        self.generacion_actual = 0
        self.iteracion_hormigas = 0
        self.actualizar_ui()
        
    def actualizar_ui(self):
        """Actualiza toda la interfaz de usuario"""
        # Actualizar labels
        self.lbl_generacion.config(text=f"Generación Genética: {self.generacion_actual}")
        self.lbl_iteracion_hormigas.config(text=f"Iteración Hormigas: {self.iteracion_hormigas}")
        
        if self.sistema.mejor_controlador:
            self.lbl_mejor_fitness.config(text=f"Mejor Fitness: {self.sistema.mejor_controlador.fitness:.4f}")
            self.lbl_mejor_controlador.config(
                text=f"Agresividad: {self.sistema.mejor_controlador.agresividad:.2f}, "
                     f"Conservador: {self.sistema.mejor_controlador.conservador:.2f}, "
                     f"Adelantamiento: {self.sistema.mejor_controlador.adelantamiento:.2f}"
            )
            
        if self.sistema.mejor_trayectoria:
            self.lbl_mejor_tiempo.config(text=f"Mejor Tiempo: {self.sistema.mejor_tiempo:.2f}")
            trayectoria_str = " → ".join(map(str, self.sistema.mejor_trayectoria[:10]))
            if len(self.sistema.mejor_trayectoria) > 10:
                trayectoria_str += " ..."
            self.lbl_mejor_trayectoria.config(text=f"Trayectoria: {trayectoria_str}")
        
        # Actualizar gráficos
        self.actualizar_grafico_pista()
        self.actualizar_grafico_evolucion()
        
    def actualizar_grafico_pista(self):
        """Actualiza el gráfico de la pista y feromonas"""
        self.ax_pista.clear()
        self.ax_feromonas.clear()
        
        # Gráfico de la pista
        tramos = range(len(self.sistema.pista))
        dificultades = [tramo['dificultad'] for tramo in self.sistema.pista]
        
        self.ax_pista.plot(tramos, dificultades, 'b-', linewidth=2, label='Dificultad')
        self.ax_pista.fill_between(tramos, 0, dificultades, alpha=0.3)
        self.ax_pista.set_ylabel('Dificultad')
        self.ax_pista.set_title('Pista de Carrera')
        self.ax_pista.legend()
        self.ax_pista.grid(True, linestyle='--', alpha=0.7)
        
        # Gráfico de feromonas
        self.ax_feromonas.bar(tramos, self.sistema.feromonas, alpha=0.7, color='orange')
        self.ax_feromonas.set_xlabel('Tramo de Pista')
        self.ax_feromonas.set_ylabel('Feromonas')
        self.ax_feromonas.set_title('Feromonas en la Pista')
        self.ax_feromonas.grid(True, linestyle='--', alpha=0.7)
        
        self.fig_pista.tight_layout()
        self.canvas_pista.draw()
        
    def actualizar_grafico_evolucion(self):
        """Actualiza los gráficos de evolución"""
        self.ax_genetico.clear()
        self.ax_hormigas.clear()
        
        # Gráfico de evolución genética
        if self.sistema.historial_fitness:
            generaciones = range(1, len(self.sistema.historial_fitness) + 1)
            self.ax_genetico.plot(generaciones, self.sistema.historial_fitness, 'g-', linewidth=2)
            self.ax_genetico.set_ylabel('Fitness')
            self.ax_genetico.set_title('Evolución del Algoritmo Genético')
            self.ax_genetico.grid(True, linestyle='--', alpha=0.7)
            
        # Gráfico de PSO (simulado)
        if self.sistema.controlador_pso.mejor_global_fitness > float('-inf'):
            self.ax_hormigas.scatter([0.5], [0.5], c='red', s=100, alpha=0.7)
            self.ax_hormigas.set_xlim(0, 1)
            self.ax_hormigas.set_ylim(0, 1)
            self.ax_hormigas.set_xlabel('Aceleración')
            self.ax_hormigas.set_ylabel('Dirección')
            self.ax_hormigas.set_title('Espacio de Búsqueda PSO')
            self.ax_hormigas.grid(True, linestyle='--', alpha=0.7)
            
        self.fig_evolucion.tight_layout()
        self.canvas_evolucion.draw()
        
    def run(self):
        self.root.mainloop()

# Ejecutar la aplicación
if __name__ == "__main__":
    app = VisualizadorCarreras()
    app.run()