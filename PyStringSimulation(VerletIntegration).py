#STRING SIMULATION - ANG WEIHENG 10C
import turtle as t
import math as m
tscreen = t.Screen()
tscreen.bgcolor("black")
tscreen.tracer(0)
t.hideturtle()
t.up()
t.color("white")
grav_constant = 2
x_constant = 0
click_mode = "set_point"
set_lock = False
first_point = None
animation_lock = False
stick_select = t.Turtle(); stick_select.hideturtle(); stick_select.up()
draw_stick = t.Turtle(); draw_stick.hideturtle(); draw_stick.up(); draw_stick.color("white"); draw_stick.width(2)
draw_point = t.Turtle(); draw_point.hideturtle(); draw_point.up(); draw_point.color("white")
def change_gravity():
    global grav_constant
    grav_constant += 6
def left_force():
    global x_constant, grav_constant
    x_constant -= 12
    grav_constant += 3
def right_force():
    global x_constant, grav_constant
    x_constant += 12
    grav_constant += 3
class Point:
    def __init__(self, x, y, is_movable):
        self.x = x
        self.y = y
        self.previous_x = x
        self.previous_y = y
        self.is_movable = is_movable
    def change_position(self):
        global x_constant, grav_constant
        if (x_constant > 0):
            x_constant -= 0.008
        if (x_constant < 0):
            x_constant += 0.008
        if (grav_constant > -3):
            grav_constant -= 0.0008
        if (not self.is_movable):
            return
        #change the position of the point by y - 1, previous position change
        #mirrors velocity, gravitational acceleration
        self.x += self.x - self.previous_x + x_constant
        self.y += self.y - self.previous_y + grav_constant
        #print(self.x - self.previous_x, self.y - self.previous_y)
        #self.x += x_constant
        #self.y += grav_constant
class Stick:
    def __init__(self, Point1, Point2):
        self.Point1 = Point1
        self.Point2 = Point2
        self.point_distance = m.sqrt(pow(Point1.x - Point2.x, 2) + pow(Point1.y - Point2.y, 2))
    def constrain_points(self):
        if (not self.Point1.is_movable and not self.Point2.is_movable):
            return
        elif (self.Point1.is_movable and self.Point2.is_movable):
            pointa = [self.Point1.x, self.Point1.y]
            pointb = [self.Point2.x, self.Point2.y]
            midpoint = [(pointa[0] + pointb[0]) / 2, (pointa[1] + pointb[1]) / 2]
            vector_b = [pointb[0] - pointa[0], pointb[1] - pointa[1]] #invert later for vector_a
            b_magnitude = m.sqrt(pow(vector_b[0], 2) + pow(vector_b[1], 2))
            unit_b = [(vector_b[0] * self.point_distance) / (b_magnitude * 2), (vector_b[1] * self.point_distance) / (b_magnitude * 2)]
            self.Point1.x = midpoint[0] - unit_b[0]; self.Point1.y = midpoint[1] - unit_b[1]
            self.Point2.x = midpoint[0] + unit_b[0]; self.Point2.y = midpoint[1] + unit_b[1]
        else:
            immovable = [self.Point1.x, self.Point1.y]
            movable = [self.Point2.x, self.Point2.y]
            if (self.Point1.is_movable):
                immovable, movable = movable, immovable
            midpoint = [(immovable[0] + movable[0]) / 2, (immovable[1] + movable[1]) / 2]
            vector_b = [movable[0] - immovable[0], movable[1] - immovable[1]] #invert later for vector_a
            b_magnitude = m.sqrt(pow(vector_b[0], 2) + pow(vector_b[1], 2))
            if (m.isclose(b_magnitude, 0)):
                b_magnitude += 0.0000000001
            unit_b = [vector_b[0] * self.point_distance / b_magnitude, vector_b[1] * self.point_distance / b_magnitude]
            if (self.Point1.is_movable):
                self.Point1.x = midpoint[0] - unit_b[0]; self.Point1.y = midpoint[1] - unit_b[1]
            else:
                self.Point2.x = midpoint[0] + unit_b[0]; self.Point2.y = midpoint[1] + unit_b[1]
