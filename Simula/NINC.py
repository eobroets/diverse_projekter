import numpy as np
import sys
import matplotlib.pyplot as plt
import math

from NRIP import read_summer_out_file
from node_com import calc_node_com

# Norne Intra&Inter node communication (NINC)

def plot_inter_node_communication_ranks(info, sGrid, num_nodes, Np):
    
    fig = plt.figure(figsize=(16,8))
    axVol = fig.add_subplot(121)
    axMes = fig.add_subplot(122)
 
    
    numM = len(info.keys())
    metNum = -1

    done=False
    for method in info.keys():
        metNum += 1
        comVol = []
        numMes = []   
        
        X = []
        x = 0
        for n in Np:
            if n in info[method][sGrid].keys():
                #print(method,sGrid, n, num_nodes)
                try:
                    comTab = info[method][sGrid][n][num_nodes]["ComTab"]
                    vol = 0
                    mes = 0
                    ranksPerNode = n
                    nodeCom = calc_node_com(comTab, ranksPerNode)

                    vol = 0
                    mes = 0
                    for nodeii in nodeCom:
                        vol += nodeii[1]
                        mes += nodeii[3]
                except:     
                    print("problem", method, sGrid, n, num_nodes)   
                    vol = 0
                    mes = 0
                                
                done=True

                numMes.append(mes)
                comVol.append(vol)
                X.append(x)
                x += 1
         
    
        
        XX = (numM + 1)*np.array(X)
        axVol.bar( XX + metNum, comVol, label=method)
        axVol.xaxis.set_ticks(XX)
        axVol.set_xticklabels(Np)

        XX = (numM +1)*np.array(X)
        axMes.bar(XX + metNum, numMes, label=method)
        axMes.xaxis.set_ticks(XX)
        axMes.set_xticklabels(Np)
    
    axVol.set_xlabel("Number of MPI-processes",fontsize=20)
    axVol.set_ylabel("Inter-nodes communication volume", fontsize=20)
    axVol.set_title("Size: " +str(sGrid) + ", Nodes: " +str(num_nodes))
    axVol.legend()

    axMes.set_xlabel("Number of MPI-processes",fontsize=20)
    axMes.set_ylabel("Number of messages sent between nodes", fontsize=20)
    axMes.set_title("Size: " +str(sGrid) + ", Nodes: " +str(num_nodes))
    axMes.legend()

def plot_inter_node_communication_nodes(info, sGrid, num_ranks,nodes):
    
    fig = plt.figure(figsize=(16,8))
    axVol = fig.add_subplot(121)
    axMes = fig.add_subplot(122)
 
    
    numM = len(info.keys())
    metNum = -1

    done=False
    for method in info.keys():
        metNum += 1
        comVol = []
        numMes = []
        
        X = []
        x = 0
        for num_nodes in nodes:
            vol = 0
            mes = 0
            if num_nodes in nodes:
                #print(method,sGrid, num_ranks, num_nodes)
                try:
                    comTab = info[method][sGrid][num_ranks][num_nodes]["ComTab"]
                
                    ranksPerNode = num_ranks

                    nodeCom = calc_node_com(comTab, ranksPerNode)

                    vol = 0
                    mes = 0
                    for nodeii in nodeCom:
                        vol += nodeii[1]
                        mes += nodeii[3]
                except:
                    print("problem")

                done=True

                numMes.append(mes)
                comVol.append(vol)
                X.append(x)
                x += 1
         
    
        
        XX = (numM + 1)*np.array(X)
        axVol.bar( XX + metNum, comVol, label=method)
        axVol.xaxis.set_ticks(XX)
        axVol.set_xticklabels(nodes)

        XX = (numM +1)*np.array(X)
        axMes.bar(XX + metNum, numMes, label=method)
        axMes.xaxis.set_ticks(XX)
        axMes.set_xticklabels(nodes)
    
    axVol.set_xlabel("Number of Nodes",fontsize=20)
    axVol.set_ylabel("Inter-nodes communication volume", fontsize=20)
    axVol.set_title("Size: " +str(sGrid) + ", Ranks per node: " +str(num_ranks))
    axVol.legend()

    axMes.set_xlabel("Number of Nodes",fontsize=20)
    axMes.set_ylabel("Number of messages sent between nodes", fontsize=20)
    axMes.set_title("Size: " +str(sGrid) + ", Ranks per node: " +str(num_ranks))
    axMes.legend()


def main():

    nodes_or_ranks = False
    info={}

    for name in sys.argv[1:]:
        read_summer_out_file(name,info)


    methods = info.keys()
    gridSizes = info[list(methods)[0]].keys()
    
    ranks = []
    for ra in info[list(methods)[0]][list(gridSizes)[0]].keys():
        ranks.append(ra)
    ranks.sort()
    nodes =  []
    for nod in info[list(methods)[0]][list(gridSizes)[0]][list(ranks)[0]].keys():
        nodes.append(nod)
    nodes.sort()
    if len(ranks)==1:
        nodes_or_ranks=True
    elif len(nodes)==1:
        nodes_or_ranks=False

    print(gridSizes)
    for sG in gridSizes:
        if nodes_or_ranks:
            for rank in ranks:
                plot_inter_node_communication_nodes(info,sG,rank, nodes)
        else:
            for node in nodes:
                plot_inter_node_communication_ranks(info, sG, node, ranks)
        plt.savefig(sG+".png")
    

if __name__ == "__main__":
    main()

