__author__ = 'Diman Zad Tootaghaj'

import pydot # import pydot or you're not going to get anywhere my friend :D
import networkx as nx
import my_lib as my_lib_var
import sys
#import winsound
import time
from scipy import stats
from my_lib import *
from my_flows_lib import *
from my_lib_optimal_async_SDN import *
#from my_lib_optimal_ILP_SDN import *
from my_lib_optimal_ILP_Max_route import *
#from my_lib_optimal_recovery import *
#from my_lib_optimal_expected_recovery import *
#from my_lib_optimal_approx_max_flow import *
#from my_lib_optimal_expected_recovery_max_flow import *
#from my_lib_optimal_approx_recovery import *
#from my_lib_optimal_recovery_multicommodity import *
#from my_lib_optimal_recovery_multicommodity_maxFlow import *
#from my_lib_optimal_recovery_multicommodity_worst import *
#from my_lib_optimal_recovery_multicommodity_best import *
from my_lib_check_routability import *
from my_lib_compute_max_demand_in_the_graph import *
#https://www.diffchecker.com/efddo0xv

work_dir=os.getcwd()
##############################################
path_to_dot_dir='../../../image_graph_dot/DotFile/'
path_to_image_dir='../../../image_graph_dot/immagini_generate/'
path_to_image_store='../../../image_graph_dot/store_images/'
path_to_stats='../../../image_graph_dot/stats/statistiche/'
path_to_file_simulation='../../../image_graph_dot/current_simulation.txt'
path_to_stat_prog='../../../image_graph_dot/stats/progress_iteration/'
path_to_stat_times='../../../image_graph_dot/stats/times/'
##############################################
print "Number of runs: "+sys.argv[5]+ "/"+sys.argv[4]
print "Simulation Parameters: "
print "Seed: "+sys.argv[1]
print "Alpha demand: "+sys.argv[2]
print "Prob edge green: "+sys.argv[3]
print "Distance metric: "+sys.argv[6]
print "Type of betweeness: "+sys.argv[7]

seed_passed=sys.argv[1]
alpha_passed=sys.argv[2]
prob_edge_passed=sys.argv[3]
distance_metric_passed=sys.argv[6]
type_of_bet_passed=sys.argv[7]
flow_c_fixed=sys.argv[8]
flow_c_value=float(sys.argv[9]) #int(sys.argv[9])
number_of_couple=int(sys.argv[10])
fixed_distruption=str(sys.argv[11])
var_distruption=float(sys.argv[12])
K_HOPS=int(sys.argv[14])
always_split=int(sys.argv[15])
random_disruption=int(sys.argv[16])
disruption_value=int(sys.argv[17])
error=float(sys.argv[18])
#Gap=float(sys.argv[19])


if sys.argv[13]!=None:
    filename_graph=str(sys.argv[13])
    print 'Graph: ' + filename_graph


path_to_graph= 'network topologies/'
path_to_graph=path_to_graph+filename_graph+'.gml'
path_to_folder_couple='distance_between_couples/'


H=nx.MultiGraph(nx.read_gml(path_to_graph))
#print H.nodes()[1]

print 'Dimensions of the Graph'
print "Nodes: %d"%H.number_of_nodes()
print "Edges: %d"%H.number_of_edges()
print "Total: %d"%(H.number_of_nodes()+H.number_of_edges())
seed_random=int(seed_passed)
#seed_random = 72
random.seed(seed_random)

print 'Seed Utilized: %f: '%seed_random


#print 'Diameter of the Graph: %d'%(compute_diameter_of_graph(H))

print 'Flow Variation: %s'%(flow_c_fixed)
if flow_c_fixed=='False':
    print 'Quantity of Flow Assigned: %d'%(flow_c_value)
else:
    print 'Vario il numero di coppie fissando il flusso: %d'%(flow_c_value)
    print 'Number of Pairs Selected: %d'%(number_of_couple)

if fixed_distruption=='True':
    print 'Fixed Disruption'
    #var_distruption=0
else:
    print 'Varied Disruption'
    print 'Variance of Disruption: %d '%(var_distruption)

