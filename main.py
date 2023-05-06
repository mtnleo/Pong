import pygame as pg

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

    while running:
        clock.tick(60)

        for event in pg.event.get():
            keys_pressed = pg.key.get_pressed()

            if event.type == pg.QUIT:
                running = False
            
        if keys_pressed[pg.K_DOWN]:
            player_glider.move_glider_down()
        if keys_pressed[pg.K_UP]:
            player_glider.move_glider_up()

        if two_players:
            if keys_pressed[pg.K_s]:
                second_glider.move_glider_down()
            if keys_pressed[pg.K_w]:
                second_glider.move_glider_up()

        screen.fill(DARK_GREY)
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
    rect_height = 50
    bottom = HEIGHT
    top = 0

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw_glider(self, screen):
        rect = pg.Rect(self.x, (self.y - self.rect_height / 2), self.rect_width, self.rect_height)
        pg.draw.rect(screen, WHITE, rect)

    def move_glider_up(self):
        if (self.y - self.rect_height / 2 != self.top):
            self.y -= 3

    def move_glider_down(self):
        if (self.y + self.rect_height / 2 != self.bottom):
            self.y += 3


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


if __name__ == "__main__":
    main()
