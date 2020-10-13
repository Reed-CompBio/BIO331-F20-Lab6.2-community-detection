from graphspace_python.api.client import GraphSpace
from graphspace_python.graphs.classes.gsgraph import GSGraph
import lab_utils
import sys

def main():
    # connect to GraphSpace
    graphspace = GraphSpace('YOUR_EMAIL','YOUR_PASSWORD')
    nodes,edges,weights,costs,adj_list = lab_utils.get_graph('example_edges.txt')
    #nodes,edges,weights,costs,adj_list = lab_utils.get_graph('mouse_visual_cortex_edges.txt')

    ## visualize the graph before community detection
    lab_utils.viz_graph(graphspace,nodes,edges,weights,'Example Graph',None)
    #lab_utils.viz_graph(graphspace,nodes,edges,weights,'Mouse Graph',None)

    ## copy the edges to pass to the community detection function
    copy_edges = [e for e in edges]

    ## get communities
    communities = get_communities(nodes,copy_edges,costs,adj_list)

    ## visualize the graph after community detection
    #lab_utils.viz_graph(graphspace,nodes,edges,weights,'Example Graph k=3',communities[2])
    #lab_utils.viz_graph(graphspace,nodes,edges,weights,'Mouse Graph k=2',communities[1])
    return

def get_communities(nodes,edges,costs,adj_list):
    partitions = [[[n for n in nodes]]] # first partition is all nodes.
    print(partitions)

    ## ADD CODE HERE

    ## return all partitions
    return partitions

if __name__ == '__main__':
    main()
