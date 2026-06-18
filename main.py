import customtkinter as ctk
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import heapq

# 1. Definir el grafo y los pesos exactos del informe
grafo_ciudades = {
    'Madrid': {'Barcelona': 600, 'París': 1050},
    'Barcelona': {'Madrid': 600, 'París': 830},
    'París': {'Madrid': 1050, 'Barcelona': 830, 'Londres': 340, 'Bruselas': 260, 'Múnich': 680, 'Zúrich': 490},
    'Londres': {'París': 340, 'Bruselas': 320},
    'Bruselas': {'París': 260, 'Londres': 320, 'Ámsterdam': 170},
    'Ámsterdam': {'Bruselas': 170, 'Berlín': 580},
    'Berlín': {'Ámsterdam': 580, 'Múnich': 500, 'Praga': 280, 'Varsovia': 520},
    'Múnich': {'París': 680, 'Berlín': 500, 'Viena': 350, 'Zúrich': 240},
    'Viena': {'Múnich': 350, 'Praga': 250, 'Budapest': 210},
    'Praga': {'Berlín': 280, 'Viena': 250, 'Varsovia': 510},
    'Varsovia': {'Berlín': 520, 'Praga': 510},
    'Budapest': {'Viena': 210},
    'Zúrich': {'Múnich': 240, 'Milán': 240, 'París': 490},
    'Milán': {'Zúrich': 240, 'Roma': 480},
    'Roma': {'Milán': 480}
}

# Posiciones aproximadas para que el grafo se parezca a un mapa real de Europa
posiciones = {
    'Madrid': (0, 0), 'Barcelona': (2, 0), 'París': (1.5, 3), 
    'Londres': (1, 4.5), 'Bruselas': (2.5, 3.8), 'Ámsterdam': (3, 4.5),
    'Berlín': (5, 4), 'Múnich': (4, 2), 'Viena': (6, 2), 
    'Praga': (5.5, 3), 'Varsovia': (7, 4), 'Budapest': (7, 1.5),
    'Zúrich': (3, 1.5), 'Milán': (3.5, 0), 'Roma': (4.5, -1.5)
}

# 2. Lógica pura del Algoritmo de Dijkstra
def calcular_dijkstra(grafo, origen, destino):
    distancias = {nodo: float('infinity') for nodo in grafo}
    distancias[origen] = 0
    camino_previo = {nodo: None for nodo in grafo}
    cola_prioridad = [(0, origen)]
    
    while cola_prioridad:
        distancia_actual, nodo_actual = heapq.heappop(cola_prioridad)
        
        if nodo_actual == destino:
            break
        if distancia_actual > distancias[nodo_actual]:
            continue
            
        for vecino, peso in grafo[nodo_actual].items():
            distancia_tentativa = distancia_actual + peso
            if distancia_tentativa < distancias[vecino]:
                distancias[vecino] = distancia_tentativa
                camino_previo[vecino] = nodo_actual
                heapq.heappush(cola_prioridad, (distancia_tentativa, vecino))
                
    # Reconstrucción de la ruta desde el destino al origen
    ruta = []
    actual = destino
    while actual is not None:
        ruta.insert(0, actual)
        actual = camino_previo[actual]
        
    if distancias[destino] == float('infinity'):
        return [], 0
    return ruta, distancias[destino]

