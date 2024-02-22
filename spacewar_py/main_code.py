import math
import time
import random
import pygame
import turtle

#Setting up the screen
wn=turtle.Screen()
wn.title('SPACEWAR - @mol_an07')
wn.bgcolor("black")
wn.setup(700,700)
wn.tracer(0)

#Icon of the window
root = turtle.Screen()._root
root.iconbitmap("spw_exe.ico")

#Loading Sounds
pygame.init()
pygame.mixer

#Loading SFX
bgs = ("M_bgm.ogg", "miss_fire.wav", "alien_death.wav", "Pop_open.wav", "Pop_close.wav", 'bomb_hit.wav',\
       "O_Ent_press.wav", "quit_exit.wav", "end_result.ogg", 'pause_info_open.wav', 'pause_info_close.wav',\
       'health_low.wav', 'Pop_click.wav', 'miss_hit_1v2_3.wav', 'miss_hit_2v2_3.wav', 'miss_hit_3v2_3.wav',\
       'shuttlehit_alien.wav', 'teleport.wav', 'spwan_ship_coll.wav', 'bomb_exp.wav', 'spwan_ship_exp.wav',\
       'spwan_ship_core_regen.wav', 'spwan_ship_misshit.wav', 'zar_death.wav', 'zal_death.wav')
ld_bgs = []
for snd in range(0, len(bgs)):
    sound = pygame.mixer.Sound(bgs[snd])
    ld_bgs.append(sound)

#Loading BGMS
bgm = ("m1.ogg","m2.ogg","m3.ogg","m4.ogg","m5.ogg","m6.ogg","m7.ogg","m8.ogg","m9.ogg","m10.ogg","miss_won.ogg",\
       "miss_lost.ogg")
ld_bgm = []
for bm in range(0, len(bgm)):
    sound = pygame.mixer.Sound(bgm[bm])
    ld_bgm.append(sound)
# Load the final mission sounds
begin_sound = pygame.mixer.Sound('m10x.ogg')
# Create a channel
channel = pygame.mixer.Channel(0)

#Registering Background Images & Ally image
bg_imgs = ("mmtext.gif", "control_pop.gif", "about_pop.gif", "quit_pop.gif", "pause_bg.gif", "ally.gif", \
           "miss_fail.gif", "miss_accomp.gif", "M1_M2.gif", "M3_M4.gif", "M5_M6.gif", "M7_M8.gif","M9.gif",\
           "M10.gif", "gameover.gif")
for img in bg_imgs:
    wn.addshape(img)
for ip in range(10):
    wn.addshape("info_m{}.gif".format(ip+1))


#Spaceship Images
model = "ship"
sp = (0, 45, 90, 135, 180, 225, 270, 315)
for u in sp:
    wn.addshape('shuttles\{}{}.gif'.format(model, u))

#Enemy Images
en_imgs = (("enemy_1.gif", "enemy_1v2.gif", "enemy_1v3.gif"),\
           ("enemy_2.gif", "enemy_2v2.gif", "enemy_2v3.gif"),\
           ("enemy_3.gif", "enemy_3v2.gif", "enemy_3v3.gif"),\
           ("veilbreaker.gif","nebulahub.gif","shadowfg.gif","zaraak.gif","bomb_off.gif","bomb_on.gif","zalthor.gif"))
for imgs in en_imgs:
    for img in imgs:
        wn.addshape(img)

#Creating classes for different attributes of the game
class Sprite(turtle.Turtle):
    
    def __init__(self, spriteshape, color, startx, starty):
        turtle.Turtle.__init__(self, shape = spriteshape)
        self.speed(0)
        self.penup()
        self.color(color)
        self.fd(0)
        self.goto(startx, starty)
        self.speed = 1
        self.col_fact = 20
        self.detect_fact = 290

    def move(self):
        self.fd(self.speed)

        # Boundary detection
        if self.xcor() > self.detect_fact:
            self.setx(self.detect_fact)
            self.rt (60)
        if self.xcor() < -self.detect_fact:
            self.setx(-self.detect_fact)
            self.rt (60)
        if self.ycor() > self.detect_fact:
            self.sety (self.detect_fact)
            self.rt (60)
        if self.ycor() < -self.detect_fact:
            self.sety(-self.detect_fact)
            self.rt (60)

    #Function for checking collision between objects of the game
    def is_collision(self, other):
        if (self.xcor() >= (other.xcor() - self.col_fact)) and \
        (self.xcor() <= (other.xcor() +self.col_fact)) and \
        (self.ycor() >= (other.ycor() - self.col_fact)) and \
        (self.ycor() <= (other.ycor() +self.col_fact)):
            return True
        else:
            return False
        
#Creating class for player i.e. spaceship
class Player(Sprite):
    def __init__(self, spriteshape, color, startx, starty):
        Sprite.__init__(self, spriteshape, color, startx, starty)
        self.speed = 3
        self.health = 100
        self.turn = 45
        self.max_health = 100
        self.warn = True
 
    def turn_left(self):
        self.lt(self.turn)
    def turn_right(self):
        self.rt(self.turn)
    def accelerate(self):
        if self.speed<=20:
            self.speed += 1
    def decelerate(self):
        if self.speed>=-20:
            self.speed -= 1

    def ship_head(self):
        dif_1 = 0
        dif_2 = 0
        deg = [0, 45, 90, 135, 180, 225, 270, 315]
        for h in range(8):
            if self.heading()>315 and self.heading()<360:
                dif_1 = -deg[h] + self.heading()
                dif_2 = deg[h+1] + self.heading()
                if dif_1 < dif_2:
                    self.setheading(deg[h])
                else:
                    self.setheading(deg[h])

            elif self.heading()>deg[h] and self.heading()<deg[h+1]:
                dif_1 = -deg[h] + self.heading()
                dif_2 = deg[h+1] + self.heading()
                if dif_1 < dif_2:
                    self.setheading(deg[h])
                else:
                    self.setheading(deg[h])

    def ship_shape(self):
        global model
        for x in [0, 45, 90, 135, 180, 225, 270, 315]:
            if x==self.heading():
                self.shape('shuttles\{}{}.gif'.format(model, x))

    #Player Health Bar
    def health_bar(self, pen):
        pen.ht()
        pen.goto(198, 310)
        pen.width(10)
        pen.pendown()
        pen.setheading(0)
        if self.health/self.max_health < 0.3:
            pen.color("red")
            #Low Health Sound
            if self.warn:
                ld_bgs[11].play()
                self.warn = False
        elif self.health/self.max_health < 0.7:
            pen.color("yellow")
        else:
            pen.color("green")
        pen.fd(100*(self.health/self.max_health))
        pen.color("grey")
        pen.fd(100*((self.max_health-self.health)/self.max_health))
        pen.penup()