#prendi la lista delle distanze da file
list_of_couples=get_list_distance_couples(path_to_folder_couple,filename_graph)
list_of_couples=subset_of_list(list_of_couples,50)
list_of_couples=select_random_couples_from_list(list_of_couples,number_of_couple)
#list_of_couples = [(16, 38, 10),(35, 44, 10)]

print 'Subset of Random Couples:'
print list_of_couples

green_edges=[]
filename_graph=path_to_graph[path_to_graph.find('/')+1:-4]
print filename_graph
filename_demand=filename_graph+'DemandGenereted'

#change the graph by assigning random values to the capacity of the edges
#assign_random_capacity_to_edges(H,filename_graph)
#sys.exit(0)

prepare_graph(H)
my_draw(H,'1-initial'+'_Seed_'+str(seed_random)+'_'+'Prob_edge_'+str(prob_edge_passed)+'_')
#sys.exit(0)


#GENERATE FEASIBLE DEMAND ON SUPPLY GRAPH
#prob_edge=0.05
#Probability green edge passed in argument
prob_edge=float(prob_edge_passed)

alfa=float(alpha_passed)
distance_metric=distance_metric_passed

feasible_solution=check_if_istance_is_feasible(H,list_of_couples,flow_c_value)

print feasible_solution

#crea file se non esiste dei tempi delle simulazioni
if not os.path.exists(path_to_stat_times):
    os.makedirs(path_to_stat_times)
path_to_file_times=path_to_stat_times+filename_graph+'_times_'+str(number_of_couple)+'_couple.txt'

if not os.path.exists(path_to_file_times):
    file=open(path_to_file_times,'w')
    file.close()

if feasible_solution==False:
    write_stat_time_simulation(path_to_stat_times,'Infeasible',filename_graph,int(sys.argv[5]),int(sys.argv[4]),seed_passed,number_of_couple,0)
    sys.exit('Seed Discarded - Solution Infeasible')



path_to_demand,green_edges=generate_demand_of_fixed_value_from_list_of_couple(H,list_of_couples,flow_c_value,prob_edge,filename_demand,alfa,seed_random,path_to_stats,distance_metric)


print 'Couples of Green Edges Seclected:'
#per passare archi particolari
#green_edges=[(3,6,3)]
print green_edges

#sys.exit(0)
copy_of_green_edges=[]
copy_of_green_edges=deepcopy(green_edges)
D=nx.MultiGraph(nx.read_gml(path_to_demand))

#print new_bet_dict
my_draw(H, '2-prepared-new_bet_alpha_%f'%alfa)

if not os.path.exists(path_to_stat_prog):
    os.makedirs(path_to_stat_prog)
file=open(path_to_stat_prog+filename_graph+'_progress.txt','w')
file.close()

H1=nx.MultiGraph(H)
H2=nx.MultiGraph(H)
H3=nx.MultiGraph(H)
H4=nx.MultiGraph(H)
H6=nx.MultiGraph(H)
H7=nx.MultiGraph(H)
H9=nx.MultiGraph(H)
H8=nx.MultiGraph(H)
merge_graphs(H,D)
select_betweeness(H,green_edges,distance_metric,type_of_bet_passed)

coor_x=45
coor_y=-75
dict_bet,temp_shortest_set,end_time_bet=select_betweeness(H,green_edges,distance_metric,type_of_bet_passed)
my_draw(H,'3-Original-Graph')

arcs=[]
capacity={}
#construct arcs array and capacity:
#for edge in H.edges(data=True):
#    print edge
#Generate demand flows in graph H
demand_flows=[]
#construct demand_flows array:
i=0
for edge in green_edges:
    name_flow='F%d'%(i)
    #name_flow = i
    demand_flows.append(name_flow)
    i+=1
i = 0
weights = []
for e in demand_flows:
  if(i/float(len(demand_flows)) <=0.4):
    weights.append(100)
  if((i/float(len(demand_flows)) >=0.4) and (i/float(len(demand_flows)) <=0.5)):
    weights.append(1)
  if((i/float(len(demand_flows)) >=0.5) and (i/float(len(demand_flows)) <=0.9)):
    weights.append(100)
  if((i/float(len(demand_flows)) >=0.9) and (i/float(len(demand_flows)) <=1)):
    weights.append(1)
  i+=1
