__author__ = 'Diman'

from gurobipy import *
from my_lib import *
import copy
from numpy.linalg import matrix_rank

# Model data

def MinProb(Cost_routing, R, R_LB, green_edges):
    MinProbeMonitors =[]
    MinProbe_Identi_link=[]
    Cost = 0
    RMin = []
    #########################GREEEDY BASED APPROACH###############################
    #Best_ILP_monitors, ILP_identifiable_links
    [MinProbMonitors, RMin, Cost, MinProbe_Identi_link] = MinProb_solution(Cost_routing, R, R_LB, green_edges)
    return MinProbMonitors, RMin, Cost, MinProbe_Identi_link

def MinProb_Iden(Cost_routing, R, R_LB, green_edges, Max_Ident):
    MinProbeMonitors =[]
    MinProbe_Identi_link=[]
    Cost = 0
    RMin = []
    #########################GREEEDY BASED APPROACH###############################
    #Best_ILP_monitors, ILP_identifiable_links
    [MinProbMonitors, RMin, Cost, MinProbe_Identi_link] = MinProb_Iden_solution(Cost_routing, R, R_LB, green_edges, Max_Ident)
    return MinProbMonitors, RMin, Cost, MinProbe_Identi_link



###
# Solve Min Prob to preserve the rank:
def MinProb_solution(Cost_routing, R, R_LB, green_edges):
    ########################START Greedy-Min-Prob Algorithm#######################################################
    ##Description: The algorithm starts by adding a path to the set of path that increase the rank most###########
    RMin=[]
    temp=[]
    IncreaseInRank=0
    currentRank =0
    Max_Increase =0
    sort_index = np.argsort(Cost_routing[:,0])
    Cost=0
    print 'Diman Sort naKarde'
    print Cost_routing
    print 'Diman Sort Karde!'
    print sort_index
    for i in sort_index:
      print 'I ro print kon'
      print i
      temp= copy.deepcopy(RMin)
      temp.append(i)
      IncreaseInRank=  matrix_rank(R_LB[temp,:]) - currentRank
      print 'Rank of R_LB, R'
      print matrix_rank(R_LB[temp,:])
      print 'IncreaseInRank'
      print IncreaseInRank
      print 'currentRank'
      print currentRank
      if i in RMin:
        RMin.remove(i)
      #temp.remove(i)
      if (IncreaseInRank > 0):
        #Print 'Yaftam!'
        #Max_Increase = IncreaseInRank
        RMin.append(i)
        currentRank= matrix_rank(R_LB[temp,:])
        Cost = Cost + Cost_routing[i,0]
      temp.remove(i)
    print 'Found R'
    print RMin
    #for x in RMin:
    print 'Rank:'
    print matrix_rank(R_LB[RMin,:])
    MinProbMonitors=[]
    for i in RMin:
      print 'This is which index'
      print i
      if green_edges[i][0] not in MinProbMonitors:
        print 'Source:'
        print green_edges[i][0]
        MinProbMonitors.append(green_edges[i][0])
      if green_edges[i][1] not in MinProbMonitors:
        print 'Destination:'
        print green_edges[i][1]
        MinProbMonitors.append(green_edges[i][1])

    ################################################################################
    TotalCost=0
    for i in sort_index:
      TotalCost = TotalCost + Cost_routing[i,0]
    #################################################################################
    MinProbeNull = null(R[RMin,:])
    print 'Null space of RMin'
    print MinProbeNull
    rows= len(MinProbeNull)
    columns = len(MinProbeNull.T)
    print 'Rows'
    print rows
    print 'Columns'
    print columns
    routing_rows = len(R[RMin,:])
    routing_columns = len(R[RMin,:].T)
    print 'Routing rows'
    print routing_rows
    print 'Routing Columns'
    print routing_columns
    iden =1
    MinProbe_Identi_link =0
    #for i in range(0,len(green_edges)-1):
    #  for j in range(0,len(my_null.T)-1):
    for i in range(0,rows):
      #print 'I ro print kon'
      #print i
      for j in range(0,columns):
        #print 'J ro print kon'
        #print j
        if (-1e-12 <MinProbeNull[i][j] < 1e-12) and (iden==1):
          iden=1
        else:
          iden=0
      if (iden == 1):
        MinProbe_Identi_link = MinProbe_Identi_link +1
        #print 'Which Row?'
        #print i
      iden=1
    #################################################################################
    print 'Number of Identofiable links:'
    print MinProbe_Identi_link
    print 'Rank of matrix:'
    print matrix_rank(R[temp,:])
    #################################################################################
    print 'Preserving rank, we have this many monitors:'
    print len(MinProbMonitors)
    print 'Minimum Number of Probes to preserve Rank:'
    print len(RMin)
    print 'Cost of Preserving Rank (Hop count):'
    print Cost
    print 'Total Cost if using all paths:'
    print TotalCost
    print '####################FINISHED MIN-Prob algorithm ######################'
    #############################################################################
    return MinProbMonitors, RMin, Cost, MinProbe_Identi_link

