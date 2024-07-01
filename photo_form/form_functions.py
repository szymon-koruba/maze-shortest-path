import cv2


class formatting_function:

    def __init__(self):
      pass


    def read_picture(self,path):
        picture = cv2.imread(path)
        return picture

    def smooth_edges(self, picture):
        smoothed_image = cv2.bilateralFilter(picture, 11, 30, 30)
        return smoothed_image

    def image_binarization(self, path):
        file = self.read_picture(path)
        picture = self.smooth_edges(file)
        bin_picture = cv2.Canny(self.smooth_edges(picture), 255, 0)
        return bin_picture



