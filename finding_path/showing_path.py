from skimage.draw import line


def path_draw(path1, end, pict):

    height, width, channels = pict.shape
    if height <= 500 or width <= 500:
        thick = 1
    elif 500 < height <= 1000 or 500 < width <= 1000:
        thick = 2
    elif 1000 < height or 1000 < width:
        thick = 4

    path = []
    node = end
    while node is not None:
        path.append(node)
        node = path1[node]

    for i in range(len(path) - 1):
        start_node = path[i]
        end_node = path[i + 1]
        row, col = start_node
        end_row, end_col = end_node

        rr, cc = line(row, col, end_row, end_col)

        for r, c in zip(rr, cc):
            for wide_r in range(-thick, thick+1):
                for wide_c in range(-thick, thick+1):
                    if 0 <= r+wide_r < pict.shape[0] and 0 <= c+wide_c < pict.shape[1]:
                        pict[r+wide_r, c+wide_c] = [0, 0, 255]

    return pict