#Class for Enemies in a game 
class Enemy(Sprite):
    def __init__(self, spriteshape, color, startx, starty):
        Sprite.__init__(self, spriteshape, color, startx, starty)
        self.speed = 6
        self.health = 1
        self.max_health = 100
        self.id = "1v1"
        self.damage = 3
        self.rebirth = False
        self.dead = False
        self.setheading(random.randint(0,360))

    #Enemy Boss Health Bar
    def health_bar(self, pen, col):
        pen.ht()
        pen.goto(-300, -333)
        pen.width(8)
        pen.pendown()
        pen.setheading(0)
        if self.health/self.max_health < 0.3:
            pen.color("red")
        elif self.health/self.max_health < 0.7:
            pen.color("orange")
        else:
            pen.color(col)
        pen.fd(600*(self.health/self.max_health))
        pen.color("grey")
        pen.fd(600*((self.max_health-self.health)/self.max_health))
        pen.penup()


#Class for Allies of the player
class Ally(Sprite):   
    def __init__(self, spriteshape, color, startx, starty):
        Sprite.__init__(self, spriteshape, color, startx, starty)
        self.speed = 4
        self.health = 50
        self.setheading (random. randint(0,360))
        self.goto(0,300)
        walk = 60

    def move(self):
        self.fd(self.speed)

        # Boundary detection
        if self.xcor() > 290:
            self.setx(290)
            self.lt (45)
        if self.xcor() < -290:
            self.setx(-290)
            self.lt (45)
        if self.ycor() > 290:
            self.sety (290)
            self.lt (45)
        if self.ycor() < -290:
            self.sety(-290)
            self.lt (45)

    def ally_death(self):
        global allies
        if self.health <= 0:
            explosion("circle", "orange", 10, self)
            self.goto(-1000, 1000)
            self.ht()
            allies.remove(self)

#Class for missile fired by the player
class Missile(Sprite):
    def __init__(self, spriteshape, color, startx, starty):
        Sprite.__init__(self, spriteshape, color, startx, starty)
        self.shapesize(stretch_wid=0.3, stretch_len=0.4, outline=None)
        self.speed = 20
        self.status= " "
        self.miss_no = 30
        
        self.track = turtle.Turtle()
        self.track.color("white")
        self.track.ht()

        self.goto (-1000, 1000)

    def fire(self):
        if self.status == "ready":
            if game.mission == 5 and self.miss_no != 0:
                self.goto (player.xcor(), player.ycor())
                self.setheading (player.heading())
                self.status = "firing"
                self.miss_no -= 1
                msg3 = "Missiles Charges : {}".format(self.miss_no)
                self.track.undo()
                self.track.ht()
                self.track.penup()
                self.track.goto(-137, -335)
                self.track.write(msg3, font=("Courier New", 16, "bold"))

                ld_bgs[1].play()
                
            elif game.mission != 5:
                self.goto (player.xcor(), player.ycor())
                self.setheading (player.heading())
                self.status = "firing"

                ld_bgs[1].play()

    def move(self):
        if self.status == "ready":
            self.goto (-1000, 1000)
        
        if self.status == "firing":
            self.fd(self.speed)

        #Border check
        if (self.xcor() < -290 or self.xcor() > 290 or \
        self.ycor() < -290 or self.ycor() > 290):
            self.goto(-1000, 1000)
            self.status="ready"

#Class for the particles involved in game
class Particle(Sprite):
    
    def __init__(self, spriteshape, color, startx, starty):
        Sprite.__init__(self, spriteshape, color, startx, starty)
        self.shapesize(stretch_wid=0.1, stretch_len=0.1, outline=None)
        self.goto(-1000,-1000)
        self.frame = 1
        self.exp_radius = 10  #For Expansion of particles after explosion

    def explode(self, startx, starty):
        self.goto(startx, starty)
        self.setheading (random.randint(0,360))
        self.frame = 1

    def move(self):
        if self.frame > 0:
            self.fd(10)
            self.frame+=1

        if self.frame > self.exp_radius:
            self.frame = 0
            self.goto(-1000, -1000)

