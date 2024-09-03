import cv2
import numpy as np


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
        self.blured_picture = cv2.GaussianBlur(self.picture, (5, 5), 4)

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

        left = {row: next(col for col in range(image.shape[1]) if image[row, col] == 0) for row in
                range(image.shape[0]) if any(image[row, col] == 0 for col in range(image.shape[1]))}

        down = {col: next(row for row in reversed(range(image.shape[0])) if image[row, col] == 0) for col in
                range(image.shape[1]) if any(image[row, col] == 0 for row in range(image.shape[0]))}

        right = {row: next(col for col in reversed(range(image.shape[1])) if image[row, col] == 0) for row in
                 range(image.shape[0]) if any(image[row, col] == 0 for col in range(image.shape[1]))}

        return up, left, down, right

    def painting(self, dilated_image, up, left, down, right):
        high, wight = dilated_image.shape
        for col, row in up.items():
            dilated_image[0:row, col] = 0

        for col, row in down.items():
            dilated_image[row:high, col] = 0

        for row, col in left.items():
            dilated_image[row, 0: col] = 0

        for row, col in right.items():
            dilated_image[row, col:wight] = 0

        for row in range(high):
            for col in range(wight):
                if dilated_image[row,col] != 0:
                    dilated_image[row, col] = 0
                else:
                    break

        for row in reversed(range(high)):
            for col in reversed(range(wight)):
                if dilated_image[row,col] != 0:
                    dilated_image[row, col] = 0
                else:
                    break

        return dilated_image

    def full_form_image(self, path):
        self.read_picture(path)
        self.smooth_picture()
        self.sharper_picture()
        self.get_edges()
        self.binaryzation()
        dilated_ima = self.binary_image
        up, left, down, right = self.getting_size_to_crop(dilated_ima)
        picture = self.painting(dilated_ima, up, left, down, right)

        return up, left, down, right, dilated_ima, picture, self.picture
