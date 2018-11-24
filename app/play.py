from copy import copy

import numpy as np
import pandas as pd

from AStar import AStar
from ObjectDistance import ObjectDistance
from DirectionsConverter import DirectionConverter
from dto.HelperDTOs import PublicFields
from dto.HelperDTOs import Directions
from dto.PublicPlayer import PublicPlayer


class Play:

    candy_in_pocket_enemy = 0
    candy_in_pocket_self = 0
    score = 0
    last_field = None
    my_last_pos = [0, 0]
    enemy_last_pos = [0, 0]

    def __init__(self, side, field: np.ndarray, my_player, enemy):
        self.side = side
        self.me = my_player
        self.enemy: PublicPlayer = enemy
        self.field = field
        self.a_star = AStar()
        self.obj_dist = ObjectDistance(self.field, self.side)
        self.defence_line = self.get_defenceline()

    def take_turn(self):
        direction = self.me.direction
        path = self.deepsearch()
        if path:
            direction = DirectionConverter.revert(self.direction_to_field(path[-1]))
        if path != False and len(path) == 0:
            direction = Directions.STOP

        return "\"" + direction + "\""

    def next_field(self, position, direction):
        direction_array = DirectionConverter.convert(direction)
        next_field = self.field[int(position[0]) + direction_array[0]][int(position[1]) + direction_array[1]]
        return next_field

    def deepsearch(self):
        self.distribute_points()
        print(Play.candy_in_pocket_self)
        print(Play.candy_in_pocket_enemy)

        enemy_avoid = not self.enemy_on_our_side() and not self.enemy.weakened and not self.me.weakened
        # if self.enemy.weakened and not self.enemy_on_our_side():
        #     goal = self.enemy.position
        # # if Capsule available
        # elif self.obj_dist.object_available(PublicFields.CAPSULE):
        #     goal = self.obj_dist.closest_object(self.me.position, PublicFields.CAPSULE)
        # # if behind in points
        # elif Play.score < 0 and self.candy_in_pocket_self < 3 and self.obj_dist.object_available(PublicFields.FOOD):
        #     goal = self.obj_dist.closest_object(self.me.position, PublicFields.FOOD)
        #
        # # if in front and enemy on our side
        # elif self.enemy_on_our_side():
        #     goal = [self]
        # else:
        #     goal = [self.me.position[0], int(len(self.field[0])/2)+self.side]
        if not self.obj_dist.object_available(PublicFields.FOOD):
            direction = self.me.position[0] - self.enemy.position[0]
            vertical_pos = copy(self.me.position[0])
            vertical_pos = self.correct_vertical(vertical_pos, direction)
            goal = [vertical_pos, self.defence_line]
        elif self.me.weakened and self.obj_dist.object_available(PublicFields.CAPSULE):
            goal = self.obj_dist.closest_object(self.me.position, PublicFields.CAPSULE)
        elif Play.candy_in_pocket_self > 0:
            direction = self.enemy.position[0] - self.me.position[0]
            vertical_pos = copy(self.enemy.position[0])
            vertical_pos = self.correct_vertical(vertical_pos, direction)
            goal = [vertical_pos, self.defence_line]
        elif Play.score <= 0:
            goal = self.obj_dist.closest_object(self.me.position, PublicFields.FOOD)
        elif self.me.weakened:
            goal = self.obj_dist.closest_object(self.me.position, PublicFields.FOOD)
        else:
            direction = self.enemy.position[0] - self.me.position[0]
            vertical_pos = copy(self.enemy.position[0])
            vertical_pos = self.correct_vertical(vertical_pos, direction)
            goal = [vertical_pos, self.defence_line]

        path = self.a_star.astar(self.map_to_binaray(enemy_avoid), tuple(self.me.position), tuple(goal))
        Play.enemy_last_pos = self.enemy.position
        Play.my_last_pos = self.me.position
        Play.last_field = self.field
        return path

    def correct_vertical(self, vertical_pos, direction):
        while self.field[vertical_pos][self.defence_line] == PublicFields.WALL:
            if direction > 0:
                vertical_pos += 1
            else:
                vertical_pos -= 1
            if vertical_pos >= np.array(self.field).shape[0] - 2:
                vertical_pos -= 2
                direction *= -1
            if vertical_pos <= 0:
                vertical_pos += 2
                direction *= -1
        return vertical_pos

    def map_to_binaray(self, enemy_avoid: bool):
        binary_field = []
        for row in self.field:
            binary_row = []
            for field in row:
                if field == PublicFields.WALL:
                    binary_row.append(1)
                else:
                    binary_row.append(0)
            binary_field.append(binary_row)
        if enemy_avoid:
            binary_field[self.enemy.position[0]][self.enemy.position[1]] = 1
        return np.array(binary_field)

    def direction_to_field(self, field):
        direction = [0, 0]
        direction[0] = (field[0] - self.me.position[0])
        direction[1] = (field[1] - self.me.position[1])
        return direction

    def enemy_on_our_side(self):
        if self.side == 1:
            result = self.enemy.position[1] > len(self.field[1])/2
        else:
            result = self.enemy.position[1] < (len(self.field[1])/2)-1
        return result

    def me_on_enemy_side(self):
        if self.side == 0:
            result = self.me.position[1] > (len(self.field[1])/2)-1
        else:
            result = self.me.position[1] < len(self.field[1])/2
        return result

    def get_defenceline(self):
        field_width = np.array(self.field).shape[1]
        if self.side == 1:
            defence_line = int(field_width/2)
        else:
            defence_line = int(field_width/2)-1
        return defence_line

    def distribute_points(self):
        if Play.last_field:
            my_place = Play.last_field[self.me.position[0]][self.me.position[1]]
            print(my_place)
            if my_place == PublicFields.FOOD and self.me_on_enemy_side():
                print('Stepped on some Food')
                Play.candy_in_pocket_self += 1
            if Play.last_field[self.enemy.position[0]][self.enemy.position[1]] == PublicFields.FOOD and self.enemy_on_our_side():
                Play.candy_in_pocket_enemy += 1
            enemy_displacement = self.enemy.position[0] - Play.enemy_last_pos[0] + self.enemy.position[1] - Play.enemy_last_pos[1]
            if enemy_displacement > 1 or enemy_displacement < -1:
                Play.candy_in_pocket_enemy = 0
            me_displacement = self.me.position[0] - Play.my_last_pos[0] + self.me.position[1] - Play.my_last_pos[1]
            if me_displacement > 1 or me_displacement < -1:
                Play.candy_in_pocket_self = 0
            if not self.enemy_on_our_side():
                Play.score -= Play.candy_in_pocket_enemy
                Play.candy_in_pocket_enemy = 0
            if not self.me_on_enemy_side():
                Play.score += Play.candy_in_pocket_self
                Play.candy_in_pocket_self = 0
