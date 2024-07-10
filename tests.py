from photo_form import form_functions as ff
from finding_path import finding_quickest_path as fqp
from finding_path import Finding_start_and_end as Fse
import cv2


Format = ff.FormattingFunction()
image = Format.full_form_image('s.jpg')
cv2.imshow('Docianny Obraz',image)
cv2.waitKey(0)
cv2.destroyAllWindows()

Path = fqp.FindQuickestPath()
graph = Path.binary_image_to_graph(image)

Start = Fse.FindingBestWayOut()
start, end = Start.full_start_and_end(image)

Path.dijkstra(graph, start, end, image)
