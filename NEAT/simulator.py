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
        return min(a[1], b[1]) <= x[1] <= max(a[1], b[1])
    return min(a[0], b[0]) <= x[0] <= max(a[0], b[0])


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
def intersection_segment_semirecta(l1, l2):
    L1 = line(l1)
    L2 = line(l2)
    D = L1[0] * L2[1] - L1[1] * L2[0]
    Dx = L1[2] * L2[1] - L1[1] * L2[2]
    Dy = L1[0] * L2[2] - L1[2] * L2[0]
    if D != 0:
        x = Dx / D
        y = Dy / D
        if in_segment(l1[0], l1[1], [x, y]) and in_semirecta(l2[0], l2[1], [x, y]):
            return x, y
    return False


# l1 and l2 are segments [[x0,y0],[x1,y1]]
def intersection_segments(l1, l2):
    L1 = line(l1)
    L2 = line(l2)
    D = L1[0] * L2[1] - L1[1] * L2[0]
    Dx = L1[2] * L2[1] - L1[1] * L2[2]
    Dy = L1[0] * L2[2] - L1[2] * L2[0]
    if D != 0:
        x = Dx / D
        y = Dy / D
        if in_segment(l1[0], l1[1], [x, y]) and in_segment(l2[0], l2[1], [x, y]):
            return x, y
    return False


def distance(p1, p2):
    return math.sqrt(math.pow(p2[0] - p1[0], 2) + math.pow(p2[1] - p1[1], 2))


class World:
    speed = 1
    angular_speed_limit = speed * math.pi / 18  # 10º

    def __init__(self, file):
        self.walls = []
        self.goals = []
        self.next_goal = 0
        self.laps = 0
        f = open(file, 'r')
        l = f.readline()
        start_pos = eval(l)
        start_pos[2] *= math.pi / 180
        self.start_pos = start_pos
        self.car = Car(self.start_pos)
        f.readline()  # "Walls\n"
        l = f.readline()
        while l != "Goals\n":
            self.walls.append(Wall(eval(l)))
            l = f.readline()
        l = f.readline()
        while l != "":
            self.goals.append(Goal(eval(l)))
            l = f.readline()

    def reset_car_position(self):
        self.car.set_pos(self.start_pos)
        self.next_goal = 0
        self.laps = 0

    def set_speed(self,speed):
        self.angular_speed_limit *= speed/self.speed
        self.speed = speed

    @property
    def num_goals(self):
        return len(self.goals)

    def get_sensor_line(self, sensor):
        d_a = (sensor - 2) * math.pi / 4
        p2 = [self.car.x + math.cos(self.car.a + d_a), self.car.y + math.sin(self.car.a + d_a)]
        return [self.car.get_pos, p2]

    def get_sensor(self, sensor):
        dist = 999999
        sensor_line = self.get_sensor_line(sensor)
        for w in self.walls:
            inters = intersection_segment_semirecta(w.get_line, sensor_line)
            if type(inters) != bool:
                d = distance(self.car.get_pos, inters)
                dist = min(d, dist)
        return dist

    def get_sensors(self):
        res = []
        for s in range(5):
            res.append(self.get_sensor(s))
        return res

    # def get_forward_line(self, pos):
    #     p2 = [pos[0] + math.cos(self.car.a), pos[1] + math.sin(self.car.a)]
    #     return [pos, p2]
    #
    # def get_dist_to_obstacle(self):
    #     dist_r = 999999
    #     dist_l = 999999
    #     forward_line_right = self.get_forward_line(self.car.get_front_right_pos)
    #     forward_line_left = self.get_forward_line(self.car.get_front_left_pos)
    #     for w in self.walls:
    #         inters_r = intersection_segment_semirecta(w.get_line, forward_line_right)
    #         inters_l = intersection_segment_semirecta(w.get_line, forward_line_left)
    #         if type(inters_r) != bool:
    #             dist_r = min(distance(self.car.get_front_right_pos, inters_r), dist_r)
    #         if type(inters_l) != bool:
    #             dist_l = min(distance(self.car.get_front_left_pos, inters_l), dist_l)
    #     return min(dist_l, dist_r)

    def will_collide(self):
        init_container_pos = self.car.get_4_container_pos
        for init_pos in init_container_pos:
            final_pos = [init_pos[0] + math.cos(self.car.a), init_pos[1] + math.sin(self.car.a)]
            for w in self.walls:
                if type(intersection_segments([init_pos, final_pos], w.get_line)) != bool:
                    return True
        return False

    def next_step(self, delta_angle):
        if delta_angle > self.angular_speed_limit:
            delta_angle = self.angular_speed_limit
        elif delta_angle < -self.angular_speed_limit:
            delta_angle = self.angular_speed_limit

        self.car.a += delta_angle

        # Check if there is a collision with a wall
        # if self.get_dist_to_obstacle() < self.speed:
        if self.will_collide():
            self.car.advance(self.speed)
            return -1

        # Count the number of goals crossed
        sensor_line = self.get_sensor_line(2)
        n = 0  # num goals crossed
        to_eliminate = []
        g = self.goals[self.next_goal]
        inters = intersection_segment_semirecta(g.get_line, sensor_line)
        if type(inters) != bool and distance(self.car.get_pos, inters) < self.speed:
            self.next_goal += 1
            if self.next_goal >= self.num_goals:
                self.next_goal = 0
                self.laps += 1
            ret = 1
        else: ret = 0

        self.car.advance(self.speed)
        return ret


