# Worlds 3.0
# John Yevsukov
# October 15, 2020

import math
import os
import random
import time
import turtle
from datetime import datetime, timedelta


game_screen = turtle.Screen()
game_screen.tracer(0)
game_screen.title("Worlds")
game_screen.bgpic("assets/sprites/bg.gif")
game_screen.bgcolor("navy")

turtle.register_shape("assets/sprites/ice_block.gif")

stamper = turtle.Turtle()
stamper.speed(0)
stamper.hideturtle()
stamper.shape("assets/sprites/ice_block.gif")
stamper.penup()

sprite_stamper = turtle.Turtle()
sprite_stamper.speed(0)
sprite_stamper.hideturtle()
sprite_stamper.penup()

obj = "push the button."
objective_pen = turtle.Turtle()
objective_pen.speed(0)
objective_pen.color("white")
objective_pen.penup()
objective_pen.setposition(-440, 420)
objectivestring = "Current Objective: {}".format(obj)
objective_pen.write(
    objectivestring, False, align="left", font=("comic sans ms", 20, "normal")
)
objective_pen.hideturtle()

GRAVITY = -3.2
STATE = False
FLOOR = -427

game_shapes = [
    "assets/sprites/bob.gif",
    "assets/sprites/bob_left.gif",
    "assets/sprites/bob_right.gif",
    "assets/sprites/flame.gif",
    "assets/sprites/button.gif",
    "assets/sprites/snow_ball.gif",
    "assets/sprites/fan.gif",
    "assets/sprites/snow_flake.gif",
    "assets/sprites/obo.gif",
    "assets/sprites/obo_left.gif",
    "assets/sprites/obo_right.gif",
    "assets/sprites/coin.gif",
]
for game_shape in game_shapes:
    turtle.register_shape(game_shape)

checker = turtle.Turtle()
checker.speed(0)
checker.shape("assets/sprites/coin.gif")
checker.hideturtle()
checker.penup()
checker.goto(-225, -127)
checker.stamp()

x = -475
y = 475
for _ in range(20):
    stamper.goto(x, y)
    stamper.stamp()
    y -= 50
x = -425
y = 475
for _ in range(19):
    stamper.goto(x, y)
    stamper.stamp()
    x += 50
x = 475
y = 425
for _ in range(19):
    stamper.goto(x, y)
    stamper.stamp()
    y -= 50
x = 425
y = -475
for _ in range(19):
    stamper.goto(x, y)
    stamper.stamp()
    x -= 50
x = -425
y = -325
for _ in range(16):
    stamper.goto(x, y)
    stamper.stamp()
    x += 50
    if x == -25:
        x = 75
x = -325
y = -175
for _ in range(14):
    stamper.goto(x, y)
    stamper.stamp()
    x += 50
x = -425
y = -25
for _ in range(16):
    stamper.goto(x, y)
    stamper.stamp()
    x += 50
    if x == -25:
        x = 75
x = -325
y = 125
for _ in range(16):
    stamper.goto(x, y)
    stamper.stamp()
    x += 50
    if x == -125:
        x = -25
    elif x == 75:
        x = 175
    elif x == 375:
        break


class Sprite:
    def __init__(self, x, y, shape, color):
        self.x = x
        self.y = y
        self.dx = 0
        self.dy = 0
        self.shape = shape
        self.color = color
        self.max_health = 100
        self.health = 100
        self.health_bar_size = 4
        self.left_token_bucket = []
        self.right_token_bucket = []
        self.up_token_bucket = []
        self.gravity = -3.2
        self.floor = -427

    def render(self, stamper):
        sprite_stamper.goto(self.x, self.y)
        sprite_stamper.shape(self.shape)
        sprite_stamper.color(self.color)
        sprite_stamper.stamp()


