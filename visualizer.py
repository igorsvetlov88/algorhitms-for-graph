import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np

class GraphVisualizer:
    def __init__(self, graph_data, algorithm_name):
        self.graph_data = graph_data
        self.algorithm_name = algorithm_name
        self.G = nx.Graph()

        for node, neighbors in graph_data.items():
            for neighbor, weight in neighbors.items():
                self.G.add_edge(node, neighbor, weight=weight)

        # Генерация случайных позиций при каждом создании визуализатора
        self.pos = self.generate_random_positions()
        self.fig, self.ax = plt.subplots(figsize=(10, 8))
        self.reset_state()

    def generate_random_positions(self):
        """Генерирует случайные позиции узлов с небольшим смещением"""
        pos = {}
        nodes = list(self.G.nodes())
        np.random.seed()  # Разные случайные позиции при каждом запуске

        # Распределение узлов по кругу
        radius = 5
        angle_step = 2 * np.pi / len(nodes)

        for i, node in enumerate(nodes):
            angle = i * angle_step + np.random.uniform(-0.1, 0.1)
            x = radius * np.cos(angle) + np.random.uniform(-0.5, 0.5)
            y = radius * np.sin(angle) + np.random.uniform(-0.5, 0.5)
            pos[node] = (x, y)

        # Оптимизация позиций
        return nx.spring_layout(self.G, pos=pos, seed=np.random.randint(0, 100), iterations=50)

    def reset_state(self):
        self.current_distances = {node: '∞' for node in self.G.nodes()}
        self.visited_nodes = set()

    def draw_graph(self, visited_nodes):
        all_nodes = set(self.G.nodes())
        missing_nodes = all_nodes - set(visited_nodes)

        # Для непосещённых вершин устанавливаем ∞
        for node in missing_nodes:
            if node not in self.current_distances:
                self.current_distances[node] = '∞'
        self.visited_nodes = visited_nodes
        node_colors = ['red' if node in visited_nodes else 'skyblue' for node in self.G.nodes()]

        self.ax.clear()
        nx.draw_networkx_nodes(self.G, self.pos, node_size=800, node_color=node_colors, ax=self.ax)
        nx.draw_networkx_edges(self.G, self.pos, width=2, edge_color='gray', ax=self.ax)

        if self.algorithm_name in ["DIJKSTRA", "BELLMAN-FORD"]:
            labels = {}
            for node in self.G.nodes():
                if node in visited_nodes:
                    labels[node] = f"{node}\n({self.current_distances[node]})"
                else:
                    labels[node] = f"{node}\n(∞)"
            nx.draw_networkx_labels(self.G, self.pos, labels=labels, font_size=10, ax=self.ax)

            edge_labels = nx.get_edge_attributes(self.G, 'weight')
            nx.draw_networkx_edge_labels(
                self.G, self.pos, edge_labels=edge_labels,
                font_color='green', font_size=10, ax=self.ax
            )
        else:
            nx.draw_networkx_labels(self.G, self.pos, font_size=12, ax=self.ax)

        plt.title(f"{self.algorithm_name} Визуализация", fontsize=14)
        plt.axis('off')

    def animate(self):
        from tracer import state_log

        def update(frame):
            self.draw_graph(state_log[frame])

        anim = FuncAnimation(
            self.fig, update, frames=len(state_log),
            interval=1000, repeat=True
        )
        plt.show()