class Car:
    width = 3
    length = 5

    def __init__(self, pos):
        self.x = pos[0]
        self.y = pos[1]
        self.a = pos[2]

    def set_pos(self, pos):
        self.x = pos[0]
        self.y = pos[1]
        self.a = pos[2]

    @property
    def get_pos(self):
        return [self.x, self.y]

    @property
    def get_front_left_pos(self):
        return [self.x + self.length/2 * math.cos(self.a) + self.width/2 * math.cos(self.a + math.pi/2),
                self.y + self.length/2 * math.sin(self.a) + self.width/2 * math.sin(self.a + math.pi/2)]

    @property
    def get_front_right_pos(self):
        return [self.x + self.length/2 * math.cos(self.a) + self.width/2 * math.cos(self.a - math.pi/2),
                self.y + self.length/2 * math.sin(self.a) + self.width/2 * math.sin(self.a - math.pi/2)]

    @property
    def get_4_container_pos(self):
        return [
            [self.x + self.length / 2 * math.cos(self.a) + self.width / 2 * math.cos(self.a + math.pi / 2),
             self.y + self.length / 2 * math.sin(self.a) + self.width / 2 * math.sin(self.a + math.pi / 2)],
            [self.x - self.length / 2 * math.cos(self.a) + self.width / 2 * math.cos(self.a + math.pi / 2),
             self.y - self.length / 2 * math.sin(self.a) + self.width / 2 * math.sin(self.a + math.pi / 2)],
            [self.x - self.length / 2 * math.cos(self.a) + self.width / 2 * math.cos(self.a - math.pi / 2),
             self.y - self.length / 2 * math.sin(self.a) + self.width / 2 * math.sin(self.a - math.pi / 2)],
            [self.x + self.length / 2 * math.cos(self.a) + self.width / 2 * math.cos(self.a - math.pi / 2),
             self.y + self.length / 2 * math.sin(self.a) + self.width / 2 * math.sin(self.a - math.pi / 2)]
        ]

    @property
    def get_ang(self):
        return self.a

    def advance(self, speed):
        self.x += speed * math.cos(self.a)
        self.y += speed * math.sin(self.a)


class Wall:
    def __init__(self, wall_description):
        self.x0 = wall_description[0][0]
        self.y0 = wall_description[0][1]
        self.x1 = wall_description[1][0]
        self.y1 = wall_description[1][1]

    @property
    def get_line(self):
        return [[self.x0, self.y0], [self.x1, self.y1]]

    def __repr__(self):
        return "Wall: " + str(self.get_line)


class Goal:
    def __init__(self, wall_description):
        self.x0 = wall_description[0][0]
        self.y0 = wall_description[0][1]
        self.x1 = wall_description[1][0]
        self.y1 = wall_description[1][1]

    @property
    def get_line(self):
        return [[self.x0, self.y0], [self.x1, self.y1]]

    def __repr__(self):
        return "Goal: " + str(self.get_line)



# car = Car([0,0,0])
# print("Car: " + str(car.get_pos()) + ", " + str(car.get_ang()) + ")")

# world = World("track1.txt")
# print(str(world.walls))
# print("Car: " + str(world.car.get_pos) + ", " + str(world.car.get_ang) + ")")
# print("Sensors: " + str(world.get_sensors()))
# for i in range(100):
#     ns = world.next_step(0)
#     print("Next step -------> " + str(ns))
#     if ns < 0:
#         print("\n\n\n\n\nPARET!!\n\n\n\n\n")
#     elif ns > 0:
#         print("\n\nMETA!!   " + str(ns) + "\n\n")
#     print("Car: " + str(world.car.get_pos) + ", " + str(world.car.get_ang) + ")")
#     print("Sensors: " + str(world.get_sensors()))


# def f_range(x, y, jump):
#    while x < y:
#        yield x
#        x += jump


# for x in f_range(-1,2,0.2):
#    print(str([x,0]) + " in semirecta [0,0],[0,1] -> " + str(in_semirecta([0,0], [1,0], [x,0])))

# car = Car([0,0,0])
# print(str(car.get_4_container_pos))