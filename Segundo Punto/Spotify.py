import random
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import ttk
import math

# Configuración del algoritmo
NUM_HORMIGAS = 10
ITERACIONES = 50
EVAPORACION = 0.3
ALFA = 1.0  # Influencia de feromonas
BETA = 2.0  # Influencia de heurística
Q = 100  # Constante de deposición de feromonas

class SistemaRecomendacion:
    def __init__(self):
        # Base de datos de canciones con características musicales
        self.canciones = {
            'song1': {'rock': 0.8, 'pop': 0.2, 'jazz': 0.1, 'energia': 0.9, 'bailabilidad': 0.7},
            'song2': {'rock': 0.3, 'pop': 0.9, 'jazz': 0.4, 'energia': 0.6, 'bailabilidad': 0.9},
            'song3': {'rock': 0.1, 'pop': 0.4, 'jazz': 0.7, 'energia': 0.4, 'bailabilidad': 0.5},
            'song4': {'rock': 0.9, 'pop': 0.1, 'jazz': 0.2, 'energia': 0.8, 'bailabilidad': 0.6},
            'song5': {'rock': 0.2, 'pop': 0.8, 'jazz': 0.3, 'energia': 0.7, 'bailabilidad': 0.8},
            'song6': {'rock': 0.4, 'pop': 0.3, 'jazz': 0.9, 'energia': 0.5, 'bailabilidad': 0.4},
            'song7': {'rock': 0.7, 'pop': 0.5, 'jazz': 0.6, 'energia': 0.8, 'bailabilidad': 0.7},
            'song8': {'rock': 0.5, 'pop': 0.7, 'jazz': 0.5, 'energia': 0.6, 'bailabilidad': 0.8},
            'song9': {'rock': 0.3, 'pop': 0.6, 'jazz': 0.8, 'energia': 0.4, 'bailabilidad': 0.6},
            'song10': {'rock': 0.8, 'pop': 0.4, 'jazz': 0.3, 'energia': 0.9, 'bailabilidad': 0.7}
        }
        
        # Matriz de feromonas inicial
        self.feromonas = self.inicializar_feromonas()
        
        # Tipos de usuario predefinidos
        self.tipos_usuario = {
            'Rockero': {'rock': 0.9, 'pop': 0.2, 'jazz': 0.1, 'energia': 0.8, 'bailabilidad': 0.4},
            'PopLover': {'rock': 0.2, 'pop': 0.9, 'jazz': 0.3, 'energia': 0.7, 'bailabilidad': 0.9},
            'JazzFan': {'rock': 0.1, 'pop': 0.3, 'jazz': 0.9, 'energia': 0.5, 'bailabilidad': 0.6},
            'Energico': {'rock': 0.6, 'pop': 0.5, 'jazz': 0.4, 'energia': 0.9, 'bailabilidad': 0.7},
            'Bailarin': {'rock': 0.4, 'pop': 0.7, 'jazz': 0.5, 'energia': 0.6, 'bailabilidad': 0.9}
        }
        
    def inicializar_feromonas(self):
        """Inicializa la matriz de feromonas con valores pequeños"""
        canciones_list = list(self.canciones.keys())
        n = len(canciones_list)
        feromonas = {}
        
        for i, cancion_i in enumerate(canciones_list):
            feromonas[cancion_i] = {}
            for j, cancion_j in enumerate(canciones_list):
                if i != j:
                    feromonas[cancion_i][cancion_j] = 0.1  # Valor inicial pequeño
                else:
                    feromonas[cancion_i][cancion_j] = 0  # No hay transición a sí misma
                    
        return feromonas
    
    def calcular_similitud(self, cancion1, cancion2):
        """Calcula la similitud musical entre dos canciones"""
        caracteristicas1 = self.canciones[cancion1]
        caracteristicas2 = self.canciones[cancion2]
        
        # Calcular distancia euclidiana y convertir a similitud
        distancia = 0
        for caracteristica in caracteristicas1:
            distancia += (caracteristicas1[caracteristica] - caracteristicas2[caracteristica]) ** 2
        
        similitud = 1 / (1 + math.sqrt(distancia))
        return similitud
    
    def calcular_afinidad(self, cancion, preferencias_usuario):
        """Calcula qué tan bien se adapta una canción a las preferencias del usuario"""
        afinidad = 0
        caracteristicas_cancion = self.canciones[cancion]
        
        for caracteristica, valor_pref in preferencias_usuario.items():
            if caracteristica in caracteristicas_cancion:
                valor_cancion = caracteristicas_cancion[caracteristica]
                afinidad += valor_pref * valor_cancion
        
        return afinidad / len(preferencias_usuario)  # Normalizar
    
    def evaluar_transicion(self, cancion_actual, siguiente_cancion, preferencias_usuario):
        """Evalúa la probabilidad de transición entre dos canciones"""
        if cancion_actual == siguiente_cancion:
            return 0
        
        similitud = self.calcular_similitud(cancion_actual, siguiente_cancion)
        afinidad_usuario = self.calcular_afinidad(siguiente_cancion, preferencias_usuario)
        feromona = self.feromonas[cancion_actual][siguiente_cancion]
        
        # Fórmula de probabilidad: (feromona^alfa) * (heurística^beta)
        heuristica = similitud * afinidad_usuario
        probabilidad = (feromona ** ALFA) * (heuristica ** BETA)
        
        return probabilidad

