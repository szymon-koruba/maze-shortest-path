from photo_form import form_functions as ff
from photo_form import outer_contour as oc
from finding_path import Finding_start_and_end as fsae
from finding_path import finding_quickest_path as fqp
from finding_path import showing_path as sp
import cv2
import matplotlib.pyplot as plt

photo_form = ff.FormattingFunction()
up, left, down, right, bin_pict, picture, main_pict = photo_form.full_form_image('k.png')

photo_form_full = oc.NewStartEndPath()
pict_af_form = photo_form_full.full_class_work(up, down, right, left, picture, bin_pict)

start_and_end_find = fsae.FindingBestWayOut()
start, end = start_and_end_find.full_start_and_end(pict_af_form)

find_path = fqp.FindQuickestPath()
graph = find_path.binary_image_to_graph(pict_af_form)
fastest_path = find_path.dijkstra(graph, start, end)

show_path = sp.path_draw(fastest_path, end, main_pict)

cv2.imshow('Obraz', show_path)
cv2.waitKey(0)
cv2.destroyAllWindows()

