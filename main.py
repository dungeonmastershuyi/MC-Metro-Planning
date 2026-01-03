import os
import pandas as pd
#get input from inputs folder
map_path = os.path.join("inputs", "city_map_input.csv")
config_path = os.path.join("inputs", "parameters_input.json")

df = pd.read_csv(map_path)
with open(config_path) as f: ...

#city_map is in the form of a pivot table, index is x and columns is y, entries is weight
#!!! ALERT !!! WEIGHT IN CITY_MAP HAS TO BE IN [1,10] !!!CANNOT BE 0!!!

'''
user -> *city_map* and *parameters*
->
solver -> *lines*                                  <--  stop? : "lines" -> final ouptut
->                                                   |
determine_path -> *paths* and *routes*               |
->                                                   |
n: {                                                 |
    montecarlo -> *test_set_n*                       |
    ->                                               |
    simulation -> *report_n*                         |
    }                                                |
    -> if montecarlo pass down *stop*: *report_set*  | 
-> evaluation -> *feedback* or *stop*               --
'''

'''
1. city_map
    pivot table (index: y coordinate, columns: x coordinate, values: weight of point)
2. parameters
    c: line capacity determinant
        used in capacity = c*line_length
    lagp=(n, a): passenger penalty function parameter
        penalty = e**[a*(t-n)]
        (t > n)
        t: passenger waiting time
        a: coefficient
    ...
3. lines
    dictionary of tuples of dictionary of 2D tuples
        key: line number
        values: 2D tuple of x, y value
    {
    1:((x11,y11),(x12,y12), ...), 
    2:((x21,y21),(x22,y22), ...),
    ...
    }
4. paths
    path and time of all adjacent stations ("adjacent" includes the meaning of connected by line)
    {
    ((xm,ym), (xn,yn)): {"path": ((xm,ym), ..., (xn,yn)), "time": t},
    ((xp,yp), (xq,yq)): {"path": ((xp,yp), ..., (xq,yq)), "time": t},
    ...
    }
5. routes
    a search chart for passenger, for any start station and end station (distinction doesn't matter),
    give shortest path and its according time (length)
    {
    ((xm,ym), (xn,yn)): {"path": ((xm,ym), ..., (xn,yn)), "time": t},
    ((xp,yp), (xq,yq)): {"path": ((xp,yp), ..., (xq,yq)), "time": t},
    ...
    }
6. test_set
    a list of passengers with passenger class, 1 of n sets of test sets for running the simulation
    [passenger1, ...]

'''