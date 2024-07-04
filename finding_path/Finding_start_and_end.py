import numpy as np
import statistics as st
from collections import Counter

class FindingBestWayOut:
    def __init__(self):
        self.up = None
        self.left = None
        self.right = None
        self.down = None
        self.up_row = None
        self.up_col = None
        self.down_row = None
        self.down_col = None
        self.left_row = None
        self.left_col = None
        self.right_row = None
        self.right_col = None

    def finding_the_nearest_outlier_pixel_value(self, image):
        self.up = {col: next(row for row in range(image.shape[0]) if image[row, col] == 0) for col in range(image.shape[1]) if any(image[row, col] == 0 for row in range(image.shape[0]))}
        self.left = {row: next(col for col in range(image.shape[1]) if image[row, col] == 0) for row in range(image.shape[0]) if any(image[row, col] == 0 for col in range(image.shape[1]))}
        self.down = {col: next(row for row in reversed(range(image.shape[0])) if image[row, col] == 0) for col in range(image.shape[1]) if any(image[row, col] == 0 for row in range(image.shape[0]))}
        self.right = {row: next(col for col in reversed(range(image.shape[1])) if image[row, col] == 0) for row in range(image.shape[0]) if any(image[row, col] == 0 for col in range(image.shape[1]))}

    def taking_out_important_data(self, image):
        self.finding_the_nearest_outlier_pixel_value(image)
        self.up_row = list(self.up.values())
        self.up_col = list(self.up.keys())
        self.down_row = list(self.down.values())
        self.down_col = list(self.down.keys())
        self.left_row = list(self.left.keys())
        self.left_col = list(self.left.values())
        self.right_row = list(self.right.keys())
        self.right_col = list(self.right.values())

    def calculating_outliers(self, data):
        np_data = np.array(data)
        q1 = np.percentile(np_data, 25)
        q3 = np.percentile(np_data, 75)
        iqr = q3 - q1
        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr
        outliers = np_data[(np_data < lower_bound) | (np_data > upper_bound)]
        return outliers

    def finding_outliers(self):
        up_out = self.calculating_outliers(self.up_row)
        down_out = self.calculating_outliers(self.down_row)
        left_out = self.calculating_outliers(self.left_col)
        right_out = self.calculating_outliers(self.right_col)
        return up_out, down_out, left_out, right_out

    def finding_columns_for_outliers(self):
        up_out, down_out, left_out, right_out = self.finding_outliers()
        out_col_up = [col for i in up_out for row, col in self.up.items() if i == row]
        out_col_down = [col for i in down_out for row, col in self.down.items() if i == row]
        out_row_left = [row for i in left_out for row, col in self.left.items() if i == col]
        out_row_right = [row for i in right_out for row, col in self.right.items() if i == col]
        return out_col_up, out_col_down, out_row_left, out_row_right

    def choose_two_longest_vectors(self):
        out_col_u, out_col_d, out_row_l, out_row_r = self.finding_columns_for_outliers()
        vectors = [out_col_u, out_col_d, out_row_l, out_row_r]
        vector_names = ['out_col_u', 'out_col_d', 'out_row_l', 'out_row_r']
        lengths = [len(vec) for vec in vectors]
        sorted_indices = np.argsort(lengths)[::-1]
        longest_vector_names = [vector_names[sorted_indices[0]], vector_names[sorted_indices[1]]]
        return longest_vector_names

    def calculating_best_start_goal_point(self):
        out_col_u, out_col_d, out_row_l, out_row_r = self.finding_columns_for_outliers()
        x = self.choose_two_longest_vectors()
        mean_val_up = None
        if len(out_col_u) != 0 and 'out_col_u' in x:
            mean_val_up = int(round(st.mean(out_col_u), 0))
        mean_val_down = None
        if len(out_col_d) != 0 and 'out_col_d' in x:
            mean_val_down = int(round(st.mean(out_col_d), 0))
        mean_val_left = None
        if len(out_row_l) != 0 and 'out_row_l' in x:
            mean_val_left = int(round(st.mean(out_row_l), 0))
        mean_val_right = None
        if len(out_row_r) != 0 and 'out_row_r' in x:
            mean_val_right = int(round(st.mean(out_row_r), 0))
        return mean_val_up, mean_val_down, mean_val_left, mean_val_right

    def finding_missing_index(self):
        counter = Counter(self.up_row)
        up_common = counter.most_common(1)[0][0]
        counter = Counter(self.down_row)
        down_common = counter.most_common(1)[0][0]
        counter = Counter(self.left_col)
        left_common = counter.most_common(1)[0][0]
        counter = Counter(self.right_col)
        right_common = counter.most_common(1)[0][0]
        return up_common, down_common, left_common, right_common

    def find_start_and_goal(self):
        c_u, c_d, r_l, r_r = self.calculating_best_start_goal_point()
        r_u, r_d, c_l, c_r = self.finding_missing_index()
        start, finish = None, None
        if c_u is not None:
            start = (r_u, c_u)
        if c_d is not None:
            if start is not None:
                finish = (r_d, c_d)
            else:
                start = (r_d, c_d)
        if r_l is not None:
            if start is not None:
                finish = (r_l, c_l)
            else:
                start = (r_l, c_l)
        if r_r is not None:
            if start is not None:
                finish = (r_r, c_r)
            else:
                start = (r_r, c_r)
        return start, finish

    def full_start_and_end(self, image):
        self.taking_out_important_data(image)
        start, finish = self.find_start_and_goal()
        return start, finish