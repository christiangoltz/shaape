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
        if has_same_direction(first_edge, last_edge):
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
