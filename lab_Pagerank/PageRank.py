#<学号>−PageRank.py 
#@param input_file_name: 描述一个graph的纯文本邻接表文件名，如 ’E:\graph. txt ’ 

#@param damping_factor

import operator
import networkx as nx

#处理输入文件，文本转化为图
def Proc_File(input_file_name):
    data = []
    nodeset = []
    with (open(input_file_name,'r')) as inputfile:
        strread = inputfile.read()
    
    #处理最后可能的换行符
    if(strread[len(strread)-1] == '\n' ):
        strread2 = strread[:-1]
    else:
        strread2 = strread

    data = strread2.split('\n')

    DG = nx.DiGraph()
    DG.name = "PageRankImp"

    for i, row in enumerate(data):
        row_sec = row.split(',')
        node_a = row_sec[0] #初始点
        node_b = row_sec[1] #结束点
        if(node_a not in nodeset):
            nodeset.append(node_a)
        DG.add_edge(node_a, node_b)
    
    return DG

#专门处理Epinions数据集
def Proc_File_2(input_file_name):
    data = []
    nodeset = []
    
    #读取数据
    with (open(input_file_name,'r')) as inputfile:
        strread = inputfile.read()
    data = strread.split('\n')
    
    DG = nx.DiGraph()
    DG.name = "PageRankSoc"

    for i, row in enumerate(data):
        row_sec = row.split('\t')
        node_a = row_sec[0]
        node_b = row_sec[1]
        if(node_a not in nodeset):
            nodeset.append(node_a)
        if(node_b not in nodeset):
            nodeset.append(node_b)
        DG.add_edge(node_a, node_b)

    return DG

def PageRank(input_file_name, damping_factor):
    d = damping_factor
    DG = Proc_File(input_file_name)
    V = len(DG)
    ranks = dict()
    ranks_store = dict()
    
    # 初始化
    for key, node in DG.nodes(data=True):
        ranks[key] = 1/V
    
    ranks_store = ranks.copy()
    
    for _ in range(40):
        ranks_store = ranks.copy()
        for key, node in DG.nodes(data=True):
            rank_sum = 0.0
            neighbors = DG.in_edges(key)
            for n in neighbors:
                outlinks = len(DG.out_edges(n[0]))
                if (outlinks > 0):
                    rank_sum  += (1 / float(outlinks)) * ranks_store[n[0]] #计算RAW
          
            ranks[key] = ((1 - float(d)) * (1/float(V))) + d*rank_sum #加工后
    
    #排序
    sorted_r = sorted(ranks.items(), key=operator.itemgetter(1,0), reverse=True)
        
    node_list_in_descending_order = sorted_r
    return node_list_in_descending_order

#处理输入的图文件
def Proc_Graph_File(input_Graph):
    data = []
    nodeset = []
    with (open(input_Graph,'r')) as inputfile:
        strread = inputfile.read()
    
    #处理最后可能的换行符
    if(strread[len(strread)-1] == '\n' ):
        strread2 = strread[:-1]
    else:
        strread2 = strread
        
    data = strread2.split('\n')

    DG = nx.DiGraph()
    DG.name = "PPR"

    for i, row in enumerate(data):
        row_sec = row.split(',')
        node_a = row_sec[0] #出发点
        node_b = row_sec[1] #结束点
        if(node_a not in nodeset):
            nodeset.append(node_a)
        if(node_b not in nodeset):
            nodeset.append(node_b)
        DG.add_edge(node_a, node_b)

    return DG

#处理输入的种子文件
#input_Seed:Seed file
def Proc_Seed_File(input_Seed):
    seed_dict = dict()
    
    with (open(input_Seed,'r')) as inputfile:
        strread = inputfile.read()
    
    #处理末尾换行符
    if(strread[len(strread)-1] == '\n' ):
        strread2 = strread[:-1]
    else:
        strread2 = strread
        
    data = strread2.split('\n')
        
    for i, row in enumerate(data):
        row_sec = row.split(',')
        node_key = row_sec[0]
        node_val = float(row_sec[1])
        seed_dict[node_key]=node_val

    return seed_dict

def PPR(input_Graph, input_Seed, damping_factor): 
     #your implementation
    d = damping_factor
    DG = Proc_Graph_File(input_Graph)
    V = len(DG)
    seeds = Proc_Seed_File(input_Seed)
    ranks = dict()
    ranks_store = dict()
    
    #赋予初始值
    for key, node in DG.nodes(data=True):
        if( key in seeds.keys() ):
            ranks[key] = float(seeds[key])
        else:
            ranks[key] = 0
    
    #迭代30次
    for _ in range(30):
        ranks_store = ranks.copy()
        for key, node in DG.nodes(data=True):
            rank_sum = 0
            neighbors = DG.in_edges(key)
            
            if( key in seeds.keys() ):
                seed = float(seeds[key])
            else:
                seed = 0
                
            for n in neighbors:
                outlinks = len(DG.out_edges(n[0]))
                if outlinks > 0:
                    rank_sum += (1 / float(outlinks)) * ranks_store[n[0]]

            ranks[key] = ((1 - float(d)) * seed ) + d*rank_sum
    
    #排序
    sorted_r = sorted(ranks.items(), key=operator.itemgetter(1,0), reverse=True)
        
    node_list_in_descending_order = sorted_r
    return node_list_in_descending_order
