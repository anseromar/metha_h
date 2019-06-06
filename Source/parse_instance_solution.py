############ Import  ################
import sys
from itertools import tee
import validator as val
import lower_bound as lbound
import upper_bound as ubound
import local_search as ls

############ Global ################


node_list = []
arc_list = []
escapes_routes = []
tpaths = []
starting_nodes_sol = []


#####################################
############ Classes ################
class Node:

    def __init__(self, nodeid, population, startingnode, safenode):
        self.nid = nodeid
        self.pop = population
        self.sfnode = safenode
        self.stgnode = startingnode

    def __str__(self):
        return "Node id " + str(self.nid) + " => { population : " + str(self.pop) + " ; is a safe node : " + str(
            self.sfnode) + " ; is a starting node : " + str(self.stgnode) + " }"

    def __repr__(self):
        pass


class Arc:

    def __init__(self, arcid, duedate, length, capacity, node1, node2):
        self.arid = arcid
        self.ddate = duedate
        self.len = length
        self.cap = capacity
        self.n1 = node1
        self.n2 = node2

    def __str__(self):
        return "Arc id " + str(self.arid) + " => { due date : " + str(self.ddate) + " ; length : " + str(
            self.len) + " ; capacity : " + str(self.cap) + " ; node_1 : " + str(self.n1) + " ; node_2 : " + str(
            self.n2) + " } "

    def __reps__(self):
        pass


class Graph:
    pass


############ Functions #############

def pairwise(iterable):
    """s -> (s0,s1), (s1,s2), (s2, s3), ..."""
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)


# Allows to parse the file containing the data of a evacuation situation
def parse_data_file(fi):
    with open(fi) as f:
        nstarting_node, safe_node = [int(x) for x in next(f).split()]
        lines = [x.rstrip('\n') for x in f.readlines()]

    evacuation_info = lines[0:nstarting_node]
    num_nodes, num_edges = map(int, lines[nstarting_node + 1].split(" "))
    graph = [x for x in lines[nstarting_node + 2:] if x]

    return nstarting_node, safe_node, num_nodes, num_edges, evacuation_info, graph


# Allows to arrange into a list of map the first part of the data file "evacuation_info"
# @return : a list of map representing each line
def arrange_evacuation_info(evacinfo):
    content = []
    for evac in evacinfo:
        e = evac.split(' ')
        info = {

            'population': int(e[1]),
            'max rate': int(e[2]),
            'k': int(e[3]),
            'escape route': [e[0]] + e[4:]
        }
        content.append((e[0], info))

    return dict(content)


# Allows to arrange into a list of map the second part of the data file "graph"
# @return : a list of map representing each line
def arrange_graph(grh):
    content = []
    for gr in grh:
        g = gr.split(' ')
        info = {
            'node_1': g[0],
            'node_2': g[1],
            'duedate': int(g[2]),
            'length': int(g[3]),
            'capacity': int(g[4])
        }
        content.append(info)

    return content


# Allows to parse the file containing the solution data of a evacuation situation
def parse_sol_file(fi):
    print(fi)
    with open(fi) as f:
        resolved_instance = [x for x in next(f).split()][0]
        nnode_evacuate = [int(x) for x in next(f).split()][0]
        lines = [x.rstrip('\n') for x in f.readlines()]

    nodes_evacuate = lines[0:nnode_evacuate]

    # To do : still the lines to split
    return (resolved_instance, nnode_evacuate, nodes_evacuate)


# Allows to arrange into a list of map the second part of the data file "graph"
# @return
def arrange_nodes_evacuation(nodesevac):
    content = []
    for nodevac in nodesevac:
        noev = nodevac.split(' ')
        info = {
            'node_id': noev[0],
            'max_rate': int(noev[1]),
            'starting_date_evacuation': int(noev[2])
        }
        content.append(info)
    return content


# instance only node in escape route
def extract_node_content_evac_info(content_evac_info, safe_node):
    node_list = []
    for nid, evac_info in content_evac_info.items():
        node_list.append(Node(nid, evac_info['population'], True, False))
        for node_esc_rout in evac_info['escape route']:
            if not any(int(node.nid) == int(node_esc_rout) for node in node_list):
                node_list.append(Node(node_esc_rout, 0, False, True if int(node_esc_rout) == int(safe_node) else False))
    return node_list


#
def extract_arc_content_graph(content_graph):
    arc_list = []
    for arcid, con_grp in enumerate(content_graph):
        if con_grp['length'] > 100:
            continue
        else:
            arc_list.append(Arc(arcid, con_grp['duedate'], con_grp['length'], con_grp['capacity'], con_grp['node_1'],
                                con_grp['node_2']))
    return arc_list


#
def extract_escapes_routes(content_evac_info):
    content = []

    for nid, con_eva_inf in content_evac_info.items():
        content.append(con_eva_inf['escape route'])
    return content


#
def extract_escape_route_path(no_list, ar_list, escape_route):
    content = []
    for n1, n2 in pairwise(escape_route):
        node_1 = next((node for node in no_list if int(node.nid) == int(n1)), None)
        node_2 = next((node for node in no_list if int(node.nid) == int(n2)), None)
        tarc = next((arc for arc in ar_list if int(arc.n1) == int(node_1.nid) and int(arc.n2) == int(node_2.nid)),
                    None)
        info = {
            'node_1': node_1,
            'arc': tarc,
            'node_2': node_2
        }
        content.append(info)

    return content


def extract_starting_nodes(content_nodes_evac):
    content = []
    for content_node_evac in content_nodes_evac:
        con = (content_node_evac['starting_date_evacuation'], content_node_evac['max_rate'])
        content.append((content_node_evac['node_id'], con))

    return dict(content)


def get_start_time_escape_route_path(tpath, starting_nodes):
    return starting_nodes[tpath[0]['node_1'].nid]




############## Main ################

def main(file_name):
    # data.txt
    nstarting_node, safe_node, num_nodes, num_edges, evacuation_info, graph = parse_data_file(file_name[1:][0])
    # sol.txt
    resolved_instance, nnode_evacuate, nodes_evacuate = parse_sol_file(file_name[1:][1])

    #
    content_evac_info = arrange_evacuation_info(evacuation_info)
    content_graph = arrange_graph(graph)
    content_nodes_evac = arrange_nodes_evacuation(nodes_evacuate)

    # fill the node_list
    node_list = extract_node_content_evac_info(content_evac_info, safe_node)
    # fill the arc_list

    arc_list = extract_arc_content_graph(content_graph)

    # fill the escapes_routes list
    escapes_routes = extract_escapes_routes(content_evac_info)

    # fill the starting_nodes list
    starting_nodes_sol = extract_starting_nodes(content_nodes_evac)

    # fill the tpaths list
    for escape_route in escapes_routes:
        tpaths.append((escape_route[0], extract_escape_route_path(node_list, arc_list, escape_route)))
        break


    #
    # val.process_objective(starting_nodes_sol, content_evac_info, tpaths)
    # lbound.lower_bound(content_evac_info, tpaths, arc_list, "My_lower_bound")
    # ubound.upper_bound(content_evac_info, tpaths, arc_list, "My_upper_bound")
    # val.validator(starting_nodes_sol, content_evac_info, tpaths, arc_list)
    ls.neighbour_date(safe_node, arc_list,node_list, starting_nodes_sol, content_evac_info, tpaths, 2)


if __name__ == '__main__':
    main(sys.argv)
