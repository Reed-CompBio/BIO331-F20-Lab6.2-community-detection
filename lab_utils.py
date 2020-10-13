from graphspace_python.api.client import GraphSpace
from graphspace_python.graphs.classes.gsgraph import GSGraph
import sys
import time
import networkx as nx

'''
read graphs
'''
def get_graph(infile):
    nodes = set()
    edges = []
    weights = {}
    costs = {}
    with open(infile) as fin:
        for line in fin:
            row = line.strip().split()
            nodes.add(row[0])
            nodes.add(row[1])
            edges.append((row[0],row[1]))
            if row[0] not in weights:
                weights[row[0]] = {}
                costs[row[0]] = {}
            if row[1] not in weights:
                weights[row[1]] = {}
                costs[row[1]] = {}
            weights[row[0]][row[1]]=float(row[2])
            weights[row[1]][row[0]]=float(row[2])
            costs[row[0]][row[1]]=float(row[3])
            costs[row[1]][row[0]]=float(row[3])
    adj_list = {n:set() for n in nodes}
    for u,v in edges:
        adj_list[u].add(v)
        adj_list[v].add(u)

    print('%d nodes and %d edges' % (len(nodes),len(edges)))
    return nodes,edges,weights,costs,adj_list

def get_betweenness_dictionary(edges,costs):
    ## This is slow, and uses a graph library.  (This is ALMOST what you're implementing for the programming assignment!)
    G = nx.Graph()
    G.add_edges_from(edges)
    for u,v in G.edges:
        G[u][v]['cost'] = costs[u][v]
    centralities = nx.edge_betweenness_centrality(G, normalized=False, weight='cost')
    return centralities

def remove_edge(e,edges,adj_list):
    u,v = e
    if (u,v) in edges:
        edges.remove((u,v))
    else:
        edges.remove((v,u))
    adj_list[u].remove(v)
    adj_list[v].remove(u)
    return ## don't need to return these - these are in place

'''
Posts a graph to GraphSpace. Inputs:
graphspace - GraphSpace client (what you passed your username & password in as)
nodes - list/set of nodes
edges - list of two-element edges (three-element lists if weighted, see below)
title - title of your graph.
communities - partition of nodes as a list of lists.
'''
def viz_graph(graphspace,nodes,edges,weights,title,communities):
    G = GSGraph()
    G.set_name(title + ' ' + str(time.time()))  ## this name is timestamped
    G.set_tags(['Lab 6']) ## tags help you organize your graphs

    node_colors = {}
    if communities != None:
        k = len(communities) # number of communities
        for i in range(len(communities)):
            for j in range(len(communities[i])):
                node_colors[communities[i][j]] = rgb_to_hex(i/k,1-i/k,0.8)

    for n in nodes:
        G.add_node(n,label=n)
        G.add_node_style(n,color=node_colors.get(n,'#FFFFFF'),shape='roundrectangle',height=30,width=40)
    for u,v in edges:
        G.add_edge(u,v,popup='weight=%f' % (weights[u][v]))
        G.add_edge_style(u,v,width=weights[u][v])

    post(G,graphspace)
    print('Done posting',title)
    return

'''
Posts the graph G to GraphSpace. Copied from Lab 2.
'''
def post(G,gs):
    try:
        graph = gs.update_graph(G)
    except:
        graph = gs.post_graph(G)
    return graph

'''
Returns the hexadecimal color code when given three channels
for red, green, and blue between 0 and 1.  Copied from Lab 3.
'''
def rgb_to_hex(red,green,blue): # pass in three values between 0 and 1
  maxHexValue= 255  ## max two-digit hex value (0-indexed)
  r = int(red*maxHexValue)    ## rescale red
  g = int(green*maxHexValue)  ## rescale green
  b = int(blue*maxHexValue)   ## rescale blue
  RR = format(r,'02x') ## two-digit hex representation
  GG = format(g,'02x') ## two-digit hex representation
  BB = format(b,'02x') ## two-digit hex representation
  return '#'+RR+GG+BB
