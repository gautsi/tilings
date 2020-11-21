from tilings import base as b
from typing import List, Dict, Tuple
import shapely.geometry as sg
from shapely.coords import CoordinateSequence
import matplotlib.pyplot as plt
from matplotlib.axes._axes import Axes
from matplotlib.figure import Figure
from functools import reduce
from descartes import PolygonPatch


def setup_plot(extent: int) -> Tuple[Figure, Axes]:
    fig, ax = plt.subplots(figsize = (5, 5))
    ax.set_xlim(left=-extent, right=extent)
    ax.set_ylim(bottom=-extent, top=extent)
    return fig, ax

def complete(pts: List[sg.Point]) -> List[sg.Polygon]:
    # triangles
    length = pts[0].distance(pts[1])
    
    c1 = pts[0].buffer(length).boundary
    c2 = pts[1].buffer(length).boundary
    return [sg.Polygon(pts + [i]) for i in list(c1.intersection(c2))]

def draw_pts(ax: Axes, pts: List[sg.Point]) -> None:
    xs = [pt.x for pt in pts]
    ys = [pt.y for pt in pts]
    ax.scatter(xs, ys)

def draw_tiling(ax: Axes, t:List[sg.Polygon]) -> None:
    for p in t:
        ax.add_patch(PolygonPatch(p))

def nearest_edge(poly: sg.Polygon) -> List[sg.Point]:
    coords = list(poly.boundary.coords)
    min_ind = None
    min_dist = None
    for i, p in enumerate(coords):
        dist = sg.Point(p).distance(sg.Point([0, 0]))
        if min_dist is None or dist < min_dist:
            min_dist = dist
            min_ind = i
    return [sg.Point(coords[min_ind]), sg.Point(coords[(min_ind + 1) % len(coords)])]

def union(t:List[sg.Polygon]) -> sg.Polygon:
    return reduce(lambda x, y: x.union(y), t)

def add_polygon(t:List[sg.Polygon]) -> List[sg.Polygon]:
    u = union(t)
    pos_ps = complete(nearest_edge(u))
    for pos_p in pos_ps:
        if pos_p.touches(u):
            t.append(pos_p)
            return t
    return None