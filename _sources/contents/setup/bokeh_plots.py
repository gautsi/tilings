# %% [markdown]
"""
Plotting tilings with bokeh
"""

# %% tags=['hide-cell']
from IPython import get_ipython
if get_ipython() is not None:
    get_ipython().run_line_magic('load_ext', 'autoreload')
    get_ipython().run_line_magic('autoreload', '2')

# %%
from bokeh.io import output_notebook, show
from bokeh.models import ColumnDataSource, Grid, LinearAxis, Patches, Plot
from tilings import utils as u
from tilings import base as b
import numpy as np
from myst_nb import glue

# %%
output_notebook()

# %%
seed_t = u.get_seed()

# %%
def get_cds(t:b.Tiling)-> ColumnDataSource:
    coords = [list(p.exterior.coords) for p in t.polys]
    xs = [[p[0] for p in c] for c in coords]
    ys = [[p[1] for p in c] for c in coords]
    return ColumnDataSource({"xs":xs, "ys":ys})


# %%
plot = Plot(
    title=None, plot_width=300, plot_height=300,
    min_border=0, toolbar_location=None)

glyph = Patches(xs="xs", ys="ys", fill_color="#fb9a99", fill_alpha=0.1)
plot.add_glyph(get_cds(seed_t), glyph)

show(plot)

# %%
ts = [seed_t]
for i in range(30):
    ts = u.update_tilings(ts)
    print(i, len(ts))
    irreg = u.get_irreg(ts)
    if irreg is not None:
        print("irreg found")
        break

# %%
for t in ts:
    plot.add_glyph(get_cds(t), glyph)

show(plot)