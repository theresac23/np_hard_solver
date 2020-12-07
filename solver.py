import networkx as nx
from parse import read_input_file, write_output_file
from utils import is_valid_solution, calculate_happiness
import sys
from os.path import basename, normpath
import glob


def solve(G, s):
    """
    Args:
        G: networkx.Graph
        s: stress_budget
    Returns:
        D: Dictionary mapping for student to breakout room r e.g. {0:2, 1:0, 2:1, 3:2}
        k: Number of breakout rooms
    """
    st = {} # student : assigned room
    rooms = {} # room : [students]
    rooms_s = {} # room : stress level
    k = len(G)
    hap = 0
    for i in range(len(G)):
        st[i] = i
        rooms[i] = [i]
        rooms_s[i] = 0
    sort = sorted(G.edges(data=True),key= lambda x: x[2]['happiness'], reverse=True)
    for edge in sort: 
        s1, s2, e = edge # output looks like (0, 9, {'happiness': 7.0, 'stress': 9.514})
        r1 = st[s1] # s1's room
        r2 = st[s2] # s2's room
        if len(rooms[r1]) == 1: # if student 1 is by themself then add to s2's room
            new_stress = room_stress(G, st, rooms, s1, s2) + rooms_s[s2]
            if new_stress <= float(s) / float(k-1): # making sure new stress added to existing stress < thrshld
                rooms_s[r2] = new_stress
                rooms_s[r1] = 0
                hap = hap + incr_hap(G, st, rooms, s1, s2)
                rooms[r1].remove(s1) # remove s1 from its own room
                st[s1] = r2 # set s1's room to s2's room
                rooms[r2].append(s1) # add s1 to s2's room
                k -= 1 
        elif len(rooms[r2]) == 1: # add s2 to s1's room
            new_stress = room_stress(G, st, rooms, s1, s2) + rooms_s[s1]
            if new_stress <= float(s) / float(k-1):
                rooms_s[r1] = new_stress
                rooms_s[r2] = 0
                hap = hap + incr_hap(G, st, rooms, s1, s2)
                rooms[r2].remove(s2) 
                st[s2] = r1 
                rooms[r1].append(s2) 
                k -= 1 
        elif r1 != r2: # in different rooms both > 1, merge s1 into s2's room
            new_stress = room_stress(G, st, rooms, s1, s2) + rooms_s[s1] + rooms_s[s2]
            if new_stress <= float(s) / float(k-1):
                rooms_s[r2] = new_stress
                rooms_s[r1] = 0
                hap = hap + incr_hap(G, st, rooms, s1, s2)
                for stu in rooms[s1_r]: # move all of s1's room's students in s2's room
                    rooms[r2].append(stu)
                    st[stu] = r2
                rooms[r1].clear() 
                k -= 1
        else: # already in same room
            continue 
    k = 0
    for r in rooms:
        if len(rooms[r]) > 0:
            k += 1

    return st, k

def incr_hap(G, st, rooms, s1, s2):
    """
    Calculates happiness between s1's room's students and s2's room's students.
    """ 
    hapenis = 0
    r1 = rooms[st[s1]]
    r2 = rooms[st[s2]]
    for st1 in r1:
        for st2 in r2:
            hapenis += G.get_edge_data(st1, st2)['happiness']
    return hapenis

def room_stress(G, st, rooms, s1, s2):
    """
    Calculates stress between s1's room's students and s2's room's students.
    """    
    stress = 0
    r1 = rooms[st[s1]]
    r2 = rooms[st[s2]]
    for st1 in r1:
        for st2 in r2:
            stress += G.get_edge_data(st1, st2)['stress']
    return stress
            
    


# Here's an example of how to run your solver.

# Usage: python3 solver.py test.in

if __name__ == '__main__':
    assert len(sys.argv) == 2
    path = sys.argv[1]
    G, s = read_input_file(path)
    D, k = solve(G, s)
    assert is_valid_solution(D, G, s, k)
    print("Total Happiness: {}".format(calculate_happiness(D, G)))
    write_output_file(D, 'outputs/small-1.out')


# For testing a folder of inputs to create a folder of outputs, you can use glob (need to import it)
# if __name__ == '__main__':
#     inputs = glob.glob('inputs/*')
#     for input_path in inputs:
#         output_path = 'outputs/' + basename(normpath(input_path))[:-3] + '.out'
#         G, s = read_input_file(input_path)
#         D, k = solve(G, s)
#         assert is_valid_solution(D, G, s, k)
#         happiness = calculate_happiness(D, G)
#         write_output_file(D, output_path)