# 3. Construcción de la Interfaz Gráfica
class AppGrafo(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Optimizador de Rutas - Matemática Discreta")
        self.geometry("950x650")
        
        # Cargar los datos matemáticos al grafo de NetworkX
        self.G = nx.Graph()
        for origen, destinos in grafo_ciudades.items():
            for destino, peso in destinos.items():
                self.G.add_edge(origen, destino, weight=peso)

        self.crear_widgets()
        self.dibujar_grafo()

    def crear_widgets(self):
        # Panel izquierdo
        frame_controles = ctk.CTkFrame(self, width=250)
        frame_controles.pack(side="left", fill="y", padx=15, pady=15)
        
        ctk.CTkLabel(frame_controles, text="Ciudad de Origen:", font=("Arial", 14, "bold")).pack(pady=(20, 5))
        self.combo_origen = ctk.CTkComboBox(frame_controles, values=list(grafo_ciudades.keys()))
        self.combo_origen.pack(pady=5)
        
        ctk.CTkLabel(frame_controles, text="Ciudad de Destino:", font=("Arial", 14, "bold")).pack(pady=(20, 5))
        self.combo_destino = ctk.CTkComboBox(frame_controles, values=list(grafo_ciudades.keys()))
        self.combo_destino.pack(pady=5)
        
        btn_calcular = ctk.CTkButton(frame_controles, text="Calcular Ruta", command=self.ejecutar_calculo)
        btn_calcular.pack(pady=30)
        
        self.lbl_resultado = ctk.CTkLabel(frame_controles, text="Resultado:\nEsperando cálculo...", justify="left", wraplength=220)
        self.lbl_resultado.pack(pady=10)

        # Panel derecho para el mapa
        self.frame_canvas = ctk.CTkFrame(self)
        self.frame_canvas.pack(side="right", fill="both", expand=True, padx=15, pady=15)
        
        self.fig, self.ax = plt.subplots(figsize=(6, 5))
        # Ajustar colores del canvas para que coincida con el modo oscuro
        self.fig.patch.set_facecolor('#2b2b2b')
        self.ax.set_facecolor('#2b2b2b')
        
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame_canvas)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

    def dibujar_grafo(self, ruta_optima=None):
        self.ax.clear()
        
        # Estilos base
        nx.draw_networkx_nodes(self.G, posiciones, ax=self.ax, node_color='#4a90e2', node_size=600)
        nx.draw_networkx_labels(self.G, posiciones, ax=self.ax, font_size=8, font_weight="bold", font_color='white')
        
        aristas_base = self.G.edges()
        nx.draw_networkx_edges(self.G, posiciones, ax=self.ax, edgelist=aristas_base, edge_color='#666666', width=1.5)
        
        labels_pesos = nx.get_edge_attributes(self.G, 'weight')
        nx.draw_networkx_edge_labels(self.G, posiciones, edge_labels=labels_pesos, ax=self.ax, font_size=7, font_color='white')

        # Resaltado visual si hay ruta calculada
        if ruta_optima and len(ruta_optima) > 1:
            aristas_ruta = [(ruta_optima[i], ruta_optima[i+1]) for i in range(len(ruta_optima)-1)]
            nx.draw_networkx_edges(self.G, posiciones, ax=self.ax, edgelist=aristas_ruta, edge_color='#ff4d4d', width=4)
            nx.draw_networkx_nodes(self.G, posiciones, ax=self.ax, nodelist=ruta_optima, node_color='#ff4d4d', node_size=700)

        self.ax.axis('off')
        self.fig.tight_layout(pad=0)
        self.canvas.draw()

    def ejecutar_calculo(self):
        origen = self.combo_origen.get()
        destino = self.combo_destino.get()
        
        if origen == destino:
            self.lbl_resultado.configure(text="El origen y destino\nson iguales.\nCosto: 0 km")
            self.dibujar_grafo()
            return
            
        ruta, costo = calcular_dijkstra(grafo_ciudades, origen, destino)
        
        if ruta:
            texto_ruta = " ->\n".join(ruta)
            self.lbl_resultado.configure(text=f"Ruta óptima:\n\n{texto_ruta}\n\nCosto total:\n{costo} km")
            self.dibujar_grafo(ruta_optima=ruta)
        else:
            self.lbl_resultado.configure(text="No se encontró ruta.")

if __name__ == "__main__":
    ctk.set_appearance_mode("Dark")
    app = AppGrafo()
    app.mainloop()