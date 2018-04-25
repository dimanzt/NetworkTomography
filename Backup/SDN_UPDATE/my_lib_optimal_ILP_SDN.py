__author__ = 'Diman Zad Tootaghaj'
#We try to minimize the applications disruption during rule uodates in Software Defined Networking!
#We consider two types of disrution: 1) Disruption due to re-routing of the existing flows which might cause a security hole, 2) Disruption due to delay of the existing flows which cross an updated SDN switch.
# Deltah is to defined to consider ithe re-routing disrupton and Thetah considers the second disruption
from gurobipy import *

# Model data, get the nodes and capacity from a graph H
def optimal_SDN(H,green_edges, K, demand_flows, w_l, w_h):
    print "Start running the ILP formulation for SDN recovery"
    nodes=[]
    #construct the array nodes:
    for node in H.nodes():
        nodes.append(node)
    """
    demand_flows=[]
    #construct demand_flows array:
    i=0
    for edge in green_edges:
        name_flow='F%d'%(i)
        demand_flows.append(name_flow)
        i+=1
    """
    arcs=[]
    capacity={}
    #construct arcs array and capacity:
    #for edge in H.edges(data=True):
    #    print edge

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

    #vertex_cost={}
    #construct vertex costs array:
    #Diman: We don't need cost for nodes or edges right now:
    #for i in H.nodes():
    #    node_cost=0
    #    if H.node[i]['status']=='destroyed':
    #        node_cost=1
    #
    #    id_node=H.node[i]['id']
    #    if not vertex_cost.has_key(id_node):
    #        vertex_cost.update({id_node:node_cost})
    #    else:
    #        print 'ERROR vertex cost'


    #arc_cost={}
    """
    K_ij = {}
    i =0
    for edge in green_edges:
        id_source=edge[0]
        id_target=edge[1]
        demand=edge[2]
        flow_label=demand_flows[i]
        for edge in arcs: 
            id_source= edge[0]
            id_target= edge[1]
            keydict=H[id_source][id_target]
            for k in keydict:
              if H[id_source][id_target][k]['type']=='normal':
                  edge_used = 0
                  if H[id_source][id_target][k]['status'] == 'used':
                      edge_used = 1
                  edge_tupla_1=(id_source,id_target)
                  if not K_ij.has_key(edge_tupla_1):
                      K_ij.update({edge_tupla_1:edge_used})
                  else:
                      print 'ERROR'
    """
    #for edge in H.edges():
    """
    for edge in arcs:
        id_source=edge[0]
        id_target=edge[1]
        keydict=H[id_source][id_target]
        for k in keydict:
            if H[id_source][id_target][k]['type']=='normal':# and H[id_source][id_target][k]['type']!='green':
                edge_cost=0
                if H[id_source][id_target][k]['status']=='destroyed':
                    edge_cost=1

                edge_tupla_1=(id_source,id_target)
                #edge_tupla_2=(id_target,id_source)
                if not arc_cost.has_key(edge_tupla_1):
                    arc_cost.update({edge_tupla_1:edge_cost})
                    #arc_cost.update({edge_tupla_2:edge_cost})
                else:
                    print 'ERROR'
    """
    inflow={}
    demand_value={}
    #construct inflow array:
    i=0
    for edge in green_edges:
        id_source=edge[0]
        id_target=edge[1]
        demand=edge[2]
        flow_label=demand_flows[i]
        flow_value = demand
        if not demand_value.has_key(flow_label):
            demand_value.update({flow_label:flow_value})
        for node in nodes:
            flow_value=0
            flow_b_value=0
            if str(node)==str(id_source):
                flow_b_value=1#demand
                #flow_value= demand
            if str(node)==str(id_target):
                flow_b_value=-1#demand
                #flow_value=-demand

            tupla_key=(flow_label,node)
            if not inflow.has_key(tupla_key):
                inflow.update({tupla_key:flow_b_value})
                #demand_value.update({tupla_key:flow_value}
            else:
                print 'ERROR'
            #if not demand_value.has_key(tupla_key):
            #    demand_value.update({tupla_key:flow_value})
            #else:
            #    print 'ERROR'
        i+=1

    """
    nodes_used=[]
    edges_used=[]
    nodes_repaired=[]
    edges_repaired=[]
    """

    my_altered_switches=[]
    my_used_arc=[]
    my_delta=[]
    my_theta=[]

    #Deltah, Thetah, Used_Edges
    my_altered_switches,my_used_arc, my_delta, my_theta =optimize_SDN(H,nodes,demand_flows,arcs,capacity,K,inflow, demand_value, w_l, w_h)

    print 'Rerouted flows'
    print my_delta #Deltah
    print 'Delayed flows'
    print my_theta #Thetah
    #print 'Used Edges'
    #print  my_used_arc#Used_Edges
    """
    for node in nodes_used:
        if H.node[node]['status']=='destroyed':
            nodes_repaired.append(node)
    """
    for edge in arcs:# Used_Edges:#edges_used:
        id_source=edge[0]
        id_target=edge[1]
        keydict=H[id_source][id_target]
        for k in keydict:
            if H[id_source][id_target][k]['type']=='normal':# and H[id_source][id_target][k]['type']!='green':
                if edge in my_used_arc: #Used_Edges:# H[id_source][id_target][k]['status']=='':#'destroyed':
                    #edges_repaired.append(edge)
                    H[id_source][id_target][k]['status'] = 'used'
                elif edge not in my_used_arc: #Used_Edges:
                    H[id_source][id_target][k]['status'] = 'on'
    #We give higher priority to the first type of disruption which is the flow re-routes
    w_low = 1
    w_high = 2
    Objective = 0
    #for i in range(0,len(my_delta)): #Deltah:
    for i in demand_flows:
      print 'Delta:'
      print my_delta[i]
      Objective = w_h*float(my_delta[i]) + Objective
    #for i in range(0, len(my_theta)): #Thetah:
    for i in demand_flows:
      print 'Theta:'
      print my_theta[i]
      Objective = w_l*float(my_theta[i]) + Objective
    return Objective, my_delta, my_theta, H, my_used_arc #Deltah, Thetah, H



