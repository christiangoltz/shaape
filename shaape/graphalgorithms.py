import networkx as nx
import numpy as np
import math

def reduce_path(nodes):
    new_nodes = []
    new_nodes = nodes[0:2]
    for i in range(2, len(nodes)):
        previous_edge = nodes[i - 1] - nodes[i - 2]
        current_edge = nodes[i] - nodes[i - 1]
        if new_nodes[-1].fusable() == True and has_same_direction(previous_edge, current_edge):
            new_nodes[-1] = nodes[i]
        else:
            new_nodes.append(nodes[i])
    if len(new_nodes) > 2 and new_nodes[0] == new_nodes[-1]:
        first_edge = new_nodes[1] - new_nodes[0]
        last_edge = new_nodes[-1] - new_nodes[-2]
        if new_nodes[-1].fusable() == True and has_same_direction(first_edge, last_edge):
            del new_nodes[-1]
            new_nodes[0] = new_nodes[-1]
    return new_nodes

def has_same_direction(v1, v2):
    if (v1[0] == 0 and v1[1] == 0) or (v2[0] == 0 and v2[1] == 0):
        return False
    if v2[0] == 0 and v1[0] == 0:
        return True
    elif v2[0] == 0:
        return False
    if v2[1] == 0 and v1[1] == 0:
        return True
    elif v2[1] == 0:
        return False

    diff_x = float(v1[0]) / v2[0]
    diff_y = float(v1[1]) / v2[1]

    if diff_x == diff_y or ((-1 * diff_x) == (-1 * diff_y)):
        return True
    else:
        return False

def planar_cycles(undirected_graph):
    def angle(v1, v2):
        x = np.array([v1[0], v1[1]])
        y = np.array([v2[0], v2[1]])
        cross = np.cross(x, y)
        dot = np.dot(x, y)
        x_length = np.sqrt((x * x).sum())
        y_length = np.sqrt((y * y).sum())
        angle = np.arccos(dot / x_length / y_length)
        return angle

    def next_neighbor(_path):
        if len(_path) == 0:
            return graph.edges()[0][0]
        neighbors = graph.neighbors(_path[-1])    
        if len(neighbors) == 0:
            return None
        else:
            if len(_path) == 1:
                return neighbors[0]
            else:
                if _path[-2] in neighbors:
                    neighbors.remove(_path[-2])
                if len(neighbors) == 0:
                    return None
                last_dir = _path[-2] - _path[-1]
            rightmost_nb = min(neighbors, key=lambda x: angle(last_dir, x - _path[-1]))
            return rightmost_nb 

    def contains_cycle(_cycles, _cycle):
        for c in _cycles:
            not_equal = False
            if len(c) == len(_cycle):
                if _cycle[0] in c:
                    start = c.index(_cycle[0])
                    for i in range(0, len(c)):
                        if c[start - i] != _cycle[i]:
                            not_equal = True
                    if not_equal == False:
                        return True
        return False
                    
        
    cycles = []
    path = []
    graph = undirected_graph.to_directed()
    while graph.edges():
        node = next_neighbor(path)
        if node:
            if node in path:
                start = path[::-1].index(node)
                start = len(path) - 1 - start
                cycle = path[start:]
                if not contains_cycle(cycles, cycle):
                    cycles.append(cycle)
                graph.remove_edge(path[-1], node)
            else:
                path.append(node)
                if len(path) > 1:
                    graph.remove_edge(path[-2], path[-1])
        else:
            path.pop()
    for c in cycles:
        c.append(c[0]) 
    return cycles
