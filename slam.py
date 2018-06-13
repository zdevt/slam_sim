#!/usr/bin/env python
#-*- coding:utf-8 -*-
#       FileName:  slam.py
#
#    Description:
#
#        Version:  1.0
#        Created:  2018-06-06 16:53:32
#  Last Modified:  2018-06-13 17:10:21
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

display_width = 800
display_height = 600
display_res = (display_width, display_height)

robotsize = (50, 50)
FPS = 10

delta = 5

slam = {}
pic = {}
slam['map'] = []


def convertPicToAlpha(file):
    im = Image.open(file)
    x, y = im.size
    p = Image.new('RGBA', im.size, (0, 0, 0))
    p.paste(im, (0, 0, x, y), im)
    p.save(file)


def loadres():
    pic['shape'] = [
        pygame.image.load("shape_sample/%d.png" % (i + 1)).convert()
        for i in range(0, 20)
    ]


def loadRobot():
    img = pygame.transform.smoothscale(
        pygame.image.load('000.png').convert(), robotsize)
    img.set_colorkey((0, 0, 0))
    return img


def getRandomPic():
    rdpicIndex = random.randrange(1, 20)
    size = (random.randrange(10, display_width / 4),
            random.randrange(10, display_height / 4))
    cor = (random.randrange(0, display_width),
           random.randrange(0, display_height))

    img = pygame.transform.smoothscale(pic['shape'][rdpicIndex], size)
    img.set_colorkey((0, 0, 0))
    return img, cor


def genBlockObject():
    pic['rdpic'] = [getRandomPic() for i in range(11)]
    return pic['rdpic']


class MySprite(pygame.sprite.Sprite):
    def __init__(self, img, cordinate):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = cordinate
        self.mask = pygame.mask.from_surface(self.image)

    def getxy(self):
        return (self.rect.x, self.rect.y)

    def setxy(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def draw(self, s):
        s.blit(self.image, (self.rect.x, self.rect.y))

    def up(self, d=delta):
        if self.rect.y >= d:
            self.rect.y -= d

    def down(self, d=delta):
        if self.rect.y + d < display_height:
            self.rect.y += d

    def left(self, d=delta):
        if self.rect.x >= d:
            self.rect.x -= d

    def right(self, d=delta):
        if self.rect.x + d < display_width:
            self.rect.x += d


def getRobotSprite():
    slam['robot'] = MySprite(loadRobot(), (0, 0))


def getVirsualLidar():
    img = pygame.transform.smoothscale(
        pygame.image.load('000.png').convert(), (1, 1))
    img.set_colorkey((0, 0, 0))
    slam['vlidar'] = MySprite(img, (0, 0))


def virtualLidarScan(r, x, y):
    p = {}
    oldx, oldy = r.getxy()
    for i in xrange(0, 360):
        a = []
        p[i] = a
        for l in xrange(1, display_width, 5):
            lx = x + l * math.cos(math.radians(i))
            ly = y - l * math.sin(math.radians(i))
            r.setxy(lx, ly)
            if collideCheck(r, slam['g1']):
                p[i].append(l)
    for k, v in p.items():
        if v:
            l = min(v)
            lx = x + l * math.cos(math.radians(k))
            ly = y - l * math.sin(math.radians(k))
            pygame.draw.line(slam['screen'], (255, 0, 0), (x, y), (lx, ly))


def getBlockObjectSpriteGroup():
    p1, c1 = getRandomPic()
    s1 = MySprite(p1, c1)

    g1 = pygame.sprite.Group()
    g1.add(s1)

    for i in xrange(10):
        p, c = getRandomPic()
        s = MySprite(p, c)
        if pygame.sprite.spritecollide(s, g1, False,
                                       pygame.sprite.collide_mask):
            # print("collide detected ",s.rect)
            pass
        else:
            g1.add(s)

    slam['g1'] = g1


def moveIt(s, key):
    if key[pygame.K_w]:
        s.up()
    elif key[pygame.K_s]:
        s.down()
    elif key[pygame.K_a]:
        s.left()
    elif key[pygame.K_d]:
        s.right()


def collideCheck(s, sg):
    if pygame.sprite.spritecollide(s, sg, False, pygame.sprite.collide_mask):
        print("collide", s.rect)
        return True
    return False


def rdMoveIt(s):
    oldx = s.rect.x
    oldy = s.rect.y
    d = random.randrange(1, 5)
    if d == 1:
        s.up()
    elif d == 2:
        s.down()
    elif d == 3:
        s.left()
    elif d == 4:
        s.right()

    if collideCheck(s, slam['g1']):
        s.setxy(oldx, oldy)
    else:
        m = s.getxy()
        # if m not in slam['map']:
            # slam['map'].append(m)
        # else:
            # s.setxy(oldx, oldy)


if __name__ == '__main__':
    pygame.init()
    slam['screen'] = pygame.display.set_mode(display_res, 0, 32)
    pygame.display.set_caption('slam')
    slam['fpsclock'] = pygame.time.Clock()

    loadres()
    getBlockObjectSpriteGroup()
    getRobotSprite()
    x = 0
    y = 0

    while True:
        slam['screen'].fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()

        # getVirsualLidar()
        # x += 4
        # y += 3
        # virtualLidarScan(slam['vlidar'], x, y)

        moveIt(slam['robot'], pygame.key.get_pressed())
        # rdMoveIt(slam['robot'])
        collideCheck(slam['robot'], slam['g1'])
        slam['g1'].draw(slam['screen'])
        slam['robot'].draw(slam['screen'])

        # slam['fpsclock'].tick(FPS)

        pygame.display.update()
