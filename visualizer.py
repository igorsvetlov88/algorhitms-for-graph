import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

class GraphVisualizer:
    def __init__(self, graph_data, algorithm_name):
        self.graph_data = graph_data
        self.algorithm_name = algorithm_name  # Название алгоритма
        self.G = nx.Graph()
        for node, edges in graph_data.items():
            for edge in edges:
                self.G.add_edge(node, edge)

        self.pos = nx.spring_layout(self.G)  # Фиксируем позиции узлов
        self.fig, self.ax = plt.subplots(figsize=(8, 6))

    def draw_graph(self, visited_nodes):
        """Рисует граф с подсвеченными посещёнными вершинами."""
        colors = ['red' if node in visited_nodes else 'blue' for node in self.G.nodes()]
        self.ax.clear()
        nx.draw(
            self.G, self.pos, with_labels=True,
            node_color=colors, node_size=800, ax=self.ax
        )
        plt.title(f"{self.algorithm_name} Visualization")  # Динамический заголовок

    def animate(self):
        """Анимирует шаги алгоритма."""
        from tracer import state_log

        def update(frame):
            self.draw_graph(state_log[frame])

        anim = FuncAnimation(self.fig, update, frames=len(state_log), interval=1000)
        plt.show()