class UsuarioHormiga:
    def __init__(self, id_hormiga, preferencias):
        self.id = id_hormiga
        self.playlist = []
        self.preferencias = preferencias
        self.canciones_visitadas = set()
        
    def construir_playlist(self, sistema, longitud_playlist=8):
        """Construye una playlist para la hormiga"""
        self.playlist = []
        self.canciones_visitadas = set()
        
        # Elegir canción inicial aleatoria
        canciones_disponibles = list(sistema.canciones.keys())
        cancion_actual = random.choice(canciones_disponibles)
        self.playlist.append(cancion_actual)
        self.canciones_visitadas.add(cancion_actual)
        
        # Construir el resto de la playlist
        while len(self.playlist) < longitud_playlist:
            siguiente_cancion = self.elegir_siguiente_cancion(sistema, cancion_actual)
            if siguiente_cancion is None:
                break
                
            self.playlist.append(siguiente_cancion)
            self.canciones_visitadas.add(siguiente_cancion)
            cancion_actual = siguiente_cancion
            
        return self.playlist
    
    def elegir_siguiente_cancion(self, sistema, cancion_actual):
        """Elige la siguiente canción basándose en probabilidades"""
        canciones_disponibles = [c for c in sistema.canciones.keys() 
                               if c not in self.canciones_visitadas]
        
        if not canciones_disponibles:
            return None
            
        # Calcular probabilidades para cada canción disponible
        probabilidades = []
        for cancion in canciones_disponibles:
            prob = sistema.evaluar_transicion(cancion_actual, cancion, self.preferencias)
            probabilidades.append(prob)
        
        # Normalizar probabilidades
        total = sum(probabilidades)
        if total == 0:
            # Si todas las probabilidades son 0, elegir aleatoriamente
            return random.choice(canciones_disponibles)
            
        probabilidades = [p / total for p in probabilidades]
        
        # Elegir basándose en las probabilidades
        return random.choices(canciones_disponibles, weights=probabilidades)[0]
    
    def evaluar_playlist(self, sistema):
        """Evalúa la calidad de la playlist construida"""
        if len(self.playlist) < 2:
            return 0
            
        calidad_total = 0
        pares_evaluados = 0
        
        # Evaluar transiciones entre canciones consecutivas
        for i in range(len(self.playlist) - 1):
            cancion_actual = self.playlist[i]
            siguiente_cancion = self.playlist[i + 1]
            
            similitud = sistema.calcular_similitud(cancion_actual, siguiente_cancion)
            afinidad = sistema.calcular_afinidad(siguiente_cancion, self.preferencias)
            
            calidad_total += similitud * afinidad
            pares_evaluados += 1
        
        return calidad_total / pares_evaluados if pares_evaluados > 0 else 0

