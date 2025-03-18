import heapq
import networkx as nxt
import numpy as np

class FindQuickestPath:
    def __init__(self):
        pass

    def binary_image_to_graph(self, image):
        gph = nxt.Graph()
        rows, cols = image.shape

        left, right, up, down = (-1, 0), (1, 0), (0, -1), (0, 1)

        moves = [down, up, right, left]
        for row in range(rows):
            for col in range(cols):
                if image[row, col] == 255:
                    gph.add_node((row, col))
                    for move in moves:
                        new_x, new_y = row + move[0], col + move[1]
                        if 0 <= new_x < rows and 0 <= new_y < cols and image[new_x, new_y] == 255:
                            euklides_weight = np.sqrt((new_x - row) ** 2 + (new_y - col) ** 2)
                            gph.add_edge((row, col), (new_x, new_y), weight=euklides_weight)
        return gph

    def heuristic(self, node, end):
        return np.sqrt((node[0] - end[0]) ** 2 + (node[1] - end[1]) ** 2)

    def a_star(self, graph, start, end):
        dists = {node: float('inf') for node in graph.nodes()}
        dist_to_my_path = {node: None for node in graph.nodes()}
        dists[start] = 0

        queue = [(0, start)]
        heapq.heapify(queue)

        while queue:
            current_cost, current_node = heapq.heappop(queue)

            if current_node == end:
                break

            for neighbor in graph.neighbors(current_node):
                weight = graph.edges[current_node, neighbor]['weight']
                tentative_g = dists[current_node] + weight

                if tentative_g < dists[neighbor]:
                    dists[neighbor] = tentative_g
                    dist_to_my_path[neighbor] = current_node
                    f_cost = tentative_g + self.heuristic(neighbor, end)
                    heapq.heappush(queue, (f_cost, neighbor))

        return dist_to_my_path



