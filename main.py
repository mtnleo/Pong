import pygame as pg
import time
import random as rd

WIDTH = 700
HEIGHT = 400

LIGHTER_GREY = (162, 178, 174)
GREY = (142, 158, 164)
DARK_GREY = (112, 128, 144)
WHITE = (255, 255, 255)

def main():
    pg.init()
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    clock = pg.time.Clock()
    running = True
    decision = False #evaluate when user selects a mode

    two_players = True ## change it depedning on what mode the player's in

    #instantiate glider
    player_glider = Player_Glider(HEIGHT)

    second_glider = Second_Glider(HEIGHT)
    cpu_glider = Cpu_Glider(HEIGHT)

    # instantiate ball
    ball = Ball()

    #keep score count
    p1_score = 0
    p2_score = 0

    #wait tick for ball
    wait_tick = 700
    last_tick = 0

    while running and not decision:
        clock.tick(60)
        
        menu_mp = MenuMultiplayer()
        menu_cpu = MenuCpu()

        for event in pg.event.get():
            keys_pressed = pg.key.get_pressed()

            if event.type == pg.QUIT:
                running = False
        
            if event.type == pg.MOUSEBUTTONDOWN:
                x, y = pg.mouse.get_pos()

                if menu_mp.check_clicked(x, y):
                    decision = True
                    two_players = True
                elif menu_cpu.check_clicked(x, y):
                    decision = True
                    two_players = False

            screen.fill(DARK_GREY)
            pg.draw.rect(screen, GREY, pg.Rect(WIDTH / 2 - 2, 0, 4, HEIGHT)) # middle line
            menu_cpu.draw_menu(screen)
            menu_mp.draw_menu(screen)
            player_glider.draw_glider(screen)
            cpu_glider.draw_glider(screen)
            pg.display.flip()


        time.sleep(0.5)
    last_tick = pg.time.get_ticks()
    while running and decision:
        
        while running and p1_score < 5 and p2_score < 5:    
            clock.tick(60)

            for event in pg.event.get():
                keys_pressed = pg.key.get_pressed()

                if event.type == pg.QUIT:
                    running = False
    

            ### 2 players
            if two_players:
                if keys_pressed[pg.K_s]:
                    second_glider.move_glider_down()
                if keys_pressed[pg.K_w]:
                    second_glider.move_glider_up()

            ## main player movement  
            if keys_pressed[pg.K_DOWN]:
                player_glider.move_glider_down()
            if keys_pressed[pg.K_UP]:
                player_glider.move_glider_up()


            ## screen fill & drawing
            screen.fill(DARK_GREY)
            pg.draw.rect(screen, GREY, pg.Rect(WIDTH / 2 - 2, 0, 4, HEIGHT))

            if pg.time.get_ticks() - last_tick > wait_tick:
                if two_players:
                    ball.move_ball(glider_1=player_glider, glider_2=second_glider)
                else:
                    ball.move_ball(glider_1=player_glider, glider_2=cpu_glider)
                ball.draw_ball(screen)

            score_rtn = ball.detect_score()
            if score_rtn == -1:
                p1_score += 1
                ball.reset()
                last_tick = pg.time.get_ticks()
            elif score_rtn == 1:
                p2_score += 1
                ball.reset()
                last_tick = pg.time.get_ticks()

            player_glider.draw_glider(screen)

            if not two_players:
                cpu_glider.draw_glider(screen)
            else:
                second_glider.draw_glider(screen)

            Menu.draw_score(screen, p1_score, p2_score)

            pg.display.flip()

        
        pg.time.wait(3000)
        running = False
            

    pg.quit()



##########################
### GLIDERS CLASSES ######
##########################

class Glider():

    rect_width = 6
    rect_height = 67
    bottom = HEIGHT
    top = 0

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.rect = pg.Rect(self.x, (self.y - self.rect_height / 2), self.rect_width, self.rect_height)

    def draw_glider(self, screen):
        self.rect = pg.Rect(self.x, (self.y - self.rect_height / 2), self.rect_width, self.rect_height)
        pg.draw.rect(screen, WHITE, self.rect)

    def move_glider_up(self):
        if (self.y - self.rect_height / 2 >= self.top):
            self.y -= 5

    def move_glider_down(self):
        if (self.y + self.rect_height / 2 <= self.bottom):
            self.y += 5


class Player_Glider(Glider):

    def __init__(self, SCR_HEIGHT):
        super().__init__(10, SCR_HEIGHT / 2)