# Solve Min Prob to preserve the rank untill reaching identifiability:
def MinProb_Iden_solution(Cost_routing, R, R_LB, green_edges, Max_Ident):
    ########################START Greedy-Min-Prob Algorithm#######################################################
    ##Description: The algorithm starts by adding a path to the set of path that increase the rank most###########
    RMin=[]
    temp=[]
    Identifiability = 0
    IncreaseInRank=0
    currentRank =0
    Max_Increase =0
    sort_index = np.argsort(Cost_routing[:,0])
    Cost=0
    print 'Diman Sort naKarde'
    print Cost_routing
    print 'Diman Sort Karde!'
    print sort_index
    for i in sort_index:
      print 'I ro print kon'
      print i
      temp= copy.deepcopy(RMin)
      temp.append(i)
      IncreaseInRank=  matrix_rank(R_LB[temp,:]) - currentRank
      print 'Rank of R_LB, R'
      print matrix_rank(R_LB[temp,:])
      print 'IncreaseInRank'
      print IncreaseInRank
      print 'currentRank'
      print currentRank
      if i in RMin:
        RMin.remove(i)
      #temp.remove(i)
      if ((IncreaseInRank > 0) and (Identifiability < Max_Ident)):
        #Print 'Yaftam!'
        #Max_Increase = IncreaseInRank
        RMin.append(i)
        currentRank= matrix_rank(R_LB[temp,:])
        Cost = Cost + Cost_routing[i,0]
      temp.remove(i)
      Identifiability =  Find_Identifibility(RMin,R)
      print 'Identifiability'
      print Identifiability 
    print 'Found R'
    print RMin
    #Identifiability = Find_Identifibility(RMin,R)
    #for x in RMin:
    #print 'Identifiability'
    #print Identifiability
    print 'Rank:'
    print matrix_rank(R_LB[RMin,:])
    MinProbMonitors=[]
    for i in RMin:
      print 'This is which index'
      print i
      if green_edges[i][0] not in MinProbMonitors:
        print 'Source:'
        print green_edges[i][0]
        MinProbMonitors.append(green_edges[i][0])
      if green_edges[i][1] not in MinProbMonitors:
        print 'Destination:'
        print green_edges[i][1]
        MinProbMonitors.append(green_edges[i][1])

    ################################################################################
    TotalCost=0
    for i in sort_index:
      TotalCost = TotalCost + Cost_routing[i,0]
    #################################################################################
    MinProbeNull = null(R[RMin,:])
    print 'Null space of RMin'
    print MinProbeNull
    rows= len(MinProbeNull)
    columns = len(MinProbeNull.T)
    print 'Rows'
    print rows
    print 'Columns'
    print columns
    routing_rows = len(R[RMin,:])
    routing_columns = len(R[RMin,:].T)
    print 'Routing rows'
    print routing_rows
    print 'Routing Columns'
    print routing_columns
    iden =1
    MinProbe_Identi_link =0
    #for i in range(0,len(green_edges)-1):
    #  for j in range(0,len(my_null.T)-1):
    for i in range(0,rows):
      #print 'I ro print kon'
      #print i
      for j in range(0,columns):
        #print 'J ro print kon'
        #print j
        if (-1e-12 <MinProbeNull[i][j] < 1e-12) and (iden==1):
          iden=1
        else:
          iden=0
      if (iden == 1):
        MinProbe_Identi_link = MinProbe_Identi_link +1
        #print 'Which Row?'
        #print i
      iden=1
    #################################################################################
    print 'Number of Identofiable links:'
    print MinProbe_Identi_link
    print 'Rank of matrix:'
    print matrix_rank(R[temp,:])
    #################################################################################
    print 'Preserving rank, we have this many monitors:'
    print len(MinProbMonitors)
    print 'Minimum Number of Probes to preserve Rank:'
    print len(RMin)
    print 'Cost of Preserving Rank (Hop count):'
    print Cost
    print 'Total Cost if using all paths:'
    print TotalCost
    print '####################FINISHED MIN-Prob algorithm ######################'
    #############################################################################
    return MinProbMonitors, RMin, Cost, MinProbe_Identi_link


def Find_Identifibility(RMin,R):
    #################################################################################
    MinProbeNull = null(R[RMin,:])
    print 'Null space of RMin'
    print MinProbeNull
    rows= len(MinProbeNull)
    columns = len(MinProbeNull.T)
    print 'Rows'
    print rows
    print 'Columns'
    print columns
    routing_rows = len(R[RMin,:])
    routing_columns = len(R[RMin,:].T)
    print 'Routing rows'
    print routing_rows
    print 'Routing Columns'
    print routing_columns
    iden =1
    MinProbe_Identi_link =0
    #for i in range(0,len(green_edges)-1):
    #  for j in range(0,len(my_null.T)-1):
    for i in range(0,rows):
      #print 'I ro print kon'
      #print i
      for j in range(0,columns):
        #print 'J ro print kon'
        #print j
        if (-1e-12 <MinProbeNull[i][j] < 1e-12) and (iden==1):
          iden=1
        else:
          iden=0
      if (iden == 1):
        MinProbe_Identi_link = MinProbe_Identi_link +1
        #print 'Which Row?'
        #print i
      iden=1
    #################################################################################
    return MinProbe_Identi_link
