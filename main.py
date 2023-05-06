import pygame as pg
import random as rd

WIDTH = 700
HEIGHT = 400

DARK_GREY = (112, 128, 144)
WHITE = (255, 255, 255)

def main():
    pg.init()
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    clock = pg.time.Clock()
    running = True

    two_players = True ## change it depedning on what mode the player's in

    #instantiate glider
    player_glider = Player_Glider(HEIGHT)

    if two_players:
        second_glider = Second_Glider(HEIGHT)
    else:
        cpu_glider = Cpu_Glider(HEIGHT)

    # instantiate ball
    ball = Ball()

    while running:
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
        if two_players:
            ball.move_ball(glider_1=player_glider, glider_2=second_glider)
        else:
            ball.move_ball(glider_1=player_glider, glider_2=cpu_glider)
        ball.draw_ball(screen)

        player_glider.draw_glider(screen)

        if not two_players:
            cpu_glider.draw_glider(screen)
        else:
            second_glider.draw_glider(screen)

        pg.display.flip()
        


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
    terminal_velocity = 1.5

    def __init__(self):
        self.radius = 6
        self.x = WIDTH / 2
        self.y = HEIGHT / 2
        self.vector = pg.Vector2(1, -2)
        self.speed = 2.5
        self.ball = pg.Rect(self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2)

    def draw_ball(self, screen):
        self.ball = pg.Rect(self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2)
        pg.draw.ellipse(screen, WHITE, self.ball)

    def move_ball(self, glider_1, glider_2):
        if self.detect_collision_y():
            self.vector.y = self.vector.y * -1

        if self.detect_collision_x(glider_1, glider_2):
            if self.vector.x <= self.terminal_velocity:
                self.vector.x = self.vector.x * -1.09
            else:
                self.vector.x = self.vector.x * -1.09
            self.vector.y += rd.uniform(-1.2, 1.2)

        vec_x = self.vector.x * self.speed
        vec_y = self.vector.y * self.speed

        self.x += vec_x
        self.y += vec_y

    def detect_collision_y(self):
        return self.y - self.radius <= 0 or self.y - self.radius >= HEIGHT
    
    def detect_collision_x(self, glider_1, glider_2):   
        return pg.Rect.colliderect(self.ball, glider_1.rect) or pg.Rect.colliderect(self.ball, glider_2.rect)

    


if __name__ == "__main__":
    main()
