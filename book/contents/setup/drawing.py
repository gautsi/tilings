# %% [markdown]
"""
# Drawing polygons with matplotlib
I want to draw tilings as collections of polygons to able to color/emphasize certain polygons. Here I explore using matplotlib to draw polygons.
"""

# %% tags=['hide-cell']
from IPython import get_ipython
if get_ipython() is not None:
    get_ipython().run_line_magic('load_ext', 'autoreload')
    get_ipython().run_line_magic('autoreload', '2')


# %%
import matplotlib.pyplot as plt
from tilings import base as b

# %%
if get_ipython() is not None:
    get_ipython().run_line_magic('matplotlib', 'inline')

# %% [markdown]
"""
Testing the fill function:
"""

# %%
fig, ax = plt.subplots(figsize=(5, 5))
ax.fill([0, 1, 2, 0], [1, 1, 0, 1], c=plt.cm.Dark2.colors[0])

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

# %%
