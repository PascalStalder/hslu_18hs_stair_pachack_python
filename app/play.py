import numpy as np
import pandas as pd

from AStar import AStar
from ArrayDistance import ArrayDistance
from DirectionsConverter import DirectionConverter
from dto.HelperDTOs import PublicFields
from dto.HelperDTOs import Directions
from dto.PublicPlayer import PublicPlayer


class Play:

    def __init__(self, side, field: np.ndarray, my_player, enemy):
        self.side = side
        self.me = my_player
        self.enemy: PublicPlayer = enemy
        self.field = field
        print(self.field)

    def take_turn(self):
        next_field = self.next_field(self.me.position, self.me.direction)
        direction = self.me.direction
        if self.enemy.activeCapsule()

        if capsule_available:
            move_to_position = self.deepsearch()[-1]
        print(move_to_position)
        direction = DirectionConverter.revert(self.direction_to_field(move_to_position))

        return "\"" + direction + "\""

    def next_field(self, position, direction):
        direction_array = DirectionConverter.convert(direction)
        next_field = self.field[int(position[0]) + direction_array[0]][int(position[1]) + direction_array[1]]
        return next_field

    def deepsearch(self):
        a_star = AStar()
        enemy_avoid = not (self.enemy_on_our_side())
        goal = ArrayDistance.closest_capsule(self.field, self.me.position, self.side)
        path = a_star.astar(self.map_to_binaray(enemy_avoid), (self.me.position[0], self.me.position[1]), (goal[0],goal[1]))
        return path

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
            print(np.array(binary_field).shape)
            print(self.enemy.position)
            binary_field[self.enemy.position[0]][self.enemy.position[1]] = 1
        return np.array(binary_field)

    def direction_to_field(self, field):
        direction = [0, 0]
        direction[0] = (field[0] - self.me.position[0])
        direction[1] = (field[1] - self.me.position[1])
        return direction

    def enemy_on_our_side(self):
        if self.side == 0:
            return self.enemy.position[1] > len(self.field[1])/2
        else:
            return self.enemy.position[1] < len(self.field[1])/2