class Player(Sprite):
    def __init__(self, x, y, shape, color):
        super().__init__(x, y, shape, color)

    def render_health(self, stamper):
        sprite_stamper.goto(self.x - 10, self.y + 25)
        sprite_stamper.pensize(self.health_bar_size)
        sprite_stamper.color("lightgreen")
        sprite_stamper.pendown()
        sprite_stamper.setheading(0)
        sprite_stamper.fd(0.20 * self.health)
        if self.health < 100:
            sprite_stamper.color("red")
            sprite_stamper.fd(0.20 * (self.max_health - self.health))
        sprite_stamper.penup()

    def left(self):
        length = len(self.left_token_bucket)
        for _ in range(10 - length):
            self.left_token_bucket.append("token")

    def right(self):
        length = len(self.right_token_bucket)
        for _ in range(10 - length):
            self.right_token_bucket.append("token")

    def move_left(self):
        self.shape = "assets/sprites/bob_left.gif"
        self.x -= 5
        if self.x < -435:
            self.x = -435

    def move_right(self):
        self.shape = "assets/sprites/bob_right.gif"
        self.x += 5
        if self.x > 435:
            self.x = 435

    def up(self):
        if self.y == self.floor:
            length = len(self.up_token_bucket)
            for _ in range(1 - length):
                self.up_token_bucket.append("token")

    def jump(self):
        os.system("afplay assets/sounds/jump_2.wav&")
        self.y += 55

    def update(self):
        self.y += self.gravity
        if (self.x >= -20 and self.x <= 20 and self.y <= -250) or (
            self.x >= 385 and self.x <= 415 and self.y <= -102 and self.y >= -300
        ):
            self.gravity = 6
        else:
            self.gravity = -3.2
        if self.y <= self.floor:
            self.y = self.floor
        if (self.y >= -295 and self.x <= -50) or (self.y >= -295 and self.x >= 50):
            self.floor = -280
        else:
            self.floor = -427
        if self.y >= -150 and self.x >= -350 and self.x <= 350:
            self.floor = -130


class EnemyAI(Sprite):
    def __init__(self, x, y, shape, color):
        super().__init__(x, y, shape, color)

    def render_health(self, stamper):
        sprite_stamper.goto(self.x - 10, self.y + 25)
        sprite_stamper.pensize(self.health_bar_size)
        sprite_stamper.color("lightgreen")
        sprite_stamper.pendown()
        sprite_stamper.setheading(0)
        sprite_stamper.fd(0.20 * self.health)
        if self.health < 100:
            sprite_stamper.color("red")
            sprite_stamper.fd(0.20 * (self.max_health - self.health))
        sprite_stamper.penup()

    def left(self):
        length = len(self.left_token_bucket)
        for _ in range(10 - length):
            self.left_token_bucket.append("token")

    def right(self):
        length = len(self.right_token_bucket)
        for _ in range(10 - length):
            self.right_token_bucket.append("token")

    def move_left(self):
        self.shape = "assets/sprites/obo_left.gif"
        self.x -= 4
        if self.x < -435:
            self.x = -435

    def move_right(self):
        self.shape = "assets/sprites/obo_right.gif"
        self.x += 4
        if self.x > 435:
            self.x = 435

    def up(self):
        if self.y == self.floor:
            length = len(self.up_token_bucket)
            for _ in range(1 - length):
                self.up_token_bucket.append("token")

    """

    - we want to move away from hard coded coordiantes

        - statements like:
        ``` if (self.x >= -20 and self.x <= 20 and self.y <= -250) or (self.x >= 385 and self.x <= 415 and self.y <= -102 and self.y >= -300):```
        ...should be replaced with statements like:
        ```if self.in_fountain():```

        ...and:
        ```elif self.x < -50 and self.y == -280:```
        ...should be replaced with statements like:
        ```if self.colliding_with_boundary_left():```

    - Things like fountains should be classes
        - references to them should be stored in a list which will be a property of the world

    """

    def update(self):
        if self.y > player.y:
            if self.x >= 0 and self.y == -130:
                self.move_right()
            if self.x < 0 and self.y == -130:
                self.move_left()
            elif self.x < -50 and self.y == -280:
                self.move_right()
            elif self.x > 50 and self.y == -280:
                self.move_left()

        if self.y < player.y:
            if self.x >= 20 and self.y == -427:
                self.move_left()
            if self.x < -20 and self.y == -427:
                self.move_right()
            elif self.x < -50 and self.y == -280:
                self.move_right()
            elif self.x > 50 and self.y == -280:
                self.move_right()

        if self.x < player.x and (self.y <= player.y + 20 and self.y >= player.y - 20):
            self.move_right()
        if self.x > player.x and (self.y <= player.y + 20 and self.y >= player.y - 20):
            self.move_left()
        self.y += self.gravity
        if (self.x >= -20 and self.x <= 20 and self.y <= -250) or (
            self.x >= 385 and self.x <= 415 and self.y <= -102 and self.y >= -300
        ):
            self.gravity = 6
            if self.x < player.x and (self.y > player.y and player.y == -427):
                self.move_right()
            if self.x > player.x and (self.y > player.y and player.y == -427):
                self.move_left()
            if self.x < player.x and self.y > -260 and self.x < 90 and self.x > -90:
                self.move_right()
            if self.x > player.x and self.y > -260 and self.x > -90 and self.x < 90:
                self.move_left()
            if self.x < player.x and self.y > -60:
                self.move_right()
            if self.x > player.x and self.y > -60:
                self.move_left()
        else:
            self.gravity = -3.2
        if self.y <= self.floor:
            self.y = self.floor
        if (self.y >= -295 and self.x <= -50) or (self.y >= -295 and self.x >= 50):
            self.floor = -280
        else:
            self.floor = -427
        if self.y >= -150 and self.x >= -350 and self.x <= 350:
            self.floor = -130


