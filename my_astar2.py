#!/usr/bin/env python
#-*- coding:utf-8 -*-
#       FileName:  my_astar2.py
#
#    Description:
#
#        Version:  1.0
#        Created:  2018-06-21 13:37:41
#  Last Modified:  2018-06-21 14:56:39
#       Revision:  none
#       Compiler:  gcc
#
#         Author:  zt ()
#   Organization:

import os
import sys
import math
import pygame
import random

from sys import exit
from PIL import Image
from pygame.locals import *

delta = 20

display_width, display_height = 800, 600
display_res = (display_width + 1, display_height + 1)

BLOCKCNT = int((display_width / delta) * (display_height / delta) / 8)

xcnt = int((display_width / delta) - 1)
ycnt = int((display_height / delta) - 1)

SCREEN = None
FPSCLOCK = None

FPS = 10

WHITE = (255, 255, 255)

_2dmap = []
start = None
end = None

block_list = []
tracklist = []
open_list = {}
close_list = {}
maplist = {}


class Node:
    def __init__(self, father, x, y):
        self.father = father

        self.x = x
        self.y = y

        if father != None:
            G2father = calc_G(father, self)
            self.G = G2father + father.G
            self.H = calc_H(self, end)
            self.F = self.G + self.H
        else:
            self.G = 0
            self.H = 0
            self.F = 0

    def reset_father(self, father, new_G):
        if father != None:
            self.G = new_G
            self.F = self.G + self.H

        self.father = father


def checkValid(x, y):
    if 0 <= x <= xcnt and 0 <= y <= ycnt:
        return True
    return False


def calc_G(node1, node2):
    x1 = abs(node1.x - node2.x)
    y1 = abs(node1.y - node2.y)
    if (x1 == 1 and y1 == 0):
        return 10
    elif (x1 == 0 and y1 == 1):
        return 10
    # elif (x1 == 1 and y1 == 1):
    # return 14
    else:
        return 0


def calc_H(cur, end):
    return abs(end.x - cur.x) + abs(end.y - cur.y)


def min_F_node():
    k = sorted(open_list.items(), key=lambda x: x[1], reverse=False)

    if len(k) > 0:
        return open_list[k[0][0]]

    return False


def addAdjacentIntoOpen(node):
    if not node:
        return False

    open_list.pop((node.x, node.y))
    close_list[(node.x, node.y)] = node

    _adjacent = []

    # if checkValid(node.x - 1, node.y - 1):
    # _adjacent.append(Node(node, node.x - 1, node.y - 1))

    if checkValid(node.x, node.y - 1):
        _adjacent.append(Node(node, node.x, node.y - 1))

    # if checkValid(node.x + 1, node.y - 1):
    # _adjacent.append(Node(node, node.x + 1, node.y - 1))

    if checkValid(node.x + 1, node.y):
        _adjacent.append(Node(node, node.x + 1, node.y))

    # if checkValid(node.x + 1, node.y + 1):
    # _adjacent.append(Node(node, node.x + 1, node.y + 1))

    if checkValid(node.x, node.y + 1):
        _adjacent.append(Node(node, node.x, node.y + 1))

    # if checkValid(node.x - 1, node.y + 1):
    # _adjacent.append(Node(node, node.x - 1, node.y + 1))

    if checkValid(node.x - 1, node.y):
        _adjacent.append(Node(node, node.x - 1, node.y))

    for a in _adjacent:
        if (a.x, a.y) == (end.x, end.y):
            new_G = calc_G(a, node) + node.G
            end.reset_father(node, new_G)
            return True

        if (a.x, a.y) in close_list:
            continue

        if (a.x, a.y) not in open_list:
            open_list[(a.x, a.y)] = a
        else:
            exist_node = open_list[(a.x, a.y)]
            new_G = calc_G(a, node) + node.G
            if new_G < exist_node.G:
                exist_node.reset_father(node, new_G)

    return False


def find_the_path(start, end):
    open_list[(start.x, start.y)] = start
    the_node = start

    while not addAdjacentIntoOpen(the_node):
        the_node = min_F_node()

    return True


def mark_path(node):
    if node.father == None:
        return

    pos = (node.x, node.y)
    # fillRect(pos, (0, 255, 0))
    tracklist.append(pos)
    mark_path(node.father)


def getPosxyByXy((x, y)):
    pos = (int(math.ceil(x / delta)), int(math.ceil(y / delta)))
    return pos


def fillRect(pos, color=WHITE):
    (posx, posy) = pos
    pygame.draw.rect(SCREEN, color, (posx * delta, posy * delta, delta, delta),
                     0)


def genRdBlockList(cnt=BLOCKCNT):
    for i in xrange(cnt):
        posx = random.randint(0, xcnt)
        posy = random.randint(0, ycnt)
        if (posx, posy) == (0, 0):
            pass
        elif (posx, posy) not in block_list:
            block_list.append((posx, posy))


def drawGrid(color=WHITE):
    for x in xrange(0, display_width + 1, delta):
        pygame.draw.line(SCREEN, color, (x, 0), (x, display_height), 1)
    for y in xrange(0, display_height + 1, delta):
        pygame.draw.line(SCREEN, color, (0, y), (display_width, y), 1)


def genMap():
    genRdBlockList()
    for p in block_list:
        (posx, posy) = p
        block_node = Node(None, posx, posy)
        close_list[(block_node.x, block_node.y)] = block_node


def drawMap():
    drawGrid((30, 30, 30))
    for k in block_list:
        fillRect(k)

    for t in tracklist:
        fillRect(t, (0, 255, 0))


if __name__ == "__main__":
    pygame.init()
    SCREEN = pygame.display.set_mode(display_res, 0, 32)
    pygame.display.set_caption('slam')
    FPSCLOCK = pygame.time.Clock()

    start = Node(None, 0, 0)
    end = Node(None, xcnt - 2, ycnt - 2)
    genMap()

    flag = False

    while True:
        SCREEN.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            elif event.type == MOUSEBUTTONDOWN:
                pressed_array = pygame.mouse.get_pressed()
                # for index in xrange(len(pressed_array)):
                # if pressed_array[index]:
                # if index == 0:
                # # print("Pressed LEFT Button!")
                # p = getPosxyByXy(pygame.mouse.get_pos())
                # c = maplist[p]
                # c.setStart()
                # elif index == 1:
                # print("The mouse whell Pressed!")
                # elif index == 2:
                # # print("Pressed RIGHT Button!")
                # p = getPosxyByXy(pygame.mouse.get_pos())
                # c = maplist[p]
                # c.setEnd()

        if not flag and find_the_path(start, end):
            mark_path(end.father)
            flag = True

        drawMap()

        FPSCLOCK.tick(FPS)
        pygame.display.update()
