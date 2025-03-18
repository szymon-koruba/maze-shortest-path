from photo_form import outer_contour as oc, form_functions as ff
from finding_path import showing_path as sp, finding_quickest_path as fqp, Finding_start_and_end as fsae
import tempfile
import cv2
from pathlib import Path
from GUI.resource_graphics import resource_path as rp
import os
import networkx


class CreatePath:
    def __init__(self):
        pass

    def load_photo(self):
        folder = Path('screens')
        if folder.exists() and folder.is_dir():
            for file in folder.iterdir():
                if file.is_file():
                    return file
        return None

    def del_pictures_from_folder(self):
        folder = Path('screens')
        if folder.exists() and folder.is_dir():
            for file in folder.iterdir():
                if file.is_file():
                    file.unlink()

    def full_path_load_pict(self):
        file_path = self.load_photo()
        if file_path is None:
            return rp('assets/Error_no_photo.png')
        else:
            photo_form = ff.FormattingFunction()
            up, left, down, right, bin_pict, picture, main_pict = photo_form.full_form_image(file_path)

            self.del_pictures_from_folder()

            photo_form_full = oc.NewStartEndPath()
            try:
                pict_af_form = photo_form_full.full_class_work(up, down, right, left, picture, bin_pict)
            except IndexError:
                return rp('assets/Error_during_program.png')
            else:

                start_and_end_find = fsae.FindingBestWayOut()
                start, end = start_and_end_find.full_start_and_end(pict_af_form)
                if start is None and end is None:
                    return rp('assets/Error_during_program.png')
                else:
                    find_path = fqp.FindQuickestPath()
                    graph = find_path.binary_image_to_graph(pict_af_form)

                    try:
                        fastest_path = find_path.a_star(graph, start, end)
                    except networkx.exception.NetworkXError:
                        return rp('assets/Error_during_program.png')
                    else:

                        show_path = sp.path_draw(fastest_path, end, main_pict)

                        temp_file = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
                        temp_file_path = temp_file.name
                        cv2.imwrite(temp_file_path, show_path)

                        self.del_pictures_from_folder()

                        return temp_file_path

