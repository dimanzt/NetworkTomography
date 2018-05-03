__author__ = 'Diman Zad Tootaghaj'
#We try to minimize the applications disruption during rule uodates in Software Defined Networking!
#We consider two types of disrution: 1) Disruption due to re-routing of the existing flows which might cause a security hole, 2) Disruption due to delay of the existing flows which cross an updated SDN switch.
# Deltah is to defined to consider ithe re-routing disrupton and Thetah considers the second disruption
from gurobipy import *
import networkx as nx
import random

# Model data, get the nodes and capacity from a graph H
def optimal_SDN_ILP(H,green_edges, K, demand_flows, w_l, w_h, Thrh, Thr, weights):
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
    Max_Time = 0
    Total_Hop = 0
    Total_ReRouted = 0
    #my_altered_switches=[]
    my_used_arc=[]
    my_delta=[]
    MaxCong = 1
    #my_theta=[]

    #Deltah, Thetah, Used_Edges
    #Time,my_used_arc, my_delta, MaxCong =optimize_SDN(H,nodes,demand_flows,green_edges,arcs,capacity,K,inflow, demand_value, w_l, w_h, Thrh, Thr)
    Max_Time,my_used_arc, my_delta, Total_Hop, Total_ReRouted = optimize_SDN(H,nodes,demand_flows,green_edges,arcs,capacity,K,inflow, demand_value, w_l, w_h, Thrh, Thr, weights)
    print 'Rerouted flows'
    print my_delta #Deltah
    print 'Delayed flows'
    #print my_theta #Thetah
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
    """
    for i in demand_flows:
      #print 'Theta:'
      #print my_theta[i]
      Objective = w_l*float(my_theta[i]) + Objective
    """
    return Objective, my_delta, H, my_used_arc, Max_Time, Total_Hop, Total_ReRouted#MaxCong #Deltah, Thetah, H



