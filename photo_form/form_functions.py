import cv2
import numpy as np


class formatting_function:

    def __init__(self):
      pass


    def read_picture(self,path):
        picture = cv2.imread(path)
        return picture

    def smooth_picture(self,picture):
        blurred = cv2.GaussianBlur(picture, (5, 5), 0)
        return blurred

    def sharper_picture(self,picture):
        kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
        sharpened = cv2.filter2D(picture, -1, kernel)
        return sharpened

    def get_edges(self,picture):
        edges = cv2.Canny(picture, 100, 200)
        return edges

    def binaryzation(self, path):
        picture = self.read_picture(path)
        smooth_picture = self.smooth_picture(picture)
        sharper_picture = self.sharper_picture(smooth_picture)
        edges = self.get_edges(sharper_picture)
        _, binary_image = cv2.threshold(edges, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        return binary_image



