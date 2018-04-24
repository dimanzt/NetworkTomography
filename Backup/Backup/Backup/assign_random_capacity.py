import pydot # import pydot or you're not going to get anywhere my friend :D
import networkx as nx
import my_lib as my_lib_var
import sys
#import winsound
import time
from scipy import stats
from my_lib import *
from my_flows_lib import *
from my_lib_optimal_recovery import *
from my_lib_optimal_recovery_multicommodity import *
from my_lib_optimal_recovery_multicommodity_worst import *
from my_lib_optimal_recovery_multicommodity_best import *
from my_lib_check_routability import *
from my_lib_compute_max_demand_in_the_graph import *

#filename_graph= '600_800_Random_Capacity'
filename_graph='erdos_renyi_graph_100_nodes_2977_edges_Diman'#'DeltaCom_Connettivity_Random_Capacity_High'#'erdos_renyi_graph_100_nodes_231_edges_Random' #'Abilene'
# erdos_renyi_graph_100_nodes_2977_edges
path_to_graph= 'network topologies/'
path_to_graph=path_to_graph+filename_graph+'.gml'
H=nx.MultiGraph(nx.read_gml(path_to_graph))


assign_random_capacity_to_edges(H,filename_graph)
