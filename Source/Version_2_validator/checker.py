from typing import List, Any

from step_1 import Parser
from step_1 import Node
from step_1 import Arc
from step_1 import node_list
from step_1 import arc_list
import sys
from itertools import tee




class Checker():
    def __init__(self, datafile, solfile):
        self.dataFile = datafile
        self.solFile = solfile

    def ini_list(self,list,startingTime):
        if startingTime != 0:
            for time in range (0,startingTime):
                list.append('0')
        return list

    def re_inserer(self,node,listCon):
        #print("Test-----  Recu   " +str(node.nid)+"  Recu list  "+ str(listCon))
        nodeid = node.nid
        population = node.pop
        safenode = node.sfnode
        startingnode = node.stgnode
        listEvac = node.lEvac
        del node_list[int(node.nid)-1]
        node_list.insert(int(node.nid)-1,Node(nodeid, population, safenode, startingnode, listCon))
        #print("Test-----"+str(node_list[int(node.nid)-1].lEvac))


    def garde_inserer(self,node,listCon):
        nodeid = node.nid
        population = node.pop
        safenode = node.sfnode
        startingnode = node.stgnode
        listEvac = node.lEvac
        del node_list[int(node.nid) - 1]

        node_list.insert(int(node.nid)-1,Node(nodeid, population, safenode, startingnode, listCon+listEvac))

    #Fait le calcul de Poupulation/Max Rate
    def gene_nombre_fois_evacuation(self,info,quotient,modulo):
        listPartTwo = []
        for time in range(0,quotient):
            listPartTwo.append(str(info['max_rate']))
        if modulo!=0:
            listPartTwo.append(str(modulo))
        return listPartTwo


    #Trouver les nodes de depart, et calculer le nmb de fois d'evacuation d'apres la max pupulation et le Max Rate
    def create_debut_list(self,content_nodes_evac):
        for info in content_nodes_evac:
            print(str(info['node_id'])+" Max Rate : "+str(info['max_rate'])+"  Start Time : "+str(info['starting_date_evacuation']))
            for no in node_list:
                if no.nid == info['node_id']:
                    listVide = []
                    listContainer =[]
                    listContainer.extend(self.ini_list(listVide, info['starting_date_evacuation']))

                    quotient = int(no.pop)//int(info['max_rate'])
                    print("Quotient is "+str(quotient))
                    modulo = int(int(no.pop)%int(info['max_rate']))
                    print("Modulo "+str(modulo))
                    listPart2 = self.gene_nombre_fois_evacuation(info, quotient, modulo)
                    self.re_inserer(no, listContainer+listPart2)

    #Simuler le traffic dans une seule path jusqu'a il atteint la safe node.
    def cumule_path(self,tPath):
        comp = 0
        for tp in tPath:

            print()
            print()
            print("Sur ce chemin il y a "+ str(tp['node_1'].nid)+"-----> "+str(tp['node_2'].nid))


            tp['arc'].nmbpassage+=1
            print("Leur ###################################   Passage :  "    +str(tp['arc'].nmbpassage)+"  fois")

            listPrepared = []
            for decal in range(0, int(tp['arc'].len)):
                listPrepared.append('0')
            print("son predesseur  list est "+str(node_list[int(tp['node_1'].nid)-1].lEvac))

            listPreparedEtat2 = listPrepared + node_list[int(tp['node_1'].nid) - 1].lEvac
            if node_list[int(tp['node_2'].nid)-1].lEvac!=[] and tp['arc'].nmbpassage <= 1:
                listSucp3 = []


                print("Deja ecrit dans cette liste, du coup fait merge les deux")
                print("PreparedEtat2  is   " + str(listPreparedEtat2))
                print(" Une liste reste deja ici-----"+str(node_list[int(tp['node_2'].nid)-1].lEvac))

                for i in range(0, max(len(listPreparedEtat2), len(node_list[int(tp['node_2'].nid)-1].lEvac))):

                    if i < min(len(listPreparedEtat2), len(node_list[int(tp['node_2'].nid)-1].lEvac)):
                        #print("111 i is " + str(i))
                        listSucp3.append(str(int(listPreparedEtat2[i]) + int(node_list[int(tp['node_2'].nid)-1].lEvac[i])))
                    elif len(listPreparedEtat2) < len(node_list[int(tp['node_2'].nid)-1].lEvac):
                        #print('222')
                        listSucp3.append(node_list[int(tp['node_2'].nid)-1].lEvac[i])
                    else:
                        #print('333')
                        listSucp3.append(listPreparedEtat2[i])
                print("----  " + str(tp['node_2'].nid) + " --- ce noeud  mis a jour son liste evac" + str(listSucp3))

                self.re_inserer(tp['node_2'], listSucp3)

            else:
                print("1 ere fois on entre ou deja passe exactement le meme arc ")
                print()
                print("----  " + str(tp['node_2'].nid) + " --- ce noeud  mis a jour son liste evac" + str(
                    listPreparedEtat2))

                self.re_inserer(tp['node_2'], (listPreparedEtat2))
        comp += 1



    def cumule_all_path(self,Parser,nodelist,arclist,escapes_routes):
        for path in escapes_routes:
            print()
            print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
            print("^^^^^^^Un chemin en train de cumuler ^^^^^^")
            print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
            tpath=Parser.get_path(nodelist, arclist, path)
            self.cumule_path(tpath)


    def check_capacite_path(self,tPath):
        for tp in tPath:
            print()
            print()
            print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
            print("^^^^^^^Check capa ^^^^^^")
            print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
            print()
            print()
            print(str(tp['node_1'].nid))
            print("son  indice est " + str(int(tp['node_1'].nid) - 1))
            print("La liste Evac de ce noeud est " + str(node_list[int(tp['node_1'].nid) - 1].lEvac))

            print("Max is " + str(max( list(map(int,node_list[int(tp['node_1'].nid) - 1].lEvac)) )))

            if max( list(map(int, node_list[int(tp['node_1'].nid) - 1].lEvac)) ) > int(tp['arc'].cap):
                print()
                print()
                print("^^^^^^^ !!!!!!!  capa  Explose !!!!!!!!^^^^^^")
                print()
                print()
                return False;

        return True

    def check_capacite_all_path(self, parser, nodelist, arclist,routes):
        for pathcheck in routes:

            tate = parser.get_path(nodelist, arclist, pathcheck)
            if self.check_capacite_path(tate) is False:
                return False
        return True


    def check_duedate_path(self,tPath):
        for tp in tPath:
            print()
            print()
            print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
            print("^^^^^^^Check DueDate ^^^^^^")
            print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
            print()
            print()
            if len( list(map(int, node_list[int(tp['node_1'].nid) - 1].lEvac)) )> int(tp['arc'].ddate):
                print()
                print()
                print("^^^^^^^ !!!!!!!  Trop tard !!!!!!!!^^^^^^")
                print()
                print()
                return False;
        return True


    def check_duedate_all_path(self,Parser,nodelist,arclist,escapes_routes):
        for pathDue in escapes_routes:
            tpath=Parser.get_path(nodelist, arclist, pathDue)
            if self.check_duedate_path(tpath) is False:
                return False
        return True



    def check_final(self,res_capa,res_due):
        if res_capa and res_due is True:
            print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
            print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
            print("^^^^^^^^           ^^^^^^^^^^^")
            print("+++++++   Valide   +++++++++++")
            print("^^^^^^^            ^^^^^^^^^^")
            print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
            print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
        else:
            print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
            print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
            print("^^^^^^^^           ^^^^^^^^^^^")
            print("++++++++  InValide ++++++++++++")
            print("^^^^^^^^^          ^^^^^^^^^^^^")
            print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
            print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")





    def find_arc_successeur_Path(self,node,tPath):
        listArcSuc = []  # type: List[Any]
        for tp in tPath:
            print("sur ce chemin il y a "+ str(tp['node_1'].nid)+"---> "+str(tp['node_2'].nid))
            if tp['node_1'].nid==node.nid:
                listArcSuc.append(tp['arc'])
        print("finished one chemin")
        return listArcSuc

    def find_arc_successeur_Graphe(self,node,parser,escapes_routes):
        listArcSuc = []
        for route in escapes_routes:
            tpath = parser.get_path(node_list, arc_list, route)
            listArcSuc=listArcSuc + self.find_arc_successeur_Path(node, tpath)
        for ll in listArcSuc:
           print("Node  "+str(node.nid)+"  Son Successeur has these arc (id):  --- "+str(ll.arid))
        return listArcSuc

    def find_node_successeur_Graphe(self,listArcSuc):
        listNodeSuc = []
        for arc in listArcSuc:
            for node in node_list:
                if node.nid == arc.n2:
                    listNodeSuc.append(node)
        for ln in listNodeSuc:
            print("Son Sucdesseur has these node (id):  ------- "+str(ln.nid))
        return listNodeSuc




   




