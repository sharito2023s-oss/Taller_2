import random
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import ttk
import time

# Configuración inicial
TIPOS = ['fuego', 'agua', 'planta', 'electrico', 'tierra']
POBLACION_SIZE = 20
GENERACIONES = 50
MUTACION_PROB = 0.1
ELITISMO = 2  # Número de mejores individuos que pasan directamente a la siguiente generación

class Pokemon:
    def __init__(self, ataque=None, defensa=None, velocidad=None, vida=None, tipo=None):
        self.ataque = ataque if ataque is not None else random.random()
        self.defensa = defensa if defensa is not None else random.random()
        self.velocidad = velocidad if velocidad is not None else random.random()
        self.vida = vida if vida is not None else random.random()
        self.tipo = tipo if tipo is not None else random.choice(TIPOS)
        self.fitness = 0
        
    def calcular_fitness(self):
        poder = (self.ataque * 0.3 +
                self.defensa * 0.2 +
                self.velocidad * 0.25 +
                self.vida * 0.25)
        
        # Bonus por tipo
        if self.tipo == 'fuego': 
            poder *= 1.1
        elif self.tipo == 'agua': 
            poder *= 1.05
        elif self.tipo == 'electrico':
            poder *= 1.03
            
        self.fitness = poder
        return poder
    
    def __str__(self):
        return f"Tipo: {self.tipo}, Ataque: {self.ataque:.2f}, Defensa: {self.defensa:.2f}, " \
               f"Velocidad: {self.velocidad:.2f}, Vida: {self.vida:.2f}, Fitness: {self.fitness:.2f}"

class AlgoritmoGenetico:
    def __init__(self, poblacion_size, generaciones, mutacion_prob, elitismo):
        self.poblacion_size = poblacion_size
        self.generaciones = generaciones
        self.mutacion_prob = mutacion_prob
        self.elitismo = elitismo
        self.poblacion = []
        self.historial_fitness = []
        self.mejor_historico = None
        
    def inicializar_poblacion(self):
        self.poblacion = [Pokemon() for _ in range(self.poblacion_size)]
        
    def evaluar_poblacion(self):
        for pokemon in self.poblacion:
            pokemon.calcular_fitness()
        self.poblacion.sort(key=lambda x: x.fitness, reverse=True)
        
        # Actualizar el mejor histórico
        if self.mejor_historico is None or self.poblacion[0].fitness > self.mejor_historico.fitness:
            self.mejor_historico = Pokemon(
                self.poblacion[0].ataque,
                self.poblacion[0].defensa,
                self.poblacion[0].velocidad,
                self.poblacion[0].vida,
                self.poblacion[0].tipo
            )
            self.mejor_historico.fitness = self.poblacion[0].fitness
            
    def seleccion(self):
        # Método de ruleta
        total_fitness = sum(pokemon.fitness for pokemon in self.poblacion)
        if total_fitness == 0:
            return random.choice(self.poblacion)
        
        r = random.uniform(0, total_fitness)
        acumulado = 0
        for pokemon in self.poblacion:
            acumulado += pokemon.fitness
            if acumulado >= r:
                return pokemon
        return self.poblacion[-1]
    
    def cruce(self, padre1, padre2):
        # Cruce de un punto
        punto_cruce = random.randint(1, 4)
        
        if punto_cruce == 1:
            hijo = Pokemon(padre1.ataque, padre2.defensa, padre2.velocidad, padre2.vida, padre2.tipo)
        elif punto_cruce == 2:
            hijo = Pokemon(padre1.ataque, padre1.defensa, padre2.velocidad, padre2.vida, padre2.tipo)
        elif punto_cruce == 3:
            hijo = Pokemon(padre1.ataque, padre1.defensa, padre1.velocidad, padre2.vida, padre2.tipo)
        else:
            hijo = Pokemon(padre1.ataque, padre1.defensa, padre1.velocidad, padre1.vida, padre2.tipo)
            
        return hijo
    
    def mutacion(self, pokemon):
        if random.random() < self.mutacion_prob:
            gen = random.randint(1, 5)
            if gen == 1:
                pokemon.ataque = random.random()
            elif gen == 2:
                pokemon.defensa = random.random()
            elif gen == 3:
                pokemon.velocidad = random.random()
            elif gen == 4:
                pokemon.vida = random.random()
            else:
                pokemon.tipo = random.choice(TIPOS)
                
    def ejecutar_generacion(self):
        # Evaluar la población actual
        self.evaluar_poblacion()
        
        # Guardar estadísticas
        mejor_fitness = self.poblacion[0].fitness
        peor_fitness = self.poblacion[-1].fitness
        promedio_fitness = sum(p.fitness for p in self.poblacion) / len(self.poblacion)
        self.historial_fitness.append((mejor_fitness, promedio_fitness, peor_fitness))
        
        # Crear nueva población (elitismo)
        nueva_poblacion = self.poblacion[:self.elitismo]
        
        # Completar la nueva población
        while len(nueva_poblacion) < self.poblacion_size:
            padre1 = self.seleccion()
            padre2 = self.seleccion()
            hijo = self.cruce(padre1, padre2)
            self.mutacion(hijo)
            nueva_poblacion.append(hijo)
            
        self.poblacion = nueva_poblacion
        
        return mejor_fitness, promedio_fitness, peor_fitness

