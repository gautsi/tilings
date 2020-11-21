# %% [markdown]
"""
# Random tilings
"""

# %% tags=['hide-cell']
from IPython import get_ipython
if get_ipython() is not None:
    get_ipython().run_line_magic('load_ext', 'autoreload')
    get_ipython().run_line_magic('autoreload', '2')

# %%
if get_ipython() is not None:
    get_ipython().run_line_magic('matplotlib', 'inline')


# %%
from tilings import utils as u
import matplotlib.pyplot as plt
import shapely.geometry as sg
import numpy as np

# %%
t = [sg.Polygon([[0, 0], [1, 0], [1, 1], [0, 1]]), sg.Polygon([[1, 0], [1, 1], [1 + np.sqrt(3)/2, 0.5]])]

# %%
fig, ax = u.setup_plot(extent=5)
u.draw_tiling(ax, t)

# %%
fig, ax = u.setup_plot(extent=5)
u.draw_pts(ax, u.nearest_edge(u.union(t)))
t = u.add_polygon(t)
u.draw_tiling(ax, t)


# %%
u.draw_tiling(ax, t)

# %%
u.add_polygon(t)

# %%
type(t[0].union(t[1]))

# %%


# %%
type(fig)

# %%

# %%
