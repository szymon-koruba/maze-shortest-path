import numpy as np
from photo_form import form_functions as ff
import cv2



class NewStartEndPath:
    def __init__(self):
        self.contour_img = None
        self.coordinates = None

    def creating_contour_map(self, up, down, right, left, bin_picture):
        self.contour_img = np.zeros_like(bin_picture)
        for row, col in up.items():
            self.contour_img[col, row] = 255

        for row, col in down.items():
            self.contour_img[col, row] = 255

        for row, col in right.items():
            self.contour_img[row, col] = 255

        for row, col in left.items():
            self.contour_img[row, col] = 255

    def finding_gaps_in_contur(self):
        rows, cols = self.contour_img.shape
        self.coordinates = []
        for row in range(rows):
            for col in range(cols):
                if self.contour_img[row, col] == 255:
                    pixel_values = [self.contour_img[row + 1, col - 1] == 255, self.contour_img[row + 1, col] == 255,
                                    self.contour_img[row + 1, col + 1] == 255, self.contour_img[row, col + 1] == 255,
                                    self.contour_img[row - 1, col + 1] == 255, self.contour_img[row - 1, col] == 255,
                                    self.contour_img[row - 1, col - 1] == 255, self.contour_img[row, col - 1] == 255]
                    if pixel_values.count(True) == 1:
                        self.coordinates.append((row, col))
                        continue
                    else:
                        continue

    def paint_and_end(self, up, down, right, left, picture):
        rows, cols = self.contour_img.shape
        u_set = set((row, col) for col, row in up.items())
        d_set = set((row, col) for col, row in down.items())
        r_set = set((row, col) for row, col in right.items())
        l_set = set((row, col) for row, col in left.items())

        up = []
        down = []
        left = []
        right = []

        for row, col in self.coordinates:
            if (row, col) in u_set or (row, col) in d_set:
                if col < cols and (row < rows/2):
                    up.append(col)
                if col < cols and (row > rows / 2):
                    down.append(col)
            if (row, col) in r_set or (row, col) in l_set:
                if row < rows and (col > cols / 2):
                    left.append(row)
                if row < rows and (col < cols / 2):
                    right.append(row)

        for row, col in self.coordinates:
            if (row, col) in u_set or (row, col) in d_set:
                if col < cols and (row < rows/2):
                    if len(up) >= 4:
                        start_row = row
                        end_row = 0
                        if start_row > end_row:
                            picture[end_row:start_row, min(up):max(up)] = 255
                if col < cols and (row > rows/2):
                    if len(down) >= 4:
                        start_row = row
                        end_row = rows
                        if start_row < end_row:
                            picture[start_row:end_row, min(down): max(down)] = 255

            if (row, col) in r_set or (row, col) in l_set:
                if row < rows and (col > cols/2):
                    if len(left) >= 4:
                        start_col = col
                        end_col = cols
                        if start_col < end_col:
                            picture[min(left):max(left), start_col:end_col] = 255
                if row < rows and (col < cols/2):
                    if len(right) >= 4:
                        start_col = col
                        end_col = 0
                        if start_col > end_col:
                            picture[min(right):max(right), end_col:start_col] = 255
        return picture

    def full_class_work(self, up, down, right, left, bin_picture, picture):
        self.creating_contour_map(up, down, right, left, picture)
        self.finding_gaps_in_contur()
        picture_mod = self.paint_and_end(up, down, right, left, bin_picture)
        return picture_mod
