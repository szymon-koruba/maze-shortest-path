import cv2
import numpy as np
from collections import Counter


class FormattingFunction:

    def __init__(self):
        self.picture = None
        self.blured_picture = None
        self.sharped_picture = None
        self.edges = None
        self.binary_image = None

    def read_picture(self, path):
        self.picture = cv2.imread(path)

    def smooth_picture(self):
        self.blured_picture = cv2.GaussianBlur(self.picture, (5, 5), 0)

    def sharper_picture(self):
        if self.blured_picture is not None:
            kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
            self.sharped_picture = cv2.filter2D(self.blured_picture, -1, kernel)

    def get_edges(self):
        self.edges = cv2.Canny(self.sharped_picture, 100, 200)

    def binaryzation(self):
        gray_picture = cv2.cvtColor(self.sharped_picture, cv2.COLOR_BGR2GRAY)
        _, self.binary_image = cv2.threshold(gray_picture, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    def getting_size_to_crop(self, image):
        up = {col: next(row for row in range(image.shape[0]) if image[row, col] == 0) for col in range(image.shape[1])
              if any(image[row, col] == 0 for row in range(image.shape[0]))}

        upl = [row for col, row in up.items()]

        left = {row: next(col for col in range(image.shape[1]) if image[row, col] == 0) for row in
                range(image.shape[0]) if any(image[row, col] == 0 for col in range(image.shape[1]))}
        lfl = [row for col, row in left.items()]

        down = {col: next(row for row in reversed(range(image.shape[0])) if image[row, col] == 0) for col in
                range(image.shape[1]) if any(image[row, col] == 0 for row in range(image.shape[0]))}
        dwl = [row for col, row in down.items()]


        right = {row: next(col for col in reversed(range(image.shape[1])) if image[row, col] == 0) for row in
                 range(image.shape[0]) if any(image[row, col] == 0 for col in range(image.shape[1]))}
        rrl = [row for col, row in right.items()]


        counter = Counter(upl)
        up_common = counter.most_common(1)[0][0]

        counter = Counter(lfl)
        left_common = counter.most_common(1)[0][0]

        counter = Counter(dwl)
        down_common = counter.most_common(1)[0][0]

        counter = Counter(rrl)
        right_common = counter.most_common(1)[0][0]

        return up_common, left_common, down_common, right_common

    def cut_picture_afeter_binariztion(self, picture, margin_up, margin_down, margin_left, margin_right):
        x1 = margin_left
        y1 = margin_up
        x2 = margin_right
        y2 = margin_down
        cropped_image = picture[y1:y2, x1:x2]
        return cropped_image

    def full_form_image(self, path):
        self.read_picture(path)
        self.smooth_picture()
        self.sharper_picture()
        self.get_edges()
        self.binaryzation()
        u, l, d, r = self.getting_size_to_crop(self.binary_image)
        full_image = self.cut_picture_afeter_binariztion(self.binary_image, u, d, l, r)

        return full_image

    def new_cut_try(self, path):
        self.read_picture(path)
        self.smooth_picture()
        self.sharper_picture()
        self.get_edges()
        bin = self.binaryzation()
        return bin


