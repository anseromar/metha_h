import parse_instance_solution as parse
import AVL as avl


def process_objective(starting_nodes_sol, content_evac_info, tpaths):
    packets = []

    for nid_start, tpath in tpaths:
        (evac_rate, start_date) = starting_nodes_sol[nid_start]

        nb_passage = content_evac_info[nid_start]['population'] // evac_rate
        for tp in tpath:
            packets.append((tp['arc'], (start_date, evac_rate, nb_passage)))
            start_date = start_date + tp['arc'].len
        packets.append(("safe", (start_date, evac_rate, nb_passage)))

    return max([pkt[1][0] + pkt[1][2] for pkt in packets if pkt[0] == "safe"])


def validator(starting_nodes_sol, content_evac_info, tpaths, arc_list, packets=None):
    vmax_rate = True
    vcapacity = True

    for nid, nid_sol in starting_nodes_sol.items():
        if nid_sol[1] > content_evac_info[nid]['max rate']:
            vmax_rate = False

    for nid_start, tpath in tpaths:
        for tp in tpath:
            if starting_nodes_sol[nid_start][1] > tp['arc'].cap:
                vmax_rate = False

    if packets is None:
        packets = []
        dummy = dict()

        for nid_start, tpath in tpaths:
            (evac_rate, start_date) = starting_nodes_sol[nid_start]
            nb_passage = content_evac_info[nid_start]['population'] // evac_rate
            for tp in tpath:
                packets.append((tp['arc'], (start_date, evac_rate, nb_passage)))
                start_date = start_date + tp['arc'].len

        for arc in arc_list:
            dummy[arc] = []
            for (tarc, (start_date, evac_rate, nb_passage)) in packets:
                if not isinstance(tarc, str) and arc.arid == tarc.arid:
                    dummy[arc].append((start_date, evac_rate, nb_passage))

        for arc, list_pkt in dummy.items():
            cap = arc.cap
            start = min(list_pkt)[0]
            end = max([x+z for (x, y, z) in list_pkt])
            for i in range(start, end):
                nb_prs = 0
                for (start_date, evac_rate, nb_passage) in list_pkt:
                    if start <= i < (evac_rate + nb_passage):
                        nb_prs = nb_prs + evac_rate
                if nb_prs > cap:
                    vcapacity = False

        return vmax_rate, vcapacity
    else:


        return vmax_rate, vcapacity
