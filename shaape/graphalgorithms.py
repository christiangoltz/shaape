import networkx as nx
import math
import vector

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

def right_angle(v1, v2):
    x = vector.Vector(v1[0], v1[1])
    y = vector.Vector(v2[0], v2[1])
    dot = vector.dot(x, y)
    _angle = math.acos(dot / x.length() / y.length())
    if x[0] * y[1] < y[0] * x[1]:
        _angle = 2 * math.pi - _angle
    return _angle

def angle(v1, v2):
    x = vector.Vector(v1[0], v1[1])
    y = vector.Vector(v2[0], v2[1])
    dot = vector.dot(x, y)
    _angle = math.acos(dot / x.length() / y.length()) / math.pi * 180
    return _angle

def is_ccw(_cycle):
    ccw_sum = 0
    for i in range(0, len(_cycle)):
        x2,y2 = _cycle[i]
        x1,y1 = _cycle[i - 1]
        ccw_sum += (x2 - x1) * (y2 + y1)
    return ccw_sum < 0

def is_chord_free(_graph, _cycle):
    cycle_is_ccw = is_ccw(_cycle)
    for i in range(1, len(_cycle) - 2):
        angle_to_next_node = right_angle(_cycle[i - 1] - _cycle[i], _cycle[i + 1] - _cycle[i]) 
        neighbors = _graph.neighbors(_cycle[i])
        for n in neighbors:
            if n != _cycle[i + 1] and n != _cycle[i - 1]:
                angle_to_neighbor = right_angle(_cycle[i - 1] - _cycle[i], n - _cycle[i]) 
                if angle_to_neighbor > angle_to_next_node and cycle_is_ccw == True:
                    return False
                if angle_to_neighbor < angle_to_next_node and cycle_is_ccw == False:
                    return False
    return True

def planar_cycles(undirected_graph):
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
            rightmost_nb = min(neighbors, key=lambda x: right_angle(last_dir, x - _path[-1]))
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
                path = path[:start]    
            else:
                path.append(node)
                if len(path) > 1:
                    graph.remove_edge(path[-2], path[-1])
        else:
            path.pop()
            
    circle_graph = nx.Graph()
    chord_free_cycles = []
    for c in cycles:
        circle_graph.add_cycle(c)
    for c in cycles:
         if is_chord_free(circle_graph, c):
            chord_free_cycles.append(c + [c[0]])
    return chord_free_cycles

  
def ccw(a, b, c):
    return (c[1] - a[1]) * (b[0] - a[0]) > (b[1] - a[1]) * (c[0] - a[0])

def line_segments_intersect(seg1, seg2):
    return ccw(seg1[0], seg2[0], seg2[1]) != ccw(seg1[1], seg2[0], seg2[1]) and ccw(seg1[0], seg1[1], seg2[0]) != ccw(seg1[0], seg1[1], seg2[1])

def point_point_distance(p1, p2):
    p1 = vector.Vector(p1)
    p2 = vector.Vector(p2)
    if p1 == p2:
        return 0
    else:
       return (p2 - p1).length()

def line_segment_point_distance(point, seg):
    seg_start = vector.Vector(seg[0][0], seg[0][1])
    seg_end = vector.Vector(seg[1][0], seg[1][1])
    x, y = point
    point = vector.Vector(x, y)

    seg_dir = seg_end - seg_start
    seg_length = seg_dir.length()**2
    if seg_length == 0:
      return (point - seg_start).length()

    t = vector.dot(point - seg_start, seg_dir) / seg_length
    if t < 0:
      return (point - seg_start).length()
    elif t > 1:
      return (point - seg_end).length()

    projection = seg_start + t * seg_dir
    return (point - projection).length()

def line_segments_distance(seg1, seg2):
    if line_segments_intersect(seg1, seg2):
        return 0
    else:
        distances = []
        distances.append(line_segment_point_distance(seg1[0], seg2))
        distances.append(line_segment_point_distance(seg1[1], seg2))
        distances.append(line_segment_point_distance(seg2[0], seg1))
        distances.append(line_segment_point_distance(seg2[1], seg1))
        return min(distances)
