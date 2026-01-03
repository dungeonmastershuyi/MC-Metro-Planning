'''
input:
1. city_map
2. lines
output:
1. paths
2. routes
'''
from useful_classes import pair_nums, snake
import pandas as pd
import math
def find_line(pair, city_map):
    startx=pair[0][0]
    starty=pair[0][1]
    endx=pair[1][0]
    endy=pair[1][1]
    path=[(startx, starty),]
    def find_point(x, y):
        nonlocal path
        opt=math.inf
        directions=((-1,+1),(0,+1),(+1,+1),
                     (-1,0),       (+1,0),
                    (-1,-1),(0,-1),(+1,-1))
        for dx, dy in directions:
            if (x+dx, y+dy) not in path:
                if (x+dx not in city_map.columns) or (y+dy not in city_map.index):
                    v=(1/city_map.loc[y+dy, x+dx] + pair_nums(pair).sld((x+dx, y+dy)))
                    if opt > v:
                        opt = v
                        optx = x+dx
                        opty = y+dy
        path.append((optx, opty))    
        return optx, opty
    stepx=startx
    stepy=starty
    while (stepx, stepy) != (endx, endy):
        stepx, stepy= find_point(stepx, stepy)
    time=0
    for i in range(len(path)-1):
        if (abs(path[i][0]-path[i+1][0])+abs(path[i][1]-path[i+1][1])) == 1:
            time=time+1
        elif (abs(path[i][0]-path[i+1][0])+abs(path[i][1]-path[i+1][1])) == 2:
            time=time+(2**0.5)
    return path, time

def dijkstra_algorithm(paths):
    stations=[]
    for i in paths.keys():
        for j, k in i:
            stations.append(j)
            stations.append(k)
    stations=tuple(set(stations))
    #give a clean tuple of all stations
    for station in stations:
        snakey=snake([station,])
        queue=[snakey,]
        routes={}
        while queue:
            snakey=queue.pop(0)
            adjacent_stations=[]
            for pair in paths.keys():
                if snakey.head() == pair[0]:
                    adjacent_stations.append(pair[1])
                elif snakey.head() == pair[1]:
                    adjacent_stations.append(pair[0])
            adjacent_stations=list(set(adjacent_stations))
            for s in adjacent_stations:
                queue.append(snakey.grow(s))
            if (snakey.butt(), snakey.head()) in routes.keys():
                if snakey.time(paths) < routes[(snakey.butt(), snakey.head())]["time"]:
                    routes[(snakey.butt(), snakey.head())]["time"]=snakey.time(paths)
            else:
                routes[(snakey.butt(), snakey.head())]={"path": snakey.body(paths), "time": snakey.time(paths)}
            queue.remove(snakey)
    return routes

def determine_path(lines, city_map):
    paths={}
    for i in lines.values():
        pairs=[]
        for j in range(len(i)-1):
            pairs.append((i[j], i[j+1]))
        tuple(pairs)
        #we see that pairs is a tuple of pairs of 2D tuples (stations), i.e. (((x11,y11),(x12,y12)), ((x21,y21),(x22,y22)), ....)        
        for k in pairs:
            path, time= find_line(k, city_map)
            paths[k]={"path": path, "time": time}
    #thus getting paths
    #there is certainity that for the same k and same city_map, the value of path is also the same, 
    #thus no need to worry about duplicated values for the same key
    routes=dijkstra_algorithm(paths)
    return paths, routes
    