#Class for controlling different states of the game
class Game():
    global pause
    
    def __init__(self):
        self.score = 0

        self.phase = "main_menu"
        self.mission = 1
        
        self.state = "playing"
        self.state2 = "continue"
        self.done = False
        self.register = True

        self.bgplay = True
        self.bgplay2 = True
        self.bgplay3 = True

        self.leave = False

        self.info_state = True

        self.enm_no = 15
        self.enm_type = "enemy_1.gif"
        self.boss_name = ''

        self.ally_no = 4
        self.bomb_no = 10

        self.total_score = 0
        self.total_kill = 0
        self.failed = 0
        self.rank = '-'

        self.pen = turtle.Turtle()
        self.pen.ht()

        
        self.Writers = []                       #Used - 5
        for t in range(5):
            self.Writers.append(turtle.Turtle())
            self.Writers[t].speed(0)
            self.Writers[t].color("white")
            self.Writers[t].penup()
            self.Writers[t].ht()

        self.bg = []                            #Used - 5
        for r in range(5):
            self.bg.append(turtle.Turtle())
            self.bg[r].penup()
            self.bg[r].ht()
    
    def draw_border(self):
        #Draw border
        self.pen.speed(0)
        self.pen.color("white")
        self.pen.pensize(3)
        self.pen.penup()
        self.pen.goto(-300, 300)
        self.pen.pendown()
        game.pen.setheading(0)
        for side in range(4):
            self.pen.fd(600)
            self.pen.rt(90)

    def show_status(self):
        msg = "Score : %s" %(self.score)
        self.Writers[2].undo()
        self.Writers[2].ht()
        self.Writers[2].penup()
        self.Writers[2].goto(-300, 310)
        self.Writers[2].write(msg, font=("Courier New", 16, "bold"))

        msg2 = "Health"
        self.Writers[0].undo()
        self.Writers[0].ht()
        self.Writers[0].goto(198, 315)
        self.Writers[0].write(msg2, font=("Courier New", 16, "bold"))

        if self.mission==4 or self.mission==6 or self.mission==8 or self.mission==9 or self.mission==10:
            self.Writers[3].undo()
            self.Writers[3].ht()
            self.Writers[3].goto(-300, -330)
            self.Writers[3].write(self.boss_name, font=("Courier New", 16, "bold"))
            
    def manager(self, mang, tsk, val):
        if mang == "score":
            if tsk=='add':
                self.score += val
            elif tsk=='sub' and self.score > 0:
                self.score -= val
            if self.score < 0:
                self.score = 0
        self.show_status()

    def start_game(self):
        if self.phase == "main_menu":
            ld_bgs[6].play()
            self.phase = "play"
            self.bg[0].ht()
            self.bgplay3 = True

    def show_control(self):
        if self.phase == "main_menu":
            ld_bgs[3].play()
            self.bg[0].shape('control_pop.gif')
            self.phase = "controls"
        elif self.phase == "controls":
            ld_bgs[4].play()
            self.phase = "main_menu"

    def show_about(self):
        if self.phase == "main_menu":
            ld_bgs[3].play()
            game.bg[0].shape('about_pop.gif')
            self.phase = "about"
        elif self.phase == "about":
            ld_bgs[4].play()
            self.phase = "main_menu"    

    def show_quit(self):
        if self.phase == "main_menu":
            ld_bgs[3].play()
            game.bg[0].shape('quit_pop.gif')
            self.phase = "quit"
        elif self.phase == "quit":
            ld_bgs[4].play()
            self.phase = "main_menu"

    def quit_y(self):
        if self.phase == "quit" or self.phase == "gameover":
            ld_bgs[7].play()
            self.leave = True

    def quit_n(self):
        if self.phase == "quit":
            ld_bgs[4].play()
            self.phase = "main_menu"

    def control_pause(self):
        global pause
        if self.phase == "play" and pause == False:
            pause = True
            self.phase = "halt"
            ld_bgs[9].play()
        elif self.phase == "halt" and pause == True:
            pause = False
            self.phase = "play"
            self.state2 = " "
            ld_bgs[10].play()

    def close_popup(self, x, y):
        if self.phase == "about" or self.phase == "controls" or self.phase == "quit":
            if ((x>270 and x<310) and (y>270 and y<310)) or ((x>280 and x<320) and (y>122 and y<162)):
                ld_bgs[4].play()
                self.phase = "main_menu"

        elif self.phase == "result_accomp":
            if ((x>35 and x<257) and (y>-220 and y<-168)):
                self.next_mission()
            elif (((x>-268 and x<-49) and (y>-220 and y<-168))):
                self.retry_mission()

        elif self.phase == "result_fail":
            if ((x>35 and x<257) and (y>-220 and y<-168)):
                self.retry_mission()
            elif (((x>-268 and x<-49) and (y>-220 and y<-168))):
                self.reset_game()
        
        elif self.phase == "gameover":
            if (x>-303 and x<-119) and (y>-271 and y<-230):
                self.quit_y()
            elif (x>125 and x<305) and (y>-276 and y<-225):
                game.done = False
                self.reset_game()


    def mission_bg(self):
        if self.mission == 1 or self.mission == 2:
            wn.bgpic("M1_M2.gif")
        elif self.mission == 3 or self.mission == 4:
            wn.bgpic("M3_M4.gif")
        elif self.mission == 5 or self.mission == 6:
            wn.bgpic("M5_M6.gif")
        elif self.mission == 7 or self.mission == 8:
            wn.bgpic("M7_M8.gif")
        elif self.mission == 9:
            wn.bgpic("M9.gif")
        else:
            wn.bgpic("M10.gif")

    def info_bg(self):
        global pause
        if self.info_state and pause:
            self.bg[3].ht()
            self.info_state = False
            pause = False
            ld_bgs[10].play()
        elif not self.info_state and self.phase == 'play':
            self.info_state = True
            ld_bgs[9].play()

    def bgmplay(self, cmd):
        global ld_bgm
        if cmd == 'play' and self.mission != 10:
            ld_bgm[self.mission-1].play(-1)
        elif cmd == 'stop':
            ld_bgm[self.mission-1].stop()
             
    def clean_up(self):
        global pause
        global enemies
        global allies
        global bosses
        global spwn
        #Writers
        self.pen.clear()
        self.Writers[0].clear()
        self.Writers[1].clear()
        self.Writers[2].clear()
        self.Writers[3].clear()
        self.Writers[4].clear()
        missile.track.clear()
        #Sprites
        enemies.clear()
        allies.clear()
        bosses.clear()
        bombs.clear()
        #status
        self.score = 0
        missile.miss_no = 30
        self.state = "playing"
        self.state2 = " "
        self.register = True
        self.bgplay2 = True
        missile.status = 'hold'
        player.warn = True
        #Sounds
        self.bgmplay('stop')
        ld_bgm[-1].stop()
        ld_bgm[-2].stop()
        ld_bgm[9].stop()
        #Others
        spwn = -220
        self.bg[2].ht()
        pause = False
            

    def reset_game(self):
        if (self.phase == "halt" or self.phase == "result_fail" or (self.phase == "gameover" and not self.done)) \
           and pause == True:
            ld_bgs[6].play()
            self.clean_up()
            result.clear()
            self.phase = "main_menu"
            self.bgplay = True
            self.info_state = True
            self.mission = 1
            missile.speed = 20
            self.total_score = 0
            self.total_kill = 0
            self.failed = 0
            self.rank = '-'
            self.done = True
            ld_bgs[8].stop()
            channel.stop()

    def next_mission(self):
        if self.phase == "result_accomp" and pause == True:
            self.total_score += self.score
            self.clean_up()
            self.phase = "play"
            self.info_state = True
            self.mission += 1
            ld_bgs[12].play()

    def retry_mission(self):
        if (self.phase == "result_fail" or self.phase == "result_accomp") and pause == True:
            self.clean_up()
            self.phase = "play"
            ld_bgs[12].play()
        elif self.mission == 10:
            self.bgplay3 = True

    def test(self,x,y):
        print("Test Function Is Active")
        print("Xcor : ", x)
        print("Ycor : ", y)


