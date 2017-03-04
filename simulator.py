#!/usr/local/bin/python
import math


def line(p1, p2):
    A = (p1[1] - p2[1])
    B = (p2[0] - p1[0])
    C = (p1[0] * p2[1] - p2[0] * p1[1])
    return A, B, -C


def intersection(L1, L2):
    D = L1[0] * L2[1] - L1[1] * L2[0]
    Dx = L1[2] * L2[1] - L1[1] * L2[2]
    Dy = L1[0] * L2[2] - L1[2] * L2[0]
    if D != 0:
        x = Dx / D
        y = Dy / D
        return x, y
    else:
        return False


def distance(p1, p2):
    return math.sqrt(math.pow(p2[0] - p1[0], 2), math.pow(p2[1] - p1[1], 2))


class World:
    def __init__(self, file):
        self.walls = []
        f = open(file, 'r')
        l = f.readline()
        self.start_pos = eval(l)
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
            for l in self.walls:
                inters = intersection(line(l[0], l[1]), line(self.car.get_pos(), self.get_sensor_line(s)))
                d = distance(self.car.get_pos(), inters)
                dist = min(d, dist)
            res.append(dist)
        return res

    def get_sensor_line(self, sensor):
        d_a = (sensor - 2) * math.pi / 4
        p2 = [self.car.x + math.cos(self.car.a + d_a), self.car.y + math.sin(self.car.a + d_a)]
        return line(self.car.get_pos(), p2)

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
        self.x1 = wall_description[0][1]
        self.y0 = wall_description[1][0]
        self.y1 = wall_description[1][1]


print("Heil Welt!")

car = Car([0,0,0])
print("Car: " + str(car.get_pos()) + ", " + str(car.get_ang()) + ")")
for i in range(40):
    car.a += math.pi/10
    car.advance()
    print("Car: " + str(car.get_pos()) + ", " + str(car.get_ang()) + ")")
