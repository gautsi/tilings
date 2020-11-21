# %% [markdown]
"""
# Drawing polygons with matplotlib
I want to draw tilings as collections of polygons to able to color/emphasize certain polygons. Here I explore using matplotlib and shapely to draw polygons.
"""

# %% tags=['hide-cell']
from IPython import get_ipython
if get_ipython() is not None:
    get_ipython().run_line_magic('load_ext', 'autoreload')
    get_ipython().run_line_magic('autoreload', '2')


# %%
import matplotlib.pyplot as plt
from tilings import base as b
from tilings import utils as u
import shapely.geometry as sg
import shapely.affinity as sa
import numpy as np
from descartes import PolygonPatch

# %%
if get_ipython() is not None:
    get_ipython().run_line_magic('matplotlib', 'inline')

# %% [markdown]
"""
## matplotlib
Testing the fill function:
"""

# %%
fig, ax = plt.subplots(figsize=(5, 5))
ax.fill([0, 1, 2, 0], [1, 1, 0, 1], c=plt.cm.Dark2.colors[0])

# %% [markdown]
"""
## shapely
I think shapely will be useful to check that polygons don't overlap.
"""

# %%
polygon1 = sg.Polygon([[0, 0], [1, 0], [0.5, np.sqrt(3)/2]])
polygon2 = sg.Polygon([[1, 0], [0.5, np.sqrt(3)/2], [1.5, np.sqrt(3)/2]])
fig, ax = plt.subplots(figsize=(5, 5))
ax.set_ylim(bottom=0, top=2)
ax.set_xlim(left=0, right=2)
ax.add_patch(PolygonPatch(polygon1, fc=plt.cm.Dark2.colors[0]))
ax.add_patch(PolygonPatch(polygon2, fc=plt.cm.Dark2.colors[1]))

# %%
polygon1.overlaps(polygon2)

# %%
polygon1.touches(polygon2)

# %% [markdown]
"""
Testing drawing a simple tiling:
"""

# %%
verts = [b.Vertex(xy=[0,0]), b.Vertex(xy=[0,1])]
t = b.Tiling(vertices=verts)


# %%
fig, ax = plt.subplots(figsize=(5, 5))
t.draw(ax)

# %% [markdown]
"""
Adding a square to an edge
"""


# %%
edge = [sg.Point([-1,1]), sg.Point([1,-1])]
fig, ax = u.setup_plot(5)
new_pts = [
    sa.rotate(edge[1], angle=-90, origin=[edge[0].x,edge[0].y]),
    sa.rotate(edge[0], angle=90, origin=[edge[1].x,edge[1].y]),
]

u.draw_pts(ax, edge + new_pts)

# %%
