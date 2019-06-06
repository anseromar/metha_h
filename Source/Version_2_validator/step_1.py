############ Import  ################
import sys
from itertools import tee

############ Global ################
node_list = []
arc_list = []


#####################################
############ Classes ################
class Node:

    def __init__(self, nodeid, population, startingnode, safenode, listEvac=[]):
        self.nid = nodeid
        self.pop = population
        self.sfnode = safenode
        self.stgnode = startingnode
        self.lEvac = listEvac

    def __str__(self):
        # return "Node id " + str(self.nid) + " => { population : " + str(self.pop) + " ; is a safe node : " + \
        #        str(self.sfnode) + " ; is a starting node : " + str(self.stgnode) + " ; his list evacuation : " + str(
        #     self.lEvac) + " }"
        return "Node id " + str(self.nid) + "{ list evacuation : " + str(
            self.lEvac) + " }"

    def __repr__(self):
        pass


class Arc:

    def __init__(self, arcid, duedate, length, capacity, node1, node2, nmbPassage=0):
        self.arid = arcid
        self.ddate = duedate
        self.len = length
        self.cap = capacity
        self.n1 = node1
        self.n2 = node2
        self.nmbpassage = nmbPassage

    def __str__(self):
        # return "Arc id " + str(self.arid) + " => { due date : " + str(self.ddate) + " ; length : " + str(
        #     self.len) + " ; capacity : " + str(self.cap) + " ; node_1 : " + str(self.n1) + " ; node_2 : " + str(
        #     self.n2) + "  nmbPass : " + str(self.nmbpassage) + " } "
        return "    "

    def __reps__(self):
        pass


class Graph:
    pass


class Parser():
    def __init__(self, datafile, solfile):
        self.dataFile = datafile
        self.solFile = solfile

    ############ Functions #############
    def pairwise(self, iterable):
        "s -> (s0,s1), (s1,s2), (s2, s3), ..."
        a, b = tee(iterable)
        next(b, None)
        return zip(a, b)

    # Allows to parse the file containing the data of a evacuation situation
    def parse_data_file(self):

        with open(self.dataFile) as f:
            nstarting_node, safe_node = [int(x) for x in next(f).split()]
            lines = [x.rstrip('\n') for x in f.readlines()]

        evacuation_info = lines[0:nstarting_node]
        num_nodes, num_edges = map(int, lines[nstarting_node + 1].split(" "))
        graph = [x for x in lines[nstarting_node + 2:] if x]

        return (nstarting_node, safe_node, num_nodes, num_edges, evacuation_info, graph)

    # Allows to arrange into a list of map the first part of the data file "evacuation_info"
    # @return : a list of map representing each line
    def arrange_evacuation_info(self, evacinfo):

        content = []
        for evac in evacinfo:
            e = evac.split(' ')
            info = {
                'starting node': e[0],
                'population': int(e[1]),
                'max rate': int(e[2]),
                'k': int(e[3]),
                'escape route': [e[0]] + e[4:]
            }
            content.append(info)

        return content

    # Allows to arrange into a list of map the second part of the data file "graph"
    # @return : a list of map representing each line
    def arrange_graph(self, grh):

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
    def parse_sol_file(self):

        with open(self.solFile) as f:
            resolved_instance = [x for x in next(f).split()][0]
            nnode_evacuate = [int(x) for x in next(f).split()][0]
            lines = [x.rstrip('\n') for x in f.readlines()]

        nodes_evacuate = lines[0:nnode_evacuate]

        # To do : still the lines to split
        return (resolved_instance, nnode_evacuate, nodes_evacuate)

    # Allows to arrange into a list of map the second part of the data file "graph"
    # @return
    def arrange_nodes_evacuation(self, nodesevac):

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
    def extract_node_content_evac_info(self, content_evac_info, safe_node):
        for evac_info in content_evac_info:
            node_list.append(Node(evac_info['starting node'], evac_info['population'], True, False))
            for node_esc_rout in evac_info['escape route']:
                if not any(int(node.nid) == int(node_esc_rout) for node in node_list):
                    node_list.append(
                        Node(node_esc_rout, 0, False, True if int(safe_node) == int(node_esc_rout) else False))

    #
    def extract_arc_content_graph(self, content_graph):

        for arcid, con_grp in enumerate(content_graph):
            if con_grp['length'] > 100:
                continue;
            else:
                arc_list.append(
                    Arc(arcid, con_grp['duedate'], con_grp['length'], con_grp['capacity'], con_grp['node_1'],
                        con_grp['node_2']))

    #
    def extract_escapes_routes(self, content_evac_info):
        content = []
        for con_eva_inf in content_evac_info:
            content.append(con_eva_inf['escape route'])
        return content

    #
    def get_path(self, no_list, ar_list, escape_route):
        content = []
        for n1, n2 in self.pairwise(escape_route):
            node_1 = next((node for node in node_list if int(node.nid) == int(n1)), None)
            node_2 = next((node for node in node_list if int(node.nid) == int(n2)), None)
            tarc = next((arc for arc in arc_list if int(arc.n1) == int(node_1.nid) and int(arc.n2) == int(node_2.nid)),
                        None)
            info = {
                'node_1': node_1,
                'arc': tarc,
                'node_2': node_2
            }
            content.append(info)
        return content