#list_Stick = []
list_Point = []
list_Stick = [Stick(Point(0, 0, False), Point(0, 0, True))]
for i in range(0, 22):
    previous_Stick = list_Stick[len(list_Stick) - 1]
    point2 = previous_Stick.Point2
    list_Stick.append(Stick(point2, Point(point2.x + 10, 0, True)))
point_1 = Point(240, 10, True)
point_2 = Point(240, -10, True)
point_3 = Point(260, 0, True)
stick_1 = Stick(point_1, point_2)
stick_2 = Stick(list_Stick[len(list_Stick) - 1].Point2, point_1)
stick_3 = Stick(list_Stick[len(list_Stick) - 1].Point2, point_2)
stick_4 = Stick(point_1, point_3)
stick_5 = Stick(point_2, point_3)
stick_6 = Stick(list_Stick[len(list_Stick) - 1].Point2, point_3)
list_stick = [stick_1, stick_2, stick_3, stick_4, stick_5, stick_6]
list_Stick.extend(list_stick)
def animate():
    t.clear()
    for i in list_Stick:
        i.Point1.previous_x = i.Point1.x; i.Point1.previous_y = i.Point1.y
        i.Point2.previous_x = i.Point2.x; i.Point2.previous_y = i.Point2.y
        i.Point1.change_position()
        i.Point2.change_position()
    for j in range(0, 50):
        for i in list_Stick:
            i.constrain_points()
    for i in list_Stick:
        t.goto(i.Point1.x, i.Point1.y); t.dot(5, "white")
        #i.Point1.previous_x = i.Point1.x; i.Point1.previous_y = i.Point1.y
        t.down()
        t.goto(i.Point2.x, i.Point2.y); t.dot(5, "white")
        #i.Point2.previous_x = i.Point2.x; i.Point2.previous_y = i.Point2.y
        t.up()
    tscreen.ontimer(animate, 0)
def screen_onclick(x, y):
    if (animation_lock):
        return
    if (click_mode == "set_point"):
        draw_point.goto(x, y)
        if (set_lock):
            list_Point.append(Point(x, y, False))
            draw_point.dot(10, "white")
        else:
            list_Point.append(Point(x, y, True))
            draw_point.dot(10, "grey")
        draw_point.write(f"({x}, {y})", align = "center")
        tscreen.update()
    else:
        global first_point
        point = None
        for i in list_Point:
            distance = m.sqrt(pow(x - i.x, 2) + pow(y - i.y, 2))
            if (distance < 15):
                point = i
                break
        else:
            first_point = None
            stick_select.clear()
            return
        if (first_point == None):
            first_point = point
            stick_select.goto(point.x, point.y)
            stick_select.dot(10, "blue")
        else:
            list_Stick.append(Stick(first_point, point))
            stick_select.clear()
            draw_stick.goto(first_point.x, first_point.y)
            draw_stick.down()
            draw_stick.goto(point.x, point.y)
            draw_stick.up()
            first_point = None
        tscreen.update()
def start_animation():
    print("Animation started")
    global animation_lock
    if (animation_lock):
        return
    animation_lock = True
    draw_point.clear()
    draw_stick.clear()
    stick_select.clear()
    animate()
def change_mode():
    if (animation_lock):
        return
    global click_mode
    if (click_mode == "set_point"):
        click_mode = "set_stick"
    else:
        click_mode = "set_point"
    print(f"Click Mode: {click_mode}")
def change_lock():
    if (animation_lock):
        return
    global set_lock
    if (set_lock):
        set_lock = False
    else:
        set_lock = True
    print(f"Point Locked: {set_lock}")
tscreen.onkey(change_gravity, "space")
tscreen.onkey(left_force, "p")
tscreen.onkey(right_force, "q")
#tscreen.onkey(change_mode, "m")
tscreen.onkey(start_animation, "s")
#tscreen.onkey(change_lock, "l")
#tscreen.onclick(screen_onclick)
tscreen.listen()
tscreen.mainloop()