import heapq
import numpy as np
import networkx as nxt
import matplotlib.pyplot as plt


class FindQuickestPath:
    def __init__(self):
        pass

    def binary_image_to_graph(self, image):
        binary_image = (image >= 127).astype(int)
        graph = nxt.Graph()
        rows, cols = binary_image.shape

        for row in range(rows):
            for col in range(cols):
                if binary_image[row, col] == 1:
                    graph.add_node((row, col))

        moves = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        for row in range(rows):
            for col in range(cols):
                if binary_image[row, col] == 1:
                    for move in moves:
                        nx, ny = row + move[0], col + move[1]
                        if 0 <= nx < rows and 0 <= ny < cols and binary_image[nx, ny] == 1:

                            weight = np.sqrt((nx - row) ** 2 + (ny - col) ** 2)
                            graph.add_edge((row, col), (nx, ny), weight=weight)
        return graph

    def dijkstra(self, graph, start, end, image):
        distances = {node: float('inf') for node in graph.nodes()}
        predecessors = {node: None for node in graph.nodes()}
        distances[start] = 0
        priority_queue = [(0, start)]

        while priority_queue:
            current_distance, current_node = heapq.heappop(priority_queue)

            if current_node == end:
                break

            if current_distance > distances[current_node]:
                continue

            for neighbor in graph.neighbors(current_node):
                weight = graph.edges[current_node, neighbor]['weight']
                distance = current_distance + weight
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    predecessors[neighbor] = current_node
                    heapq.heappush(priority_queue, (distance, neighbor))

        path = []
        node = end
        while node is not None:
            path.append(node)
            node = predecessors[node]

        binary_image = (image >= 127).astype(int)
        image_with_path = np.copy(binary_image)

        for node in path:
            row, col = node
            image_with_path[row, col] = 0

        plt.figure(figsize=(8, 8))
        plt.imshow(image_with_path, cmap='grey')
        plt.title('Najkrótsza ścieżka na obrazie zbinaryzowanym')
        plt.axis('off')
        plt.show()
        return distances