############## Main ################
def main():

    #############################################
    ############  Parser Part  #################
    #############################################

    my_parser = Parser(sys.argv[1], sys.argv[2])
    # data.txt
    nstarting_node, safe_node, num_nodes, num_edges, evacuation_info, graph = my_parser.parse_data_file()
    # sol.txt
    resolved_instance, nnode_evacuate, nodes_evacuate = my_parser.parse_sol_file()

    content_evac_info = my_parser.arrange_evacuation_info(evacuation_info)
    content_graph = my_parser.arrange_graph(graph)
    content_nodes_evac = my_parser.arrange_nodes_evacuation(nodes_evacuate)

    my_parser.extract_node_content_evac_info(content_evac_info, safe_node)

    my_parser.extract_arc_content_graph(content_graph)

    escapes_routes = my_parser.extract_escapes_routes(content_evac_info)




    #Trier la liste de node pour faciliter le traitement
    listInter = [];
    listInter = sorted(node_list, key=lambda onenode: onenode.nid)

    node_list.clear();
    node_list.extend(listInter)


    #############################################
    ############  Checker Part  #################
    #############################################
    my_checker = Checker(sys.argv[1], sys.argv[2])
    my_checker.create_debut_list(content_nodes_evac)


    #Tracer tout le diagramme de grund ici
    my_checker.cumule_all_path(my_parser, node_list, arc_list, escapes_routes)


    #Check capacite de tous les arc, si le trffic est superieur a la capacite, une alarme est signale.
    Res1 = my_checker.check_capacite_all_path(my_parser, node_list, arc_list, escapes_routes)
    #Check the duedate
    Res2 = my_checker.check_duedate_all_path(my_parser, node_list, arc_list, escapes_routes)
    #Affiche le resultat de checker
    my_checker.check_final(Res1, Res2)

    #############################################
    ############  Affiche le node list  #################
    #############################################
    for node in node_list:
        print(node)
        print()





    # tpathTest = my_parser.get_path(node_list, arc_list, escapes_routes[0])
    # my_checker.cumule_path(tpathTest)
    #
    # print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
    # print("^^^^^^^Deuxieme chemin^^^^^^")
    # print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
    #
    # tpathTest2 = my_parser.get_path(node_list, arc_list, escapes_routes[1])
    # my_checker.cumule_path(tpathTest2)





    #listContient.extend(my_checker.find_arc_successeur_Graphe(node_list[0], my_parser, escapes_routes))
    # print("Testpoint   "+str(listContient[0].arid))
    # print("Testpoint2   " + str(listContient[1].arid))
    #listSucNodes = my_checker.find_node_successeur_Graphe(listContient)
    # my_checker.merge_list_noeuds_predesseur(listSucNodes,node_list[3],listContient)




    #

    #my_checker.find_arc_predesseur_Graphe(nodeTest,my_parser, escapes_routes)
    # # only the first escape route
    # for route in escapes_routes:
    #     tpath = my_parser.get_path(node_list, arc_list, route)
    #     my_checker.find_arc_predesseur_Path(nodeTest, tpath)



    #my_checker.parcour_recurssif(node_list[5],my_parser, escapes_routes, content_nodes_evac)

    #############################################
    ############  Affiche le chemin  #################
    #############################################

    # tpath2 = my_parser.get_path(node_list, arc_list, escapes_routes[0])
    #
    #
    #
    #
    # for tp in tpath2:
    #     print("#########")
    #     print(tp['node_1'])
    #     print(tp['arc'])
    #     print(tp['node_2'])
    #     print("#########")
    #
    # tpath3 = my_parser.get_path(node_list, arc_list, escapes_routes[1])
    #
    # for tp in tpath3:
    #     print("#########")
    #     print(tp['node_1'])
    #     print(tp['arc'])
    #     print(tp['node_2'])
    #
    # tpath4 = my_parser.get_path(node_list, arc_list, escapes_routes[2])
    #
    # for tp in tpath4:
    #     print("#########")
    #     print(tp['node_1'])
    #     print(tp['arc'])
    #     print(tp['node_2'])



    # print("La borne inferieur d'une path est "+str(get_inferior_borene_path(tpath)))
    # print("La borne inferieur du graphe  est "+str(get_inferior_borene_graph(escapes_routes)))
    # write_solution()

    print("mec " + str(len(node_list)))
    print("mec " + str(len(arc_list)))
if __name__ == '__main__':
    main()
