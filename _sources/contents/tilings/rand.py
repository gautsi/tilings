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
t = [sg.Polygon([[0, 0], [1, 0], [0.5, np.sqrt(3)/2]])]

# %%
fig, ax = plt.subplots(figsize = (5, 5))
ax.set_xlim(left=-10, right=10)
ax.set_ylim(bottom=-10, top=10)
u.draw_tiling(ax, t)

# %%
for i in range(30):
    t = u.add_polygon(t)

# %%
fig, ax = plt.subplots(figsize = (5, 5))
ax.set_xlim(left=-10, right=10)
ax.set_ylim(bottom=-10, top=10)
u.draw_tiling(ax, t)