from photo_form import form_functions as ff
from photo_form import outer_contour as oc
from finding_path import Finding_start_and_end as fsae
from finding_path import finding_quickest_path as fqp
from finding_path import showing_path as sp
from tkinter import filedialog
import tkinter as tk
import tempfile
import cv2
import os
import networkx


class CreatePath:
    def __init__(self):
        pass

    def load_pict(self):
        root = tk.Tk()
        root.lift()
        root.withdraw()
        file_path = filedialog.askopenfilename()
        root.destroy()
        return file_path

    def full_path_load_pict(self):
        file_path = self.load_pict()
        photo_form = ff.FormattingFunction()
        up, left, down, right, bin_pict, picture, main_pict = photo_form.full_form_image(file_path)

        photo_form_full = oc.NewStartEndPath()
        try:
            pict_af_form = photo_form_full.full_class_work(up, down, right, left, picture, bin_pict)
        except IndexError:
            return os.path.join(os.path.dirname(__file__), '..', 'graphics', 'gate.jpg')
        else:
            start_and_end_find = fsae.FindingBestWayOut()
            start, end = start_and_end_find.full_start_and_end(pict_af_form)

            if start is None and end is None:
                return os.path.join(os.path.dirname(__file__), '..', 'graphics', 'gate.jpg')
            else:
                find_path = fqp.FindQuickestPath()
                graph = find_path.binary_image_to_graph(pict_af_form)

                try:
                    fastest_path = find_path.dijkstra(graph, start, end)
                except networkx.exception.NetworkXError:
                    return os.path.join(os.path.dirname(__file__), '..', 'graphics', 'gate.jpg')
                else:

                    show_path = sp.path_draw(fastest_path, end, main_pict)

                    temp_file = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
                    temp_file_path = temp_file.name
                    cv2.imwrite(temp_file_path, show_path)

                    return temp_file_path
