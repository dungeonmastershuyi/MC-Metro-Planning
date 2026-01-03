'''
input:
1. city_map
2. test_set
3. lines
4. paths
5. routes
6. parameter c
7. parameter lagp
output:
single report for the current input of test_set
report includes 3 elements:
1. cost
    cost of maintaining the metro system, here to avoid arbitrary,
    because cost is linear correlated, set cost = whole length of the metro system
2. sum_lag
    sum of all lag penalties from all passengers
3. remains
    at the end of the test period, number of passengers with status of WAITING, IN_METRO, FROM_OFF_STATION
'''
'''
notes
logic of passenger:
1. upon spawning, the passenger will use a greedy heuristic to choose only the closest station to go to, 
   in the same logic, the passenger will choose the off_station closest to its destination point
2. when arriving at station, change status from the original TO_ON_STATION to WAITING, and file a form to the line of that station,
   the form includes the on_station and off_station of the passenger ON THAT LINE
   meaning that if a passenger is to interchange out of the line, the off_station submitted to the line will be that interchange,
   instead of the ultimate off_station
   when WAITING, the penalty timer will start ticking
3. the line will check its line capacity
   if capacity is not yet full, it will agree to take in the passenger,
   thus passenger status will be changed from WAITING to IN_METRO
   if capacity is already full, the line will reject the passenger's request,
   the passenger will keep status as WAITING and keep filing a form to the line every second, until agreed to take metro
4. when at off_station, passenger gets off, if it needs to use that station as interchange and wait for metro again,
   it changes status back to WAITING, and repeat 3
   if it doesn't need to interchange, it gets out of station and change status to FROM_OFF_STATION
5. passenger will walk to its destination point, upon arrival, change status to FINISHED, end for that passenger
'''
from useful_classes import passenger, status
import pandas
import math
import random
def initialization(city_map, test_set, lines, paths, routes, c, lagp):
    #create a reverse lookup dictionary for lines:
    reverse_lines={}
    for line_name, line_line in lines.items():
        for point in line_line:
            if point not in reverse_lines:
                reverse_lines[point]=[]
            reverse_lines[point].append(line_name)
    #thus getting reverse_lines, in form {(x,y):[line_name, ], ...}
    #lagp is in the form (n, a)
    #p is short for passenger, which already exists as the class name
    stations=[]
    for i in paths.keys():
        for j, k in i:
            stations.append(j)
            stations.append(k)
    stations=tuple(set(stations))
    #stations is the tuple of all stations\
    closest_to_spawn_stations={}
    closest_to_des_stations={}
    interchanges={}
    for p in test_set:
        min_d_to_spawn=math.inf
        min_d_to_des=math.inf
        for station in stations:
            d_to_spawn=((station[0]-p.spawn_point[0])**2+(station[1]-p.spawn_point[1])**2)**0.5
            d_to_des=((station[0]-p.destination_point[0])**2+(station[1]-p.destination_point[1])**2)**0.5
            if d_to_spawn < min_d_to_spawn:
                min_d_to_spawn = d_to_spawn
                closest_to_spawn=station
            if d_to_des < min_d_to_des:
                min_d_to_des = d_to_des
                closest_to_des=station
        #thus getting the closest stations for that passenger: closest_to_spawn, closest_to_des
        closest_to_spawn_stations[p]=(closest_to_spawn, min_d_to_spawn)
        closest_to_des_stations[p]=(closest_to_des, min_d_to_des)
        #thus they are in the form {passenger: ((x,y), d), ...}
    for p in test_set:
        if (closest_to_spawn_stations[p][0], closest_to_des_stations[p][0]) in routes.keys():
            p_route=routes[(closest_to_spawn_stations[p][0], closest_to_des_stations[p][0])]
        elif (closest_to_des_stations[p][0], closest_to_spawn_stations[p][0]) in routes.keys():
            p_route=routes[(closest_to_des_stations[p][0], closest_to_spawn_stations[p][0])]
        #thus p_route is a dictionary in the form {"path": ..., "time": ...}
        #it can be proven that for the Dijkstra algorithm, it will not pick a route in form that
        #i and i+2 are in the same line but i+1 is an interchange,
        #for there will always be a better route than that (which is to go straight from i to i+2 in the same line)
        #thus the determination of interchange need not consider that "i and i+2 not in same line" will miss interchanges
        if len(p_route["path"]) >=3:    
            for step in range(len(p_route["path"])-2):
                butt_in_lines=reverse_lines[p_route["path"][step]]
                head_in_lines=reverse_lines[p_route["path"][step+2]]
                middle_in_lines=reverse_lines[p_route["path"][step+1]]
                common_line_butt_middle=set(butt_in_lines) & set(middle_in_lines)
                common_line_head_middle=set(head_in_lines) & set(middle_in_lines)
                if common_line_butt_middle and common_line_head_middle and common_line_butt_middle != common_line_head_middle:
                    if p not in interchanges:
                        interchanges[p]=[]
                    interchanges[p].append(p_route["path"][step+1])
        else:
            interchanges[p]=[]
        #thus interchanges is in the form {passenger: [interchange stations], ...}
    line_capacity={}
    
    #up to now, what we have for upcoming code are:
    #reverse_lines, stations, closest_to_spawn/des_stations, interchanges, and all that are passed in

def action_tos(closest_to_spawn_stations, psgr):
    if closest_to_spawn_stations[psgr][1] ==0: #这里需要向下取整floor
        psgr.status=status.WAITING
        return
    else:
        closest_to_spawn_stations[psgr][1] = closest_to_spawn_stations[psgr][1] -1
        return

def action_w(city_map, test_set, lines, paths, routes, c, lagp, reverse_lines, stations,
             closest_to_spawn_stations, closest_to_des_stations, interchanges, psgr, waiting_on):
    #there is proof that for every sub point in a Dijkstra path, the route to the same destination will
    #follow the remaining route of the original
    #这里我想做一个mapping，把interchanges给map到route（这个route是subpoint到终点的route，根据Dijkstra算法的证明可知其依然会沿着原来的路线走）上去，
    #这样就知道哪个interchange（或没有interchange）离waiting_on最近，而且这个最近即为真正的下一个interchange，因为是从route取得的
    if (waiting_on, closest_to_des_stations[psgr][0]) in routes:
        route=routes[(waiting_on, closest_to_des_stations[psgr][0])]["path"]
    else:
        route=routes[(closest_to_des_stations[psgr][0], waiting_on)]["path"]
    if interchanges[psgr] 为空:
        going_to=closest_to_des_stations[psgr][0]
    else:
        for i in route:
            for j in interchanges[psgr]:
                if j == i:
                    going_to=i
    #thus getting going_to
    if line_pop
    

def simulation(city_map, test_set, lines, paths, routes, c, lagp, reverse_lines, stations, 
               closest_to_spawn_stations, closest_to_des_stations, interchanges):
    #now the timer starts, passengers will call on different action functions based on their status
    line_pop={}
    #line_pop is in the form {line_number: {"current":, "max": }, ...}
    for sec in range(1, 1441):
        random.seed()
        for psgr in test_set: #这里改成每秒都随机洗牌一次乘客顺序
            if psgr.status == status.TO_ON_STATION:
                action_tos(closest_to_spawn_stations, psgr)
                if psgr.status == status.WAITING:
                    waiting_on=closest_to_spawn_stations[psgr][0]
                    action_w(psgr, waiting_on)