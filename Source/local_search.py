import sys
import os
import time
import copy
import random
from operator import itemgetter
import parse_instance_solution as parse
import validator as val
import print_solution as prt_sol
import re


def create_new_packets(step, safe_node, packets, noeud_limit, content_evac_info, arc_list, node_list):
    dummy = []

    new_packets = copy.deepcopy(packets)
    escape_route = content_evac_info[noeud_limit[0]]['escape route']

    dummy.append((escape_route[0], parse.extract_escape_route_path(node_list, arc_list, escape_route)))

    for nid_start, arcs in dummy:
        for arc in arcs:
            tarc = (arc['node_1'].nid, arc['node_2'].nid)
            new_packets[(noeud_limit[0], tarc)] = (
                new_packets[(noeud_limit[0], tarc)][0] - step, new_packets[(noeud_limit[0], tarc)][1])
        new_packets[(noeud_limit[0], (str(safe_node), -1))] = (
            new_packets[(noeud_limit[0], (str(safe_node), -1))][0] - step,
            new_packets[(noeud_limit[0], (str(safe_node), -1))][1])
    return new_packets


def neighbour_date(safe_node, arc_list, node_list, starting_nodes_sol, content_evac_info, tpaths, step):
    packets = dict()

    for nid_start, tpath in tpaths:
        print(starting_nodes_sol)
        (start_date, evac_rate) = starting_nodes_sol[nid_start]
        for tp in tpath:
            packets[(nid_start, (tp['node_1'].nid, tp['node_2'].nid))] = (start_date, evac_rate)
            start_date = start_date + tp['arc'].len
        packets[(nid_start, (tpath[-1]['node_2'].nid, -1))] = (start_date, evac_rate)

    temps_evac = [(nid_start, packets[(nid_start, (str(safe_node), -1))]) for nid_start, tpath in tpaths]
    noeud_limit = max(temps_evac,
                      key=itemgetter(1))

    if (starting_nodes_sol[noeud_limit[0]][0] - step) >= 0:
        new_packets = create_new_packets(step, safe_node, packets, noeud_limit, content_evac_info, arc_list, node_list)
        if val.validator(starting_nodes_sol, content_evac_info, tpaths, arc_list, new_packets) == (True, True):
            return True, new_packets
        else:
            temps_evac.remove(noeud_limit)
            node_aux = max(temps_evac, key=itemgetter(1))
            if (starting_nodes_sol[noeud_limit[0]][0] - step) >= 0:
                new_packets = create_new_packets(step, safe_node, packets, noeud_limit, content_evac_info, arc_list, node_list)
                if val.validator(starting_nodes_sol, content_evac_info, tpaths, arc_list, new_packets) == (True, True):
                    return True, new_packets
                else:
                    return False, {}
            else:
                return False, {}
    else:
        return False, {}