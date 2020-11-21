from typing import List
from matplotlib.axes._axes import Axes
import shapely.geometry as sg

class Vertex(object):
    def __init__(self, polygons: List = [], xy: List[float] = None):
        self.polygons = polygons
        self.xy = xy
        self.point = sg.Point(xy)

class Polygon(object):
    def __init__(self, vertices: List[Vertex]):
        self.vertices = vertices

class Square(Polygon):
    def __init__(self, vertices: List[Vertex]):
        super().__init__(vertices=vertices)

class Triangle(Polygon):
    def __init__(self, vertices: List[Vertex]):
        super().__init__(vertices=vertices)

class Tiling(object):
    def __init__(self, vertices: List[Vertex] = [], polygons: List[Polygon] = []):
        self.vertices = vertices
        self.polygons = polygons

    def draw(self, ax:Axes)->None:
        vertex_coords = zip(*[v.xy for v in self.vertices])
        ax.scatter(*vertex_coords)