############################################################################
#Generate edges in graph H
for edge in H.edges():
    id_source=edge[0]
    id_target=edge[1]

    keydict=H[id_source][id_target]
    arc=(id_source,id_target)
    #print arc
    #print keydict
    for k in keydict:
        if H[id_source][id_target][k]['type']=='normal':# and H[id_source][id_target][k]['type']!='green':
            if arc not in arcs:
                arcs.append(arc)
            else:
                print 'ERROR'
                print arc
            cap=H[id_source][id_target][k]['capacity']
            if not capacity.has_key(arc):
                capacity.update({arc:cap})
            else:
                print 'ERROR'
                print arc

arcs = tuplelist(arcs)
#print 'arcs:'
#print arcs
#print 'Edges of the graph H:'
#print H.edges()
#########################################################################################################################
K= {}
for h in demand_flows:
    for i,j in H.edges():#arcs:
    #for h in demand_flows:
        K[h,i,j]= 0
        K[h,j,i]= 0
##########Divide the green edges into two parts: First part is used to make the initial routing and second part is used to update the SDN switches:
half_greens= len(green_edges)/2# -1 #len(green_edges)-2 #len(green_edges)/2
count = 0
green_edges_1 = []
green_edges_2 = []
for (i,j,d) in green_edges:
    if count < half_greens:
        green_1=(i,j,d)
        green_edges_1.append(green_1)
    else:
        green_2=(i,j,d)
        green_edges_2.append(green_2)
    count = count + 1
print 'green_edges'
print green_edges
print 'green_edges_1:'
print green_edges_1
print 'green_edges_2'
print green_edges_2
#########################################################################################################################
demand_flows_1 = []
i=0
for edge in green_edges_1:
    name_flow='F%d'%(i)
    demand_flows_1.append(name_flow)
    i+=1
demand_flows_2 = []
i=0
for edge in green_edges_2:
    name_flow='F%d'%(i)
    demand_flows_2.append(name_flow)
    i+=1

#----------------------------------------------------------OPTIMAL-------------------------------------------------------
print 'Inizio algoritmo OPTIMAL recovery'
del H
SumDelta = 0
SumTheta = 0
OBJ = 0
Deltah = []
Thetah = []
my_used_arcs = []
#Diman commented two comments
H=nx.MultiGraph(nx.read_gml(path_to_graph))  #grafo supply
prepare_graph(H)
#merge_graphs(H,D)

green_edges=deepcopy(copy_of_green_edges)


start_time_optimal=time.time()
#############################################################################################################
OBJ_T = 0
Deltah_T = []
Thetah_T = []
my_used_arcs_T = []
#Diman commented two comments
H_T=nx.MultiGraph(nx.read_gml(path_to_graph))  #grafo supply
prepare_graph(H_T)
#merge_graphs(H,D)

green_edges_T=deepcopy(copy_of_green_edges)
w_l = 0
w_h = 0
Max_Time_T=0
Total_Hop_T = 0
Thr= len(arcs)*100
Thrh = Thr
Total_ReRouted_T = 0
[OBJ_T, Deltah_T, H4, my_used_arcs_T, Max_Time_T, Total_Hop_T, Total_ReRouted_T]= optimal_SDN_LP(H,green_edges, K, demand_flows, w_l, w_h, Thrh, Thr,weights)

#[OBJ_T, Deltah_T, Thetah_T, H2, my_used_arcs_T] = optimal_SDN_Max(H_T,green_edges_T, K, demand_flows, w_l, w_h)
Min_Hops = 0
for h in demand_flows:
    for i,j in H.edges():
        if (my_used_arcs_T[h,i,j] ==1):
            Min_Hops = Min_Hops + 1
        if (my_used_arcs_T[h,j,i] ==1):
            Min_Hops = Min_Hops + 1
