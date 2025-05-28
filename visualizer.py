import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

class GraphVisualizer:
    def __init__(self, graph_data, algorithm_name):
        self.graph_data = graph_data
        self.algorithm_name = algorithm_name
        self.G = nx.Graph()

        for node, neighbors in graph_data.items():
            for neighbor, weight in neighbors.items():
                self.G.add_edge(node, neighbor, weight=weight)

        self.pos = nx.spring_layout(self.G, seed=42)
        self.fig, self.ax = plt.subplots(figsize=(10, 8))
        self.reset_state()  # Инициализация состояния

    def reset_state(self):
        """Полный сброс состояния визуализации"""
        self.current_distances = {node: '∞' for node in self.G.nodes()}
        self.visited_nodes = set()

    def draw_graph(self, visited_nodes):
        # Обновляем множество посещённых вершин
        self.visited_nodes = visited_nodes

        node_colors = ['red' if node in visited_nodes else 'skyblue' for node in self.G.nodes()]

        self.ax.clear()
        nx.draw_networkx_nodes(self.G, self.pos, node_size=800, node_color=node_colors, ax=self.ax)
        nx.draw_networkx_edges(self.G, self.pos, width=2, edge_color='gray', ax=self.ax)

        # Отображаем расстояния только для Дейкстры
        if self.algorithm_name == "DIJKSTRA":
            labels = {}
            for node in self.G.nodes():
                # Для посещённых вершин показываем реальное расстояние
                if node in visited_nodes:
                    labels[node] = f"{node}\n({self.current_distances[node]})"
                # Для непосещённых - всегда ∞
                else:
                    labels[node] = f"{node}\n(∞)"
            nx.draw_networkx_labels(self.G, self.pos, labels=labels, font_size=10, ax=self.ax)

            # Веса рёбер
            edge_labels = nx.get_edge_attributes(self.G, 'weight')
            nx.draw_networkx_edge_labels(
                self.G, self.pos, edge_labels=edge_labels,
                font_color='green', font_size=10, ax=self.ax
            )
        else:
            # Для BFS/DFS - обычные подписи
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