#Global Variables
pause = False
dam_factor = 0
spwn = -220

#Create game object
game = Game()

#Create player and missile sprites
player = Player("triangle", "white", 0, 0)
missile = Missile("triangle", "yellow", 0, 0)
player.ht()
missile.ht()

enemies = []
allies = []
bosses = []
bombs = []
particles = []

#Creating explosion particles
for k in range(20):
    particles.append(Particle("circle", "green", 0, 0))
    particles[k].ht()

#Turtle for End result
result = turtle.Turtle()
result.penup()
result.color = "black"
result.ht()

#Hiding & Unhiding all turtles from screen
def hide_unhide(a, b, l1, l2, l3, l4, l5):
    global pause
    global game
    if pause:
        a.ht()
        b.ht()
        missile.status = 'hold'
        for p in l1:
            p.ht()
        if game.mission==3 or game.mission==8:
            for q in l2:
                q.ht()
        for r in l3:
            r.ht()
        if game.mission==4 or game.mission==6 or game.mission==8 or game.mission==9 or game.mission==10:
            for s in l4:
                s.ht()
            for t in l5:
                t.ht()
        #Hiding border
        game.pen.clear()

    elif not pause and game.phase!="main_menu":
        a.st()
        b.st()
        missile.status = 'ready'
        for p in l1:
            p.st()
        if game.mission==3 or game.mission==8:
            for q in l2:
                q.st()
        for r in l3:
            r.st()
        if game.mission==4 or game.mission==6 or game.mission==8 or game.mission==9 or game.mission==10:
            for s in l4:
                s.st()
            for t in l5:
                t.st()
        #Redrawing border
        game.draw_border()
        game.show_status()

#Identifying Enemies
def setenm(idx):
    global enemies
    if game.enm_type==en_imgs[0][1] or game.enm_type==en_imgs[1][1] or game.enm_type==en_imgs[2][1]:
        enemies[idx].health = 2
        if game.enm_type==en_imgs[0][1]:
            enemies[idx].id = "1v2"
        elif game.enm_type==en_imgs[1][1]:
            enemies[idx].id = "2v2"
        else:
            enemies[idx].id = "3v2"
    elif game.enm_type==en_imgs[0][2] or game.enm_type==en_imgs[1][2] or game.enm_type==en_imgs[2][2]:
        enemies[idx].health = 3
        if game.enm_type==en_imgs[0][2]:
            enemies[idx].id = "1v3"
        elif game.enm_type==en_imgs[1][2]:
            enemies[idx].id = "2v3"
        else:
            enemies[idx].id = "3v3"
    else:
        if game.enm_type==en_imgs[1][0]:
            enemies[idx].id = "2v1"
        elif game.enm_type==en_imgs[2][0]:
            enemies[idx].id = "3v1"

#Paricle Explosion
def explosion(shp, col, exp, obj):
    global missile
    global particle
    for particle in particles:
        particle.exp_radius = exp
        particle.color(col)
        particle.shape(shp)
        particle.explode(obj.xcor(), obj.ycor())

#Single element list to string
def strl(lst):
    for st in lst:
        return st

#Keyboard bindings
turtle.onkeypress(player.turn_left, "Left")
turtle.onkeypress(player.turn_right, "Right")
turtle.onkeypress(player.accelerate, "Up")
turtle.onkeypress(player.decelerate, "Down")
turtle.onkeypress(missile.fire, "space")

turtle.onkeypress(game.start_game, "Return")
turtle.onkeypress(game.show_control, "c")
turtle.onkeypress(game.show_about, "a")
turtle.onkeypress(game.show_quit, "q")

turtle.onkeypress(game.control_pause, "Escape")
turtle.onkeypress(game.info_bg, "i")

turtle.onkeypress(game.quit_y, "y")
turtle.onkeypress(game.quit_n, "n")
turtle.onkeypress(game.reset_game, "o")
turtle.onscreenclick(game.close_popup, 1)
#turtle.onscreenclick(game.test)
turtle.listen()

