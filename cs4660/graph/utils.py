"""
utils package is for some quick utility methods

such as parsing
"""

from io import open

# import graph
from . import graph as g

class Tile(object):
    """Node represents basic unit of graph"""
    def __init__(self, x, y, symbol):
        self.x = x
        self.y = y
        self.symbol = symbol

    def __str__(self):
        return 'Tile(x: {}, y: {}, symbol: {})'.format(self.x, self.y, self.symbol)
    def __repr__(self):
        return 'Tile(x: {}, y: {}, symbol: {})'.format(self.x, self.y, self.symbol)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.x == other.x and self.y == other.y and self.symbol == other.symbol
        return False
    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(str(self.x) + "," + str(self.y) + self.symbol)



def parse_grid_file(graph, file_path):
    """
    ParseGridFile parses the grid file implementation from the file path line
    by line and construct the nodes & edges to be added to graph

    Returns graph object
    """

    # TODO: read the filepaht line by line to construct nodes & edges
    # TODO: for each node/edge above, add it to graph

    rows = []

    f = open(file_path, encoding='utf-8')
    text = f.read()
    lines = text.split('\n')
    for line in lines:
        if line:
            rows.append([line[i:i+2] for i in range(1, len(line[1:-1]), 2)])
    rows = rows[1:-1]        
    

    tiles = {}

    for y in range(len(rows)):
        for x in range (len(rows[0])):
            tile = Tile(x, y, rows[y][x])
            graph.add_node(g.Node(tile))
            tiles[(x, y)] = tile

    for y in range(len(rows)):
        for x in range (len(rows[0])):
            curr_tile = Tile(x, y, rows[y][x])

            if curr_tile.symbol == "##":
                continue 

            ## add top edge
            if (x, y - 1) in tiles:
                top_tile = tiles[(x, y - 1)]
                if top_tile.symbol != "##":
                    graph.add_edge(g.Edge(g.Node(curr_tile), g.Node(top_tile), 1))   

            # add right edge
            if (x + 1, y) in tiles:
                right_tile = tiles[(x + 1, y)]
                if right_tile.symbol != "##":
                    graph.add_edge(g.Edge(g.Node(curr_tile), g.Node(right_tile), 1))

            # add bottom edge
            if (x, y + 1) in tiles:
                bottom_tile = tiles[(x, y + 1)]
                if bottom_tile.symbol != "##":
                    graph.add_edge(g.Edge(g.Node(curr_tile), g.Node(bottom_tile), 1))

            # add left edge
            if (x - 1, y) in tiles:
                left_tile = tiles[(x - 1, y)]
                if left_tile.symbol != "##":
                    graph.add_edge(g.Edge(g.Node(curr_tile), g.Node(left_tile), 1))


    return graph

def convert_edge_to_grid_actions(edges):
    """
    Convert a list of edges to a string of actions in the grid base tile

    e.g. Edge(Node(Tile(1, 2), Tile(2, 2), 1)) => "S"
    """

    actions = ""
    for edge in edges:

        if (edge.to_node.data.x - edge.from_node.data.x) > 0 :
            actions += "E"
        elif (edge.to_node.data.x - edge.from_node.data.x) < 0 :
            actions += "W"
        elif (edge.to_node.data.y - edge.from_node.data.y) > 0 :
            actions += "S"
        else:
            actions += "N"    
    return actions