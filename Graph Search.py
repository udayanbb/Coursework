from search import Edge, UndirectedGraph, do_nothing_fn, make_generic_search
import read_graphs

all_graphs = read_graphs.get_graphs()
GRAPH_0 = all_graphs['GRAPH_0']
GRAPH_1 = all_graphs['GRAPH_1']
GRAPH_2 = all_graphs['GRAPH_2']
GRAPH_3 = all_graphs['GRAPH_3']
GRAPH_FOR_HEURISTICS = all_graphs['GRAPH_FOR_HEURISTICS']


#### PART 1: Helper Functions #########################################

def path_length(graph, path):
 
    if len(path) == 0:
        return 0

    length = 0
    for i in range(len(path) - 1):
        length += graph.get_edge(path[i], path[i+1]).length

    return length
        

def has_loops(path):
    path_dict = {}
    for node in path:
        if node in path_dict:
            return True
        else:
            path_dict[node] = 1
    return False
    


def extensions(graph, path):
    edges = graph.get_neighboring_edges(path[-1])
    new_paths = []
    for edge in edges:
        temp_path = path[:]
        temp_path.append(edge.endNode)
        if not has_loops(temp_path): 
            new_paths.append(temp_path)
    return sorted(new_paths)


def sort_by_heuristic(graph, goalNode, nodes):


    temp_nodes = nodes[:]
    temp_nodes = sorted(nodes)
    return sorted(temp_nodes, key = lambda node: graph.get_heuristic_value(node, goalNode))



generic_search = make_generic_search(extensions, has_loops)

#### PART 2: Search Algorithms #########################################


def dfs(graph, startNode, goalNode):

    paths = [[startNode]]
    
    while True:
        if paths[0][-1] == goalNode:
            return paths[0]
        extended_path = extensions(graph, paths[0])
        paths[1:1] = extended_path
        if len(paths) >= 2:
            del(paths[0])
        else:
            return None



def bfs(graph, startNode, goalNode):

    paths = [[startNode]]

    while True:
            if paths[0][-1] == goalNode:
                return paths[0]

            extended_path = extensions(graph, paths[0])

            paths.extend(extended_path)

            if len(paths) >= 2:
                del(paths[0])
            else:
                return None
            
    


def hill_climbing(graph, startNode, goalNode):
     paths = [[startNode]]
    
     while True:
        extended_path = extensions(graph, paths[0])
        if extended_path == []:
            if len(paths) >= 2:
                del(paths[0])
            else:
                return None
        else:


            extended_path = sorted(extended_path, key = lambda dist: graph.get_heuristic_value(dist[-1], goalNode))
            
            if extended_path[0][-1] == goalNode:
                return extended_path[0]
            paths[1:1] = extended_path
            del(paths[0])
        

#['best_first', GRAPH_1, 'a', 'd', 'abcd', EXTRA],

def best_first(graph, startNode, goalNode):
    
     paths = [[startNode]]
    
     while True:
        extended_path = extensions(graph, paths[0])
        
        paths[1:1] = extended_path
        
        del(paths[0])

        paths = sorted(paths, key = lambda dist: graph.get_heuristic_value(dist[-1], goalNode))

        if paths[0][-1] == goalNode:
            return paths[0]
           



def beam(graph, startNode, goalNode, beam_width):

    paths = [[startNode]]
   
    while True:

            new_paths = [[]]
            for path in paths:

                if path[-1] == goalNode:
                        return path

                extended_path = extensions(graph, path)

                    
                if new_paths == [[]]:
                    new_paths = extended_path[:]
                else:
                    new_paths.extend(extended_path)

            paths = new_paths[:]
            if paths == [[]]:
                return None
            #print 'Paths at start', paths
            paths = sorted(paths)
            paths = sorted(paths, key = lambda dist: graph.get_heuristic_value(dist[-1], goalNode))
            paths = paths[0:beam_width]

            #print 'Paths at end', [[path, graph.get_heuristic_value(path[-1], goalNode)] for path in paths], '\n'

            #['beam', GRAPH_2, 'S', 'G', 2, 'SBYCEG'],


#print beam(GRAPH_2, 'S', 'G', 2)

def branch_and_bound(graph, startNode, goalNode):
     paths = [[startNode]]
    
     while True:

        extended_path = extensions(graph, paths[0])
        
        paths[1:1] = extended_path


        del(paths[0])


        if len(paths) == 0:
            return None

        paths = sorted(paths, key = lambda path: path_length(graph, path))

        if paths[0][-1] == goalNode:
            return paths[0]


def branch_and_bound_with_heuristic(graph, startNode, goalNode):

    paths = [[startNode]]

    while True:

        extended_path = extensions(graph, paths[0])

        paths[1:1] = extended_path

        del(paths[0])

        if len(paths) == 0:
            return None

        paths = sorted(paths, key = lambda path: path_length(graph, path) + graph.get_heuristic_value(path[-1], goalNode))

        if paths[0][-1] == goalNode:
            return paths[0]


