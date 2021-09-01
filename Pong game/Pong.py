
import pygame
import math
pygame.init()
#pygame.mixer.init

screenWidth = 680
screenHeight = 420

win = pygame.display.set_mode((screenWidth, screenHeight),
                              pygame.RESIZABLE) #creating a window 
pygame.display.set_caption("Pong") #Setting a title 
clock = pygame.time.Clock()
hitSound = pygame.mixer.Sound("TypeWriter.wav") 
music = pygame.mixer.music.load("MainTheme.mp3") 
pygame.mixer.music.play(-1)



class paddle(object):
    '''Initializing co ordinates of first paddle'''
    def __init__(self, x, y, l, b, color):
        self.x = x
        self.y = y
        self.l = l
        self.b = b
        self.color = color
        self.vel = 20
        self.score = 0

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.b, self.l))        


class ball(object):
    '''Initializing Co ordinates of pong'''
    def __init__(self, x, y, radius, color, hits):
        self.x = x 
        self.y = y
        self.radius = radius
        self.color = color
        self.vel_x = 12.5 #velocity of the ball 
        self.vel_y = 12 #velocity of the ball
        self.hits = hits

    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x,self.y), self.radius)


def redraw(): 
    '''Draws the two paddles and everything else'''
    win.fill((0,0,0))
    
    text = font.render('SCORE', 1, (0, 200, 0))
    text_rect = text.get_rect()
    text_rect.center = (screenWidth*0.5 , 20)
    win.blit(text, text_rect)
    #win.blit(text, (screenWidth*0.5 -30, 0))
    
    textScore = font.render(f'{p1.score}:{p2.score}', 1, (0, 200, 0))
    win.blit(textScore, (screenWidth*0.5 -20, 40))
    speed = font.render(f'Speed:({round(pong.vel_x, 2)}, {round(pong.vel_y, 2)})', 1, (200, 0, 200))
    speed_rect = speed.get_rect()
    speed_rect.center = (screenWidth//3, screenHeight-20)
    win.blit(speed, speed_rect)
    hit = font.render(f'Hits:{pong.hits}', 1, (200, 200, 0))
    hit_rect = hit.get_rect()
    hit_rect.center = ((2*screenWidth)//3, screenHeight-20)
    win.blit(hit, hit_rect)
    p1.draw(win)
    p2.draw(win)
    pong.draw(win) 
    endgame() 
    pygame.display.update()

def vel_coeff(numHits):
    '''calculates coefficient of velocity of the ball'''
    k_vel = math.log10(10 + numHits)/math.log10(9 + numHits)
    #print(k_vel)
    return k_vel

def reset(winner_num):
    '''resets the gameboard'''
    N = winner_num #player who won the point

    if N==1:
        pong.vel_x = abs(pong.vel_x) #pong starts moving right
    elif N==2:
        pong.vel_x = -abs(pong.vel_x) #pong starts moving left
    pong.x = int((N/3)*screenWidth)
    pong.y = int((N/3)*screenHeight)
    pygame.time.delay(500)


def gameover(): 
    pong.x = int(screenWidth//2)
    pong.y = int(screenHeight//2)
    #p1.x = 0
    p1.y = screenHeight*0.5 - 110
    #p2.x = screenWidth - 20 
    p2.y = screenHeight*0.5 + 10

def endgame():
    font1 = pygame.font.SysFont('comicsans', 50, bold=True,)

    if p1.score == 10:
        text = font1.render('PLAYER RED WINS !!', 1, (255, 0, 0))
        win.blit(text, (340- text.get_width()/2, 200))
        gameover()

    elif p2.score == 10:
        text = font1.render('PLAYER BLUE WINS !!', 1, (0, 0, 255))
        win.blit(text, (340- text.get_width()/2, 200))
        gameover()

def restart():
    pong.x = int(screenWidth//2)
    pong.y = int(screenHeight//2)
    #p1.x = 0
    p1.y = screenHeight*0.5 - 110
    #p2.x = screenWidth - 20 
    p2.y = screenHeight*0.5 + 10
    p1.score = 0
    p2.score = 0
    pong.vel_x = 12.5
    pong.vel_y = 12
    pong.hits = 0


### MAIN LOOP ###
font = pygame.font.SysFont('calibri', 30, bold=True)
hits = 0
p1 = paddle(0, screenHeight*0.5 -110, 100, 20, (255, 0, 0)) 
p2 = paddle(screenWidth-20, screenHeight*0.5 +10, 100, 20, (0, 0, 255)) 
pong = ball(int(screenWidth//2), int(screenHeight//2), 6, (0,250,100), hits)
k_vel = 1
p1.score, p2.score = 0, 0
hits = 0
run = True # Controls the execution

while run:

    time_passed = clock.tick(30) 
    time_sec = time_passed//1000
    
    pong.x += pong.vel_x
    pong.y += pong.vel_y

    if pong.x < p1.x + p1.b +5: 
        if pong.y > p1.y and pong.y < p1.y + p1.l:
            pong.hits += 1
            k_vel = vel_coeff(pong.hits)
            pong.vel_x *= -k_vel
            pong.vel_y *= k_vel
            hitSound.play()

    if pong.x > p2.x - 5: 
        if pong.y > p2.y and pong.y< p2.y + p2.l:
            pong.hits += 1
            k_vel = vel_coeff(pong.hits)
            pong.vel_x *= -k_vel
            pong.vel_y *= k_vel
            
            hitSound.play()

    if pong.y < 5 or pong.y > screenHeight -5: 
        pong.vel_y *= -1 
        hitSound.play()

    if pong.x < 0: 
        p2.score += 1
        reset(2)

    if pong.x > screenWidth + pong.radius*2: 
        p1.score += 1
        reset(1)

    for event in pygame.event.get(): # Inputs all the events
        if event.type == pygame.QUIT: 
            run= False
            pygame.quit() # Exits the window
            quit()
    keys = pygame.key.get_pressed() # Creates a list of events

    if keys[pygame.K_w] and p1.y > 0: # Controls upward movement
        p1.y -= p1.vel

    if keys[pygame.K_s] and p1.y < screenHeight-p1.l: #Controls downward movement
        p1.y += p1.vel

    if keys[pygame.K_UP] and p2.y > 0: # Controls upward movement
        p2.y -= p2.vel

    if keys[pygame.K_DOWN] and p2.y < screenHeight-p2.l: # Controls downward movement 
        p2.y += p2.vel

    if keys[pygame.K_p]: # Restart button
        restart()
        k_vel = 1 # Starting again with default speed

    redraw()

#pygame.mixer.quit()
#pygame.display.quit()
pygame.quit() # Exits the window
#quit()
