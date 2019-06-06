import sys
import time
import parse_instance_solution as parse
import validator as val
import print_solution as prt_sol


def lower_bound(content_evac_info, tpaths, arc_list, resolved_instance):
    stime = time.time()
    solution = dict()
    for nid, nid_evac_info in content_evac_info.items():
        solution[nid] = (min(nid_evac_info['max rate'],
                               min([tp['arc'].cap for nid_start, tpath in tpaths if nid_start == nid_start for tp in tpath])),
                           0)
    vmax_rate, vcapacity = val.validator(solution, content_evac_info, tpaths, arc_list,None)
    etime = time.time()
    processing_time = etime - stime

    prt_sol.print_solution(resolved_instance, len(solution), solution, "Valid" if vmax_rate == vcapacity == True else "Not valid", val.process_objective(solution, content_evac_info, tpaths), processing_time, "Lower bound")
    return val.process_objective(solution, content_evac_info, tpaths)


if __name__ == "__main__":
    pass
