from tilings import base as b
from typing import List, Dict, Tuple, Optional
import shapely.geometry as sg
import shapely.affinity as sa
from shapely.ops import snap
from shapely.coords import CoordinateSequence
import matplotlib.pyplot as plt
from matplotlib.axes._axes import Axes
from matplotlib.figure import Figure
from functools import reduce
from descartes import PolygonPatch
import logging

eps = 0.01


def setup_plot(extent: int) -> Tuple[Figure, Axes]:
    fig, ax = plt.subplots(figsize=(5, 5))
    ax.set_xlim(left=-extent, right=extent)
    ax.set_ylim(bottom=-extent, top=extent)
    return fig, ax


def complete(pts: List[sg.Point]) -> List[List[sg.Point]]:
    # triangles
    length = pts[0].distance(pts[1])

    c1 = pts[0].buffer(length).boundary
    c2 = pts[1].buffer(length).boundary
    triangles = [pts + [i] for i in list(c1.intersection(c2))]

    # squares
    squares = [
        pts
        + [
            sa.rotate(
                pts[j],
                angle=i * (2 * j - 1) * 90,
                origin=[pts[1 - j].x, pts[1 - j].y],
            )
            for j in [0, 1]
        ]
        for i in [1, -1]
    ]

    return triangles + squares


def draw_pts(ax: Axes, pts: List[sg.Point]) -> None:
    xs = [pt.x for pt in pts]
    ys = [pt.y for pt in pts]
    ax.scatter(xs, ys)


def draw_polygon(ax: Axes, poly: sg.Polygon, c: Tuple = plt.cm.Dark2.colors[0]) -> None:
    ax.add_patch(PolygonPatch(poly, fc=c))


def draw_tiling(ax: Axes, t: b.Tiling) -> None:
    for p in t.polys:
        c = plt.cm.Dark2.colors[len(p.boundary.coords) - 4]
        draw_polygon(ax, p, c=c)


def nearest_edge(poly: sg.Polygon) -> List[sg.Point]:
    coords = list(poly.exterior.coords)
    min_ind = None
    min_dist = None
    for i, p in enumerate(coords):
        dist = sg.Point(p).distance(sg.Point([0, 0]))
        if min_dist is None or dist < min_dist:
            min_dist = dist
            min_ind = i
    return [sg.Point(coords[min_ind]), sg.Point(coords[(min_ind + 1) % len(coords)])]


def union(t: List[sg.Polygon]) -> sg.Polygon:
    return reduce(lambda x, y: x.union(y), t)


def snap_pts(pts: List[sg.Point], u: sg.Polygon) -> List[sg.Point]:
    return [snap(pt, u, 0.01) for pt in pts]


def small_buffer(p: sg.Polygon) -> sg.Polygon:
    return p.buffer(eps, 1, sg.JOIN_STYLE.mitre).buffer(-eps, 1, sg.JOIN_STYLE.mitre)


def add_polygon(t: b.Tiling) -> List[b.Tiling]:
    pos_ps = complete(nearest_edge(t.u))
    new_t = []
    for pos_p in pos_ps:
        snap_p = snap_pts(pos_p, t.u)
        snap_poly = sg.Polygon(snap_p)
        if snap_poly.intersection(t.u).area < 0.01:
            repeat_p, new_union = repeat(snap_p, t.u)
            new_polys = t.polys + [sg.Polygon(pts) for pts in repeat_p]
            new_t.append(b.Tiling(polys=new_polys, u=new_union))
    return new_t


def repeat(
    pts: List[sg.Point], u: sg.Polygon = None
) -> Tuple[List[List[sg.Point]], sg.Polygon]:
    poly_pts = [pts]
    if u is None:
        u = sg.Polygon(pts)
    else:
        u = u.union(sg.Polygon(pts))
    for i in range(5):
        new_pts = snap_pts(
            [sa.rotate(pt, (i + 1) * 60, origin=[0, 0]) for pt in pts], u
        )
        poly_pts.append(new_pts)
        u = u.union(sg.Polygon(new_pts))
    return poly_pts, u


def get_irreg(ts: List[b.Tiling]) -> Optional[b.Tiling]:
    for t in ts:
        if t.check_shapes():
            return t
    return None


def update_tilings(ts: List[b.Tiling]) -> List[b.Tiling]:
    logging.info(f"updating tilings: currently {len(ts)} tilings")
    new_ts = [ti for t in ts for ti in add_polygon(t)]
    logging.info(f"now {len(new_ts)} tilings")
    return new_ts
