__author__ = 'Diman'

from gurobipy import *

# Model data

def optimal_LP_tomography_prob(my_path_comb,my_objects, Max_prob_Cost, My_probes, Cost_routing):
    Best_ILP_paths=[]
    ILP_identifiable_links=[]
    #########################GREEEDY BASED APPROACH###############################
    Best_greedy=0
    Best_greedy_paths=[]
    Identified_links=[]
    """
    #for obj in my_objects:
        #print obj.e
        #print obj.m
        #print obj.n
    #print '########################START MONITOR LISTS###################'
    #for mon in my_path_comb:
        #print 'Identifiable_Links:'
        #print mon.ident
        #print 'Number:'
        #print mon.num
        #print 'Monitor Combination:'
        #print mon.monitors
    """
    Best_ILP_paths, ILP_identifiable_links = LP_solution_best_prob(my_path_comb, my_objects, Max_prob_Cost, My_probes, Cost_routing)

    return Best_ILP_paths, ILP_identifiable_links
###
# Solve ILP of max flow problem where the Sets are given and each set can identify a set of links,

def LP_solution_best_prob(my_path_comb, my_objects, Max_prob_Cost, My_probes, Cost_routing):
    Best_ILP_paths=[]
    ILP_identifiable_links=[]
    #########################GREEEDY BASED APPROACH###############################
    Best_greedy=0
    Best_greedy_paths=[]
    Identified_links=[]
    Edges=[]

    #All Edges and set of moniotrs that can identify them
    for obj in my_objects:
        #print obj.e
        #print obj.m
        #print obj.n
        if obj.n not in Edges:
            Edges.append(obj.n)
    #print '########################START MONITOR LISTS###################'
    #All monitors and set of edges that can be identified by them
    #for mon in my_path_comb:
        #print 'Identifiable_Links:'
        #print mon.ident
        #print 'Number:'
        #print mon.num
        #print 'Monitor Combination:'
        #print mon.monitors
    

    # Create optimization model
    # Xl = Identifiable links,
    # Zs = Selected Sets
    # Yv = Selected Monitors 
    my_Model = Model('maxCoverage')
    Yv = {}
    Xl = {}
    Zs = {}
    #GRB.CONTINUOUS GRB.BINARY
    for m in My_probes:
        Yv[m] = my_Model.addVar(ub=1,lb=0, vtype=GRB.BINARY, name='Selected_Paths%s'% (m))  #m_cost[m], 
    for e in Edges:
        Xl[e] = my_Model.addVar(ub =1,lb=0, vtype=GRB.BINARY, name='Identified_Links%s'% (e)) 
    for mon in my_path_comb:
        Zs[mon.num] = my_Model.addVar(ub=1,lb=0, vtype=GRB.CONTINUOUS, name='Selected_Set%s'% (mon.num) )
    my_Model.update()
    my_Model.addConstr(quicksum(Cost_routing[m,0]*Yv[m] for m in My_probes) <= Max_prob_Cost, 'Max_Monitors')
    #This part is not completely correct:
    for obj in my_objects:
        my_Model.addConstr(Xl[obj.n] <= quicksum(Zs[i] for i in obj.mon_num), 'Identifiable_links' )
    my_Model.update()
    #This constraint Zs <= Yv for \each s and \each v \in Ms:
    for mon in my_path_comb:
        i= mon.num
        #print i
        #print type(i)
        #print mon.ident
        for j in mon.monitors:
            #print 'Identifiable links:'
            #print j
            #if j:
                #k= (int)j
            my_Model.addConstr(Zs[i] <= Yv[j], 'Coverage' )

    #for mon in my_path_comb:
    #    i= mon.num
    #    for j in mon.ident:
    #        #if j:
    #        my_Model.addConstr(Zs[i] <= Xl[j], 'LinkCoverage')
    #for obj in my_objects:
    #    for m in obj.m
    #        m.addConstr(quicksum() <= )

    my_Model.update()
    # Set objective
    my_Model.setObjective(quicksum(Xl[l] for l in Edges), GRB.MAXIMIZE)

    my_Model.update()
    my_Model.setParam('MIPGap',0.5)
    #m.setParam('MIPGAPABS',2)
    #m.setParam('ITERATION_LIMIT',Gaps)
    #m.params.timeLimit = Gaps
    #m.setParam('IterationLimit',Gaps)
    #m.setParam('TimeLimit', Gaps)
    my_Model.update()
    my_Model.optimize()

    if my_Model.status == GRB.status.OPTIMAL:

        ILP_identifiable_links=[]#my_used_arc=[]
        Best_ILP_paths=[]#my_used_vertex=[]
        Best_Selected_Sets=[]
        for m in My_probes:
           var_reference = my_Model.getVarByName('Selected_Paths%s'% (m))    #selected monitor
           if var_reference.x>0:
                print var_reference.x
                Best_ILP_paths.append(m)
                print 'BEST MONITORSSSSSSSSSSSSSSSSSSSSSSS'
                print Best_ILP_paths

        for e in Edges:
            var_reference=my_Model.getVarByName('Identified_Links%s'% (e))
            if var_reference.x>0:
                print var_reference.x
                if e not in ILP_identifiable_links:
                  ILP_identifiable_links.append(e)
                print 'IDENTIFIED LINKSSSSSSSSSSSSSSSSSS:'
                print ILP_identifiable_links
        for mon in my_path_comb:
            i = mon.num
            var_reference=my_Model.getVarByName('Selected_Set%s' % (mon.num))
            if var_reference.x >0:
                print var_reference.x
                print 'Selected_Set'
                Best_Selected_Sets.append(i)
                print Best_Selected_Sets
    #print 'YOHOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO'
    #print Best_ILP_paths
    #print ILP_identifiable_links
    return Best_ILP_paths, ILP_identifiable_links

