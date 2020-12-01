# Tilings

I've become interested in space-filling tilings of the plane made with squares and equilateral triangles of the same side length. I wrote (fairly manual) code to draw the start of what I think is such a tiling of the plane, see [here](http://gautsi.github.io/post/2020/11/13/tiling.html). I have an idea for a process to find tilings more automatically, which I will lay out and try to implement here. I also noticed that I was making decisions about which shape to place next, and wonder about how many tilings there are.

I want to start by considering the tilings with a hexagon made up with six triangles in them, with squares at the top and bottom of the hexagon, like this:

```{glue:} seed
```

## Methods
### shapely
My first attempt uses [shapely](https://shapely.readthedocs.io/en/latest/), an impressively featured geometry library, for finding tilings. Tiles are Polygon objects, tilings are lists of Polygons and the code makes extensive use of shapely functions for deciding where and how to place new tiles. Here is an example tiling that came from this process:
```{glue:} shapely_ex
``` 

Unfortunately, as a tiling's size grows, shapely's floating point calculations start to introduce artifacts to the tiling like tiny spaces between tiles. I've found these artfacts difficult to correct for, and uncorrected they make it hard to build a clean process for adding tiles. See for example the shapely calculated union of the tiles in the example tiling above:  
```{glue:} artifact_ex
``` 
Notice the lines into the polygon that represent the tiny spaces between tiles, and my code picks up on them as possible places to add tiles and fails.

But going through this experiment has made me realize that there are many more tilings with squares and triangles than I thought!

## Tilings as a graph
I think it will be helpful to represent tilings as a graph. 

## Simpler version
The nodes in the graph are the tiles of the tiling, and relationships between tiles that share an edge. For such a graph to represent a tiling, it would have to satisfy some conditions:
- all triangle tiles are connected to exactly three other tiles
- all square tiles are connected to exactly four other tiles

### More complicated version
A more complicated idea has polygons and vertices as nodes. There are relationships between polygons and their vertices (and may include in the future relationships between symmetric vertices). Such a graph would have to satisfy some conditions to represent a tiling:
- all triangle nodes are connected to exactly three vertices
- all square nodes are connected to exactly four vertices
- each vertex is connected to at most
    - four squares,
    - six triangles or
    - two squares and three triangles
- two polygons can share at most two vertices
- if a vertex is connected to a complete set of polygons (4 squares or 6 triangles or 2 squares, 3 triangles), then every connected polygon shares a vertex with exactly two other connected polygons

I think there are some other connectivity conditions that are similar to the last condition above but don't require the focus vertex to be connected to a complete set. For example, if a vertex is connected to only three squares, we want a condition that requires one of the squares to share vertices with the other two squares.

I imagine a process that starts with the 'seed' graph that represents a hexagon with two squares top and bottom and iteratively tries to add a polygon to the graph while preserving the above conditions. We can specify that the new polygon should connect to an existing polygon at two vertices (and possibly a second or third polygon as well). So each iteration, find a pair of vertices that can support another polygon.

If the chosen vertices can support both a square and triangle, continue with both versions in the next iterations. If no pair of vertices can support any new polygon, retire the version. In this way the process finds all of the possible tilings.

Preserving the symmetry means adding a symmetric polygon to the vertices symmetric to the chosen vertices each iteration.

I call vertices that are connected to a complete set of polygons (4 squares or 6 triangles or 2 squares, 3 triangles) `internal` (in that they are 'inside' the tiling and cannot support any more polygons), otherwise `border`. The goal of the process is to make as many vertices internal as possible, in other words filling the space. 