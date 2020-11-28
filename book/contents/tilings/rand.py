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
from tilings import base as b
import matplotlib.pyplot as plt
import shapely.geometry as sg
import numpy as np
from myst_nb import glue

# %%
seed_t = u.get_seed()

# %%
fig, ax = u.setup_plot(extent=2)
u.draw_tiling(ax, seed_t)
glue("seed", fig)

# %%
fig, ax = u.setup_plot(extent=5)
u.draw_tiling(ax, u.update_tilings([seed_t])[0])



# %%
ts = [seed_t]
for i in range(2):
    ts = u.update_tilings(ts)
    print(i, len(ts))
    irreg = u.get_irreg(ts)
    if irreg is not None:
        print("irreg found")
        break

# %%
ts = u.update_tilings(ts)
print(i, len(ts))


# %%
for t in ts:
    fig, ax = u.setup_plot(extent=6)
    u.draw_pts(ax, u.nearest_edge(t.u))
    u.draw_tiling(ax, t)

# %%
new_seed = ts[2]

# %%
ts2 = [new_seed]
for i in range(38):
    ts2 = u.update_tilings(ts2)
    print(i, len(ts2))
    irreg = u.get_irreg(ts2)
    if irreg is not None:
        print("irreg found")
        break


# %%
for t in ts2[:10]:
    fig, ax = u.setup_plot(extent=9)
    u.draw_pts(ax, u.nearest_edge(t.u))
    u.draw_tiling(ax, t)

# %%
for t in ts2[-10:]:
    fig, ax = u.setup_plot(extent=9)
    u.draw_pts(ax, u.nearest_edge(t.u))
    u.draw_tiling(ax, t)

# %%
glue("shapely_ex", fig)

# %%
fig, ax = u.setup_plot(extent=6)
u.draw_polygon(ax, t.u)
glue("artifact_ex", fig)

# %%
