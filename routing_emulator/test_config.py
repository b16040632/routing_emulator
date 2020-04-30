# -*- coding: utf-8 -*-
"""
:Project: routing_emulator
:File: test_config.py

:Author: Tanbixuan
:Created: 2020-04-20
"""


import random
import pymunk
from pymunk import pygame_util
from .water_current import SeaMap
from .floating_node import FloatingNode
from .algorithm import RoutingAlgorithm
from .trace_point import TracePoint
from math import sqrt
from routing_emulator import movable_node


class TestConfig(object):
    def __init__(self):

        pymunk.pygame_util.positive_y_is_up = False
        self.map_size = 1000
        self.recursive_speed = 0.1
        self.minimum_dis = 100
        self.sea_map = SeaMap(self.map_size)
        self.sea_map.draw_image()

        self.floating_node_space = pymunk.Space()
        self.floating_node_space.gravity = 0, 0
        self.floating_node_list = []
        self.floating_node_num = 15

        '''set random value of floating nodes' valocation, witch satisfied to gaussian distribute. '''
        rand_value_matrix = []
        for i in range(self.floating_node_num):
            while True:
                rerand_flag = False
                x = random.randrange(self.map_size / 10, self.map_size * 9 / 10)
                y = random.randrange(self.map_size / 10, self.map_size * 9 / 10)
                for point in rand_value_matrix:
                    if sqrt( (x - point[0]) ** 2 + (y - point[1]) ** 2) < self.minimum_dis:
                        rerand_flag = True
                        break
                if not rerand_flag:
                    break
            rand_value_matrix.append([x, y])
        for i in range(self.floating_node_num):
            self.floating_node_list.append(
                FloatingNode([0xE8, 0xFF, 0xFF],
                             self.map_size, rand_value_matrix[i],
                             self.floating_node_space,
                             self.sea_map)
            )
            self.floating_node_list[i].id = i
        for i in range(self.floating_node_num):
            self.floating_node_space.add(self.floating_node_list[i].static_body)
            self.floating_node_space.add(self.floating_node_list[i].node_body.body,
                                         self.floating_node_list[i].node_body)
            self.floating_node_list[i].update_callback()

        """ get and draw the hull """
        self.convex_hull_obj = RoutingAlgorithm(self)
        self.convex_hull_obj.get_convex_hulls()
        
        """ add movable node """
        ori_location_node_num = self.convex_hull_obj.hull.vertices[0]
        movable_node_ori_location = self.convex_hull_obj.node_list[ori_location_node_num]
        self.movable_node = movable_node.ConvexHullMovableNode(self, movable_node_ori_location)

        self.movable_node_space = pymunk.Space()
        self.movable_node_space.gravity = 0, 0
        self.movable_node_space.add(self.movable_node.node_body.body, self.movable_node.node_body)
        self.movable_node.update_callback()
        self.trace_point = TracePoint()
        self.trace_point_list = []

    def set_trace(self):
        x = self.movable_node.location[0][0] + 15
        y = self.movable_node.location[0][1] + 15
        self.trace_point_list.append([x, y])