##############################################################################################################
#optimal solution run one by one:
w_l = 0
w_h = 0
#[OBJ, Deltah, Thetah, H2, my_used_arcs] = optimal_SDN(H,green_edges_1, K, demand_flows_1, w_l, w_h)
[OBJ, Deltah, Thetah, H2, my_used_arcs] = optimal_SDN_Max(H,green_edges_1, K, demand_flows_1, w_l, w_h)
i = 0
for edge in green_edges_1:
    #residual_graph=nx.MultiGraph(supply_graph)
    source=edge[0]
    target=edge[1]
    #demand= edge[2]
    arc=(source,target)
    (length, path) = my_prob_single_source_dijkstra(H,distance_metric, source, target)
    print 'Length'
    print length
    print 'Path:'
    print path
    try:
      print 'Path:'
      print path[target]
      print type(path[target]), len(path[target]), path[target]
      h = demand_flows_1[i]
      for node in path[target]:
          if node==source:
              node_1 = node
          else:
              ###K[h, node_1, node] = 1
              #K[h, node, node_1] = 1
              node_1 = node
    except KeyError:
        raise nx.NetworkXNoPath("node %s not reachable from %s" % (source, target))
demand_flows_this = []
This_green = []
i = 0
"""
for edge in green_edges_1:
    #demand_flows_this = []
    #This_green = []
    This_green.append(edge)
    SumDelta = 0
    SumTheta = 0
    OBJ = 0
    Deltah = []
    Thetah = []
    my_used_arcs = []
    name_flow='F%d'%(i)
    demand_flows_this.append(name_flow)
    i+=1
    [OBJ, Deltah, Thetah, H2, my_used_arcs] = optimal_SDN(H,This_green, K, demand_flows_this, w_l, w_h)
    for h in demand_flows_1:
        for i,j in H.edges():
            K[h,i,j] = 0
            if (my_used_arcs[h,i,j] ==1):
                K[h,i,j] = 1
            if (my_used_arcs[h,j,i] ==1):
                K[h,j,i] = 1
"""
print 'OBJECTIVE:'
print OBJ
print 'Deltah'
print Deltah
print 'Thetah'
print Thetah
print 'My Used Arcs:'
print my_used_arcs
#Diman: Uncomment here if you want not to use Dijkstra's shortest path
#K= my_used_arcs

for h in demand_flows_1:
    for i,j in H.edges():
        K[h,i,j] = 0
        if (my_used_arcs[h,i,j] ==1):
            K[h,i,j] = 1
        if (my_used_arcs[h,j,i] ==1):
            K[h,j,i] = 1

print 'Khij:'
print K
"""
for h in demand_flows_1:
    print 'h:'
    print h
    for i,j in H.edges():#arcs:
        K[h,i,j]= my_used_arcs[h,i,j]
        K[h,j,i]= my_used_arcs[h,i,j]
"""
###################################################
#Next round:######################################
OBJ = 0
Deltah = []
Thetah = []
my_used_arcs = []
w_l = 100#0.001 #100
w_h = 200#0.002 #200
Thr= Min_Hops*error #len(arcs)*disruption_value #var_distruption #len(arcs)/2
Thrh= float(Thr)/float(len(demand_flows))#Thrh*len(demand_flows)*0.8
#Thr = Thrh*len(demand_flows)
print 'Thr and Thrh: HEEEEEEEEEEEEEEEEEEEEEREEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE'
print Thrh, Thr, error
MaxCong = 1
Max_Time = 0
Total_Hop = 0
Total_ReRouted = 0
#[OBJ, Deltah, H3, my_used_arcs, MaxCong] 
[OBJ, Deltah, H3, my_used_arcs, Max_Time, Total_Hop, Total_ReRouted]= optimal_SDN_LP(H,green_edges, K, demand_flows, w_l, w_h, Thrh, Thr, weights)
##[OBJ, Deltah, Thetah, H3, my_used_arcs] = optimal_SDN(H,green_edges, K, demand_flows, w_l, w_h)
print 'OBJECTIVE:'
print OBJ
print 'Deltah'
print Deltah
print 'Thetah'
print Thetah
i = 0
Objective = 0
for h in demand_flows:
    SumDelta= SumDelta + Deltah[h]
    Objective += weights[i]*Deltah[h]
    i = i + 1
    #SumTheta = SumTheta + Thetah[h]
