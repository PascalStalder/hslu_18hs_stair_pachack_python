import numpy as np
import pandas as pd

from AStar import AStar
from ArrayDistance import ArrayDistance
from DirectionsConverter import DirectionConverter
from dto.HelperDTOs import PublicFields
from dto.HelperDTOs import Directions
from dto.PublicPlayer import PublicPlayer


class Play:

    candy_in_pocket_enemy = 0
    candy_in_pocket_self = 0
    score = 0

    def __init__(self, side, field: np.ndarray, my_player, enemy):
        self.side = side
        self.me = my_player
        self.enemy: PublicPlayer = enemy
        self.field = field
        self.a_star = AStar()
        self.array_dist = ArrayDistance(self.field, self.side)

    def take_turn(self):
        direction = self.me.direction
        path = self.deepsearch()
        if path:
            direction = DirectionConverter.revert(self.direction_to_field(path[-1]))

        return "\"" + direction + "\""

    def next_field(self, position, direction):
        direction_array = DirectionConverter.convert(direction)
        next_field = self.field[int(position[0]) + direction_array[0]][int(position[1]) + direction_array[1]]
        return next_field

    def deepsearch(self):
        enemy_avoid = not self.enemy_on_our_side() and not self.enemy.weakened
        if self.enemy.weakened:
            goal = self.enemy.position
        elif self.array_dist.capsule_available():
            goal = self.array_dist.closest_capsule(self.me.position)

        elif Play.score < 0 and self.candy_in_pocket_self < 3
            goal = self.nearest_candy()
        else:
            goal = [self.me.position[0], int(len(self.field[0])/2)+self.side]

        path = self.a_star.astar(self.map_to_binaray(enemy_avoid), tuple(self.me.position), tuple(goal))
        print('path = ', path)
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
            binary_field[self.enemy.position[0]][self.enemy.position[1]] = 1
        return np.array(binary_field)

    def direction_to_field(self, field):
        direction = [0, 0]
        direction[0] = (field[0] - self.me.position[0])
        direction[1] = (field[1] - self.me.position[1])
        return direction

    def enemy_on_our_side(self):
        result = None
        if self.side == 1:
            result = self.enemy.position[1] > len(self.field[1])/2
        else:
            result = self.enemy.position[1] < len(self.field[1])/2
        return result
