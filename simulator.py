#!/usr/local/bin/python

class World:

    def __init__(self, file):
        self.car = Car()
        self.walls = []
        self.set_map(file)

    def set_map(self, file):
        f = open(file, 'r')
        l = f.readline()
        self.car.set_start_pos(eval(l))
        l = f.readline()
        while l != "":
            self.walls.append(Wall(eval(l)))
            l = f.readline()

    def car(self):
        return self.car

    def nextStep(self, delta_angle):
        return "noob"

class Car:

    def __init__(self):
        self.x = 0
        self.y = 0
        self.a = 0

    def set_start_pos(self, start_pos):
        self.x = start_pos[0]
        self.y = start_pos[1]
        self.a = start_pos[2]


class Wall:

    def __init__(self, wall_description):
        self.x0 = wall_description[0][0]
        self.x1 = wall_description[0][1]
        self.y0 = wall_description[1][0]
        self.y1 = wall_description[1][1]

print("Heil Welt!")