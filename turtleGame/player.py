import turtle
import time
import random

turtle.fd(0)
turtle.speed(0)
turtle.bgcolor("black")
turtle.ht()
turtle.setundobuffer(1)
turtle.tracer(0)

class Game():
    def __init__(self):
        self.level = 1
        self.score = 0
        self.state = "playing"
        self.pen = turtle.Turtle()
        self.lives = 3
    def draw_border(self):
        #Draw border
        self.pen.speed(0)
        self.pen.color("white")
        self.pen.pensize(3)
        self.pen.penup()
        self.pen.goto(-300,300)
        self.pen.pendown()
        for side in range(4):
            self.pen.fd(600)  # 600 * 600
            self.pen.rt(90)  # turn left
        self.pen.penup()
        self.pen.ht()
        self.pen.pendown()

    def show_status(self):
        self.pen.undo()
        msg = "Score %s" %(self.score)
        self.pen.penup()
        self.pen.goto(-300,310)
        self.pen.write(msg,font=("Arial",16,"normal"))

game = Game()
game.draw_border()
game.show_status()


class Sprite(turtle.Turtle):
    def __init__(self,spriteshape,color,startx,starty):
        turtle.Turtle.__init__(self,shape=spriteshape)
        self.speed(0)
        self.penup()
        self.color(color)
        self.fd(0)
        self.goto(startx,starty)
        self.speed = 1
    def move(self):
        self.fd(self.speed)

        # boundary detection
        if self.xcor()>290:
            self.setx(290)
            self.rt(60)
        if self.xcor()<-290:
            self.setx(-290)
            self.rt(60)
        if self.ycor()<-290:
            self.sety(-290)
            self.rt(60)
        if self.ycor()>290:
            self.sety(290)
            self.rt(60)

    def is_collision(self,other):
        if (self.xcor() >= (other.xcor() - 20)) and \
                (self.xcor() <= (other.xcor() + 20)) and \
            (self.ycor() >= (other.ycor() - 20)) and \
            (self.ycor() <= (other.ycor() + 20)):
            return True
        else:
            return False

                # child of Sprite and grandchild of turtle
class Player(Sprite):
    def __init__(self,spriteshape,color,startx,starty):
        Sprite.__init__(self,spriteshape,color,startx,starty)
        self.speed = 4
        self.lives = 3
    def turn_left(self):
        self.lt(45)
    def turn_right(self):
        self.rt(45)
    def accelerate(self):
        self.speed += 1
    def decelerate(self):
        self.speed -= 1

class Missile(Sprite):
    def __init__(self,spriteshape,color,startx,starty):
        Sprite.__init__(self,spriteshape,color,startx,starty)
        self.speed = 20
        self.status = "ready"
        self.shapesize(0.3,0.3,None)
        #hide from start
        self.goto(-1000,1000)

    def fire(self):
        if self.status == "ready":
            #self.status = "firing"
            self.goto(player.xcor(),player.ycor())
            self.setheading(player.heading())
            self.status = "firing"

    # over write sprite.move
    def move(self):
        if self.status == "ready":
            self.goto(-1000, 1000)
            self.status = "ready"

        if self.status == "firing":
            self.fd(self.speed)

        #border check
        if (self.xcor() < -290 or self.xcor() > 290 or
            self.ycor() < -290 or self.ycor() > 290) and not (self.xcor()==-1000 and self.ycor()==1000):
            self.goto(-1000,1000)
            self.status = "ready"

class Enemy(Sprite):
    def __init__(self,spriteshape,color,startx,starty):
        Sprite.__init__(self,spriteshape,color,startx,starty)
        self.speed = 6
        self.setheading(random.randint(0,360))

class Ally(Sprite):
    def __init__(self,spriteshape,color,startx,starty):
        Sprite.__init__(self,spriteshape,color,startx,starty)
        self.speed = 8
        self.setheading(random.randint(0, 360))

    def move(self):
        self.fd(self.speed)

        # boundary detection
        if self.xcor()>290:
            self.setx(290)
            self.lt(60)
        if self.xcor()<-290:
            self.setx(-290)
            self.lt(60)
        if self.ycor()<-290:
            self.sety(-290)
            self.lt(60)
        if self.ycor()>290:
            self.sety(290)
            self.lt(60)



# create instance
player = Player("triangle","white",0,0)
#enemy = Enemy("circle","red",-100,0)
missile = Missile("triangle","yellow",0,0)
#ally = Ally("square","blue",100,0)

enemies = []
for i in range(6):
    enemies.append(Enemy("circle","red",-100,0))
allies = []
for i in range(6):
    allies.append(Ally("square", "blue", 100, 0))


# Keyboard bindings
turtle.onkey(player.turn_left,"Left")
turtle.onkey(player.turn_right,"Right")
turtle.onkey(player.accelerate,"Up")
turtle.onkey(player.decelerate,"Down")
turtle.onkey(missile.fire,"space")
turtle.listen()

# Main game loop
while True:
    turtle.update()
    time.sleep(0.02)

    player.move()
    missile.move()

    for ally in allies:
        ally.move()

        if missile.is_collision(ally):
            x = random.randint(-250, 250)
            y = random.randint(-250, 250)
            ally.goto(x, y)
            missile.status = "ready"

            # decrease score
            game.score -= 1
            game.show_status()

    for enemy in enemies:
        enemy.move()

        if player.is_collision(enemy):
            x = random.randint(-250,250)
            y = random.randint(-250,250)
            enemy.goto(x,y)
            game.score -= 1
            game.show_status()

        if missile.is_collision(enemy):
            x = random.randint(-250,250)
            y = random.randint(-250,250)
            enemy.goto(x,y)
            missile.status = "ready"
            #missile.goto(-1000,1000)
            #missile.status = "ready"

            #increase scores
            game.score += 1
            game.show_status()
