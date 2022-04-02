import turtle
import random

############
#  WINDOW  #
############

wn = turtle.Screen()
wn.bgcolor("black")
wn.tracer(0, 0)

wn.setup(480, 600)
wn.bgpic("backboard.gif")
wn.register_shape("truck.gif")
wn.register_shape("tree.gif")
wn.register_shape("frog.gif")

car_vert_positions = [-240, -200, -160, -120, -80]  # car tracks xcor on the road
tree_vert_positions = [0.0, 40.0, 80.0, 120.0, 160.0]
colors = ["red", "orange", "yellow", "green", "blue", "purple"]
cars = []  # will store car objects in a list
trees = []
player_stamps = []
gen_speed = 1500  # counter goes up by one every loop, if % == 0 by this number, spawn a car / tree
in_pocket = False
score = 0
lives = 5

pen = turtle.Turtle()
pen.penup()
pen.ht()
pen.goto(-200, 270)
pen.color("white")
pen.write(f"Score: {score}    Lives: {lives}", font=("Press Start 2P", 15, "normal"))


class Car:
    def __init__(self):
        self.car = turtle.Turtle()
        self.car.penup()
        self.car.shape("truck.gif")

        self.speed = -0.1

        self.start_pos()

    def start_pos(self):
        self.car.goto(self.car.xcor() + 300, random.choice(car_vert_positions))

    def move(self):
        self.car.goto(self.car.xcor() + self.speed, self.car.ycor())


class Tree:
    def __init__(self):
        self.tree = turtle.Turtle()
        self.tree.penup()
        self.tree.shape("tree.gif")
        self.water_track = random.choice(tree_vert_positions)

        if not tree_vert_positions.index(self.water_track) % 2:
            self.speed = -0.1
            self.LEFT_OR_RIGHT = 300
        else:
            self.speed = 0.1
            self.LEFT_OR_RIGHT = -300

        self.start_pos()

    def start_pos(self):
        self.tree.goto(self.tree.xcor() + self.LEFT_OR_RIGHT, self.water_track)

    def move(self):
        self.tree.goto(self.tree.xcor() + self.speed, self.tree.ycor())


class Player:
    def __init__(self):
        self.player = turtle.Turtle()
        self.player.shape("frog.gif")
        self.player.penup()

    def update(self):
        self.player.goto(self.player.xcor(), self.player.ycor())
        self.player.shape("frog.gif")
        stamp = self.player.stamp()
        player_stamps.append(stamp)

    def start_pos(self):
        self.player.goto(0, -280)

    def go_up(self, distance=40):
        self.player.goto(self.player.xcor(), self.player.ycor() + distance)

    def go_right(self, distance=40):
        self.player.goto(self.player.xcor() + distance, self.player.ycor())

    def go_down(self):
        if self.player.ycor() > -280:
            self.go_up(-40)

    def go_left(self):
        if frog.player.xcor() > -210 and not self.player.ycor() == 0:
            self.go_right(-40)
        elif frog.player.ycor() >= 0:
            self.go_right(-40)


def touched_pocket():
    global score, lives, in_pocket, player_in_pocket  # player in pocket is a clone of the player, but in the pocket

    score += 1
    pen.clear()
    pen.write(f"Score: {score}    Lives: {lives}", font=("Press Start 2P", 15, "normal"))
    in_pocket = True

    player_in_pocket = frog.player.clone()
    frog.start_pos()


def die():
    global score, lives, frog
    lives -= 1
    if lives <= 0:
        quit()

    frog.start_pos()
    print(lives)
    pen.clear()
    pen.write(f"Score: {score}    Lives: {lives}", font=("Press Start 2P", 15, "normal"))


def gen_car():
    car = Car()
    cars.append(car)


def gen_tree():
    tree = Tree()
    trees.append(tree)


frog = Player()
frog.start_pos()

wn.listen()
wn.onkeypress(frog.go_up, "w")
wn.onkeypress(frog.go_down, "s")
wn.onkeypress(frog.go_left, "a")
wn.onkeypress(frog.go_right, "d")

gen_car()

slow_down_timer = 0

###############
#  GAME LOOP  #
###############
while True:
    frog.player.clearstamps()

    player_x = frog.player.xcor()
    player_y = frog.player.ycor()

    # KILL IF OUT OF BOUNDS
    if frog.player.xcor() >= 260 or frog.player.xcor() <= -260:
        print("player went out of bounds")
        die()

    if 185 < player_x < 225 and player_y >= 200:
        touched_pocket()
    if 85 < player_x < 125 and player_y >= 200:
        touched_pocket()
    if -25 < player_x < 15 and player_y >= 200:
        touched_pocket()
    if -125 < player_x < -85 and player_y >= 200:
        touched_pocket()
    if -225 < player_x < -185 and player_y >= 200:
        touched_pocket()

    on_water = True

    ###############
    #  CAR LOGIC  #
    ###############
    for index, car in enumerate(cars):
        if len(cars) > 5:
            cars.pop(0)
        if frog.player.ycor() == car.car.ycor() and car.car.xcor() + 30 >= frog.player.xcor() >= car.car.xcor() - 30:
            die()

        car.car.clear()
        car.move()

        if car.car.xcor() < -300:
            car.car.clear()
            car.car.goto(1000, 1000)
            del cars[index]

    ################
    #  TREE LOGIC  #
    ################

    for index, tree in enumerate(trees):
        if len(trees) > 5:
            trees.pop(0)

        ##################
        #  IF ON BRANCH  #
        ##################
        if frog.player.ycor() == tree.tree.ycor() and tree.tree.xcor() + 55 >= frog.player.xcor() >= tree.tree.xcor() - 55:
            if tree.speed == -0.1:
                frog.player.goto(frog.player.xcor() + -0.1, frog.player.ycor())
            else:
                frog.player.goto(frog.player.xcor() + 0.1, frog.player.ycor())
            on_water = False

        tree.tree.clear()
        tree.move()

        ######################
        #  IF OUT OF BOUNDS  #
        ######################
        if tree.tree.xcor() < -300:
            tree.tree.clear()
            tree.tree.goto(1000, 1000)
            del trees[index]

    ######################
    #  KILL IF ON WATER  #
    ######################
    if frog.player.ycor() >= 0 and on_water and not in_pocket:
        die()

    ####################
    #  GEN TREE & CAR  #
    ####################
    if slow_down_timer % gen_speed == 0:
        gen_car()

    if slow_down_timer % gen_speed == 0:
        gen_tree()

    frog.update()
    slow_down_timer += 1  # used to generate cars and trees
    wn.update()
