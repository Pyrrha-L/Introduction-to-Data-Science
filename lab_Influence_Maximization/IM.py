 #<学号>−IM.py
#@param input_file_name: 描述一个影响力graph的纯文本邻接表文件名，如 ’E:\ diggs.edge’。
#@param k: 种子数 

import operator
import networkx as nx

# input_file_name: filename of the input file
def Proc_Input_File(input_file_name):
    data = []
    prob = dict()
    
    with (open(input_file_name,'r')) as inputfile:
        strread = inputfile.read()
    
    #possible‘\n’
    if(strread[len(strread)-1] == '\n' ):
        strread2 = strread[:-1]
    else:
        strread2 = strread
        
    data = strread2.split('\n')

    G = nx.DiGraph()
    G.name = "IM"
    
    for i, row in enumerate(data):
        
        #skip the first line
        if( i == 0 ):
            continue
        
        row_sec = row.split(' ')
        node_a = int(row_sec[0]) #出发点
        node_b = int(row_sec[1]) #结束点
        prob_r = float(row_sec[2])
            
        G.add_edge(node_a, node_b)
        
        keyprob = row_sec[0] + '.' + row_sec[1]
        prob[keyprob] = float(prob_r)
    
    return G,prob

# get probability between u and v
def GetProb(u,v,prob):
    u_str = str(u)
    v_str = str(v)
    # compose key
    key_str = u_str + '.' + v_str
    if( key_str in prob.keys() ):
        deg = prob[key_str]
    else:
        deg = 0
    return deg

# main function. G: graph. k: output amount. prob: probablity dict.
def degreeDiscountIC(G, k, prob):
    S = [] # result returned
    dd = dict()
    p = dict() # number of adjacent vertices that are in S
    d = dict() # degree of each vertex
    
    #used to find maximum
    max_node = -1
    max_deg = -1
    
    # initialize degree discount
    for u in G.nodes():
        # d[u] = len(G[u]) # each neighbor adds degree 1
        p[u] = 1.0 # prob of each node
        d[u] = 1.0
        
        for v in G[u]:
            d[u] += GetProb(u,v,prob)
        
        dd[u] = d[u]*p[u]
        
        if(dd[u]>max_deg):
            max_deg = dd[u]
            max_node = u
    #print(dd)
    
    S.append(max_node)
    max_deg = -1
    
    #print("initialize done.")
    # add vertices to S greedily
    for i in range(k-1):
        # update info about u->v nodes
        for v in G[max_node] :
            if(v not in S):
                d[v] -= GetProb(v,max_node,prob)
                #p[v] *= (1-GetProb(max_node,v,prob))
                #d[v] -= GetProb(max_node,v,prob)
        
        for v in G.nodes():
            if(G.has_edge(v,max_node) and (v not in S)):
                p[v] *= (1-GetProb(max_node,v,prob))
                #d[v] -= GetProb(v,max_node,prob)
                # print(v,p[v],d[v])
        
        for u in G.nodes():
            dd[u] = p[u] * d[u]
            if ((u not in S) and (dd[u]>max_deg)) :
                max_deg = dd[u]
                max_node = u
                
        #print(dd)
        S.append(max_node)
        max_deg = -1
        
    return S

# used to evaluate output. output_filename: filename of the output file. res: result.
def write_res(output_filename, res):
    f = open(output_filename,'w')
    f.write(str(len(res)))
    f.write('\n')
    
    #write into file
    for i in range(len(res)):
        f.write(str(res[i])+'\n')
    
    f.close()
    
def IM(input_file_name, k): 
    G,prob = Proc_Input_File(input_file_name)
    seed_node_list = degreeDiscountIC(G, k, prob)
    write_res(r'F:\dataset\res.txt',seed_node_list)
    #your implementation
    return seed_node_list

res = IM('F:\dataset\diggs.txt',50)
print(res)