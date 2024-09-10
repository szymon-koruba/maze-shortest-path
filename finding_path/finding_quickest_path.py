import heapq
import networkx as nxt


class FindQuickestPath:
    def __init__(self):
        pass

    def binary_image_to_graph(self, image):
        bin_img = (image >= 127).astype(int)
        gph = nxt.Graph()
        rows, cols = bin_img.shape

        for row in range(rows):
            for col in range(cols):
                if bin_img[row, col] == 1:
                    gph.add_node((row, col))

        left = (-1, 0)
        right = (1, 0)
        up = (0, -1)
        down = (0, 1)

        moves = [down, up, right, left]
        for row in range(rows):
            for col in range(cols):
                if bin_img[row, col] == 1:
                    for move in moves:
                        new_x, new_y = row + move[0], col + move[1]
                        if 0 <= new_x < rows and 0 <= new_y < cols and bin_img[new_x, new_y] == 1:
                            euklides_weight = pow((new_x - row) ** 2 + (new_y - col) ** 2, 1/2)
                            gph.add_edge((row, col), (new_x, new_y), weight=euklides_weight)
        return gph

    def dijkstra(self, graph, start, end):
        distances = {node: float('inf') for node in graph.nodes()}
        dist_before = {node: None for node in graph.nodes()}
        distances[start] = 0
        queue = [(0, start)]

        while queue:
            distance_now, node_now = heapq.heappop(queue)

            if distance_now == end:
                break

            if distance_now > distances[node_now]:
                continue

            for neighbor in graph.neighbors(node_now):
                weight = graph.edges[node_now, neighbor]['weight']
                distance = distance_now + weight
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    dist_before[neighbor] = node_now
                    heapq.heappush(queue, (distance, neighbor))
        return dist_before
