from enum import Enum
'''
1. pair_nums
class for a pair of points
'''
class pair_nums:
    def __init__(self, pair):
        #pair is in the form ((startx, starty), (endx, endy))
        self.pair=pair
    def sld(self, *coor):
        #coor is in the form (cx, cy)
        #sld stands for straight line distance
        A=self.pair[1][1] - self.pair[0][1]
        B=self.pair[0][0] - self.pair[1][0]
        C=self.pair[0][1]*self.pair[1][0] - self.pair[1][1]*self.pair[0][0]
        numerator=abs(A*coor[0] + B*coor[1] + C)
        denominator=(A**2 + B**2)**0.5
        if denominator==0:
            return 0.0
        distance=numerator/denominator
        return round(distance, 2)
'''
2. snake
class for a snake consisting of a tuple of stations ((x1,y1), ..., (xn,yn))
'''
class snake:
    def __init__(self, snakey):
        self.snakey=snakey
    def head(self):
        return self.snakey[-1]
    def butt(self):
        return self.snakey[0]
    def time(self, paths):
        time=0
        for i in range(len(self.snakey)-1):
            if (self.snakey[i], self.snakey[i+1]) in paths:
                time=time+paths[(self.snakey[i], self.snakey[i+1])]["time"]
            elif (self.snakey[i+1], self.snakey[i]) in paths:
                time=time+paths(self.snakey[i+1], self.snakey[i])["time"]
        return time
    def body(self, paths):
        body=[]
        for i in range(len(self.snakey)-1):
            if (self.snakey[i], self.snakey[i+1]) in paths:
                for point in paths[(self.snakey[i], self.snakey[i+1])]["path"]:
                    body.append(point)
            elif (self.snakey[i+1], self.snakey[i]) in paths:
                for point in paths[(self.snakey[i+1], self.snakey[i])]["path"]:
                    body.append(point)
        return body
    def grow(self, new_station):
        new_snakey=self.snakey.copy()
        new_snakey.append(new_station)
        return snake(new_snakey)
'''
3. passenger
class for passengers in the map
'''
class status(Enum):
    TO_ON_STATION=1
    WAITING=2
    IN_METRO=3
    FROM_OFF_STATION=4
    FINISHED=5

class passenger:
    def __init__(self, spawn_time, spawn_point, destination_point, lag_penalty, status):
        self.spawn_time=spawn_time
        self.spawn_point=spawn_point
        self.destination_point=destination_point
        self.lag_penalty=lag_penalty
        self.status=status
        