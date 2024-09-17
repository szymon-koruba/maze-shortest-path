import networkx as nxt

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
                            euklides_weight = pow((new_x - row) ** 2 + (new_y - col) ** 2, 1/2)
                            gph.add_edge((row, col), (new_x, new_y), weight=euklides_weight)
        return gph

    def dijkstra(self, graph, start, end):
        dists = {node: float('inf') for node in graph.nodes()}
        dist_to_my_path = {node: None for node in graph.nodes()}
        dists[start] = 0
        queue = [(0, start)]

        while queue:
            distance_now, node_now = min(queue)
            queue.remove((distance_now, node_now))

            if distance_now > dists[node_now]:
                continue

            if distance_now == end:
                break

            for near_node_now in graph.neighbors(node_now):
                weight = graph.edges[node_now, near_node_now]['weight']
                suma = distance_now + weight
                if suma < dists[near_node_now]:
                    dists[near_node_now] = suma
                    dist_to_my_path[near_node_now] = node_now
                    new_node = (suma, near_node_now)
                    queue.append(new_node)
                    queue.sort()
        return dist_to_my_path
