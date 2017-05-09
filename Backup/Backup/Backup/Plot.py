# Author: Diman Zad Tootaghaj
import pydot # import pydot or you're not going to get anywhere my friend :D
import networkx as nx
import my_draw as my_lib_var
import sys
#import winsound
import time
import itertools
from scipy import stats
import numpy as np
import copy
from numpy.linalg import svd
from my_draw import *
#from my_flows_lib import *
#from my_lib_optimal_recovery import *
#from my_lib_optimal_expected_recovery import *
#from my_lib_optimal_approx_max_flow import *
#from my_lib_optimal_expected_recovery_max_flow import *
#from my_lib_optimal_approx_recovery import *
#from my_lib_optimal_recovery_multicommodity import *
#from my_lib_optimal_recovery_multicommodity_maxFlow import *
#from my_lib_optimal_recovery_multicommodity_worst import *
#from my_lib_optimal_recovery_multicommodity_best import *
#from my_lib_check_routability import *
#from my_lib_compute_max_demand_in_the_graph import *
##from my_lib_optimal_tomography import *
#from my_lib_optimal_ILP_tomography import *
#from my_lib_optimal_LP_Relax_tomography import *
#from my_lib_optimal_ILP_tomography_prob import *
#from my_lib_optimal_LP_Relax_tomography_prob import *
#from my_lib_Max_rank import *
##from my_lib_optimal_risk_averse_expected_recovery import *
#from my_lib_optimal_risk_behavior_expected_recovery import *
#from numpy.linalg import matrix_rank

#https://www.diffchecker.com/efddo0xv

work_dir=os.getcwd()

path_to_dot_dir='../../../image_graph_dot/DotFile/'
path_to_image_dir='../../../image_graph_dot/immagini_generate/'
path_to_image_store='../../../image_graph_dot/store_images/'
path_to_stats='../../../image_graph_dot/stats/statistiche/'
path_to_file_simulation='../../../image_graph_dot/current_simulation.txt'
path_to_stat_prog='../../../image_graph_dot/stats/progress_iteration/'
path_to_stat_times='../../../image_graph_dot/stats/times/'


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
flow_c_value=int(sys.argv[9])
number_of_couple=int(sys.argv[10])
Percentage = float(sys.argv[18])
Monitors = int(sys.argv[17])
#fixed_distruption=str(sys.argv[11])
#var_distruption=float(sys.argv[12])
#K_HOPS=int(sys.argv[14])
#always_split=int(sys.argv[15])
#random_disruption=int(sys.argv[16])
#disruption_value=int(sys.argv[17])
#error=float(sys.argv[18])
#Gap=float(sys.argv[19])
ProbeCost = int(sys.argv[19])
#risk=int(sys.argv[20])

if sys.argv[13]!=None:
    filename_graph=str(sys.argv[13])
    print 'Graph: ' + filename_graph


path_to_graph= 'network topologies/'
path_to_graph=path_to_graph+filename_graph+'.gml'
path_to_folder_couple='distance_between_couples/'


H=nx.MultiGraph(nx.read_gml(path_to_graph))

prepare_graph(H)
my_draw(H,'CAIDA')



H=nx.MultiGraph(nx.read_gml(path_to_graph))  #grafo supply
prepare_graph(H)
nx.write_gml(H,"CAIDA.gml")


#distruggi di nuovo e recover whit multicommodity
#nodes_destroyed,edges_destroyed=destroy_graph(H,29,-95,10) #per abilene

my_draw(H,'7-destroyed_for_optimal')
#nx.draw(H)
graphDot=nx.to_pydot(H)

graphDot.write_png('1'+'.png')
mygraph=nx.read_gml(path_to_graph)

graphDot = nx.to_pydot(mygraph)

graphDot.write_png('CAIDA' +'.png')
