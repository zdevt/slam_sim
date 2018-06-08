#!/usr/bin/env python
#-*- coding:utf-8 -*-
#       FileName:  slam.py
#
#    Description:
#
#        Version:  1.0
#        Created:  2018-06-06 16:53:32
#  Last Modified:  2018-06-08 14:06:28
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

FPS = 10

pic = {}
global screen
global fpsclock


def formatpic(file):
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


def test():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()

        screen.fill((0, 255, 0))

        gbo = genBlockObject()
        pic1, p1 = gbo[0]
        sp1 = MySprite(pic1, p1)
        screen.blit(pic1, p1)
        pic2, p2 = gbo[1]
        sp2 = MySprite(pic2, p2)
        screen.blit(pic2, p2)
        pygame.display.update()
        fpsclock.tick(FPS)

        if pygame.sprite.collide_mask(sp1, sp2):
            print("collide:", p1, p2)
            raw_input()


def test2():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()

        fpsclock.tick(FPS)
        screen.fill((0, 0, 0))

        p1, c1 = getRandomPic()
        p2, c2 = getRandomPic()

        s1 = MySprite(p1, c1)
        s2 = MySprite(p2, c2)

        pygame.draw.rect(screen, (255, 0, 0), s1.rect, 1)
        pygame.draw.rect(screen, (255, 0, 0), s2.rect, 1)

        screen.blit(p1, c1)
        screen.blit(p2, c2)

        if pygame.sprite.collide_mask(s1, s2):
            print("  cordinate:", c1, c2)
            print("sprite rect:", s1.rect, s2.rect)
            print(s1.mask.count(), s2.mask.count())
            # raw_input()

        raw_input()
        pygame.display.update()


def genBlockObjectsprite():
    screen.fill((0, 0, 0))

    p1, c1 = getRandomPic()
    s1 = MySprite(p1, c1)

    sGroup = pygame.sprite.Group()
    sGroup.add(s1)

    screen.blit(p1, c1)
    pygame.draw.rect(screen, (255, 0, 0), s1.rect, 1)

    for i in xrange(10):
        p, c = getRandomPic()
        s = MySprite(p, c)
        if pygame.sprite.spritecollide(s, sGroup, False,
                                       pygame.sprite.collide_mask):
            print("collide detected")
        else:
            sGroup.add(s)
            screen.blit(p, c)
            pygame.draw.rect(screen, (255, 0, 0), s.rect, 1)

    pygame.display.update()
    return sGroup


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode(display_res, 0, 32)
    screen.fill((0, 0, 0))
    pygame.display.set_caption('slam')
    pygame.display.update()
    fpsclock = pygame.time.Clock()

    # for i in xrange(0, 20):
    # formatpic('shape_sample/%d.png' % (i + 1))

    loadres()
    # test()
    # test2()
    genBlockObjectsprite()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
