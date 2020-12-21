# %% [markdown]
"""
# Tilings tree
"""

# %% tags=['hide-cell']
from IPython import get_ipython

if get_ipython() is not None:
    get_ipython().run_line_magic("load_ext", "autoreload")
    get_ipython().run_line_magic("autoreload", "2")

# %%
from tilings import utils as u
import networkx as nx
from bokeh.io import output_notebook, show
from bokeh.plotting import figure, from_networkx
from bokeh.models import (
    Ellipse,
    ColumnDataSource,
    CDSView,
    GroupFilter,
    Patches,
    CustomJS,
    HoverTool,
)
from bokeh.layouts import row
import matplotlib.pyplot as plt
import numpy as np

# %%
if get_ipython() is not None:
    get_ipython().run_line_magic("matplotlib", "inline")

# %%
if get_ipython() is not None:
    output_notebook()

# %%
seed = u.get_seed()

# %%
tiling_tree = nx.DiGraph()
tiling_tree.add_node(seed)

# %%
for i in range(6):
    u.update_tiling_tree(tiling_tree)

# %%
def plot_tree(tiling_tree) -> None:

    layout = nx.spring_layout(tiling_tree)
    nodes = layout.keys()
    node_cds = {"x": [], "y": [], "n": []}
    edge_cds = {"xs": [], "ys": []}
    tiling_cds = {"xs": [], "ys": [], "n": []}
    for i, n in enumerate(nodes):
        node_cds["x"].append(layout[n][0])
        node_cds["y"].append(layout[n][1])
        node_cds["n"].append(str(i))
        tiling_cds["n"].append(str(i))
        tiling_cds["xs"].append([])
        tiling_cds["ys"].append([])
        for p in n.polys:
            coords = list(p.exterior.coords)
            xs = [c[0] for c in coords]
            ys = [c[1] for c in coords]
            tiling_cds["xs"][-1].extend(xs + [np.nan])
            tiling_cds["ys"][-1].extend(ys + [np.nan])
    for e in tiling_tree.edges:
        edge_cds["xs"].append([layout[e[0]][0], layout[e[1]][0]])
        edge_cds["ys"].append([layout[e[0]][1], layout[e[1]][1]])

    node_source = ColumnDataSource(node_cds)
    tiling_source = ColumnDataSource(tiling_cds)
    edge_source = ColumnDataSource(edge_cds)
    tiling_view = CDSView(
        source=tiling_source, filters=[GroupFilter(column_name="n", group="0")]
    )
    graph_plot = figure(
        x_range=(-1.1, 1.1),
        y_range=(-1.1, 1.1),
        tools="",
        toolbar_location=None,
        plot_width=400,
        plot_height=400,
    )
    tiling_plot = figure(
        x_range=(-10, 10),
        y_range=(-10, 10),
        tools="",
        toolbar_location=None,
        plot_width=400,
        plot_height=400,
    )
    gc = graph_plot.circle(x="x", y="y", size=20, source=node_source)

    graph_plot.multi_line(
        xs="xs",
        ys="ys",
        source=edge_source,
    )

    tiling_plot.patches(
        xs="xs",
        ys="ys",
        source=tiling_source,
        view=tiling_view,
        fill_color="#fb9a99",
        fill_alpha=1,
        # line_alpha=0,
        line_width=2,
    )

    hover_cb_code = """
        let n = source.data['n'][cb_data.index.indices[0]]
        if (typeof n !== 'undefined') {
            view.filters[0].group=n;
            view.properties.filters.change.emit()
            console.log(view)
            console.log(view.filters[0].group)
        }
    """

    callback = CustomJS(
        args={"source": gc.data_source, "view": tiling_view}, code=hover_cb_code
    )
    graph_plot.add_tools(HoverTool(tooltips=None, callback=callback, renderers=[gc]))

    show(row(graph_plot, tiling_plot))