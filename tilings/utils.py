from tilings import base as b
from typing import List, Dict
import shapely.geometry as sg
from matplotlib.axes._axes import Axes
from functools import reduce
from descartes import PolygonPatch

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

def add_polygon(t:List[sg.Polygon]) -> List[sg.Polygon]:
    u = reduce(lambda x, y: x.union(y), t)
    for p in t:
        coords = p.boundary.coords
        for i in range(len(coords)-1):
            pos_ps = complete([sg.Point(coords[i]), sg.Point(coords[i+1])])
            for pos_p in pos_ps:
                if pos_p.touches(u):
                    t.append(pos_p)
                    return t
    return None