#print 'Sum Theta:'
#print SumTheta
print 'Sum Delta:'
print SumDelta
print 'My Used Arcs:'
print my_used_arcs

time_elapsed_optimal=round(time.time() - start_time_optimal,3)
print("--- %s seconds ---" % str(time_elapsed_optimal))
write_stat_time_simulation(path_to_stat_times,'OPT',filename_graph,int(sys.argv[5]),int(sys.argv[4]),seed_passed,number_of_couple,time_elapsed_optimal)
#sys.exit(0)
#Gap=time_elapsed_optimal/(len(nodes_recovered_optimal)*100)
#---------------------------------------------------------Expected -OPTIMAL-------------------------------------------------------
filename_stat='stat_simulations_'+filename_graph+"_Prob_"+str(prob_edge)+"_Alpha_"+str(alfa)+"_KHOP_"+str(K_HOPS)+"_distance_metric_"+str(distance_metric_passed)+"_type_of_bet_"+str(type_of_bet_passed)+"_always_put_monitor_"+str(always_split)+"_randomDisruption_"+str(random_disruption)+"_disruption_value_"+str(disruption_value)+"_error_"+str(error)+".txt"

#numero della simulazione corrente e scrivo statistiche
num_sim=get_num_simulation(path_to_file_simulation)

Nodes= len(H.nodes())
Edges = len(H.edges())
write_stat_SDN(path_to_stats,filename_stat,prob_edge,seed_random,alfa,
                          SumDelta,MaxCong,Objective,Total_Hop,Max_Time,Min_Hops, #Number of flows which get re-routed ,Number of flows which get delayed ,OPTIMAL Objective
                          num_sim,
                          flow_c_value,                                #Total demand of the graph, amount of flow for each demand pair
                          number_of_couple,                            #number of couples
                          Nodes,                                     #number of nodes
                          Edges)                                    #number of edges


"""
write_stat_num_reparation(path_to_stats,filename_stat,prob_edge,seed_random,alfa,
                          num_rip_isp_nodes,num_rip_isp_edges,nodes_truely_recovered_isp,edges_truely_recovered_isp, num_not_needed,        #ISP
                          num_rip_optimal_nodes,num_rip_optimal_edges,#OPTIMAL
                          num_rip_expected_optimal_nodes,num_rip_expected_optimal_edges,num_rip_expected_truely_optimal_nodes,num_rip_expected_truely_optimal_edges,#Expected,
                          num_rip_one_shot_expected_optimal_nodes,num_rip_one_shot_expected_optimal_edges,num_rip_one_shot_expected_truely_optimal_nodes,num_rip_one_shot_expected_truely_optimal_edges,#One Shot Expected,
                          num_rip_one_shot_expected_optimal_nodes,num_rip_one_shot_expected_optimal_edges,num_rip_BB_expected_truely_optimal_nodes,num_rip_BB_expected_truely_optimal_edges,#BB Expected,
                          num_rip_mult_nodes,num_rip_mult_edges,num_rip_truely_mult_nodes,num_rip_truely_mult_edges,       #Multicommodity generale
                          num_rip_mult_worst_nodes,num_rip_mult_worst_edges, #Multicommodity worst
                          num_rip_mult_best_nodes,num_rip_mult_best_edges,    #Multicommodity best
                          num_rip_shortest_nodes,num_rip_shortest_edges,num_rip_truely_shortest_nodes, num_rip_truely_shortest_edges,      #Shortest Based
                          num_rip_ranked_nodes,num_rip_ranked_edges,          #Ranked based
                          num_rip_all_nodes,num_rip_all_edges,                #All repairs algorithm
                          num_sim,
                          flag_solution_MCG,                                  #True se ho dovuto usare il MCG per terminare l'algoritmo
                          total_demand_of_graph,                                #Domanda totale sul grafo
                          demand_not_satisfied_sb,                             #Domanda non soddisfatta da shortest based
                          num_rip_all_nodes,num_rip_all_edges,
                          num_rip_all_nodes,num_rip_all_edges,
                          0,
                          flow_c_value,                                        #valore di flusso fixed assegnato per questa run
                          number_of_couple,                                     #numero di coppie scelto per rappresentare la domanda
                          var_distruption)
"""

