import numpy as np
import sys
import matplotlib.pyplot as plt

# Norne Read Info and Plot (NRIP)

def parse_fname(name, info):

    fname = name.split("/")[-1]
    method = fname.split("_")[0]
    num_nodes = int(fname.split("_")[2].split("-")[0])    
    rankPnode = int(fname.split("_")[1].split("-")[0])
    if "size" in fname:
        sizeGrid  = fname.split("_")[3].split("-")[0]
    else:
        X = int(fname.split("_")[3].split("-")[0])
        Y= int(fname.split("_")[4].split("-")[0])
        Z = int(fname.split("_")[5].split("-")[0])
        sizeGrid = X*Y*Z

    mpiSize = num_nodes*rankPnode



    if method not in info.keys():
        info[method] = {}
    if sizeGrid not in info[method].keys():
        info[method][sizeGrid] = {}
    if rankPnode not in info[method][sizeGrid].keys():
        info[method][sizeGrid][rankPnode] = {}
    if num_nodes not in info[method][sizeGrid][rankPnode].keys():
        info[method][sizeGrid][rankPnode][num_nodes] = []
        
    #print (method, rankPnode, num_nodes, sizeGrid)
    return method, rankPnode, num_nodes, sizeGrid

def read_summer_out_file(name, info):


    method, rankPnode, num_nodes, sizeGrid = parse_fname(name, info)
    
    f = open (name, "r")
    lines = f.readlines()
    f.close()

    finfo = {}
    

    for line in lines:
    
        line_list = line.split()
        #print (line_list)
        
        if "before" in line_list:
            if "Interior" not in finfo.keys():
                finfo["Interior"] = {}
            finfo["Interior"][int(line_list[3])] = int(line.split(":")[1].strip())

        if "After" in line_list:
            if "Cells" not in finfo.keys():
                finfo["Cells"] = {}
            try:
                finfo["Cells"][int(line_list[3])] = int(line_list[5])
            except:
                print("problem",name)
                #finfo["Cells"][int(line_list[3])] = int(line_list[5])

        if "Edge-cut:" in line_list:
            finfo["Edge-cut"] = int(line_list[1])
            
        if "ghost" in line_list:
            cti = line.split(":")[1].split()
            if "ComTab" not in finfo.keys():
                finfo["ComTab"] = []
            ct = []
            try:
                if len(cti) == rankPnode*num_nodes:
                    for cc in cti:
                        ct.append(int(cc))
                else:
                    for i in range(int(rankPnode*num_nodes)):
                    
                        ct.append(int(cti[i]))
            
                finfo["ComTab"].append(ct)
            except:
                print("problem", name)
            
        if "Matrix-vector" in line_list and line_list[0]!="Average":
            if "SpMV" not in finfo.keys():
                finfo["SpMV"] = []
            finfo["SpMV"].append(float(line_list[5]))

        if "Matrix-vector" in line_list and line_list[0]=="Average":
            if "avgSpMV" not in finfo.keys():
                finfo["avgSpMV"] = []
            finfo["avgSpMV"].append(float(line_list[6]))

        if "copyOwnerToAll" in line_list and line_list[0]!="Average":
            if "copyOwnerToAll" not in finfo.keys():
                finfo["copyOwnerToAll"] = []
            finfo["copyOwnerToAll"].append(float(line_list[4]))

        if "copyOwnertoAll" in line_list and line_list[0]=="Average":
            if "avgCopyOwnerToAll" not in finfo.keys():
                finfo["avgCopyOwnerToAll"] = []
            finfo["avgCopyOwnerToAll"].append(float(line_list[5]))
        if "Number" in line_list:
            if "ranksPerNode" not in finfo.keys():
                finfo["ranksPerNode"] = []
            finfo["ranksPerNode"].append(int(line.split(":")[1]))


        info[method][sizeGrid][rankPnode][num_nodes] = finfo
        #info[method]["Np"].append(rankPnode)
