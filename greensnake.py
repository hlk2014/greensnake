import pygame
import sys
import time
import random

from pygame.locals import *

FPS = 12
pygame.init()
fpsClock=pygame.time.Clock()

SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
surface = pygame.Surface(screen.get_size())
surface = surface.convert()
surface.fill((255,255,255))
#clock = pygame.time.Clock()
#pygame.key.set_repeat(1, 100)
pygame.key.set_repeat()

GRIDSIZE=20
GRID_WIDTH = SCREEN_WIDTH / GRIDSIZE
GRID_HEIGHT = SCREEN_HEIGHT / GRIDSIZE
UP    = (0, -1)
DOWN  = (0, 1)
LEFT  = (-1, 0)
RIGHT = (1, 0)
    
#screen.blit(surface, (0,0))

def draw_box(surf, color, pos):
    r = pygame.Rect((pos[0], pos[1]), (GRIDSIZE, GRIDSIZE))
    pygame.draw.rect(surf, color, r)

def draw_circle(surf, color, pos, radius, width=0):
    pygame.draw.circle(surf, color, pos, radius, width)
    
class Snake(object):
    def __init__(self):
        self.lose()
        self.color = (0,200,0)

    def get_head_position(self):
        return self.positions[0]

    def lose(self):
        self.length = 3
        self.positions =  [((SCREEN_WIDTH / 2), (SCREEN_HEIGHT / 2))]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])

    def point(self, pt):
        if self.length > 1 and (pt[0] * -1, pt[1] * -1) == self.direction:
            return
        else:
            self.direction = pt

    def move(self):
        cur = self.positions[0]
        x, y = self.direction
        new = (((cur[0]+(x*GRIDSIZE)) % SCREEN_WIDTH), (cur[1]+(y*GRIDSIZE)) % SCREEN_HEIGHT)
        if len(self.positions) > 2 and new in self.positions[2:]:
            self.lose()
        else:
            self.positions.insert(0, new)
            if len(self.positions) > self.length:
                self.positions.pop()
    
    def draw(self, surf):
        for p in self.positions[0::2]:
            draw_box(surf, (0,100,0), p)
        for p in self.positions[1::2]:
            draw_box(surf, (0,200,0),p)
            
class Apple(object):
    def __init__(self):
        self.position = (0,0)
        self.color = (255,0,0)
        self.randomize()

    def randomize(self):
        self.position = (random.randint(0, GRID_WIDTH-1) * GRIDSIZE, random.randint(0, GRID_HEIGHT-1) * GRIDSIZE)

    def draw(self, surf):
        draw_box(surf, self.color, self.position)
        draw_box(surf, self.color, (self.position[0]+GRIDSIZE, self.position[1]+GRIDSIZE))
        draw_box(surf, self.color, (self.position[0]+GRIDSIZE, self.position[1]))
        draw_box(surf, self.color, (self.position[0], self.position[1]+GRIDSIZE))
        
        #draw_circle(surf, self.color, self.position, 20)
        
def check_eat(snake, apple):
    if snake.get_head_position() == apple.position:
        snake.length += 1
        apple.randomize()

    if snake.get_head_position() == (apple.position[0]+GRIDSIZE, apple.position[1]):
        snake.length += 1
        apple.randomize()

    if snake.get_head_position() == (apple.position[0], apple.position[1]+GRIDSIZE):
        snake.length += 1
        apple.randomize()

    if snake.get_head_position() == (apple.position[0]+GRIDSIZE, apple.position[1]+GRIDSIZE):
        snake.length += 1
        apple.randomize()
    

        
if __name__ == '__main__':
    snake = Snake()
    apple = Apple()

    def updatescreen():
        surface.fill((255,255,255))
        snake.move()
        check_eat(snake, apple)
        snake.draw(surface)
        apple.draw(surface)
        font = pygame.font.Font(None,  30)
        snakePos=snake.get_head_position()
        textStr= str(snakePos[0]) + ' ' + str(snakePos[1]) + ' ' + str(snake.length)
        text = font.render(textStr, 1, (10, 10, 10))
        textpos = text.get_rect()
        textpos.centerx = 60
        surface.blit(text, textpos)
        screen.blit(surface, (0,0))
        pygame.display.flip()
        pygame.display.update()
        #fpsClock.tick(FPS + snake.length/3)
        

    while True:
        
        for event in pygame.event.get():

            print event.type
            
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_UP:
                    snake.point(UP)
                elif event.key == K_DOWN:
                    snake.point(DOWN)
                elif event.key == K_LEFT:
                    snake.point(LEFT)
                elif event.key == K_RIGHT:
                    snake.point(RIGHT)

        updatescreen()
                #snake.move()

                #updatescreen()
       # snake.move()        

        fpsClock.tick(FPS )
       
