#!/usr/local/bin/python
import math


epsilon = 1e-7


def line(l):
    p1 = l[0]
    p2 = l[1]
    A = (p1[1] - p2[1])
    B = (p2[0] - p1[0])
    C = (p1[0] * p2[1] - p2[0] * p1[1])
    return A, B, -C


def in_segment(a, b, x):
    if abs(a[0] - b[0]) < epsilon:
        return min(a[1],b[1]) <= x[1] <= max(a[1],b[1])
    return min(a[0],b[0]) <= x[0] <= max(a[0],b[0])


def in_semirecta(a, b, x):
    if abs(a[0] - b[0]) < epsilon:
        ax = a[1]
        bx = b[1]
        xx = x[1]
    else:
        ax = a[0]
        bx = b[0]
        xx = x[0]
    if ax < bx:
        return ax <= xx
    else:
        return xx <= ax


# l1 is a segment [[x0,y0],[x1,y1]]
# l2 is a semirecta [[x0,y0],[x1,y1]] starting at P0 and directed towards P1
def intersection(l1, l2):
    L1 = line(l1)
    L2 = line(l2)
    D = L1[0] * L2[1] - L1[1] * L2[0]
    Dx = L1[2] * L2[1] - L1[1] * L2[2]
    Dy = L1[0] * L2[2] - L1[2] * L2[0]
    if D != 0:
        x = Dx / D
        y = Dy / D
        if in_segment(l1[0], l1[1], [x,y]) and in_semirecta(l2[0], l2[1], [x,y]):
            return x, y
    return False


def distance(p1, p2):
    return math.sqrt(math.pow(p2[0] - p1[0], 2) + math.pow(p2[1] - p1[1], 2))


class World:
    def __init__(self, file):
        self.walls = []
        f = open(file, 'r')
        l = f.readline()
        start_pos = eval(l)
        start_pos[2] *= math.pi / 180
        self.start_pos = start_pos
        self.car = Car(self.start_pos)
        l = f.readline()
        while l != "":
            self.walls.append(Wall(eval(l)))
            l = f.readline()

    def reset_car_position(self):
        self.car.set_pos(self.start_pos)

    def get_sensors(self):
        res = []
        for s in range(5):
            dist = 999999
            sensor_line = self.get_sensor_line(s)
            for w in self.walls:
                inters = intersection(w.get_line(), sensor_line)
                print("Intersection with wall " + str(w) + ": " + str(inters))
                if type(inters) != bool:
                    d = distance(self.car.get_pos(), inters)
                    dist = min(d, dist)
            res.append(dist)
        return res

    def get_sensor_line(self, sensor):
        d_a = (sensor - 2) * math.pi / 4
        p2 = [self.car.x + math.cos(self.car.a + d_a), self.car.y + math.sin(self.car.a + d_a)]
        print("Sensor " + str(sensor) + " line: " + str((self.car.get_pos(), p2)))
        return [self.car.get_pos(), p2]

    def nextStep(self, delta_angle):
        self.car.a += delta_angle
        self.car.advance()


class Car:
    def __init__(self, pos):
        self.x = pos[0]
        self.y = pos[1]
        self.a = pos[2]

    def set_pos(self, pos):
        self.x = pos[0]
        self.y = pos[1]
        self.a = pos[2]

    def get_pos(self):
        return [self.x, self.y]

    def get_ang(self):
        return self.a

    def advance(self):
        self.x += math.cos(self.a)
        self.y += math.sin(self.a)


class Wall:
    def __init__(self, wall_description):
        self.x0 = wall_description[0][0]
        self.y0 = wall_description[0][1]
        self.x1 = wall_description[1][0]
        self.y1 = wall_description[1][1]

    def get_line(self):
        return [[self.x0, self.y0], [self.x1, self.y1]]

    def __repr__(self):
        return "Wall: " + str(self.get_line())


print("Heil Welt!")

# car = Car([0,0,0])
# print("Car: " + str(car.get_pos()) + ", " + str(car.get_ang()) + ")")

world = World("track1.txt")
print(str(world.walls))
print("Car: " + str(world.car.get_pos()) + ", " + str(world.car.get_ang()) + ")")
print("Sensors: " + str(world.get_sensors()))
# for i in range(20):
#    world.nextStep(math.pi/10)
#    print("Car: " + str(world.car.get_pos()) + ", " + str(world.car.get_ang()) + ")")
#    print("Sensors: " + str(world.get_sensors()))
# print(str(math.pi*3))


#def f_range(x, y, jump):
#    while x < y:
#        yield x
#        x += jump


#for x in f_range(-1,2,0.2):
#    print(str([x,0]) + " in semirecta [0,0],[0,1] -> " + str(in_semirecta([0,0], [1,0], [x,0])))