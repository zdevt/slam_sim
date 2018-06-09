#!/usr/bin/env python
#-*- coding:utf-8 -*-
#       FileName:  slam.py
#
#    Description:
#
#        Version:  1.0
#        Created:  2018-06-06 16:53:32
#  Last Modified:  2018-06-09 13:41:37
#       Revision:  none
#       Compiler:  gcc
#
#         Author:  zt ()
#   Organization:

import os
import pygame
from pygame.locals import *
from sys import exit
import random
from PIL import Image

display_width = 800
display_height = 600
display_res = (display_width, display_height)
robotsize = (100, 100)
FPS = 10

slam = {}
pic = {}


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

    def setxy(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def draw(self, s):
        s.blit(self.image, (self.rect.x, self.rect.y))

    def up(self):
        self.rect.y -= 5

    def down(self):
        self.rect.y += 5

    def left(self):
        self.rect.x -= 5

    def right(self):
        self.rect.x += 5


def getRobotSprite():
    slam['robot'] = MySprite(loadRobot(), (0, 0))


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


if __name__ == '__main__':
    pygame.init()
    slam['screen'] = pygame.display.set_mode(display_res, 0, 32)
    pygame.display.set_caption('slam')
    slam['fpsclock'] = pygame.time.Clock()

    loadres()
    getBlockObjectSpriteGroup()
    getRobotSprite()

    if pygame.sprite.spritecollide(slam['robot'], slam['g1'], False,
                                   pygame.sprite.collide_mask):
        print("collide", slam['robot'])

    while True:
        slam['screen'].fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
        key = pygame.key.get_pressed()
        moveIt(slam['robot'], key)
        slam['g1'].draw(slam['screen'])
        slam['robot'].draw(slam['screen'])
        pygame.display.update()
