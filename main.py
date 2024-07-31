from camera import camera_function as cf
from finding_path import finding_quickest_path as fqp
from finding_path import Finding_start_and_end as fse
from kontur_zew import NewStartEndPath
import cv2
from photo_form import form_functions as ff


start = fse.FindingBestWayOut()
form = ff.FormattingFunction()
u, l, d, r, bin_pict, picture = form.full_form_image('plos.jpg')


ns = NewStartEndPath()
pict = ns.full_class_work(u,d,l,r, picture, bin_pict)

sta, end = start.full_start_and_end(pict)

path = fqp.FindQuickestPath()
grap = path.binary_image_to_graph(pict)
path.dijkstra(grap, sta, end, bin_pict)








