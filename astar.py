#!/usr/bin/env python
#-*- coding:utf-8 -*-
#       FileName:  astar.py
#
#    Description:
#
#        Version:  1.0
#        Created:  2018-06-19 09:47:15
#  Last Modified:  2018-06-21 13:39:49
#       Revision:  none
#       Compiler:  gcc
#
#         Author:  zt ()
#   Organization:

import sys

_2dmap = []
start = None
end = None
open_list = {}
close_list = {}
map_border = ()


class Node:
    def __init__(this, father, x, y):
        if x < 0 or x >= map_border[0] or y < 0 or y >= map_border[1]:
            raise Exception("node position can't beyond the border!")

        this.father = father

        this.x = x
        this.y = y

        if father != None:
            G2father = calc_G(father, this)
            if not G2father:
                raise Exception("father is not valid!")
            this.G = G2father + father.G
            this.H = calc_H(this, end)
            this.F = this.G + this.H
        else:
            this.G = 0
            this.H = 0
            this.F = 0

    def reset_father(this, father, new_G):
        if father != None:
            this.G = new_G
            this.F = this.G + this.H

        this.father = father


def calc_G(node1, node2):
    x1 = abs(node1.x - node2.x)
    y1 = abs(node1.y - node2.y)
    if (x1 == 1 and y1 == 0):
        return 10  # same row
    if (x1 == 0 and y1 == 1):
        return 10  # same col
    if (x1 == 1 and y1 == 1):
        return 14  # cross
    else:
        return 0


def calc_H(cur, end):
    return abs(end.x - cur.x) + abs(end.y - cur.y)


def min_F_node():
    if len(open_list) == 0:
        raise Exception("not exist path!")

    k = sorted(open_list.items(), key=lambda x: x[1], reverse=False)[0]
    return open_list[k[0]]


# 把相邻节点加入open list, 如果发现终点说明找到了路径
def addAdjacentIntoOpen(node):
    # 将该节点从开放列表移到关闭列表当中。
    open_list.pop((node.x, node.y))
    close_list[(node.x, node.y)] = node

    _adjacent = []
    # 相邻节点还没有注意边界的情况
    try:
        _adjacent.append(Node(node, node.x - 1, node.y - 1))
    except Exception, e:
        pass

    try:
        _adjacent.append(Node(node, node.x, node.y - 1))
    except Exception, e:
        pass

    try:
        _adjacent.append(Node(node, node.x + 1, node.y - 1))
    except Exception, e:
        pass

    try:
        _adjacent.append(Node(node, node.x + 1, node.y))
    except Exception, e:
        pass

    try:
        _adjacent.append(Node(node, node.x + 1, node.y + 1))
    except Exception, e:
        pass

    try:
        _adjacent.append(Node(node, node.x, node.y + 1))
    except Exception, e:
        pass

    try:
        _adjacent.append(Node(node, node.x - 1, node.y + 1))
    except Exception, e:
        pass

    try:
        _adjacent.append(Node(node, node.x - 1, node.y))
    except Exception, e:
        pass

    for a in _adjacent:
        if (a.x, a.y) == (end.x, end.y):
            new_G = calc_G(a, node) + node.G
            end.reset_father(node, new_G)
            print "find path finish!"
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
    try:
        while not addAdjacentIntoOpen(the_node):
            the_node = min_F_node()
    except Exception, e:
        print e
        return False

    return True


#=======================================================================
def print_map():
    print '    Y',
    for i in xrange(len(_2dmap)):
        print i,
    print
    print '  X'
    row = 0
    for l in _2dmap:
        print '%3d' % row, ' ',
        row = row + 1
        for i in l:
            print i,
        print


def mark_path(node):
    if node.father == None:
        return

    _2dmap[node.x][node.y] = '#'
    mark_path(node.father)


def preset_map():
    global start, end, map_border
    _2dmap.append('S X . . . . X. . . . . . . . . X . . . .'.split())
    _2dmap.append('. X . . . . X . . . . . . . . X . . . .'.split())
    _2dmap.append('. X . . . . X X . . . . . . . X . . . .'.split())
    _2dmap.append('. . . . . . . X . . . . . . . X . . . .'.split())
    _2dmap.append('. . . . . . . . . X . . . . . X . . . .'.split())
    _2dmap.append('. . . . . . . . . X . . . . . . . . . .'.split())
    _2dmap.append('. . . . . . . . . X . . . . . X X X X .'.split())
    _2dmap.append('. . . . . . . . . X . . . . . X . . . .'.split())
    _2dmap.append('. . . . . . . . . X . . . . . X . X X X'.split())
    _2dmap.append('. . . . . . . . . . X . . . . X . X . .'.split())
    _2dmap.append('. . . . . . . . . . . . . . . X . X . E'.split())
    _2dmap.append('. . . . . . . . . . . . . . . X . X . .'.split())
    _2dmap.append('. . . . . . . . . . . . . . . X . X . .'.split())
    _2dmap.append('. . . . . . . . . . . . . . . X . X . .'.split())
    _2dmap.append('. . . . . . . . . . . . . . . X . X . .'.split())
    _2dmap.append('. . . . . . . . . . . . . . . X . . X .'.split())
    map_border = (len(_2dmap), len(_2dmap[0]))

    row_index = 0
    for row in _2dmap:
        col_index = 0
        for n in row:
            if n == 'X':
                block_node = Node(None, row_index, col_index)
                close_list[(block_node.x, block_node.y)] = block_node
            elif n == 'S':
                start = Node(None, row_index, col_index)
            elif n == 'E':
                end = Node(None, row_index, col_index)
            col_index = col_index + 1
        row_index = row_index + 1


if __name__ == '__main__':
    # if len(sys.argv) < 3:
        # preset_map()
    # else:
        # x = int(sys.argv[1])
        # y = int(sys.argv[2])
        # map_border = (x, y)

        # _start = raw_input('pls input start point:')
        # _end = raw_input('pls input end point:')
        # _start = _start.split(',')
        # _end = _end.split(',')
        # _start = (int(_start[0]), int(_start[1]))
        # _end = (int(_end[0]), int(_end[1]))
        # start = Node(None, _start[0], _start[1])
        # end = Node(None, _end[0], _end[1])
        # # gen map
        # _2dmap = [['.' for i in xrange(y)] for i in xrange(x)]
        # # put start and end
        # _2dmap[_start[0]][_start[1]] = 'S'
        # _2dmap[_end[0]][_end[1]] = 'E'
        # # input blocks
        # while True:
            # _block = raw_input('input block:')
            # if not _block:
                # break

            # _block = _block.split(',')
            # _block = (int(_block[0]), int(_block[1]))
            # _2dmap[_block[0]][_block[1]] = 'X'
            # block_node = Node(None, _block[0], _block[1])
            # close_list[(block_node.x, block_node.y)] = block_node

    preset_map()
    print "orignal map:"
    print_map()

    if find_the_path(start, end):
        mark_path(end.father)
        print "found road as follow:"
        print_map()
