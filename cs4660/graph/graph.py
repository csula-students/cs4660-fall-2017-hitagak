# Homework 1

from io import open
from operator import itemgetter

def construct_graph_from_file(graph, file_path):
    """
    TODO: read content from file_path, then add nodes and edges to graph object
    note that graph object will be either of AdjacencyList, AdjacencyMatrix or ObjectOriented

    In example, you will need to do something similar to following:
    1. add number of nodes to graph first (first line)
    2. for each following line (from second line to last line), add them as edge to graph
    3. return the graph

    """

    # read the file by path
    f = open(file_path, encoding='utf-8')
    text = f.read()
    lines = text.split('\n')
    # number of nodes of each graph is written in the first line.
    numOfNodes = int(lines[0])
    lines = lines[1:]
   
    # add node to graph
    for i in range(0, numOfNodes):
        graph.add_node(Node(i))

    # add edge to graph
    for line in lines:
        if line != "":
            line = line.split(":")
            # Edge(fromnode,tonode,weight)
            graph.add_edge(Edge(Node(int(line[0])), Node(int(line[1])), int(line[2])))
    return graph

class Node(object):
    """Node represents basic unit of graph"""
    def __init__(self, data):
        self.data = data

    def __str__(self):
        return 'Node({})'.format(self.data)
    def __repr__(self):
        return 'Node({})'.format(self.data)

    def __eq__(self, other_node):
        return self.data == other_node.data
    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self.data)

class Edge(object):
    """Edge represents basic unit of graph connecting between two edges"""
    def __init__(self, from_node, to_node, weight):
        self.from_node = from_node
        self.to_node = to_node
        self.weight = weight
    def __str__(self):
        return 'Edge(from {}, to {}, weight {})'.format(self.from_node, self.to_node, self.weight)
    def __repr__(self):
        return 'Edge(from {}, to {}, weight {})'.format(self.from_node, self.to_node, self.weight)

    def __eq__(self, other_node):
        return self.from_node == other_node.from_node and self.to_node == other_node.to_node and self.weight == other_node.weight
    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash((self.from_node, self.to_node, self.weight))


class AdjacencyList(object):
    """
    AdjacencyList is one of the graph representation which uses adjacency list to
    store nodes and edges
    """
    def __init__(self):
        # adjacencyList should be a dictonary of node to edges
        self.adjacency_list = {}

    # return True/False if node1 and node 2 are directly connected or not
    def adjacent(self, node_1, node_2):
        neighbors = self.neighbors(node_1)
        for n in neighbors:
            if n == node_2:
                return True
        return False
    
    # return all nodes which is adjacent from node
    def neighbors(self, node):
        list = []
        for edge in self.adjacency_list[node]:
            list.append(edge.to_node)     
        return list

    # return True if node does "NOT" exists otherwise return false
    def add_node(self, node):
        # node exists
        if node in self.adjacency_list:
            return False
        # node not exists
        self.adjacency_list[node] = []
        return True
        
    # return true of node is removed otherwise return false
    def remove_node(self, node):
        if node not in self.adjacency_list:
            return False
        self.adjacency_list[node] = []

        #remove edge which connected to node
        for edges in self.adjacency_list.values():
            for edge in edges:
                if edge.to_node == node:
                    self.remove_edge(edge)
        return True

    # add edge and return true otherwise, return false
    def add_edge(self, edge):
        if edge.from_node in self.adjacency_list and edge not in self.adjacency_list[edge.from_node]:
            self.adjacency_list[edge.from_node].append(edge)
            return True
        return False

    # remove edge and return true, otherwise, return false
    def remove_edge(self, edge):
        adjacent_edges = self.adjacency_list[edge.from_node]
        if edge not in adjacent_edges:
            return False
        adjacent_edges.remove(edge)
        return True

class AdjacencyMatrix(object):
    def __init__(self):
        # adjacency_matrix should be a two dimensions array of numbers that
        # represents how one node connects to another
        self.adjacency_matrix = []
        # in additional to the matrix, you will also need to store a list of Nodes
        # as separate list of nodes
        self.nodes = []

    # return true if node_1 and node_2 is connected
    def adjacent(self, node_1, node_2):
        node_1_index =  self.__get_node_index(node_1)
        node_2_index =  self.__get_node_index(node_2)
        if self.adjacency_matrix[node_1_index][node_2_index] == None or node_1 not in self.nodes or node_2 not in self.nodes:
            return False
        return True
    
    # return all nodes which adjacent from node
    def neighbors(self, node):
        nodelist = []
        x = 0
        if node not in self.nodes:
            return nodelist   
        
        node_index =  self.__get_node_index(node) 
        for n in self.adjacency_matrix[node_index]:
            if n != None:
                nodelist.append(Node(x))
            x += 1
        return nodelist
    
    # return true if node is added, otherwise, return false
    def add_node(self, node):
        if node in self.nodes:
            return False
        self.nodes.append(node)
        for i in self.adjacency_matrix:
            i.append(None)
        self.adjacency_matrix.append([None] * len(self.nodes))
        return True
        
        
    # return true if node is added, otherwise, return false.
    def remove_node(self, node):

        if node not in self.nodes:
            return False
        
        for n in self.adjacency_matrix:
            del n[self.__get_node_index(node)]
        self.nodes.remove(node)

        return True
        

    # return true if edge is added, otherwise, return false
    def add_edge(self, edge):

        fromnode_index = self.__get_node_index(edge.from_node)
        tonode_index = self.__get_node_index(edge.to_node)
        
        if self.adjacency_matrix[fromnode_index][tonode_index] is None:
            self.adjacency_matrix[fromnode_index][tonode_index] = edge.weight
            return True
        return False
    
    # return true if edge is removed, otherwise, return false
    def remove_edge(self, edge):
        tonode = edge.to_node
        fromnode = edge.from_node

        fromnode_index = self.__get_node_index(fromnode)
        tonode_index = self.__get_node_index(tonode)

        if self.adjacency_matrix[fromnode_index][tonode_index] is None:
            return False
        self.adjacency_matrix[fromnode_index][tonode_index] = None
        return True

    def __get_node_index(self, node):
        """helper method to find node index"""
        return self.nodes.index(node)


class ObjectOriented(object):
    """ObjectOriented defines the edges and nodes as both list"""
    def __init__(self):
        # implement your own list of edges and nodes
        self.edges = []
        self.nodes = []

    # return true if node_1 and node_2 is directly connected
    def adjacent(self, node_1, node_2):
        for edge in self.edges:
            if edge.from_node == node_1 and edge.to_node == node_2:
                return True
        return False
    
    # return all nodes which is adjacent from node
    def neighbors(self, node):
        nodelist = []
        if node in self.nodes:
            for edge in self.edges:
                if edge.from_node == node:
                    nodelist.append(edge.to_node)
        return nodelist

    # adds new node to data structure
    def add_node(self, node):
        if node in self.nodes:
            return False
        self.nodes.append(node)
        return True

    # remove node from data structure
    def remove_node(self, node):
        if node not in self.nodes:
            return False
        self.nodes.remove(node)

        #remove edges which connected to removed node
        for edge in self.edges:
            if edge.from_node == node or edge.to_node == node:
                self.remove_edge(edge)
        return True

    # add new edge to data structure
    def add_edge(self, edge):
        if edge in self.edges:
            return False
        self.edges.append(edge)
        return True

    # remove edge from data structure
    def remove_edge(self, edge):
        if edge not in self.edges:    
            return False
        self.edges.remove(edge)
        return True 



