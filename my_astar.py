#!/usr/bin/env python
#-*- coding:utf-8 -*-
#       FileName:  my_astar.py
#
#    Description:
#
#        Version:  1.0
#        Created:  2018-06-19 16:22:23
#  Last Modified:  2018-06-20 14:42:20
#       Revision:  none
#       Compiler:  gcc
#
#         Author:  zt ()
#   Organization:

import os
import math
import pygame
from pygame.locals import *
from sys import exit
import random
from PIL import Image

display_width, display_height = 800, 600
display_res = (display_width + 1, display_height + 1)

openlist = []
closedlist = []
tracklist = []
maplist = {}

delta = 20
BLOCKCNT = 150

robotsize = (delta, delta)

global SCREEN, FPSCLOCK
FPS = 20

WHITE = (255, 255, 255)


class Cell:
    def __init__(self, pos):
        (self.x, self.y) = pos
        self.G = 0
        self.H = 0
        self.F = 0
        self.flag = 0  # 0:空 1:障碍 2:起点 3: 终点 4:轨迹

    def getPos(self):
        return (self.x, self.y)

    def setEmpty(self):
        self.flag = 0

    def isEmpty(self):
        return (0 == self.flag)

    def setBlock(self):
        self.flag = 1

    def isBlock(self):
        return (1 == self.flag)

    def setStart(self):
        self.flag = 2

    def isStart(self):
        return (2 == self.flag)

    def setEnd(self):
        self.flag = 3

    def isEnd(self):
        return (3 == self.flag)

    def setTrack(self):
        self.flag = 4

    def isTrack(self):
        return (4 == self.flag)

    def calcF(self):
        self.F = self.G + self.H

    def calcG(self):  #起点到当前移动量
        pass

    def calcH(self):  #当前到终点预估移动量
        pass


def getPosxyByXy((x, y)):
    pos = (int(math.ceil(x / delta)), int(math.ceil(y / delta)))
    return pos


def fillRect(pos, color=WHITE):
    (posx, posy) = pos
    pygame.draw.rect(SCREEN, color, (posx * delta, posy * delta, delta, delta),
                     0)


def genRdBlockList(cnt=BLOCKCNT):
    blocklist = []
    for i in xrange(cnt):
        posx = random.randint(0, (display_width / delta) - 1)
        posy = random.randint(0, (display_height / delta) - 1)
        if (posx, posy) not in blocklist:
            blocklist.append((posx, posy))
    return blocklist


def drawGrid(color=WHITE):
    for x in xrange(0, display_width + 1, delta):
        pygame.draw.line(SCREEN, color, (x, 0), (x, display_height), 1)
    for y in xrange(0, display_height + 1, delta):
        pygame.draw.line(SCREEN, color, (0, y), (display_width, y), 1)


def genMap():
    blist = genRdBlockList()
    for p in blist:
        c = Cell(p)
        c.setBlock()
        maplist[p] = c


def drawMap():
    drawGrid((30, 30, 30))
    for v in maplist.values():
        if v.isBlock():
            fillRect(v.getPos())
        elif v.isEmpty():
            pass
        elif v.isStart():
            fillRect(v.getPos(), (0, 0, 255))
        elif v.isEnd():
            fillRect(v.getPos(), (255, 0, 0))
        elif v.isTrack():
            fillRect(v.getPos(), (0, 255, 0))


if __name__ == "__main__":
    pygame.init()
    SCREEN = pygame.display.set_mode(display_res, 0, 32)
    pygame.display.set_caption('slam')
    FPSCLOCK = pygame.time.Clock()

    genMap()

    while True:
        SCREEN.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            elif event.type == MOUSEBUTTONDOWN:
                pressed_array = pygame.mouse.get_pressed()
                for index in xrange(len(pressed_array)):
                    if pressed_array[index]:
                        if index == 0:
                            # print("Pressed LEFT Button!")
                            p = getPosxyByXy(pygame.mouse.get_pos())
                            c = Cell(p)
                            c.setStart()
                            if not maplist.has_key(p):
                                maplist[p] = c
                        elif index == 1:
                            print("The mouse whell Pressed!")
                        elif index == 2:
                            # print("Pressed RIGHT Button!")
                            p = getPosxyByXy(pygame.mouse.get_pos())
                            c = Cell(p)
                            c.setEnd()
                            if not maplist.has_key(p):
                                maplist[p] = c
                # pos = pygame.mouse.get_pos()
                # print(pos)
            elif event.type == MOUSEMOTION:
                pos = pygame.mouse.get_pos()
                mouse_x = pos[0]
                mouse_y = pos[1]

        drawMap()

        FPSCLOCK.tick(FPS)
        pygame.display.update()
