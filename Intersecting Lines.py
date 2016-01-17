from bst import insert, search, delete

'''
Problem Statement:
You are given n vertical or horizontal segments on the plane. The goal is to find any pair of
segments that intersect or to report that there is no such a pair.
You are guaranteed that no three endpoints lie on a vertical or horizontal straight line. In particular, any intersecting pair consists of a vertical and a horizontal segment.
Design and implement an algorithm for this problem with running time O(n log n).

'''
get_smallest_at_least: finds a node in the given subtree with the smallest key
that is greater than or equal to the given lower bound, or decides that there is
no such node
ARGS:
  node  - the root of the subtree
  bound - the lower bound for the key
RETURN:
  if there are nodes with key at least bound, return such a node with smallest
  key; otherwise return None
'''
def get_smallest_at_least(node, bound):
    current_smallest = None
    if node == None:
        return None
    while True:
        if node.key == bound:
           return node
        elif node.key > bound:
            current_smallest = node
            node = node.left
        else:
            node = node.right
        if node == None:
            return current_smallest

'''
def get_successor(node):
    if node == None:
        return None

    if node.right != None:
        return get_smallest(node.right)

    parent = node.parent
    while parent != None and parent.right == node:
        node = parent
        parent = parent.parent
    return parent
'''
'''
def get_smallest(node):
    while (True):
        if(node.left == None):
            return node
        else:
            node = node.left

'''


'''

root = None
root = insert(root, 1)
root = insert(root, 3)
root = insert(root, 5)
root = insert(root, 14)
root = insert(root, 2)
root = insert(root, 6)

print get_successor(search(root, 2)).key
# should print 5
'''



'''
find_intersection: finds an intersection of the given line segments, or decides
that there is no intersection
ARGS:
  segments - list of tuples of the form ((x1, y1), (x2, y2)), where (x1, y1) and
  (x2, y2) are the endpoints of the line segment; detailed specifications can be
  found in the problem statement
RETURN:
  if there are intersections between the given line segments, return one such
  intersection as a tuple (x, y); otherwise return None
'''

'''
def print_tree(node):
    """Prints the keys from the tree rooted at node in the sorted order."""
    if node is None:
        return
    print_tree(node.left)
    print node.key
    print_tree(node.right)
'''

class lineEvent:
    def __init__(self, line, type, trigger_x):
        self.line = line
        self.type = type
        self.trigger_x = trigger_x

'''
def find_intersection(segments):


    root = None

    line_dict = {el[0][0]: el for el in segments}

    for el in segments:
        root = insert(root, el[0][0])

    test_node = get_smallest(root)
    test_key = test_node.key
    active_lines = []


    while(True):

        test_line = line_dict[test_key]

        #discard old lines
        active_lines_copy = active_lines[:]
        for line in active_lines_copy:
            if test_key >  line[1][0]:
                active_lines.remove(line)

        #either test line is a vertical line or a horizontal line
        if test_line[0][1] == test_line[1][1]: #horizontal line
            active_lines.append(test_line)
        else:   #vertical line
            for line in active_lines:
                if line[0][1] > test_line[0][1] and line[0][1] < test_line[1][1]:
                    return (test_line[0][0], line[0][1])

        root = delete(root, test_key)
        test_node = get_smallest_at_least(root, test_key)

        if test_node == None:
            return None
        else:
            test_key = test_node.key

'''

def find_intersection(segments):
    line_events = []
    for line in segments:
        if line[0][1] == line[1][1]:  #horiztonal
            line_events.append(lineEvent(line, 'start', line[0][0]))
            line_events.append(lineEvent(line, 'end', line[1][0]))
        else: #vertical
            line_events.append(lineEvent(line, 'vert', line[0][0]))

    line_dict = {el[0][1]: el for el in segments}       #to lookup treap keys
    line_events = sorted(line_events, key = lambda line_event: line_event.trigger_x)
    horizontal_treap = None

    for event in line_events:
        if event.type == 'start':
            horizontal_treap = insert(horizontal_treap, event.line[0][1])
        elif event.type == 'end':
            horizontal_treap = delete(horizontal_treap,event.line[0][1])
        else: #vertical line
            test_node = get_smallest_at_least(horizontal_treap, event.line[0][1])
            if test_node != None:
                test_line = line_dict[test_node.key]
                if event.line[1][1] > test_line[0][1]:
                    return (event.line[0][0], test_line[0][1])
    return None



'''
print find_intersection([((0, 0.5), (10, 0.5)), ((5, -5), (5, 5))])
    # should return None
print find_intersection([((0, 0), (10, 0)),((5, 5), (5, 15))])
      # should return None
print find_intersection([((0, 0), (20, 0)),((5, -5), (5, 5)),((10, -50), (10, 50))])
      # can return either (5, 0) or (10, 0)
'''


#print find_intersection([((0, 0), (5, 0)),((2, 1), (8, 1)), ((7, -20), (4, 20))])
