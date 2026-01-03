'''
input:
city_map
output:
set of class passengers
'''
'''
notes
for Monte Carlo, we take a pseudo-physics approach to get the set of passengers
for each point on city_map, define gravity
g = w^2 * u
w: weight of point
u: normalization of the distance coefficient u = distance/map_length, thus u is between 0 and 1
when a "ball" is dropped onto a random point on city_map, it starts its one and only determinization
the ball picks the point that has the biggest gravity pull on it, then proceeds to go to that point
on the way there will be a friction hindering the ball, friction is random based on a normal distribution
if the "potential energy" of the point is decayed by the "friction work", i.e. w^2 * u^0.5 = f * u
then the ball will stop at the distance it lost all energy and move to the nearest point from that position
release a number of balls of equal density on the whole city_map
the positions of balls after the process will be the spawn position
'''
from useful_classes import passenger, status
import pandas
import random
import numpy as np
def single_ball_movement(city_map, ball_coor):
    #ball_coor is in the form (x,y)
    gravities={}
    m=max(len(city_map.index), len(city_map.columns))
    for x in city_map.columns:
        for y in city_map.index:
            w=city_map.loc[y,x]
            d=((ball_coor[0]-x)**2+(ball_coor[1]-y)**2)**0.5
            u=d/m
            g=(w**2)*u
            gravities[(x,y)]=g
    maxg = max(gravities.values())
    candidate_points = [point for point, g in gravities.items() if g == maxg]
    maxpoint = random.choice(candidate_points)
    #maxpoint is in the form (x,y)
    #for ball to maxpoint, there is maxw, maxu, thus there will be maxd
    #based on the function w^2 * u^0.5 = f * u, the deducted function of u is u = (w^2 / f)^2
    #if u is bigger than maxu, ball will get to point
    #if u is smaller than maxu, stop, go to nearest point
    #delta x = (u/maxu) * (maxpointx - ballx)
    #delta y = (u/maxu) * (maxpointy - bally)
    #because there will be a fair chance that f < w^2 / sprt maxu, u > maxu has a fair chance of occuring
    #the value of f is provided through function f=Fp, where F is a constant and p ~ N(mean, sd^2)
    #judging from the fact that w is in [1,10], have F=2, p ~ N(0.6, 0.04)
    maxw=city_map.loc[maxpoint[1], maxpoint[0]]
    maxd=((ball_coor[0]-maxpoint[0])**2+(ball_coor[1]-maxpoint[1])**2)**0.5
    maxu= maxd/m
    F=2
    f=np.random.normal(loc= 0.6, scale= 0.2)
    f=F*d
    bu=(maxw**2 / f)**2
    if bu >= maxu:
        return maxpoint
    elif bu < maxu:
        deltax = (bu/maxu)*(maxpoint[0]-ball_coor[0])
        deltay = (bu/maxu)*(maxpoint[1]-ball_coor[1])
        ball_coor=(ball_coor[0]+deltax, ball_coor[1]+deltay)
        distances={}
        for ux in city_map.columns:
            for uy in city_map.index:
                distances[(ux,uy)]=((ball_coor[0]-ux)**2+(ball_coor[1]-uy)**2)**0.5
        mind = min(distances.values())
        same_distances = [point for point, d in distances.items() if d == mind]
        settle_point = random.choice(same_distances)
        return settle_point
    #thus single_ball_movement could handle any ball at an initial starting point and return the point in the map where it settles
    #thus the point it settles is its spawn_point

def monte_carlo(city_map, lagp):
    test_set=[]
    map_x_axis=city_map.columns
    map_y_axis=city_map.index
    ball_x_axis=[]
    ball_y_axis=[]
    for i in range(len(map_x_axis)-1):
        ones=map_x_axis[i]
        ball_x_axis.append(ones+0.1, ones+0.2, ones+0.3, ones+0.4, ones+0.5, ones+0.6, ones+0.7, ones+0.8, ones+0.9)
    for j in range(len(map_y_axis)-1):
        ones=map_y_axis[j]
        ball_y_axis.append(ones+0.1, ones+0.2, ones+0.3, ones+0.4, ones+0.5, ones+0.6, ones+0.7, ones+0.8, ones+0.9)
    #thus getting the dense equally distributed map of balls
    #by setting back 1 decimal point, ball number is 100 times the map size
    points=[]
    for p in city_map.columns:
        for q in city_map.index:
            points.append((p,q))
    for m in ball_x_axis:
        for n in ball_y_axis:
            sp=single_ball_movement(city_map, (m,n))
            st=random.randint(0, 1440)
            dp=random.choice(points)
            ball=passenger(st, sp, dp, lagp, status.TO_ON_STATION)
            test_set.append(ball)
    return test_set