#Main Game Loop
while True:
    #Implementing Pause in Game
    if not pause:
        
        wn.update()
        #Frame Speed
        time.sleep(0.03)

        #Displaying info of mission
        if game.info_state and game.phase == 'play':
            pause = True

        #Main Menu Screen
        if game.phase == "main_menu":
            wn.bgpic("main_menu_bg.gif")
            game.bg[0].shape('mmtext.gif')
            game.bg[0].st()
            game.bg[1].ht()

            if game.bgplay:
                ld_bgs[0].play(-1)
                game.bgplay = False

        #Resuming the game from where it was left
        if game.phase == "play" and game.state2!= "continue":
            #hide_unhide(player, missile, enemies, allies, particles, bosses, bombs) #might not be required
            game.bg[1].ht()
            game.state2 = "continue"

        #Main Gameplay
        if game.phase == "play":
            #Setting Things Acc to Mission
            if game.mission == 1:
                player.turn = 45
                game.enm_no = 15
                game.enm_type = "enemy_1.gif"
                if game.score > 0 and len(enemies)==0:
                    pause = True
                    game.phase = "result_accomp"

            if game.mission == 2:
                player.turn = 0
                game.enm_no = 12
                if game.score > 0 and len(enemies)==0:
                    pause = True
                    game.phase = "result_accomp"

            if game.mission == 3:
                missile.speed = 25
                player.turn = 45
                game.enm_no = 12
                game.ally_no = 4
                if (len(enemies)==0 and len(allies)>0) and game.score > 0:
                    pause = True
                    game.phase = "result_accomp"

            if game.mission == 4:
                missile.speed = 25
                player.turn = 45
                game.enm_no = 13
                if (len(bosses)==0 and len(enemies)==0) and game.score > 0:
                    pause = True
                    game.phase = "result_accomp"

            if game.mission == 5:
                game.enm_no = 15
                missile.speed = 30
                if missile.miss_no == 30:
                    msg3 = "Missiles Charges : {}".format(missile.miss_no)
                    missile.track.undo()
                    missile.track.ht()
                    missile.track.penup()
                    missile.track.goto(-137, -335)
                    missile.track.write(msg3, font=("Courier New", 16, "bold"))
                if game.score > 0 and len(enemies)==0:
                    pause = True
                    game.phase = "result_accomp"

            if game.mission == 6:
                player.turn = 45
                game.enm_no = 15
                missile.speed = 30
                if (len(bosses)==0 and len(enemies)==0) and game.score > 0:
                    pause = True
                    game.phase = "result_accomp"

            if game.mission == 7:
                player.turn = -45
                game.enm_no = 20
                missile.speed = 35
                if game.score > 0 and len(enemies)==0:
                    pause = True
                    game.phase = "result_accomp"

            if game.mission == 8:
                player.turn = 45
                game.enm_no = 17
                missile.speed = 40
                if (len(bosses)==0 and len(enemies)==0) and game.score > 0:
                    pause = True
                    game.phase = "result_accomp"

            if game.mission == 9:
                player.turn = 45
                missile.speed = 45
                game.bomb_no = 5
                if len(bosses)==0 and game.score > 0:
                    pause = True
                    game.phase = "result_accomp"

            if game.mission == 10:
                player.turn = 45
                game.enm_no = 15
                game.bomb_no = 5
                game.ally_no = 5
                missile.speed = 45
                if not channel.get_busy() and game.bgplay3:
                    ld_bgm[9].play(-1)
                    game.bgplay2 = False
                if (len(bosses)==0 and len(enemies)==0) and game.score > 0:
                    pause = True
                    game.phase = "gameover"
                    game.total_score += game.score
                    channel.stop()
                    ld_bgm[9].stop()
                    ld_bgs[8].play(-1)
            
            #Animating Ship Head with Turtle's Head
            if player.heading() not in [0, 45, 90, 135, 180, 225, 270, 315]:
                player.ship_head()
            if player.heading() in [0, 45, 90, 135, 180, 225, 270, 315]:
                player.ship_shape()

            #Moving Player and Missile
            player.move()
            missile.move()

            if game.state == "playing":
                ld_bgs[0].stop()
                game.mission_bg()
                game.bgmplay('play')
                #Playing Final Bgm
                if game.mission==10:
                    channel.play(begin_sound)

                #Show Player & Missile
                player.goto(0,-280)
                player.setheading(90)
                player.speed = 3
                missile.status = "ready"
                player.st()
                missile.st()

                #Show Health Bar
                player.health = 100 #Reset Health
                player.health_bar(game.Writers[1])

                #Generating Enemies Acc to Mission
                if game.mission != 9:
                    for i in range(game.enm_no):
                        if game.mission == 2:
                            game.enm_type = strl(random.choices([en_imgs[0][0], en_imgs[0][1]], weights = [3, 2]))
                        elif game.mission == 3:
                            game.enm_type = strl(random.choices(en_imgs[0], weights = [5, 3, 1]))
                        elif game.mission == 4:
                            game.enm_type = strl(random.choices(en_imgs[0], weights = [3, 2, 2]))
                        elif game.mission == 5:
                            game.enm_type = random.choice([en_imgs[1][0], en_imgs[1][1]])
                        elif game.mission == 6:
                            game.enm_type = strl(random.choices(en_imgs[1], weights = [3, 2, 2]))
                        elif game.mission == 7:
                            game.enm_type = random.choice([en_imgs[2][0], en_imgs[2][1]])
                        elif game.mission == 8:
                            game.enm_type = strl(random.choices(en_imgs[2], weights = [3, 2, 2]))
                        elif game.mission == 10:
                            temp_enm = en_imgs[0]+en_imgs[1]+en_imgs[2]
                            game.enm_type = strl(random.choices(temp_enm, weights = [3, 2, 1, 3, 2, 1, 3, 2, 1]))
                        enemies.append(Enemy(game.enm_type, "red", -100, 0))
                        setenm(i)
                        enemies[i].st()
                        #Showing Enemies spawning from ship
                        if game.mission==4 or game.mission==6 or game.mission==8 or game.mission==10:
                            enemies[i].goto(-220, 220)

                #Generating Allies
                if game.mission == 3:
                    for j in range(4):
                        allies.append(Ally("ally.gif", "blue", 0, 0))
                        allies[j].st()

                #Generating Bombs
                if game.mission == 9 or game.mission == 10:
                    for m in range(game.bomb_no):
                        bombs.append(Enemy("bomb_off.gif", "blue", 0, 0))
                        bombs[m].speed = 3
                        bombs[m].st()
                        bombs[m].id = 'off'

                #Generating Bosses
                if game.mission==4 or game.mission==6 or game.mission==8 or game.mission==9 or game.mission==10:
                    for i in range(2):
                        bosses.append(Enemy("circle", "red", 0, 0))
                        bosses[i].goto(-220, 220)
                        bosses[i].health = 100
                        if game.mission==4:
                            bosses[i].shape("veilbreaker.gif")
                            bosses[i].id = 'VeilBreaker Citadel'
                            bosses[i].st()
                            #Show Boss Health Bar
                            bosses[i].health_bar(game.Writers[4], 'turquoise')
                            game.boss_name = bosses[i].id
                            break
                        elif game.mission==6:
                            bosses[i].shape("nebulahub.gif")
                            bosses[i].id = 'Nebula Nexus Hub'
                            bosses[i].st()
                            #Show Boss Health Bar
                            bosses[i].health_bar(game.Writers[4], 'gold')
                            game.boss_name = bosses[i].id
                            break
                        elif game.mission==8:
                            bosses[i].shape("shadowfg.gif")
                            bosses[i].id = 'Zephyr Shadowforge'
                            bosses[i].st()
                            #Show Boss Health Bar
                            bosses[i].health_bar(game.Writers[4], 'fuchsia')
                            game.boss_name = bosses[i].id
                            break
                        elif game.mission==9:
                            bosses[i].shape("zaraak.gif")
                            bosses[i].id = 'Zaraaks'
                            bosses[i].goto(spwn, 220)
                            spwn += 220
                            bosses[i].st()
                            #Show Boss Health Bar
                            bosses[i].health_bar(game.Writers[4], 'silver')
                            game.boss_name = bosses[i].id
                        elif game.mission==10:
                            bosses[i].shape("zalthor.gif")
                            bosses[i].id = 'Lord Zalthor'
                            bosses[i].st()
                            #Show Boss Health Bar
                            bosses[i].health_bar(game.Writers[4], 'white')
                            game.boss_name = bosses[i].id
                            break

                #Draw the game border
                game.draw_border()               
                #Show the game status
                game.show_status()
                        

            #Enemy Movement and collisions
            if game.mission != 9:
                for enemy in enemies:
                    enemy.move()

                    #Check for collision between player and enemy
                    if player.is_collision(enemy):
                        #Decrease the score
                        game.manager("score", "sub", 50)
                        
                        if '1v' in enemy.id:
                            dam_factor = 0
                            enemy.setheading(random.choice([45, 90, 135, 180, 225, 270, 315]))
                            ld_bgs[16].play()
                        elif '2v' in enemy.id:
                            dam_factor = 4
                            x = random.randint(-250, 250)
                            y = random.randint(-250, 250)
                            enemy.goto(x, y)
                            ld_bgs[16].play()
                        elif '3v' in enemy.id:
                            dam_factor = 6
                            if (game.mission == 8 or game.mission==10) and len(bosses)!= 0:
                                explosion('square', 'red', 10, enemy)
                                enemy.goto(bosses[0].xcor(), bosses[0].ycor())
                            else:
                                explosion('square', 'red', 10, enemy)
                                enemy.ht()
                                enemy.goto(-1000, 1000)
                                enemies.remove(enemy)
                                enemy.dead = True
                            ld_bgs[5].play()
                            
                        #Reducing Health on collision
                        if player.health > 0:
                            player.health -= enemy.damage + dam_factor
                            player.health_bar(game.Writers[1])

                            #logs
                            #print("ENMY : ", enemy.id)
                            #print("DAM : ", dam_factor)

                    #Check for a collision between the missile and the enemy
                    if missile.is_collision(enemy):
                        enemy.health -= 1

                        if (enemy.health <= 0 and (game.mission==4 or game.mission==6 or game.mission==8 or game.mission==10)) and (len(bosses)!= 0):
                            #respawn point in boss levels
                            enemy.goto(bosses[0].xcor(), bosses[0].ycor())
                            enemy.rebirth = True
                            #ld_bgs[2].play()
                            game.total_kill += 1

                            #Increase the score
                            game.manager("score", "add", 100)
                            ld_bgs[21].play()

                            if '1v' in enemy.id:
                                explosion("square", "green", 10, missile)
                            elif '2v' in enemy.id:
                                explosion("square", "pink", 10, missile)
                            else:
                                explosion("square", "red", 10, missile)
                            
                        elif enemy.health <= 0 and not enemy.dead:
                            enemy.ht()
                            enemy.goto(-1000, 1000)
                            enemies.remove(enemy) 
                            ld_bgs[2].play()
                            game.total_kill += 1
                            #Increase the score
                            game.manager("score", "add", 100)
                            #Do the explosion
                            if '1v' in enemy.id:
                                explosion("square", "green", 10, missile)
                            elif '2v' in enemy.id:
                                explosion("square", "pink", 10, missile)
                            else:
                                explosion("square", "red", 10, missile)


                        if (enemy.id == "1v2" or enemy.id == "2v2" or enemy.id == "3v2") and (not enemy.rebirth):
                            if enemy.id == "1v2":
                                ld_bgs[13].play()
                            elif enemy.id == "2v2":
                                x = random.randint(-250, 250)
                                y = random.randint(-250, 250)
                                ld_bgs[14].play()
                                enemy.goto(x, y)
                            elif enemy.id == "3v2":
                                enemy.towards(player)
                            enemy.speed += 4

                        if (enemy.id == "1v3" or enemy.id == "2v3" or enemy.id == "3v3") and (not enemy.rebirth):
                            if enemy.id == "1v3":
                                ld_bgs[13].play()
                            elif enemy.id == "2v3":
                                x = random.randint(-250, 250)
                                y = random.randint(-250, 250)
                                ld_bgs[14].play()
                                enemy.goto(x, y)
                            elif enemy.id == "3v3":
                                enemy.towards(player)
                            enemy.speed += 3
                            enemy.damage += 2

                        #Reloading after hit
                        missile.status = "ready"
                        

            #Ally Movement and collisions
            if game.mission == 3:
                for ally in allies:
                    ally.move()

                    #Check for a collision between the missile and ally
                    if missile.is_collision(ally):
                        ally.health -= 4
                        ally.ally_death()
                        missile.status = "ready"

                        #Decrease the score
                        game.manager("score", "sub", 25)

                    #Reloading after hit
                        missile.status = "ready"

                    #Check for a collision between the player and ally
                    if player.is_collision(ally):
                        ally.setheading(random.choice([45, 90, 135, 180, 225, 270, 315]))
                        ally.health -= 2
                        if player.health > 0:
                            player.health -= 2
                            player.health_bar(game.Writers[1])
                        ally.ally_death()

                        #Decrease the score
                        game.manager("score", "sub", 50)

                    #Check for a collision between the ally and the enemy
                    for enemy in enemies:
                        if enemy.is_collision(ally):
                            enemy.setheading(random.choice([45, 90, 135, 180, 225, 270, 315]))
                            ally.health -= 1
                            ally.ally_death()

            #Bomb Movement and collisions
            if game.mission == 9 or game.mission == 10:
                for tnt in bombs:
                    tnt.move()

                    #Check for a collision between the missile and bomb
                    if missile.is_collision(tnt):
                        if tnt.id == 'off':
                            tnt.id = 'on'
                            tnt.shape("bomb_on.gif")
                            tnt.setheading(random.choice([45, 90, 135, 180, 225, 270, 315]))
                        else:
                            explosion("square", "orange", 10, tnt)
                            ld_bgs[19].play()
                            #To avoid empty list error
                            if len(bosses)!=0:
                                tnt.id = 'off'
                                tnt.shape("bomb_off.gif")
                                bspwn = random.choice(bosses)
                                tnt.goto(bspwn.xcor(), bspwn.ycor())
                            else:
                                tnt.ht()
                                tnt.goto(-1000, 1000)
                                bombs.remove(tnt)

                    #Reloading after hit
                        missile.status = "ready"

                    #Check for a collision between the player and bomb
                    if player.is_collision(tnt):
                        
                        if player.health > 0:
                            if tnt.id == 'off':
                                player.health -= 5
                                ld_bgs[18].play()
                            else:
                                player.health -= 10
                                ld_bgs[5].play()
                            player.health_bar(game.Writers[1])
                        
                        explosion("square", "orange", 10, tnt)
                        #To avoid empty list error
                        if len(bosses)!=0:
                            tnt.id = 'off'
                            tnt.shape("bomb_off.gif")
                            bspwn = random.choice(bosses)
                            tnt.goto(bspwn.xcor(), bspwn.ycor())
                        else:
                            tnt.ht()
                            tnt.goto(-1000, 1000)
                            bombs.remove(tnt)
                        
                        #Decrease the score
                        game.manager("score", "sub", 15)

                    #Check for a collision between the bomb and zaraak
                    for boss in bosses:
                        #For Mission 10
                        if (boss.id == "Zaraaks" or boss.health<=60) and len(bosses)!=0:
                            boss.col_fact = 60
                            #For Mission 9 & 10
                            if boss.is_collision(tnt):
                                if tnt.id == 'on':
                                    ld_bgs[15].play()
                                    ld_bgs[5].play()
                                    if boss.id == "Zaraaks":
                                        boss.health -= 15
                                    else:
                                        boss.health -= 5
                                    boss.health_bar(game.Writers[4], 'silver')
                                    explosion("square", "orange", 10, tnt)
                                    tnt.id = 'off'
                                    tnt.shape("bomb_off.gif")
                                    bspwn = random.choice(bosses)
                                    tnt.goto(bspwn.xcor(), bspwn.ycor())

                                    if boss.health <= 0:
                                        boss.ht()
                                        boss.goto(-1000, 1000)
                                        bosses.remove(boss)
                                        game.total_kill += 1
                                        if boss.id == 'Zaraaks':
                                            explosion("square", "silver", 50, tnt)
                                            ld_bgs[23].play()
                                        else:
                                            explosion("square", "white", 100, tnt)
                                            ld_bgs[24].play()
                                        #Bonus
                                        if player.health <= 50:
                                            player.health += 25
                                            player.health_bar(game.Writers[1])

                                else:
                                    tnt.setheading(random.choice([45, 90, 135, 180, 225, 270, 315]))


            #Boss Movement and collisions
            if game.mission==4 or game.mission==6 or game.mission==8 or game.mission==9 or game.mission==10:

                #Setting Factors for bosses
                #boss.col_fact = 20
                missile.col_fact = 70
                player.col_fact = 70

                for boss in bosses:
                    #Moving bosses
                    if boss.id == 'VeilBreaker Citadel':
                        boss.speed = 2
                    elif boss.id == 'Nebula Nexus Hub':
                        boss.speed = 2   
                    elif boss.id == 'Zephyr Shadowforge':
                        boss.speed = 3
                    elif boss.id == 'Zaraaks':
                        boss.speed = 2
                    else:
                        boss.speed = 4
                    boss.detect_fact = 230
                    boss.move()
                        

                    #Check for a collision between the missile and boss
                    if missile.is_collision(boss):
                        game.manager("score", "add", 200)

                        if boss.id == 'VeilBreaker Citadel':
                            boss.health -= 3.5
                            ld_bgs[22].play()
                            if boss.health >= 0:
                                boss.health_bar(game.Writers[4], 'turquoise')
                        elif boss.id == 'Nebula Nexus Hub':
                            boss.health -= 3
                            ld_bgs[22].play()
                            if boss.health >= 0:
                                boss.health_bar(game.Writers[4], 'gold')
                        elif boss.id == 'Zephyr Shadowforge':
                            boss.health -= 2.5
                            ld_bgs[22].play()
                            if boss.health >= 0:
                                boss.health_bar(game.Writers[4], 'fuchsia')
                        elif boss.id == 'Zaraaks':
                            ld_bgs[17].play()
                            x = random.randint(-250, 250)
                            y = random.randint(-250, 250)
                            boss.goto(x, y)
                        else:
                            if boss.health <= 60:
                                ld_bgs[17].play()
                                x = random.randint(-250, 250)
                                y = random.randint(-250, 250)
                                boss.goto(x, y)
                            else:
                                ld_bgs[15].play()
                                boss.health -= 1.5

                            if boss.health >= 0:
                                boss.health_bar(game.Writers[4], 'white')
                        
                        
                        if boss.health <= 0:
                            boss.ht()
                            boss.goto(-1000, 1000)
                            bosses.remove(boss)
                            game.total_kill += 1
                            #Do the explosion
                            #if boss.id == 'VeilBreaker Citadel' or boss.id == 'Nebula Nexus Hub' or boss.id == 'Zephyr Shadowforge':
                            explosion("circle", "yellow", 70, missile)
                            ld_bgs[20].play()
                            #Bonus
                            if player.health <= 50:
                                player.health += 30
                                player.health_bar(game.Writers[1])

                        #Reloading after hit
                        missile.status = "ready"

                    #Check for a collision between the player and boss
                    if player.is_collision(boss):
                        game.manager("score", "sub", 100)
                        ld_bgs[18].play()
                        if player.health > 0:
                            player.health -= 10
                            player.health_bar(game.Writers[1])
                            player.lt(45)
            
            #Exploded Paricles Movement
            for particle in particles:
                    particle.move()
                    particle.st()

            #Clearing Health bar
            if len(bosses)==0 and (game.mission==4 or game.mission==6 or game.mission==8 or \
                                   game.mission==9 or game.mission==10):
                game.Writers[3].clear()
                game.Writers[4].clear()

            #Mission Failure Check
            if (player.health <= 0) or (game.mission==3 and len(allies)<3) or \
               (missile.miss_no<=0) or (game.score <= 0 and len(enemies)==0 and game.mission!=9) or \
               (game.score<=0 and len(bosses)==0 and game.mission==9):
                game.phase = "result_fail"
                pause = True

            game.state = "All_Turtles_On_Screen"


        #Reseting factors to default
        missile.col_fact = 20
        player.col_fact = 20
        

        #Quit the game
        if game.leave:
            ld_bgs[0].stop()
            break
        
    else:
        wn.update()

        #Final Sound Error Fix
        if not channel.get_busy() and game.bgplay3 and game.mission==10:
            ld_bgm[9].play(-1)
            game.bgplay3 = False

        #Hiding Elements during pause
        hide_unhide(player, missile, enemies, allies, particles, bosses, bombs)

        #Fixes Blocked particles during paused
        for particle in particles:
            particle.move()

        #Screens to show when paused Screen
        #Mission Info Screen
        if game.info_state and game.phase == 'play':
            for mis in range(1, 11):
                if game.mission == mis:
                    game.bg[3].shape("info_m{}.gif".format(mis))
                    game.bg[3].st()
                else:
                    continue
        #Mission Accomplished Screen
        elif game.phase == "result_accomp":
            if game.bgplay2:
                game.bgmplay('stop')
                game.bgplay2 = False
                ld_bgm[-2].play()
            game.bg[2].shape("miss_accomp.gif")
            game.bg[2].st()
        #Mission Failed Screen
        elif game.phase == "result_fail":
            if game.register:
                game.failed += 1
                game.register = False
                game.bgmplay('stop')
                ld_bgm[9].stop()
                channel.stop()
                ld_bgm[-1].play()
            game.bg[2].shape("miss_fail.gif")
            game.bg[2].st()
        #Paused Screen on ESC press
        elif game.phase == "halt":
            game.bg[1].shape("pause_bg.gif")
            game.bg[1].st()
                
        #Result display screen at Gameover
        elif game.phase == "gameover":
            game.done = True
            game.bg[2].shape("gameover.gif")
            game.bg[2].st()
            if game.failed == 0:
                game.rank = 'S++'
            elif game.failed <=5:
                game.rank = 'S+'
            elif game.failed <=10:
                game.rank = 'A'
            elif game.failed <=15:
                game.rank = 'B'
            elif game.failed <=20:
                game.rank = 'C'
            else:
                game.rank = 'D'
            result.goto(16, 54)
            result.write(game.total_score, font=("Courier New", 24, "bold"))
            result.goto(90, 3)
            result.write(game.total_kill, font=("Courier New", 24, "bold"))
            result.goto(-15, -49)
            result.write(game.failed, font=("Courier New", 24, "bold"))
            result.goto(51, -100)
            result.write(game.rank, font=("Courier New", 24, "bold"))

        #Quit the game
        if game.leave:
            ld_bgs[0].stop()
            ld_bgs[8].stop()
            break
            

#Closes turtle window
wn.bye()