def optimize_SDN(H,nodes,demand_flows,green_edges,arcs,capacity,K,inflow, demand_value, w_l, w_h, Thrh, Thr, weights):

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
    i = 0
    for h in demand_flows:
        Deltah[h] = m.addVar(ub=1, obj=w_h*weights[i], vtype=GRB.BINARY, name='Deltah_%s' % (h)) # 2.0
        #Deltah[h] = m.addVar(ub=1, obj=100, vtype=GRB.BINARY, name='Deltah_%s' % (h)) # 2.0
        i = i + 1
    m.update()
    #Add Thetah for existing flows which are not being re-routed but cross through an updated switch we give lower cost (1) to them
    #Thetah = {}
    #for h in demand_flows:
    #    Thetah[h] = m.addVar(ub=1, obj=w_l, vtype=GRB.BINARY, name='Thetah_%s' % (h)) # 1.0
    #m.update()
    #Add and auxiulary variable to indicate altered switches:
    t = {}
    for i in nodes:
      for h in demand_flows:
        t[i,h] = m.addVar(ub=1, obj=0.0, vtype=GRB.BINARY, name='T_%s_%s' % (i,h))
    m.update()
    T = {}
    T[1]= m.addVar(ub=len(demand_flows), obj=0.0, vtype=GRB.CONTINUOUS, name='StragglerT')
    m.update()
    """
    t = {}
    for i in nodes:
        t[i]= m.addVar(ub=1, obj=0.0, vtype=GRB.BINARY, name='T_%s' % (i))
    m.update()
    """
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
    #for h in demand_flows:
    #    m.addConstr((Deltah[h]+ Thetah[h]) <= 1, 'OneDisruption_%s' % (h))
    #m.update()
    #Add Constraint to ensure \delta is 1 only when there is a re-routing of the exisiting flows:
    for h in demand_flows:
        m.addConstr(((quicksum(x[h,i,j]+K[h,i,j]-2*x[h,i,j]*K[h,i,j] for i,j in arcs)))  <= (Deltah[h]*len(arcs)), 'ReRoutingDis_%s' % (h))
    m.update()
    #Add Constraint per flow QoS:
    #Thrh= len(arcs)/2
    for h in demand_flows:
        m.addConstr((quicksum(x[h,i,j]+x[h,j,i] for i,j in arcs) <= Thrh), 'Qosh_%s' % (h))
    m.update()
    #Thr= Thrh*len(demand_flows)*0.8
    m.addConstr((quicksum(x[h,i,j]+x[h,j,i] for h in demand_flows for i,j in arcs) <= Thr), 'TotalQos_%s' % (h))
    m.update()
    #Add a constraint for altered switches for each flow, t[i,h]= 1:
    for i in nodes:
        for h in demand_flows:
            m.addConstr(((quicksum(x[h,i,j]+K[h,i,j] -2*x[h,i,j]*K[h,i,j] for j in H.neighbors(i)))) <= (len(nodes)*t[i,h]) , 'AlteredSwitch_%s_%s' % (i,h))
    m.update()

    for i in nodes:
        for h in demand_flows:
            m.addConstr(t[i,h] <= ((quicksum(x[h,i,j]+K[h,i,j] -2*x[h,i,j]*K[h,i,j] for j in H.neighbors(i)))) , 'ZeroAlteredSwitch_%s_%s' % (i,h))
    m.update()
    for i in nodes:
        m.addConstr((quicksum(t[i,h] for h in demand_flows)) <= T[1], 'StragglerConst_%s' % (i))
    m.update()
    #Add Constraint to make sure \delta is 1 once both delta and theta can be one
    """
    for h in demand_flows:
        for i in nodes:
            #print 'Neighbors:'
            #print H.neighbors(i)
            #print 'h,i,j:'
            #print h,i,j 
            m.addConstr(((quicksum(x[h,i,j] for j in H.neighbors(i))) +len(H.neighbors(i))*(t[i] -1)) <= (len(H.neighbors(i))*(Deltah[h] + Thetah[h])) , 'Deltah_%s_%s' % (h, i) )
    m.update()
    """
    #Add constraint to make sure the altered switches are marked with t_i = 1
    """
    for i in nodes:
        m.addConstr(((quicksum(x[h,i,j]+K[h,i,j] -2*x[h,i,j]*K[h,i,j] for h in demand_flows for j in H.neighbors(i)))) <= (len(nodes)*len(demand_flows)*t[i]) , 'AlteredSwitch_%s' % (i))
    m.update()
    """
    #Add Constraint to make sure t_i is zero when both K[ij] and x[ij] are zero:
    """
    for i in nodes:
        m.addConstr(t[i] <= (quicksum(x[h,i,j]+K[h,i,j] -2*x[h,i,j]*K[h,i,j] for h in demand_flows for j in H.neighbors(i))), 'ZerosAltSwitch_%s' % (i))
    m.update()
    """
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

        Total_Hop=0
        my_used_arc={}#[]
        RR_used_arc = {}
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
                RR_used_arc[h,i,j] =0
                RR_used_arc[h,j,i] =0
                if var_reference.x>0:# or var_reference_reverse.x>0:
                    This= (i,j,h)
                    my_used_arc[h,i,j] = 1
                    Total_Hop= Total_Hop + 1
                if var_reference_reverse.x>0:
                    my_used_arc[h,j,i] = 1
                    Total_Hop= Total_Hop + 1
        ##############################################################
        #Define used capacity
        Usedcapacity={}
        for edge in H.edges():
            id_source=edge[0]
            id_target=edge[1]
            keydict=H[id_source][id_target]
            arc=(id_source,id_target)
            for k in keydict:
                if H[id_source][id_target][k]['type']=='normal':# and H[id_source][id_target][k]['type']!='green':
                    cap=0
                    if not Usedcapacity.has_key(arc):
                        Usedcapacity.update({arc:cap})
                    else:
                        print 'ERROR'
                        print arc    
        ##############################################################
        """
        #Use Random Rounding to select one path for each demand flow:
        g_edge_cnt = 0
        for h in demand_flows:
          edge = green_edges[g_edge_cnt]
          g_edge_cnt = g_edge_cnt + 1
          print 'RANDOM ROUNDING edge'
          print edge
          source = edge[0]
          target = edge[1]
          H_temp=nx.Graph()
          for i,j in arcs:
            if i not in H_temp.nodes():
              H_temp.add_node(i)
            if j not in H_temp.nodes():
              H_temp.add_node(j)
            if (i,j) not in H_temp.edges():
              H_temp.add_edge(i,j)
          paths = [p for p in nx.all_shortest_paths(H_temp, source, target)]
          Total_Cap = 0
          path_probabilities = []
          selected_path = []
          for p in paths:
            length_path = len(p)
            if (p[0], p[1]) in H.edges():
              Min_Capacity = capacity[p[0],p[1]]
            if (p[1],p[0]) in H.edges():
              Min_Capacity = capacity[p[1], p[0]]
            for i in range(0, length_path-1):
               if (p[i],p[i+1]) in H.edges():
                  if (capacity[p[i],p[i+1]] < Min_Capacity):
                      Min_Capacity = capacity[p[i],p[i+1]]
               if (p[i+1],p[i]) in H.edges():
                  if (capacity[p[i+1],p[i]] < Min_Capacity):
                      Min_Capacity = capacity[p[i+1],p[i]]
            path_probabilities.append(Min_Capacity)
            #if not Usedcapacity.has_key(arc):
            #Usedcapacity.update({arc:cap})
            selected_path.append(p)
            Total_Cap = Total_Cap + Min_Capacity
          #Select one path based on the probabilities:
          ranm = random.randint(0, Total_Cap)
          cnt =0
          minbound = 0
          for x in path_probabilities:
            if (ranm >= minbound) and (ranm <= (minbound +x )):
              #The path paths[cnt] is selected;
              Sel_path= paths[cnt]
              length_selected = len(Sel_path)
              for i in range(0, length_selected -1):
                RR_used_arc[h,Sel_path[i],Sel_path[i+1]] = 1
                RR_used_arc[h,Sel_path[i+1],Sel_path[i]] = 1
                if (Sel_path[i], Sel_path[i+1]) in H.edges():
                    new_cap = Usedcapacity[Sel_path[i],Sel_path[i+1]]
                    new_cap = new_cap + demand_value[h]
                    Usedcapacity.update({(Sel_path[i],Sel_path[i+1]):new_cap})
                if (Sel_path[i+1], Sel_path[i]) in H.edges():
                    new_cap = Usedcapacity[Sel_path[i+1],Sel_path[i]]
                    new_cap = new_cap + demand_value[h]
                    Usedcapacity.update({(Sel_path[i+1],Sel_path[i]):new_cap})
                #Usedcapacity[Sel_path[i],Sel_path[i+1]] = demand_value[h] + Usedcapacity[Sel_path[i],Sel_path[i+1]]
            minbound = minbound + x
            cnt = cnt+1
        ######################################################################
        #Compute the maximum amount of congestion: That is for all i,j \in E Usedcapacity < MaxCong
        MaxCong = 1
        for edge in H.edges():
          id_source=edge[0]
          id_target=edge[1]
          if float(Usedcapacity[id_source, id_target])/float(capacity[id_source,id_target]) > MaxCong:
            MaxCong = float(Usedcapacity[id_source, id_target])/float(capacity[id_source,id_target])
        #Start finding the solution for the altered switches:
        """
        """
        for i in nodes:
            var_reference = m.getVarByName('T_%s' %(i))
            my_altered_switch[i] = 0
            if var_reference.x>0:
                my_altered_switch[i] = 1
        """
        #for i in nodes:
        #  for h in demand_flows:
        #      var_reference = m.getVarByName('T_%s_%s', %(i,h))
        #      my_altered_switch[i] = 0
        #      if var_reference.x>0:
        #          my_altered_switch[i] = 1
        #Start finding the straggler Time:
        Time= 0
        Max_Time = 0
        for i in nodes:
            for h in demand_flows:
                var_reference = m.getVarByName('T_%s_%s' % (i,h))
                if var_reference.x >0:
                    Time = Time + 1
            if (Time > Max_Time):
                Max_Time = Time
            Time = 0
        var_reference = m.getVarByName('StragglerT')
        print 'var_reference:'
        print var_reference
        print var_reference.x
        if var_reference.x>0:
            Time = var_reference.x
        #Start finding the solution for Delta_h
        Total_ReRouted= 0
        for h in demand_flows:
            var_reference = m.getVarByName('Deltah_%s' %(h))
            my_delta[h] = 0
            if var_reference.x>0:
                my_delta[h] =1
                Total_ReRouted = Total_ReRouted + 1
        print 'Path Length:'
        print Total_Hop
        print 'Straggler Time:'
        print Max_Time
        print 'Time:'
        print Time
        print 'Total Rerouted Flows:'
        print Total_ReRouted
        #Start finding the solution for Theta_h
        """
        for h in demand_flows:
            var_reference = m.getVarByName('Thetah_%s' %(h))
            my_theta[h] = 0
            if var_reference.x>0:
              my_theta[h] = 1
    
        """
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
        #print my_altered_switch
        MaxCong = 1
        print 'MaxCongestion'
        print MaxCong
        return Max_Time,my_used_arc, my_delta, Total_Hop, Total_ReRouted #my_used_arc -> RR_used_arc
