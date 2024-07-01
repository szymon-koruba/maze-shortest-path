from photo_form import form_functions as ff
import photo_form as pf
import cv2
import heapq
import numpy as np
import statistics as st

test = ff.formatting_function()

screen0 = test.image_binarization('przyk.jpg')
print(screen0[170,220])


class finding_best_way_out():
    def __init__(self):
        pass

    def find_start_and_finish(self, image):

    # dla góry
        up = {col: next(row for row in range(image.shape[0]) if image[row, col] == 255) for col in range(image.shape[1]) if any(image[row, col] == 255 for row in range(image.shape[0]))}

    # dla lewej strony
        left = {row: next(col for col in range(image.shape[1]) if image[row, col] == 255) for row in range(image.shape[0]) if any(image[row, col] == 255 for col in range(image.shape[1]))}

    # dla dołu
        down = {col: next(row for row in reversed(range(image.shape[0])) if image[row, col] == 255) for col in range(image.shape[1]) if any(image[row, col] == 255 for row in range(image.shape[0]))}

    # dla prawej strony
        right = {row: next(col for col in reversed(range(image.shape[1])) if image[row, col] == 255) for row in range(image.shape[0]) if any(image[row, col] == 255 for col in range(image.shape[1]))}

        L=[]
        for ind,wart in up.items():
            L.append(wart)

        La = np.array(L)

        Q1 = np.percentile(La, 25)
        Q3 = np.percentile(La, 75)
        IQR = Q3 - Q1

        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR

        outliers = La[(La < lower_bound) | (La > upper_bound)]

        mean_val_row = int(round(st.mean(L),0))

        Z = []
        for ind, wart in up.items():
            if wart in outliers:
                Z.append(ind)

        mean_val_col = int(round(st.mean(Z),0))

        print(mean_val_row,mean_val_col)



        print(Z)

    def djikstra(self, image, start, goal):
        rows, cols = len(image), len(image[0])
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        distance = [[float('inf')] * cols for _ in range(rows)]
        distance[start[0]][start[1]] = 0
        priority_queue = [(0, start)]

        while priority_queue:
            dist, (x, y) = heapq.heappop(priority_queue)
            if (x, y) == goal:
                return dist

            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if 0 <= nx < rows and 0 <= ny < cols and image[nx][ny] == 1:
                    new_dist = dist + 1
                    if new_dist < distance[nx][ny]:
                        distance[nx][ny] = new_dist
                        heapq.heappush(priority_queue, (new_dist, (nx, ny)))

        return -1


test1 = finding_best_way_out()
test1.find_start_and_finish(screen0)

cv2.imshow('Zdjęcie', screen0)
cv2.waitKey(0)
cv2.destroyAllWindows()