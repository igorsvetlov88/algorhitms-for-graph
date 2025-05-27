from tracer import run_with_tracer, log_state, state_log
from visualizer import GraphVisualizer

def bfs(graph):
    visited = set()
    all_nodes = list(graph.keys())

    for node in all_nodes:
        if node not in visited:
            queue = [node]

            while queue:
                current = queue.pop(0)
                if current not in visited:
                    visited.add(current)
                    log_state(visited) # состояние логируется после посещения вершины

                    for neighbor in graph[current]:
                        if neighbor not in visited:
                            queue.append(neighbor)

def is_connected(graph): # проверка на связность графа
    visited = set()
    start_node = next(iter(graph))
    queue = [start_node]

    while queue:
        node = queue.pop(0)
        if node not in visited:
            visited.add(node)
            for neighbor in graph[node]:
                if neighbor not in visited:
                    queue.append(neighbor)

    return len(visited) == len(graph)


def dfs(graph):
    visited = set()
    all_nodes = list(graph.keys())

    for node in all_nodes:
        if node not in visited:
            stack = [node]

            while stack:
                current = stack.pop()
                if current not in visited:
                    visited.add(current)

                    # Логируем состояние после посещения вершины
                    log_state(visited)

                    for neighbor in reversed(graph[current]):
                        if neighbor not in visited:
                            stack.append(neighbor)



if __name__ == "__main__":
    # Определяем граф
    graph = {
        'A': ['B', 'C'],
        'B': ['A', 'D', 'E', 'H'],
        'C': ['A', 'F'],
        'D': ['B'],
        'E': ['B', 'F'],
        'F': ['C', 'E'],
        'H': ['B']
    }

    algorithm = input("Выберите алгоритм bfs/dfs: ").strip().lower()

    if algorithm == 'bfs':
        algorithm_name = 'BFS'
        bfs(graph)
    elif algorithm == 'dfs':
        algorithm_name = 'DFS'
        dfs(graph)
    else:
        print("Неизвестный алгоритм!")
        exit()

    visualizer = GraphVisualizer(graph, algorithm_name)
    visualizer.animate()