class Cpu_Glider(Glider):

    def __init__(self, SCR_HEIGHT):
        super().__init__(WIDTH - 16, SCR_HEIGHT / 2)

class Second_Glider(Glider):

    def __init__(self, SCR_HEIGHT):
        super().__init__(WIDTH - 16, SCR_HEIGHT / 2)

##########################
### BALL CLASSES #########
##########################

class Ball():
    x: int
    y: int
    terminal_velocity_x = 1.5
    terminal_velocity_y = 2.3
    vector_velocities_x = [-1.7, -1.2, 1.2, 1.7]
    vector_velocities_y = [-1.5, -1, -.5, .5, 1, 1.5]

    def __init__(self):
        self.radius = 6
        self.x = WIDTH / 2
        self.y = HEIGHT / 2
        self.vector = pg.Vector2(rd.choice(self.vector_velocities_x), rd.choice(self.vector_velocities_y))
        self.speed = 2.5
        self.ball = pg.Rect(self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2)

    def draw_ball(self, screen):
        self.ball = pg.Rect(self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2)
        pg.draw.ellipse(screen, WHITE, self.ball)

    def move_ball(self, glider_1, glider_2):
        if self.detect_collision_y():
            self.vector.y = self.vector.y * -1

        if self.detect_collision_x(glider_1, glider_2):
            if self.vector.x <= self.terminal_velocity_x:
                self.vector.x = self.vector.x * -1.09
            else:
                self.vector.x = self.vector.x * -1.09
            
            if self.vector.y <= self.terminal_velocity_y:
                self.vector.y += rd.uniform(-.92, .9)
            else:
                self.vector.y += rd.uniform(-.92, .52)

        vec_x = self.vector.x * self.speed
        vec_y = self.vector.y * self.speed

        self.x += vec_x
        self.y += vec_y

    def reset(self):
        self.speed = 2.5
        self.x = WIDTH / 2
        self.y = HEIGHT / 2
        self.vector = pg.Vector2(rd.choice(self.vector_velocities_x), rd.choice(self.vector_velocities_y))


    def detect_collision_y(self):
        return self.y - self.radius <= 0 or self.y - self.radius >= HEIGHT - self.radius * 2
    
    def detect_collision_x(self, glider_1, glider_2):   
        return pg.Rect.colliderect(self.ball, glider_1.rect) or pg.Rect.colliderect(self.ball, glider_2.rect)
    
    def detect_score(self):
        # return 0 if nothing happened, returns -1 if player1 scores, returns 1 if cpu/player2 scores
        score = 0
        if self.x <= 0:
            score = 1
        elif self.x >= WIDTH:
            score = -1

        return score

    
##########################
###### MAIN MENU #########
##########################

class Menu():

    rect: pg.Rect
    x: int
    y: int

    def __init__(self, x: int, y: int):
        self.rect_width = 250
        self.rect_height = 60
        self.x = x
        self.y = y

    def check_clicked(self, x, y):
        return self.rect.collidepoint(x, y)
    
    def draw_menu(self, screen):
        font = pg.font.SysFont("Consola", 40,)
        pg.draw.rect(screen, WHITE, self.rect, width=0)
        text_draw = font.render(self.text, True, (0, 0, 0))
        screen.blit(text_draw, (self.rect.center[0] - 80, self.rect.center[1] - 15))

    def draw_score(screen, score1, score2):
        font = pg.font.SysFont("Consola", 40, bold=True)
        text_score1 = font.render(str(score1), True, LIGHTER_GREY)
        text_score2 = font.render(str(score2), True, LIGHTER_GREY)
        screen.blit(text_score1, ((WIDTH / 2) - 50, 30))
        screen.blit(text_score2, ((WIDTH / 2) + 33, 30))

class MenuMultiplayer(Menu):

    def __init__(self):
        super().__init__(WIDTH / 2, HEIGHT / 2 - 20)
        self.rect = pg.Rect(self.x - self.rect_width / 2, self.y - self.rect_height, self.rect_width, self.rect_height)
        self.text = "multiplayer"

class MenuCpu(Menu):

    def __init__(self):
        super().__init__(WIDTH / 2, HEIGHT / 2 - 20)
        self.rect = pg.Rect(self.x - self.rect_width / 2, self.y + self.rect_height, self.rect_width, self.rect_height)
        self.text = "   vs. CPU"



##########################
######## MAIN ############
##########################
    
if __name__ == "__main__":
    main()
