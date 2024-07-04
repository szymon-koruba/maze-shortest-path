from photo_form import form_functions as ff
from finding_path import finding_quickest_path as fqp
from finding_path import Finding_start_and_end as Fse
import cv2


# Krok 1: Formatuj obraz
Format = ff.FormattingFunction()
image = Format.full_form_image('sw.jpg')

# Krok 2: Utwórz graf z binarnego obrazu
Path = fqp.FindQuickestPath()
graph = Path.binary_image_to_graph(image)

# Krok 3: Znajdź punkty startowy i końcowy na obrazie
Start = Fse.FindingBestWayOut()
start, end = Start.full_start_and_end(image)

# Krok 4: Uruchom algorytm Dijkstry, aby znaleźć najkrótszą ścieżkę
Path.dijkstra(graph, start, end, image)