class SimuladorEvolucion:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Simulador de Evolución de Pokémon")
        self.root.geometry("1000x700")
        
        self.ag = AlgoritmoGenetico(POBLACION_SIZE, GENERACIONES, MUTACION_PROB, ELITISMO)
        self.generacion_actual = 0
        
        self.setup_ui()
        self.ag.inicializar_poblacion()
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
        control_frame = ttk.LabelFrame(main_frame, text="Control", padding="5")
        control_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Button(control_frame, text="Ejecutar Una Generación", command=self.ejecutar_generacion).grid(row=0, column=0, padx=5)
        ttk.Button(control_frame, text="Ejecutar 10 Generaciones", command=self.ejecutar_10_generaciones).grid(row=0, column=1, padx=5)
        ttk.Button(control_frame, text="Reiniciar Simulación", command=self.reiniciar).grid(row=0, column=2, padx=5)
        
        # Información de la generación actual
        info_frame = ttk.LabelFrame(main_frame, text="Información de la Generación", padding="5")
        info_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        
        self.lbl_generacion = ttk.Label(info_frame, text="Generación: 0")
        self.lbl_generacion.grid(row=0, column=0, sticky=tk.W, pady=2)
        
        self.lbl_mejor_fitness = ttk.Label(info_frame, text="Mejor Fitness: 0.00")
        self.lbl_mejor_fitness.grid(row=1, column=0, sticky=tk.W, pady=2)
        
        self.lbl_promedio_fitness = ttk.Label(info_frame, text="Promedio Fitness: 0.00")
        self.lbl_promedio_fitness.grid(row=2, column=0, sticky=tk.W, pady=2)
        
        self.lbl_peor_fitness = ttk.Label(info_frame, text="Peor Fitness: 0.00")
        self.lbl_peor_fitness.grid(row=3, column=0, sticky=tk.W, pady=2)
        
        # Mejor Pokémon histórico
        mejor_frame = ttk.LabelFrame(info_frame, text="Mejor Pokémon Histórico", padding="5")
        mejor_frame.grid(row=4, column=0, sticky=(tk.W, tk.E), pady=(10, 0))
        
        self.lbl_mejor_pokemon = ttk.Label(mejor_frame, text="Tipo: -")
        self.lbl_mejor_pokemon.grid(row=0, column=0, sticky=tk.W, pady=2)
        
        # Lista de Pokémon actual
        lista_frame = ttk.LabelFrame(main_frame, text="Población Actual (Top 10)", padding="5")
        lista_frame.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10), pady=(10, 0))
        
        # Crear Treeview para mostrar los Pokémon
        columns = ('Tipo', 'Ataque', 'Defensa', 'Velocidad', 'Vida', 'Fitness')
        self.tree = ttk.Treeview(lista_frame, columns=columns, show='headings', height=10)
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=80)
        
        self.tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Scrollbar para el Treeview
        scrollbar = ttk.Scrollbar(lista_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Gráfico de evolución
        grafico_frame = ttk.LabelFrame(main_frame, text="Evolución del Fitness", padding="5")
        grafico_frame.grid(row=1, column=1, rowspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.fig, self.ax = plt.subplots(figsize=(6, 5))
        self.canvas = FigureCanvasTkAgg(self.fig, master=grafico_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Configurar pesos de grid
        main_frame.rowconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)
        main_frame.columnconfigure(1, weight=1)
        lista_frame.rowconfigure(0, weight=1)
        lista_frame.columnconfigure(0, weight=1)
        
    def actualizar_ui(self):
        # Actualizar información de la generación
        self.lbl_generacion.config(text=f"Generación: {self.generacion_actual}")
        
        if self.generacion_actual > 0:
            mejor, promedio, peor = self.ag.historial_fitness[-1]
            self.lbl_mejor_fitness.config(text=f"Mejor Fitness: {mejor:.2f}")
            self.lbl_promedio_fitness.config(text=f"Promedio Fitness: {promedio:.2f}")
            self.lbl_peor_fitness.config(text=f"Peor Fitness: {peor:.2f}")
            
            # Actualizar mejor Pokémon histórico
            if self.ag.mejor_historico:
                self.lbl_mejor_pokemon.config(
                    text=f"Tipo: {self.ag.mejor_historico.tipo}\n"
                         f"Ataque: {self.ag.mejor_historico.ataque:.2f}\n"
                         f"Defensa: {self.ag.mejor_historico.defensa:.2f}\n"
                         f"Velocidad: {self.ag.mejor_historico.velocidad:.2f}\n"
                         f"Vida: {self.ag.mejor_historico.vida:.2f}\n"
                         f"Fitness: {self.ag.mejor_historico.fitness:.2f}"
                )
        
        # Actualizar lista de Pokémon
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        self.ag.evaluar_poblacion()
        for i, pokemon in enumerate(self.ag.poblacion[:10]):
            self.tree.insert('', tk.END, values=(
                pokemon.tipo,
                f"{pokemon.ataque:.2f}",
                f"{pokemon.defensa:.2f}",
                f"{pokemon.velocidad:.2f}",
                f"{pokemon.vida:.2f}",
                f"{pokemon.fitness:.2f}"
            ))
            
        # Actualizar gráfico
        self.actualizar_grafico()
        
    def actualizar_grafico(self):
        self.ax.clear()
        
        if len(self.ag.historial_fitness) > 0:
            generaciones = list(range(1, len(self.ag.historial_fitness) + 1))
            mejores = [h[0] for h in self.ag.historial_fitness]
            promedios = [h[1] for h in self.ag.historial_fitness]
            peores = [h[2] for h in self.ag.historial_fitness]
            
            self.ax.plot(generaciones, mejores, 'g-', label='Mejor')
            self.ax.plot(generaciones, promedios, 'b-', label='Promedio')
            self.ax.plot(generaciones, peores, 'r-', label='Peor')
            
            self.ax.set_xlabel('Generación')
            self.ax.set_ylabel('Fitness')
            self.ax.set_title('Evolución del Fitness')
            self.ax.legend()
            self.ax.grid(True, linestyle='--', alpha=0.7)
            
        self.canvas.draw()
        
    def ejecutar_generacion(self):
        if self.generacion_actual < self.ag.generaciones:
            self.ag.ejecutar_generacion()
            self.generacion_actual += 1
            self.actualizar_ui()
            
    def ejecutar_10_generaciones(self):
        for _ in range(10):
            if self.generacion_actual < self.ag.generaciones:
                self.ag.ejecutar_generacion()
                self.generacion_actual += 1
                self.actualizar_ui()
                self.root.update()
                time.sleep(0.1)  # Pequeña pausa para visualización
                
    def reiniciar(self):
        self.ag = AlgoritmoGenetico(POBLACION_SIZE, GENERACIONES, MUTACION_PROB, ELITISMO)
        self.generacion_actual = 0
        self.ag.inicializar_poblacion()
        self.actualizar_ui()
        
    def run(self):
        self.root.mainloop()

# Ejecutar la aplicación
if __name__ == "__main__":
    app = SimuladorEvolucion()
    app.run()