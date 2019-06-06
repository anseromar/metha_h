def print_solution(resolved_instance, nnode_evacuate, nodes_evacuate, is_valid, aim_function, processing_time, method):
    file = open("../Solutions/" + resolved_instance, "w+")

    file.write(resolved_instance + "\n")
    file.write(str(nnode_evacuate) + "\n")
    for nid, node_evac_info in nodes_evacuate.items():
        file.write(nid + "\t")
        file.write(str(node_evac_info[0]) + "\t")
        file.write(str(node_evac_info[1]) + "\n")
    file.write(is_valid + "\n")
    file.write(str(aim_function) + "\n")
    file.write(str(processing_time) + "\n")
    file.write(method + "\n")
    file.close()
