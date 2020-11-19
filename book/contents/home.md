# Tilings

I've become interested in space-filling tilings of the plane made with squares and equilateral triangles of the same side length. I wrote (fairly manual) code to draw the start of what I think is such a tiling of the plane, see [here](http://gautsi.github.io/post/2020/11/13/tiling.html). I have an idea for a process to find tilings more automatically, which I will lay out and try to implement here. I also noticed that I was making decisions about which shape to place next, and wonder about how many tilings there are.

I want to start by considering the symmetric (six-fold) tilings with a hexagon made up with six triangles in them, with squares at the top and bottom of the hexagon, like this `fill in picture here`.

## Tilings as a graph
I think it will be helpful to represent tilings as a graph, with polygons (squares and triangles) and vertices as nodes. There are relationships between polygons and their vertices, and between symmetric vertices. Such a graph would have to satisfy some conditions to represent a tiling:
- all triangle nodes are connected to exactly three vertices
- all square nodes are connected to exactly four vertices
- each vertex is connected to at most
    - four squares,
    - six triangles or
    - two squares and three triangles
- two polygons can share at most two vertices
- if a vertex is connected to a complete set of polygons (4 squares or 6 triangles or 2 squares, 3 triangles), then every connected polygon shares a vertex with exactly two other connected polygons

I think there are some other connectivity conditions that are similar to the last condition above but don't require the focus vertex to be connected to a complete set. For example, if a vertex is connected to only three squares, we want a condition that requires one of the squares to share vertices with the other two squares.

I imagine a process that starts with the 'seed' graph that represents a hexagon with two squares top and bottom and iteratively tries to add a polygon to the graph.

I call vertices that are connected to a complete set of polygons (4 squares or 6 triangles or 2 squares, 3 triangles) `internal` (in that they are 'inside' the tiling and cannot support any more polygons), otherwise `border`. The goal of the process is to make as many vertices internal as possible, in other words filling the space. 