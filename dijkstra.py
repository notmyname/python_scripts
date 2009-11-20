#!/usr/bin/env python

# based on pseudocode at http://en.wikipedia.org/wiki/Dijkstra%27s_algorithm

import copy

def dijkstra(graph, start_node, target=None):
    # initialize distance list
    dist = dict()
    previous = dict()
    dist[start_node] = 0
    Q = copy.deepcopy(graph)
    def extract_min():
        min = None
        ret = None
        for key in dist:
            if key in Q and ((dist[key] < min) if min != None else True):
                min = dist[key]
                ret = key
        if ret is not None:
            del Q[ret]
        return ret
    while Q:
        u = extract_min()
        for v in graph[u]:
            alt = dist[u] + graph[u][v]
            if v not in dist or alt < dist[v]:
                dist[v] = alt
                previous[v] = u
    node_list = list()
    try:
        next = target
        while True:
            node_list.insert(0,next)
            next = previous[next]
    except:
        pass
    return node_list


# graph structure:
# dictionary whose keys are the nodes in the graph
# the value of the dictionary ot each key is a dictionary containing the adjacent nodes and the value of the edge

test_graph = {'A':{'B':1,'C':3},
              'B':{'A':1,'C':1},
              'C':{'A':3,'B':1},
             }
test_graph2 = {'A':{'B':3,'C':1},
               'B':{'A':1,'C':1},
               'C':{'A':3,'B':1},
              }
             
print dijkstra(test_graph, 'A', 'C')
print dijkstra(test_graph2, 'A', 'C')