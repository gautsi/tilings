from typing import List
from matplotlib.axes._axes import Axes
import shapely.geometry as sg

class Tiling(object):
    def __init__(self, polys: List[sg.Polygon] = [], u: sg.Polygon = None):
        self.polys = polys
        self.u = u

    def check_shapes(self):
        irreg = False
        for p in self.polys:
            if len(p.boundary.coords) not in [4, 5]:
                irreg = True
        return irreg