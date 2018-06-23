#!/usr/bin/env python
#-*- coding:utf-8 -*-
#       FileName:  my_astar.py
#
#    Description:
#
#        Version:  1.0
#        Created:  2018-06-19 16:22:23
#  Last Modified:  2018-06-23 10:50:35
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

delta = 20

display_width, display_height = 800, 600
display_res = (display_width + 1, display_height + 1)

BLOCKCNT = int((display_width / delta) * (display_height / delta) / 8)

xcnt = int((display_width / delta) - 1)
ycnt = int((display_height / delta) - 1)

global SCREEN, FPSCLOCK
FPS = 10

WHITE = (255, 255, 255)

startPoint = (0, 0)
targetPoint = (xcnt, ycnt)
# targetPoint = (2, 2)
currentPoint = None

stepComplete = False
allComplete = False

moveDirection = [(-1, 0), (1, 0), (0, -1), (0, 1)]

arrive_list = []
block_list = []
back_list = []

maxstepCnts = xcnt * ycnt


def IsAtDestination(cur, des):
    if cur == des:
        return True
    return False


def NextStep(pos, arrive_list, block_list, back_list):
    (x, y) = pos
    global currentPoint

    if not (0 <= x <= xcnt):
        return False

    if not (0 <= y <= ycnt):
        return False

    if pos in arrive_list:
        return False

    if pos in block_list:
        return False

    if pos in back_list:
        return False

    currentPoint = pos
    arrive_list.append(pos)
    return True


def BackStep(arrive_list, back_list):
    global currentPoint
    back_list.append(currentPoint)
    if len(arrive_list) > 1:
        arrive_list.pop()
        currentPoint = arrive_list[-1]
        return True
    return False


def DfsAlg(block_list, arrive_list, back_list):
    global stepComplete, allComplete, currentPoint
    currentPoint = startPoint

    i = 0

    while not allComplete:
        stepComplete = False

        while not stepComplete:
            (cx, cy) = currentPoint
            if IsAtDestination(currentPoint, targetPoint):
                allComplete = True
                break

            mvlist = [(cx + x, cy + y) for (x, y) in moveDirection]
            for pos in mvlist:
                if NextStep(pos, arrive_list, block_list, back_list):
                    stepComplete = True
                    break
            if not stepComplete:
                BackStep(arrive_list, back_list)
        i += 1
        if i > maxstepCnts:
            print(".............exit")
            break


def DfsAlg2(block_list, arrive_list, back_list):
    global stepComplete, allComplete, currentPoint

    if not currentPoint:
        print("init currentPoint")
        currentPoint = startPoint

    if allComplete:
        print("allComplete")
        return

    if IsAtDestination(currentPoint, targetPoint):
        allComplete = True
        stepComplete = True
        print("IsAtDestination")
        return

    stepComplete = False

    # while not stepComplete:
    (cx, cy) = currentPoint
    mvlist = [(cx + x, cy + y) for (x, y) in moveDirection]

    for pos in mvlist:
        if NextStep(pos, arrive_list, block_list, back_list):
            stepComplete = True
            break
        else:
            stepComplete = False

    if not stepComplete:
        if not BackStep(arrive_list, back_list):
            allComplete = True
            print("error.........")
            # break


def getPosxyByXy((x, y)):
    return (int(math.ceil(x / delta)), int(math.ceil(y / delta)))


def fillRect(pos, color=WHITE):
    (x, y) = pos
    pygame.draw.rect(SCREEN, color, (x * delta, y * delta, delta, delta), 0)


def genMap(cnt=BLOCKCNT):
    global block_list
    for i in xrange(cnt):
        x = random.randint(0, xcnt)
        y = random.randint(0, ycnt)
        block_list.append((x, y))


def drawGrid(color=WHITE):
    for x in xrange(0, display_width + 1, delta):
        pygame.draw.line(SCREEN, color, (x, 0), (x, display_height), 1)
    for y in xrange(0, display_height + 1, delta):
        pygame.draw.line(SCREEN, color, (0, y), (display_width, y), 1)


def drawMap():
    drawGrid((30, 30, 30))
    for p in block_list:
        fillRect(p, (255, 255, 255))

    for p in arrive_list:
        fillRect(p, (0, 255, 0))

    for p in back_list:
        fillRect(p, (0, 128, 0))

    fillRect(startPoint, (0, 0, 255))
    fillRect(targetPoint, (255, 0, 0))


if __name__ == "__main__":
    pygame.init()
    SCREEN = pygame.display.set_mode(display_res, 0, 32)
    pygame.display.set_caption('slam')
    FPSCLOCK = pygame.time.Clock()

    genMap()

    # flag = False
    flag = True

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
                            startPoint = getPosxyByXy(pygame.mouse.get_pos())
                        elif index == 1:
                            print("The mouse whell Pressed!")
                        elif index == 2:
                            # print("Pressed RIGHT Button!")
                            targetPoint = getPosxyByXy(pygame.mouse.get_pos())
                            flag = True

        if flag:
            # arrive_list = []
            # back_list = []
            # stepComplete = False
            # allComplete = False
            # DfsAlg(block_list, arrive_list, back_list)
            # flag = False
            DfsAlg2(block_list, arrive_list, back_list)
        drawMap()

        FPSCLOCK.tick(FPS)
        pygame.display.update()