def branch_and_bound_with_extended_set(graph, startNode, goalNode):

    paths = [[startNode]]



    #print 'start', graph, startNode, goalNode

    endNode_counts = {}

    while True:

        #print 'Paths at start', paths

        if paths[0][-1] == goalNode:
                return paths[0]

        if paths[0][-1] in endNode_counts:
            #print 'Removing', test_path, ', minimum found at ', endNode_counts[test_path[-1]]
            del(paths[0])
            if len(paths) == 0:
                return None
        else:
            endNode_counts[paths[0][-1]] = 1


            extended_path = extensions(graph, paths[0])



            paths[1:1] = extended_path

            del(paths[0])


            if len(paths) == 0:
                return None


            #print 'Paths before extended set check', [[path, path_length(graph, path)] for path in paths]


            #print 'Paths after extended set check', [[path, path_length(graph, path)] for path in paths]

            paths = sorted(paths, key = lambda path: path_length(graph, path))

            #print 'Paths at end', [[path, path_length(graph, path)] for path in paths], '\n'


def a_star(graph, startNode, goalNode):


    paths = [[startNode]]

    endNode_counts = {}

    while True:

        if paths[0][-1] in endNode_counts:
            #print 'Removing ', paths[0]
            del(paths[0])
            if len(paths) == 0:
                return None
        else:
            endNode_counts[paths[0][-1]] = 1

            if paths[0][-1] == goalNode:
                return paths[0]

            #print 'Paths at start', paths

            extended_path = extensions(graph, paths[0])

            #print 'paths before extended check', [[path, path_length(graph, path) + graph.get_heuristic_value(path[-1], goalNode)] for path in extended_path + paths[1:]]

            temp_paths = extended_path[:]



            paths[1:1] = extended_path

            del(paths[0])

            if len(paths) == 0:
                return None

            #print 'Paths after extended set check ', [[path, path_length(graph, path) + graph.get_heuristic_value(path[-1], goalNode)] for path in paths]


            paths = sorted(paths, key = lambda path: path_length(graph, path) + graph.get_heuristic_value(path[-1], goalNode))

            #print 'Paths at end', [[path, path_length(graph, path) + graph.get_heuristic_value(path[-1], goalNode)] for path in paths], '\n'




#### PART 3: Generic Search #######################################

def break_ties(paths):
    return sorted(paths)

def heuristic_sort(graph, goalNode, paths):


    #print 'Original: ', [[path, graph.get_heuristic_value(path[-1], goalNode)] for path in paths]

    return_paths = break_ties(paths)

    return_paths = sorted(return_paths, key = lambda path: graph.get_heuristic_value(path[-1], goalNode))

    #print 'After:, ', [[path, graph.get_heuristic_value(path[-1], goalNode)] for path in return_paths]
    return return_paths

def distance_sort(graph, goalNode, paths):

    return_paths = break_ties(paths)
    return sorted(return_paths, key = lambda path: path_length(graph, path))

def dual_sort(graph, goalNode, paths):

    #print 'Paths before sort', [[path, path_length(graph, path) + graph.get_heuristic_value(path[-1], goalNode)] for path in paths]

    return_paths = break_ties(paths)
    return_paths = sorted(return_paths, key = lambda path: path_length(graph, path) + graph.get_heuristic_value(path[-1], goalNode))

    #print 'Paths after sort', [[path, path_length(graph, path) + graph.get_heuristic_value(path[-1], goalNode)] for path in return_paths], '\n'

    return return_paths

generic_dfs = [do_nothing_fn, True, do_nothing_fn, False]

generic_bfs = [do_nothing_fn, False, do_nothing_fn, False]

generic_hill_climbing = [heuristic_sort, True, do_nothing_fn, False]

generic_best_first = [do_nothing_fn, True, heuristic_sort, False]

generic_branch_and_bound = [do_nothing_fn, True, distance_sort, False]

generic_branch_and_bound_with_heuristic = [do_nothing_fn, True, dual_sort, False]

generic_branch_and_bound_with_extended_set = [do_nothing_fn, True, distance_sort, True]

generic_a_star = [do_nothing_fn, True, dual_sort, True]


def level_has_been_extended(paths):
    max_len = 0
    for path in paths:
        max_len = max(len(path), max_len)
    for path in paths:
        if len(path) < max_len:
            #print 'Not extended: ', paths
            return False
    #print 'Extended'
    return True

def my_beam_sorting_fn(graph, goalNode, paths, beam_width):
    #print 'Sorting'
    if level_has_been_extended(paths):
        #print 'Original: ', [[path, graph.get_heuristic_value(path[-1], goalNode)] for path in paths]
        #print 'After:, ', [[path, graph.get_heuristic_value(path[-1], goalNode)] for path in heuristic_sort(graph, goalNode, paths)[0:beam_width]]
        return heuristic_sort(graph, goalNode, paths)[0:beam_width]
    else:
        return paths

generic_beam = [do_nothing_fn, False, my_beam_sorting_fn, False]


#### PART 4: Heuristics ###################################################

def is_admissible(graph, goalNode):

    for node in graph.nodes:
        test_path = branch_and_bound_with_extended_set(graph, node, goalNode)

        if not test_path == None:

            actual_dist = path_length(graph, test_path)

            if graph.get_heuristic_value(node, goalNode) > actual_dist:
                return False
    return True

def is_consistent(graph, goalNode):
    for node in graph.nodes:
        for adj_node in extensions(graph, [node]):
            h_dist = graph.get_heuristic_value(node, goalNode) - graph.get_heuristic_value(adj_node[-1], goalNode)
            h_dist = abs(h_dist)
            if h_dist > graph.get_edge(node, adj_node[-1]).length:
                return False

    return True


