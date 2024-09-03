from skimage.draw import line


def path_draw(predecessors, end, pict):
    path = []
    node = end
    while node is not None:
        path.append(node)
        node = predecessors[node]
    path = path[::-1]

    for i in range(len(path) - 1):
        start_node = path[i]
        end_node = path[i + 1]
        row, col = start_node
        end_row, end_col = end_node

        rr, cc = line(row, col, end_row, end_col)
        pict[rr, cc] = [0, 0, 255]

    return pict