class FireParticle:
    state = "off"

    def __init__(self, x, y, color, shape):
        self.dx = 0
        self.dy = 0
        self.dxx = random.randint(-15, 15)
        self.dyy = random.randint(-15, 15)
        self.x = x
        self.y = y
        self.state = "off"
        self.shape = shape
        self.color = color
        self.size_length = 0.20
        self.size_width = 0.20
        # self.heading = random.randint(0, 360)

    def update_expl(self):
        self.x += self.dxx
        self.y += self.dyy

    def update(self):
        self.dx = random.randint(1, 10)
        self.dy = random.randint(-2, 2)
        self.x += self.dx
        self.y += self.dy
        if self.x > player.x + random.randint(150, 170):
            self.y = player.y
            self.x = player.x + 20

    def render(self, stamper):
        stamper.goto(self.x, self.y)
        stamper.shape(self.shape)
        stamper.color(self.color)
        stamper.shapesize(self.size_length, self.size_width)
        stamper.stamp()


class SnowBall:
    def __init__(self, x, y, start_location, shape, color):
        self.dx = 0
        self.dy = 0
        self.x = x
        self.y = y
        self.start_location = start_location
        self.size_length = 0.5
        self.size_width = 0.5
        self.shape = shape
        self.color = color
        self.switch = True
        self.sound_bucket = ["a"]

    def update(self):
        global STATE
        if self.start_location == "left":
            self.dx = 5
            if STATE == False:
                if self.x == -250:
                    left_snowballs.append(
                        SnowBall(
                            -425, -325, "left", "assets/sprites/snow_ball.gif", "white"
                        )
                    )
                    print("append")
            if self.x == 450:
                STATE = True
                self.x = -425
                self.y = -325
                print("switch")
        elif self.start_location == "right":
            self.dx = -5
        self.x += self.dx
        self.y += GRAVITY
        if self.y <= -437:
            self.y = -437
        if self.x > player.x - 12 and self.x < player.x + 12 and self.switch == True:
            player.health -= 0.5
            print("hello")
            self.switch = False
        if self.x > player.x + 13:
            self.switch = True

    def render(self, stamper):
        stamper.goto(self.x, self.y)
        stamper.shape(self.shape)
        stamper.color(self.color)
        stamper.shapesize(self.size_length, self.size_width)
        stamper.stamp()