def optimize_SDN(H,nodes,demand_flows,arcs,capacity,K,inflow, demand_value, w_l, w_h):

    dmax=100
    #print 'USED EDGES:'
    #print K
    # Create optimization model
    m = Model('SDN_Disruption')
    # Create variables
    x = {}
    #X_ij is a variable that shows which edges will be used after the optimization
    for h in demand_flows:
        for i,j in arcs:
            x[h,i,j] = m.addVar(ub=1, obj=1, vtype=GRB.BINARY,
                                   name='x_%s_%s_%s' % (h, i, j))
            x[h,j,i] = m.addVar(ub=1, obj=1, vtype=GRB.BINARY,
                                   name='x_r_%s_%s_%s' % (h, j, i))
    m.update()
    #Add Deltah for re-routing cost which has a higher cost, we give 2 
    Deltah = {}
    for h in demand_flows:
        Deltah[h] = m.addVar(ub=1, obj=w_h, vtype=GRB.BINARY, name='Deltah_%s' % (h)) # 2.0
    m.update()
    #Add Thetah for existing flows which are not being re-routed but cross through an updated switch we give lower cost (1) to them
    Thetah = {}
    for h in demand_flows:
        Thetah[h] = m.addVar(ub=1, obj=w_l, vtype=GRB.BINARY, name='Thetah_%s' % (h)) # 1.0
    m.update()
    #Add and auxiulary variable to indicate altered switches:
    t = {}
    for i in nodes:
        t[i]= m.addVar(ub=1, obj=0.0, vtype=GRB.BINARY, name='T_%s' % (i))
    m.update()
    #I don't need the cost of nodes or edges for now:
    """
    usedArc = {}
    for i,j in arcs:
        usedArc[i,j] = m.addVar(ub=1, obj=arc_cost[i,j], vtype=GRB.BINARY, name='usedArc_%s_%s' % (i,j))
        usedArc[j,i] = m.addVar(ub=1, obj=arc_cost[i,j], vtype=GRB.BINARY, name='usedArc_%s_%s' % (j,i))


    m.update()

    usedVertex = {}
    for i in nodes:
        usedVertex[i] = m.addVar(ub=1, obj=vertex_cost[i], vtype=GRB.BINARY, name='usedVertex_%s' % (i))
    m.update()
    """


    # Flow conservation constraints
    for h in demand_flows:
        for i in nodes:
            list=[]
            list.extend(arcs.select('*',i))
            list.extend(arcs.select(i,'*'))
            to_i=[]
            from_i=[]
            for index in range(0,len(list)):
                id_source=(list[index])[0]
                id_target=(list[index])[1]
                edge=(id_source,id_target)
                reverse_edge=(id_target,id_source)
                if edge[0]==i:
                    if edge not in from_i:
                        from_i.append(edge)
                    if reverse_edge not in to_i:
                        to_i.append(reverse_edge)
                elif edge[1]==i:
                    if reverse_edge not in from_i:
                        from_i.append(reverse_edge)
                    if edge not in to_i:
                        to_i.append(edge)
                else:
                    print 'ERROR'
                    print i,edge
            #print 'node i:'
            #print i
            #print 'inflow[h,i], for h'
            #print inflow[h,i], h
            #m.addConstr( (quicksum(x[h,k,i] for k,i in to_i) + inflow[h,i]) == (quicksum(x[h,i,j] for i,j in from_i)),'node_%s_%s' % (h, i))
            m.addConstr( (quicksum(x[h,k,i] for k in H.neighbors(i)) + inflow[h,i]) == (quicksum(x[h,i,j] for j in H.neighbors(i))),'node_%s_%s' % (h, i))

    m.update()
    print 'Demand Value:'
    print demand_value
    # Arc capacity constraints 
    for i,j in arcs:
        #print 'Capacity:'
        #print capacity[i,j]
        m.addConstr(quicksum(x[h,i,j]*demand_value[h]+x[h,j,i]*demand_value[h] for h in demand_flows) <= capacity[i,j], 'cap_%s_%s' % (i, j))
    m.update()
    #Add Constraint to ensure one disruption is counted at a time
    for h in demand_flows:
        m.addConstr((Deltah[h]+ Thetah[h]) <= 1, 'OneDisruption_%s' % (h))
    m.update()
    #Add Constraint to ensure \delta is 1 only when there is a re-routing of the exisiting flows:
    for h in demand_flows:
        m.addConstr(((quicksum(x[h,i,j]+K[h,i,j]-2*x[h,i,j]*K[h,i,j] for i,j in arcs)))  <= (Deltah[h]*len(arcs)), 'ReRoutingDis_%s' % (h))
    m.update()
    #Add Constraint to make sure \delta is 1 once both delta and theta can be one
    for h in demand_flows:
        for i in nodes:
            #print 'Neighbors:'
            #print H.neighbors(i)
            #print 'h,i,j:'
            #print h,i,j 
            m.addConstr(((quicksum(x[h,i,j] for j in H.neighbors(i))) +len(H.neighbors(i))*(t[i] -1)) <= (len(H.neighbors(i))*(Deltah[h] + Thetah[h])) , 'Deltah_%s_%s' % (h, i) )
    m.update()
    #Add constraint to make sure the altered switches are marked with t_i = 1
    for i in nodes:
        m.addConstr(((quicksum(x[h,i,j]+K[h,i,j] -2*x[h,i,j]*K[h,i,j] for h in demand_flows for j in H.neighbors(i)))) <= (len(nodes)*len(demand_flows)*t[i]) , 'AlteredSwitch_%s' % (i))
    m.update()
    #Add Constraint to make sure t_i is zero when both K[ij] and x[ij] are zero:
    for i in nodes:
        m.addConstr(t[i] <= (quicksum(x[h,i,j]+K[h,i,j] -2*x[h,i,j]*K[h,i,j] for h in demand_flows for j in H.neighbors(i))), 'ZerosAltSwitch_%s' % (i))
    m.update()

    """
    for i in nodes:

        arcs_inc_i=[]
        arcs_inc_i.extend(arcs.select(i,'*'))
        arcs_inc_i.extend(arcs.select('*',i))
        m.addConstr(quicksum(usedArc[i,j] for i,j in arcs_inc_i) <=usedVertex[i]*dmax,'nodeRec_%s' % (i))

    m.update()

    #positiveness
    for h in demand_flows:
        for i,j in arcs:
            m.addConstr(flow[h,i,j]>=0)

    m.update()
    """
    m.optimize()

    if m.status == GRB.status.OPTIMAL:


        my_used_arc={}#[]
        my_altered_switch={}#[]
        my_delta={}#[]
        my_theta={}#[]
        #Start finding the solution after the optimization for used arc in h:
        for h in demand_flows:
            for i,j in arcs:
                var_reference = m.getVarByName('x_%s_%s_%s' %(h, i, j)) #used arc for flow h
                var_reference_reverse = m.getVarByName('x_r_%s_%s_%s' %(h, j, i))
                my_used_arc[h,i,j] =0
                my_used_arc[h,j,i] =0
                if var_reference.x>0:# or var_reference_reverse.x>0:
                    This= (i,j,h)
                    my_used_arc[h,i,j] = 1
                if var_reference_reverse.x>0:
                    my_used_arc[h,j,i] = 1

        #Start finding the solution for the altered switches:
        for i in nodes:
            var_reference = m.getVarByName('T_%s' %(i))
            my_altered_switch[i] = 0
            if var_reference.x>0:
                my_altered_switch[i] = 1

        #Start finding the solution for Delta_h
        for h in demand_flows:
            var_reference = m.getVarByName('Deltah_%s' %(h))
            my_delta[h] = 0
            if var_reference.x>0:
                my_delta[h] =1

        #Start finding the solution for Theta_h
        for h in demand_flows:
            var_reference = m.getVarByName('Thetah_%s' %(h))
            my_theta[h] = 0
            if var_reference.x>0:
              my_theta[h] = 1
    
        """
        for i,j in arcs:
           var_reference = m.getVarByName('usedArc_%s_%s' % (i,j))    #edge ij
           var_reference_reverse=m.getVarByName('usedArc_%s_%s'%(j,i)) #edge ji
           if var_reference.x>0 or var_reference_reverse.x>0:
                if arc_cost[i,j]!=0:
                    edge=(i,j)
                    my_used_arc.append(edge)

        for i in nodes:
            var_reference=m.getVarByName('usedVertex_%s'%(i))
            #print var_reference, var_reference.x
            if var_reference.x>0:
                if vertex_cost[i] !=0:
                    my_used_vertex.append(i)
        """
        print 'Solution:'
        print('The optimal objective is %g' % m.objVal)
        print 'My Altered Switches:'
        print my_altered_switch
        return my_altered_switch,my_used_arc, my_delta, my_theta
