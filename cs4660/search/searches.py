# Homework 2

import math
try:
    import Queue as Q 
except ImportError:
    import queue as Q
from graph import graph as g

def bfs(graph, initial_node, dest_node):
  
    q = Q.Queue()
    q.put(initial_node)
    visited = {}
    visited[initial_node] = None
    path = []
    

    while not q.empty():
        node = q.get()           

        for child in graph.neighbors(node):
            if child not in visited:
                q.put(child)
                visited[child] = node

    current_node = dest_node
    while current_node != initial_node:
        parent = visited[current_node]
        path.append(g.Edge(parent,current_node,graph.distance(parent,current_node)))
        current_node = parent
    
    path.reverse()

    return path



def dfs(graph, initial_node, dest_node):

    q = [] 
    q.append(initial_node)
    visited = {}
    visited[initial_node] = None
    path = []
    

    while q: 
        node = q[-1] 

        not_visit = [child for child in graph.neighbors(node) if child not in visited]
        if not_visit:
            child = not_visit[0]
            q.append(child) 
            visited[child] = node

        else:
            q.pop()
    
    current_node = dest_node
    while current_node != initial_node:
        parent = visited[current_node]
        path.append(g.Edge(parent, current_node, graph.distance(parent, current_node)))
        current_node = parent
    path.reverse()

    return path

    

def dijkstra_search(graph, initial_node, dest_node):

    q = Q.PriorityQueue()
    key = 1 
    q.put((0, key, initial_node)) 
    visited = {}
    visited[initial_node] = None
    cost = {}
    cost[initial_node] = 0
    path = []
    

    while q:
        node = q.get()[2]

        if node == dest_node:
            break

        for child in graph.neighbors(node):
            new_cost = cost[node] + graph.distance(node, child)
            if child not in cost or new_cost < cost[child]:
                cost[child] = new_cost
                priority = new_cost
                key += 1
                q.put((priority, key, child))
                visited[child] = node
                   
    current_node = dest_node
    while current_node != initial_node:
        parent = visited[current_node]
        path.append(g.Edge(parent, current_node, graph.distance(parent, current_node)))
        current_node = parent
    path.reverse()

    return path 



def a_star_search(graph, initial_node, dest_node):

    q = Q.PriorityQueue()
    key = 1 
    q.put((0, key, initial_node)) 
    visited = {}
    visited[initial_node] = None
    cost = {}
    
    cost[initial_node] = 0
    path = []
    node = dest_node

    while not q.empty():
        node = q.get()[2]

        if node == dest_node:
            break

        for child in graph.neighbors(node):
            new_cost = cost[node] + graph.distance(node, child)
            if child not in cost or new_cost < cost[child]:
                cost[child] = new_cost
                priority = new_cost + heuristic(dest_node, child)
                key += 1
                q.put((priority, key, child))
                visited[child] = node
                

    while node != initial_node:
        parent = visited[node]
        path.append(g.Edge(parent, node, graph.distance(parent, node)))
        node = parent
    path.reverse()

    return path 
   


def heuristic(dest_node, node):

    x = abs(dest_node.data.x - node.data.x)
    y = abs(dest_node.data.y - node.data.y)
   
    return (x + y)
 