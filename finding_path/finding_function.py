from photo_form import form_functions as ff
import cv2
import heapq
import numpy as np
import statistics as st
from collections import Counter


test = ff.formatting_function()

screen0 = test.binaryzation('skoski.jpg')
cv2.imshow('Zdjęcie', screen0)
cv2.waitKey(0)
cv2.destroyAllWindows()


class Finding_best_way_out:
    def __init__(self):
        pass

    def finding_the_nearest_outlier_pixel_value(self, image):
        up = {col: next(row for row in range(image.shape[0]) if image[row, col] == 255) for col in range(image.shape[1])
              if any(image[row, col] == 255 for row in range(image.shape[0]))}

        left = {row: next(col for col in range(image.shape[1]) if image[row, col] == 255) for row in
                range(image.shape[0]) if any(image[row, col] == 255 for col in range(image.shape[1]))}

        down = {col: next(row for row in reversed(range(image.shape[0])) if image[row, col] == 255) for col in
                range(image.shape[1]) if any(image[row, col] == 255 for row in range(image.shape[0]))}

        right = {row: next(col for col in reversed(range(image.shape[1])) if image[row, col] == 255) for row in
                 range(image.shape[0]) if any(image[row, col] == 255 for col in range(image.shape[1]))}

        return up, left, down, right

    def taking_out_important_data(self,image):
        up, left, down, right = self.finding_the_nearest_outlier_pixel_value(image)
        up_row, up_col = [], []
        down_row, down_col = [], []
        left_col, left_row = [], []
        right_col, right_row = [], []

        for col, row in up.items():
            up_row.append(row)
            up_col.append(col)
        for col, row in down.items():
            down_row.append(row)
            down_col.append(col)
        for row,col in left.items():
            left_col.append(col)
            left_row.append(row)
        for row,col in right.items():
            right_col.append(col)
            right_row.append(row)

        return up_row, down_row, left_col, right_col, up_col, down_col, left_row, right_row

    def calculating_outliers(self,data):
        np_data = np.array(data)
        Q1 = np.percentile(np_data, 25)
        Q3 = np.percentile(np_data, 75)
        IQR = Q3 - Q1

        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR

        outliers = np_data[(np_data < lower_bound) | (np_data > upper_bound)]
        return outliers

    def finding_outliers(self, image):
        up, down, left, right, *rest = self.taking_out_important_data(image)
        up_out = self.calculating_outliers(up)
        down_out = self.calculating_outliers(down)
        left_out = self.calculating_outliers(left)
        right_out = self.calculating_outliers(right)

        return up_out, down_out, left_out, right_out

    def finding_columns_for_outliners(self, image):
        up, left, down, right = self.finding_the_nearest_outlier_pixel_value(image)
        up_out, down_out, left_out, right_out = self.finding_outliers(image)

        out_col_u = []
        out_col_d = []
        out_row_l = []
        out_row_r = []
        for i in up_out:
            for col, row in up.items():
                if i == row:
                    out_col_u.append(col)

        for i in down_out:
            for col, row in down.items():
                if i == row:
                    out_col_d.append(col)

        for i in left_out:
            for row, col in left.items():
                if i == col:
                    out_row_l.append(row)

        for i in right_out:
            for row, col in right.items():
                if i == col:
                    out_row_r.append(row)

        return out_col_u, out_col_d, out_row_l, out_row_r

    def choose_two_longest_vectors(self, image):
        out_col_u, out_col_d, out_row_l, out_row_r = self.finding_columns_for_outliners(image)
        vectors = [out_col_u, out_col_d, out_row_l, out_row_r]
        vector_names = ['out_col_u', 'out_col_d', 'out_row_l', 'out_row_r']

        lengths = [len(vec) for vec in vectors]
        sorted_indices = np.argsort(lengths)[::-1]

        longest_vectors = [vectors[sorted_indices[0]], vectors[sorted_indices[1]]]
        longest_vector_names = [vector_names[sorted_indices[0]], vector_names[sorted_indices[1]]]
        return longest_vector_names



    def calculating_best_start_goal_point(self, image):
        out_col_u, out_col_d, out_row_l, out_row_r = self.finding_columns_for_outliners(image)
        x = self.choose_two_longest_vectors(image)
        print(x)

        mean_val_up = None
        if len(out_col_u) != 0 and 'out_col_u' in x:
            mean_val_up = int(round(st.mean(out_col_u), 0))

        mean_val_down = None
        if len(out_col_d) != 0 and 'out_col_d' in x:
            mean_val_down = int(round(st.mean(out_col_d), 0))

        mean_val_left = None
        if len(out_row_l) and 'out_row_l' in x:
            mean_val_left = int(round(st.mean(out_row_l), 0))
            print( mean_val_left)

        mean_val_right = None
        if len(out_row_r) != 0 and 'out_row_r' in x:
            mean_val_right = int(round(st.mean(out_row_r), 0))

        print(mean_val_up, mean_val_down, mean_val_left, mean_val_right
)

        return mean_val_up, mean_val_down, mean_val_left, mean_val_right


    def finding_missing_index(self, image):
        up_row, down_row,_ ,_ ,_ ,_, left_row, right_row = self.taking_out_important_data(image)
        counter = Counter(up_row)
        up_common = counter.most_common(1)[0][0]

        counter = Counter(down_row)
        down_common = counter.most_common(1)[0][0]

        counter = Counter(left_row)
        left_common = counter.most_common(1)[0][0]

        counter = Counter(right_row)
        right_common = counter.most_common(1)[0][0]

        return up_common, down_common, left_common, right_common

    def find_start_and_goal(self, image):
        r_u, r_d, c_l, c_r = self.calculating_best_start_goal_point(image)
        c_u, c_d, r_l, r_r = self.finding_missing_index(image)
        if r_u != None:
            start = [r_u,c_u]
        if r_d != None:
            if 'start' in locals():
                finish = [r_d, c_d]
            else:
                start = [r_d, c_d]
        if c_l != None:
            if 'start' in locals():
                finish = [r_l, c_l]
            else:
                start = [r_l, c_l]
        if c_r != None:
            if 'start' in locals():
                finish = [r_r, c_r]
            else:
                start = [r_r, c_r]

        print(start,finish)
        return start, finish





test1 = Finding_best_way_out()
start, finish = test1.find_start_and_goal(screen0)


x, y = start[0], start[1]
color = (100, 0, 0)
cv2.circle(screen0, (x, y), 5, color, -1)

x, y = finish[0], finish[1]
color = (100, 255, 0)
cv2.circle(screen0, (x, y), 5, color, -1)

cv2.imshow('Zdjęcie', screen0)
cv2.waitKey(0)
cv2.destroyAllWindows()
