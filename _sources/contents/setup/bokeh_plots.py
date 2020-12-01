# %% [markdown]
"""
# Plotting tilings with bokeh
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

# %%
from bokeh.layouts import column
from bokeh.models import ColumnDataSource, CustomJS, Slider
from bokeh.plotting import Figure, output_file, show

output_file("js_on_change.html")

x = [x*0.005 for x in range(0, 200)]
y = x

source = ColumnDataSource(data=dict(x=x, y=y))

plot = Figure(plot_width=400, plot_height=400)
plot.line('x', 'y', source=source, line_width=3, line_alpha=0.6)

callback = CustomJS(args=dict(source=source), code="""
    var data = source.data;
    var f = cb_obj.value
    var x = data['x']
    var y = data['y']
    for (var i = 0; i < x.length; i++) {
        y[i] = Math.pow(x[i], f)
    }
    source.change.emit();
""")

slider = Slider(start=0.1, end=4, value=1, step=.1, title="power")
slider.js_on_change('value', callback)

layout = column(slider, plot)

show(layout)

# %%
