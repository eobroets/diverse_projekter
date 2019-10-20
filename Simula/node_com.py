import numpy as np
import sys

from RIP import read_summer_out_file as rsof

def calc_node_com(comTab, ranksPerNode):
    
    ranks = len(comTab)
    nodes = int(ranks/ranksPerNode)

    nodeCom = []
    for i in range(nodes):
        nodeCom.append([0,0,0,0])

    for ranki in range(ranks):

        nodei = int(ranki/ranksPerNode)
        for rankj in range(ranks):
            nodej = int(rankj/ranksPerNode)

            if comTab[ranki][rankj] > 0:
                if nodej == nodei:

                    nodeCom[nodei][0] += comTab[ranki][rankj]
                    nodeCom[nodei][2] += 1
                else:
                    nodeCom[nodei][1] += comTab[ranki][rankj]
                    nodeCom[nodei][3] += 1
    return nodeCom


def main():
    info = {}
    for name in sys.argv[1:]:
        rsof(name, info)
if __name__ == "__main__":
    main()
