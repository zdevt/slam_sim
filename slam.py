#!/usr/bin/env python
#-*- coding:utf-8 -*-
#       FileName:  slam.py
#
#    Description:
#
#        Version:  1.0
#        Created:  2018-06-06 16:53:32
#  Last Modified:  2018-06-07 13:13:50
#       Revision:  none
#       Compiler:  gcc
#
#         Author:  zt ()
#   Organization:

import pygame
from pygame.locals import *
from sys import exit
import random

display_width = 800
display_height = 600
display_res = (display_width, display_height)

FPS = 1

pic = {}
global screen
global fpsclock


def loadres():
    pic['shape'] = [
        pygame.image.load("shape_sample/%d.png" % (i + 1)).convert_alpha()
        for i in range(0, 20)
    ]


def getRandomPic():
    rdpicIndex = random.randrange(1, 20)
    size = (random.randrange(10, display_width / 4),
            random.randrange(10, display_height / 4))
    cor = (random.randrange(0, display_width),
           random.randrange(0, display_height))
    return pygame.transform.smoothscale(pic['shape'][rdpicIndex], size), cor


def genBlockObject():
    pic['rdpic'] = [getRandomPic() for i in range(10)]
    return pic['rdpic']


def test():
    while True:
        screen.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == QUIT:
                exit()

        for (p, c) in genBlockObject():
            screen.blit(p, c)

        pygame.display.update()
        fpsclock.tick(FPS)


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode(display_res, 0, 32)
    screen.fill((0, 0, 0))
    pygame.display.set_caption('slam')
    pygame.display.update()

    fpsclock = pygame.time.Clock()

    loadres()
    test()