class VisualizadorSpotify:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Sistema de Recomendación Spotify - Algoritmo de Hormigas")
        self.root.geometry("1200x800")
        
        self.sistema = SistemaRecomendacion()
        self.iteracion_actual = 0
        self.mejor_playlist_global = None
        self.mejor_calidad_global = 0
        self.historial_calidad = []
        
        self.setup_ui()
        
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
        control_frame = ttk.LabelFrame(main_frame, text="Configuración", padding="5")
        control_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Selección de tipo de usuario
        ttk.Label(control_frame, text="Tipo de Usuario:").grid(row=0, column=0, padx=5)
        self.tipo_usuario_var = tk.StringVar(value='Rockero')
        tipo_combo = ttk.Combobox(control_frame, textvariable=self.tipo_usuario_var, 
                                 values=list(self.sistema.tipos_usuario.keys()))
        tipo_combo.grid(row=0, column=1, padx=5)
        
        ttk.Button(control_frame, text="Ejecutar 1 Iteración", 
                  command=self.ejecutar_iteracion).grid(row=0, column=2, padx=5)
        ttk.Button(control_frame, text="Ejecutar 10 Iteraciones", 
                  command=self.ejecutar_10_iteraciones).grid(row=0, column=3, padx=5)
        ttk.Button(control_frame, text="Reiniciar", 
                  command=self.reiniciar).grid(row=0, column=4, padx=5)
        
        # Información de la iteración
        info_frame = ttk.LabelFrame(main_frame, text="Información", padding="5")
        info_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        
        self.lbl_iteracion = ttk.Label(info_frame, text="Iteración: 0")
        self.lbl_iteracion.grid(row=0, column=0, sticky=tk.W, pady=2)
        
        self.lbl_mejor_calidad = ttk.Label(info_frame, text="Mejor Calidad: 0.00")
        self.lbl_mejor_calidad.grid(row=1, column=0, sticky=tk.W, pady=2)
        
        self.lbl_playlist_actual = ttk.Label(info_frame, text="Playlist Actual: -")
        self.lbl_playlist_actual.grid(row=2, column=0, sticky=tk.W, pady=2)
        
        # Mejor playlist global
        mejor_frame = ttk.LabelFrame(info_frame, text="Mejor Playlist Global", padding="5")
        mejor_frame.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=(10, 0))
        
        self.lbl_mejor_playlist = ttk.Label(mejor_frame, text="Playlist: -", wraplength=300, justify=tk.LEFT)
        self.lbl_mejor_playlist.grid(row=0, column=0, sticky=tk.W, pady=2)
        
        # Lista de canciones disponibles
        canciones_frame = ttk.LabelFrame(main_frame, text="Canciones Disponibles", padding="5")
        canciones_frame.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10), pady=(10, 0))
        
        # Treeview para canciones
        columns = ('Canción', 'Rock', 'Pop', 'Jazz', 'Energía', 'Bailabilidad')
        self.tree_canciones = ttk.Treeview(canciones_frame, columns=columns, show='headings', height=8)
        
        for col in columns:
            self.tree_canciones.heading(col, text=col)
            self.tree_canciones.column(col, width=80)
        
        self.tree_canciones.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(canciones_frame, orient=tk.VERTICAL, command=self.tree_canciones.yview)
        self.tree_canciones.configure(yscrollcommand=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Gráfico de evolución
        grafico_frame = ttk.LabelFrame(main_frame, text="Evolución de la Calidad", padding="5")
        grafico_frame.grid(row=1, column=1, rowspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.fig, self.ax = plt.subplots(figsize=(8, 6))
        self.canvas = FigureCanvasTkAgg(self.fig, master=grafico_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Grafo de recomendaciones
        grafo_frame = ttk.LabelFrame(main_frame, text="Grafo de Recomendaciones", padding="5")
        grafo_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(10, 0))
        
        self.fig_grafo, self.ax_grafo = plt.subplots(figsize=(10, 4))
        self.canvas_grafo = FigureCanvasTkAgg(self.fig_grafo, master=grafo_frame)
        self.canvas_grafo.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Configurar pesos de grid
        main_frame.rowconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)
        main_frame.rowconfigure(3, weight=1)
        main_frame.columnconfigure(1, weight=1)
        canciones_frame.rowconfigure(0, weight=1)
        canciones_frame.columnconfigure(0, weight=1)
        
        self.actualizar_ui_inicial()
        
    def actualizar_ui_inicial(self):
        """Actualiza la UI con los datos iniciales"""
        # Actualizar lista de canciones
        for item in self.tree_canciones.get_children():
            self.tree_canciones.delete(item)
            
        for cancion, caracteristicas in self.sistema.canciones.items():
            self.tree_canciones.insert('', tk.END, values=(
                cancion,
                f"{caracteristicas['rock']:.2f}",
                f"{caracteristicas['pop']:.2f}",
                f"{caracteristicas['jazz']:.2f}",
                f"{caracteristicas['energia']:.2f}",
                f"{caracteristicas['bailabilidad']:.2f}"
            ))
        
        self.actualizar_grafo()
        
    def ejecutar_iteracion(self):
        """Ejecuta una iteración del algoritmo de colonia de hormigas"""
        preferencias = self.sistema.tipos_usuario[self.tipo_usuario_var.get()]
        hormigas = [UsuarioHormiga(i, preferencias) for i in range(NUM_HORMIGAS)]
        
        # Construir playlists
        for hormiga in hormigas:
            hormiga.construir_playlist(self.sistema)
        
        # Evaluar playlists y encontrar la mejor
        mejor_calidad = 0
        mejor_playlist = None
        mejor_hormiga = None
        
        for hormiga in hormigas:
            calidad = hormiga.evaluar_playlist(self.sistema)
            if calidad > mejor_calidad:
                mejor_calidad = calidad
                mejor_playlist = hormiga.playlist
                mejor_hormiga = hormiga
        
        # Actualizar feromonas (evaporación)
        for cancion_i in self.sistema.feromonas:
            for cancion_j in self.sistema.feromonas[cancion_i]:
                self.sistema.feromonas[cancion_i][cancion_j] *= (1 - EVAPORACION)
        
        # Depositar feromonas de la mejor hormiga
        if mejor_hormiga:
            delta_feromona = Q * mejor_calidad
            for i in range(len(mejor_playlist) - 1):
                cancion_actual = mejor_playlist[i]
                siguiente_cancion = mejor_playlist[i + 1]
                self.sistema.feromonas[cancion_actual][siguiente_cancion] += delta_feromona
        
        # Actualizar estadísticas globales
        self.iteracion_actual += 1
        self.historial_calidad.append(mejor_calidad)
        
        if mejor_calidad > self.mejor_calidad_global:
            self.mejor_calidad_global = mejor_calidad
            self.mejor_playlist_global = mejor_playlist.copy()
        
        self.actualizar_ui(mejor_playlist, mejor_calidad)
        
    def ejecutar_10_iteraciones(self):
        """Ejecuta 10 iteraciones del algoritmo"""
        for _ in range(10):
            self.ejecutar_iteracion()
            
    def reiniciar(self):
        """Reinicia la simulación"""
        self.sistema = SistemaRecomendacion()
        self.iteracion_actual = 0
        self.mejor_playlist_global = None
        self.mejor_calidad_global = 0
        self.historial_calidad = []
        self.actualizar_ui_inicial()
        
    def actualizar_ui(self, playlist_actual, calidad_actual):
        """Actualiza la interfaz de usuario"""
        self.lbl_iteracion.config(text=f"Iteración: {self.iteracion_actual}")
        self.lbl_mejor_calidad.config(text=f"Mejor Calidad: {self.mejor_calidad_global:.4f}")
        
        # Mostrar playlist actual
        if playlist_actual:
            playlist_str = " → ".join(playlist_actual)
            self.lbl_playlist_actual.config(text=f"Playlist Actual: {playlist_str}")
        
        # Mostrar mejor playlist global
        if self.mejor_playlist_global:
            mejor_playlist_str = " → ".join(self.mejor_playlist_global)
            self.lbl_mejor_playlist.config(text=f"Playlist: {mejor_playlist_str}\nCalidad: {self.mejor_calidad_global:.4f}")
        
        # Actualizar gráficos
        self.actualizar_grafico_evolucion()
        self.actualizar_grafo()
        
    def actualizar_grafico_evolucion(self):
        """Actualiza el gráfico de evolución de la calidad"""
        self.ax.clear()
        
        if self.historial_calidad:
            iteraciones = list(range(1, len(self.historial_calidad) + 1))
            self.ax.plot(iteraciones, self.historial_calidad, 'b-', linewidth=2)
            self.ax.set_xlabel('Iteración')
            self.ax.set_ylabel('Calidad de Playlist')
            self.ax.set_title('Evolución de la Calidad de Recomendación')
            self.ax.grid(True, linestyle='--', alpha=0.7)
            
        self.canvas.draw()
        
    def actualizar_grafo(self):
        """Actualiza el grafo de recomendaciones"""
        self.ax_grafo.clear()
        
        # Crear grafo
        G = nx.DiGraph()
        
        # Añadir nodos (canciones)
        for cancion in self.sistema.canciones:
            G.add_node(cancion)
        
        # Añadir aristas con pesos basados en feromonas
        edge_weights = []
        for cancion_i in self.sistema.feromonas:
            for cancion_j in self.sistema.feromonas[cancion_i]:
                if self.sistema.feromonas[cancion_i][cancion_j] > 0.1:  # Solo mostrar conexiones significativas
                    G.add_edge(cancion_i, cancion_j, weight=self.sistema.feromonas[cancion_i][cancion_j])
                    edge_weights.append(self.sistema.feromonas[cancion_i][cancion_j])
        
        if G.number_of_edges() > 0:
            # Dibujar grafo
            pos = nx.spring_layout(G, k=1, iterations=50)
            
            # Normalizar pesos para el grosor de las aristas
            if edge_weights:
                max_weight = max(edge_weights)
                edge_widths = [5 * (w / max_weight) for w in edge_weights]
            else:
                edge_widths = [1] * G.number_of_edges()
            
            nx.draw_networkx_nodes(G, pos, node_size=500, node_color='lightblue', 
                                 alpha=0.7, ax=self.ax_grafo)
            nx.draw_networkx_edges(G, pos, width=edge_widths, alpha=0.6, 
                                 edge_color='gray', arrows=True, ax=self.ax_grafo)
            nx.draw_networkx_labels(G, pos, font_size=8, ax=self.ax_grafo)
            
            # Dibujar etiquetas de pesos en las aristas
            edge_labels = {(u, v): f"{d['weight']:.2f}" for u, v, d in G.edges(data=True)}
            nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=6, ax=self.ax_grafo)
        
        self.ax_grafo.set_title("Grafo de Recomendaciones (Feromonas)")
        self.ax_grafo.axis('off')
        
        self.canvas_grafo.draw()
        
    def run(self):
        self.root.mainloop()

# Ejecutar la aplicación
if __name__ == "__main__":
    app = VisualizadorSpotify()
    app.run()