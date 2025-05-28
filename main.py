from tracer import run_with_tracer, log_state, state_log
from visualizer import GraphVisualizer
import heapq

def bfs(graph):
    visited = set()
    all_nodes = list(graph.keys())
    global state_log
    state_log = []

    for node in all_nodes:
        if node not in visited:
            queue = [node]
            while queue:
                current = queue.pop(0)
                if current not in visited:
                    visited.add(current)
                    log_state(visited.copy())
                    for neighbor in graph[current]:
                        if neighbor not in visited:
                            queue.append(neighbor)
            log_state(visited.copy())

def dfs(graph):
    visited = set()
    all_nodes = list(graph.keys())
    global state_log
    state_log = []

    for node in all_nodes:
        if node not in visited:
            stack = [node]
            while stack:
                current = stack.pop()
                if current not in visited:
                    visited.add(current)
                    log_state(visited.copy())
                    for neighbor in reversed(list(graph[current].keys())):
                        if neighbor not in visited:
                            stack.append(neighbor)
            log_state(visited.copy())

def dijkstra(graph, start_node, visualizer):
    global state_log
    state_log = []

    # Полный сброс состояния визуализатора
    visualizer.reset_state()

    distances = {node: float('inf') for node in graph}
    distances[start_node] = 0
    visited = set()

    # Начальное состояние - все вершины непосещены
    log_state(set())

    priority_queue = [(0, start_node)]

    while priority_queue:
        current_dist, current_node = heapq.heappop(priority_queue)

        if current_node in visited:
            continue

        visited.add(current_node)
        # Обновляем ТОЛЬКО для посещённой вершины
        visualizer.current_distances[current_node] = current_dist
        log_state(visited.copy())

        for neighbor, weight in graph[current_node].items():
            distance = current_dist + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(priority_queue, (distance, neighbor))

    return distances

if __name__ == "__main__":
    graph = {
        'A': {'B': 3, 'C': 2},
        'B': {'A': 3, 'D': 4, 'E': 1, 'H': 5},
        'C': {'A': 2, 'F': 3},
        'D': {'B': 4},
        'E': {'B': 1, 'F': 2},
        'F': {'C': 3, 'E': 2},
        'H': {'B': 5}
    }

    algorithm = input("Выберите алгоритм (bfs/dfs/dijkstra): ").strip().lower()
    visualizer = GraphVisualizer(graph, algorithm.upper())

    if algorithm == 'bfs':
        bfs(graph)
    elif algorithm == 'dfs':
        dfs(graph)
    elif algorithm == 'dijkstra':
        start_node = input("Введите начальную вершину: ").strip().upper()
        if start_node not in graph:
            print("Такой вершины нет в графе!")
            exit()
        dijkstra(graph, start_node, visualizer)
    else:
        print("Неизвестный алгоритм!")
        exit()

    visualizer.animate()