# %% [markdown]
"""
# Utility functions
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
from descartes import PolygonPatch
import shapely.geometry as sg

# %%
if get_ipython() is not None:
    get_ipython().run_line_magic('matplotlib', 'inline')


# %%
v1 = sg.Point([0, 0])
v2 = sg.Point([0,1])

# %%
t1, t2 = u.complete([v1, v2])

# %%
fig, ax = plt.subplots(figsize=(5, 5))
ax.set_ylim(bottom=-2, top=2)
ax.set_xlim(left=-2, right=2)
ax.add_patch(PolygonPatch(t1, fc=plt.cm.Dark2.colors[0], alpha=0.5))
ax.add_patch(PolygonPatch(t2, fc=plt.cm.Dark2.colors[0], alpha=0.5))
u.draw_pts(ax, [v1, v2])