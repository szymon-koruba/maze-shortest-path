import cv2

class formatting_function:

    def __init__(self):
        self.path = None


    def read_picture(self):
        picture = cv2.imread(self.path)
        return picture

    def smooth_edges(self, picture):
        smoothed_image = cv2.bilateralFilter(picture, 11, 30, 30)
        return smoothed_image

    def image_binarization(self):
        file = self.read_picture()
        picture = self.smooth_edges(file)
        bin_picture = cv2.Canny(self.smooth_edges(picture), 255, 0)
        return bin_picture




test = formatting_function()

screen2 = test.read_picture('screen_0.jpg')


screen0 = test.image_binarization('screen_0.jpg')

cv2.imshow('Wygladzone krawedzie',screen0)

print(screen0)
cv2.waitKey(0)
cv2.destroyAllWindows()