class FanParticle:
    def __init__(self, x, y, shape, color):
        self.dx = 0
        self.dy = random.randint(1, 3)
        self.x = x
        self.y = y
        self.size_length = 0.2
        self.size_width = 0.2
        self.shape = shape
        self.color = color

    def update(self):
        self.x += self.dx
        self.y += self.dy
        if self.y >= -250:
            self.y = -430
            random.randint(-15, 15)
            self.dy = random.randint(1, 5)
            # self.dy = random.randint(1,7)

    def update_two(self):
        self.x += self.dx
        self.y += self.dy
        if self.y >= -104:
            self.y = -282
            random.randint(-15, 15)
            self.dy = random.randint(1, 5)
            # self.dy = random.randint(1,7)

    def render(self, stamper):
        stamper.goto(self.x, self.y)
        stamper.shape(self.shape)
        stamper.color(self.color)
        stamper.shapesize(self.size_length, self.size_width)
        stamper.stamp()


def fire_fire_particles():
    if FireParticle.state == "off":
        for fire_particle in fire_particles:
            fire_particle.state = "on"
        FireParticle.state = "on"
    elif FireParticle.state == "on":
        FireParticle.state = "off"


player = Player(425, -427, "assets/sprites/bob.gif", "white")

button = Sprite(0, -135, "assets/sprites/button.gif", "red")

fan = Sprite(0, -424, "assets/sprites/fan.gif", "red")

fan_two = Sprite(400, -276, "assets/sprites/fan.gif", "red")

obo = EnemyAI(-275, 172, "assets/sprites/obo.gif", "red")

fire_particles = []
for i in range(20):
    fire_particles.append(
        FireParticle(1000, 1000, "orange", "assets/sprites/flame.gif")
    )

left_snowballs = []
for _ in range(10):
    left_snowballs.append(
        SnowBall(-425, -325, "left", "assets/sprites/snow_ball.gif", "white")
    )

right_snowballs = []

fan_particles = []
fan_particles_two = []
for _ in range(10):
    fan_particles.append(FanParticle(random.randint(-15, 15), -430, "circle", "white"))
for _ in range(10):
    fan_particles_two.append(
        FanParticle(random.randint(385, 415), -282, "circle", "white")
    )

game_screen.listen()
game_screen.onkeypress(player.left, "Left")
game_screen.onkeypress(player.right, "Right")
game_screen.onkeypress(player.up, "space")
game_screen.onkeypress(fire_fire_particles, "f")

while True:
    print(obo.y)
    # print(player.x)
    # print("---------")
    # print(player.y)
    # print("---------")
    sprite_stamper.clear()
    player.update()
    for fire_particle in fire_particles:
        if fire_particle.state == "on" and FireParticle.state == "on":
            fire_particle.update()
        elif FireParticle.state == "off":
            if fire_particle.x < player.x + 140:
                fire_particle.update()
            elif fire_particle.x >= player.x + random.randint(120, 139):
                fire_particle.y = 1000
                fire_particle.x = 1000
        fire_particle.render(sprite_stamper)
    if player.left_token_bucket:
        player.move_left()
        player.left_token_bucket.pop()
    if player.right_token_bucket:
        player.move_right()
        player.right_token_bucket.pop()
    if player.up_token_bucket:
        player.jump()
        player.up_token_bucket.pop()
    # for left_snowball in left_snowballs:
    #     left_snowball.update()
    #     left_snowball.render(sprite_stamper)
    for fan_particle in fan_particles:
        fan_particle.update()
        fan_particle.render(sprite_stamper)
    for fan_particle in fan_particles_two:
        fan_particle.update_two()
        fan_particle.render(sprite_stamper)
    obo.update()
    obo.render(sprite_stamper)
    fan_two.render(stamper)
    fan.render(sprite_stamper)
    button.render(sprite_stamper)
    player.render_health(sprite_stamper)
    player.render(sprite_stamper)
    game_screen.update()
