import pygame
import os
pygame.font.init()
pygame.mixer.init()


HEALTH_FONT =  pygame.font.SysFont('comicsans', 40)
WINNER_FONT =  pygame.font.SysFont('comicsans', 40)

HIT_SOUND = pygame.mixer.Sound(os.path.join('Assets','Grenade+1.mp3'))
FIRE_SOUND =pygame.mixer.Sound(os.path.join('Assets','Gun+Silencer.mp3'))

WIDTH, HEIGHT = 900,500
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
FPS = 60
VEL = 5
BULLET_VEL = 7
MAX_BULLETS = 3

YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 50,40
BORDER = pygame.Rect(WIDTH//2-5,0, 10,HEIGHT)
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("first Game!")
YELLOW_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join('Assets','spaceship_yellow.png'))
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(
    YELLOW_SPACESHIP_IMAGE,(SPACESHIP_WIDTH, SPACESHIP_HEIGHT)),90)
RED_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join('Assets','spaceship_red.png'))
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(
    RED_SPACESHIP_IMAGE,(SPACESHIP_WIDTH, SPACESHIP_HEIGHT)),-90)
SPACE = pygame.transform.scale(pygame.image.load(os.path.join('Assets','space.png')),(WIDTH,HEIGHT))
SPACE_BLUR = pygame.transform.scale(pygame.image.load(os.path.join('Assets','space_blur.png')),(WIDTH,HEIGHT))

click = False
def draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health):
    WIN.blit(SPACE,(0,0))
    pygame.draw.rect(WIN,BLACK, BORDER)
    
    red_health_text = HEALTH_FONT.render("Health: "+str(red_health),1,RED)
    yellow_health_text = HEALTH_FONT.render("Health: "+str(yellow_health),1,YELLOW)
    
    WIN.blit(red_health_text,(WIDTH - red_health_text.get_width()-10,10))
    WIN.blit(yellow_health_text,(10,10))

    WIN.blit(YELLOW_SPACESHIP,(yellow.x,yellow.y))
    WIN.blit(RED_SPACESHIP,(red.x,red.y))   

    for bullet in red_bullets: 
        pygame.draw.rect(WIN,RED, bullet)

    for bullet in yellow_bullets: 
        pygame.draw.rect(WIN,YELLOW, bullet)

    pygame.display.update()

def yellow_handele_movement(keys_pressed, yellow):
    if keys_pressed[pygame.K_a] and yellow.x - VEL > 0:# this is left
        yellow.x -= VEL
    if keys_pressed[pygame.K_d] and yellow.x + VEL + yellow.height < BORDER.x :# this is right
        yellow.x += VEL            
    if keys_pressed[pygame.K_w] and yellow.y - VEL > 0:# this is up
        yellow.y -= VEL
    if keys_pressed[pygame.K_s] and yellow.y + VEL + yellow.width<  HEIGHT :# this is down
        yellow.y += VEL
        
def red_handele_movement(keys_pressed, red):
    if keys_pressed[pygame.K_LEFT] and red.x - VEL > BORDER.x:# this is left
        red.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and red.x + VEL + red.height < 900 :# this is right
        red.x += VEL            
    if keys_pressed[pygame.K_UP] and red.y - VEL > 0:# this is up
        red.y -= VEL
    if keys_pressed[pygame.K_DOWN] and red.y + VEL + red.width<  HEIGHT :# this is down
        red.y += VEL

def handle_bullets(yellow_bullets,red_bullets,yellow,red):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.x -= BULLET_VEL           
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)

def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH//2 - draw_text.get_width()//2, HEIGHT//2- draw_text.get_height()//2))
    pygame.display.update()
    pygame.time.delay(5000)

def maimmenu():
    WIN.blit(SPACE_BLUR,(0,0))
    clock = pygame.time.Clock()
    run = True
    click = False
    while run:
        mx, my = pygame.mouse.get_pos()
        start_text = WINNER_FONT.render("Start", 1, WHITE)
        options_text = WINNER_FONT.render("Options", 1, WHITE)
        quit_text = WINNER_FONT.render("Quit", 1, WHITE)

        button_1 = pygame.Rect(WIDTH//2-100, 100, 200, 50)
        button_2 = pygame.Rect(WIDTH//2-100, 200, 200, 50)
        button_3 = pygame.Rect(WIDTH//2-100, 400, 200, 50)

        if button_1.collidepoint(mx,my):
            if click:
                main()
        if button_2.collidepoint(mx,my):
            if click:
                pass
        if button_3.collidepoint(mx,my):
            if click:
                pygame.quit()

        pygame.draw.rect(WIN, BLACK,button_1)
        pygame.draw.rect(WIN, BLACK,button_2)
        pygame.draw.rect(WIN, BLACK,button_3)
        WIN.blit(start_text, (WIDTH//2 - start_text.get_width()//2, 112))
        WIN.blit(options_text, (WIDTH//2 - options_text.get_width()//2, 212))
        WIN.blit(quit_text, (WIDTH//2 - quit_text.get_width()//2, 412))

        click = False
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
        pygame.display.update()
()

def draw_menu():
    WIN.blit(SPACE,(0,0))



    pygame.display.update()



def main():
    red = pygame.Rect(850, 250, SPACESHIP_WIDTH,SPACESHIP_HEIGHT)
    yellow = pygame.Rect(0, 250, SPACESHIP_WIDTH,SPACESHIP_HEIGHT)
    red_bullets = []
    yellow_bullets = []
    red_health = 10
    yellow_health = 10
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        click = False
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(yellow_bullets)<MAX_BULLETS:
                    bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height//2 -2,10,5)
                    yellow_bullets.append(bullet)
                    #FIRE_SOUND.play()

                if event.key == pygame.K_RCTRL and len(red_bullets)<MAX_BULLETS:
                    bullet = pygame.Rect(red.x , red.y + red.height//2 -2,10,5)
                    red_bullets.append(bullet)
                    #FIRE_SOUND.play()

            
            if event.type == RED_HIT:
                red_health -= 1
                #HIT_SOUND.play()
            
            if event.type == YELLOW_HIT:
                yellow_health -= 1
                #HIT_SOUND.play()


        winner = ""
        if red_health <=0:
            winner = "Yellow wins"
        
        if yellow_health <=0:
            winner = "red wins"
    
        if winner != "":
            draw_winner(winner)
            break
        
        keys_pressed = pygame.key.get_pressed()
        yellow_handele_movement(keys_pressed,yellow)
        red_handele_movement(keys_pressed,red)

        handle_bullets(yellow_bullets, red_bullets, yellow, red)

        draw_window(red, yellow, red_bullets, yellow_bullets,red_health,yellow_health)
    main()

if __name__ == "__main__":
    #main()
    maimmenu()