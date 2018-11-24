import numpy as np

from AStar import AStar
from DirectionsConverter import DirectionConverter
from dto.ReturnDirections import ReturnDirections
from app.dto.PublicPlayer import PublicPlayer
from dto.HelperDTOs import PublicFields
from dto.HelperDTOs import Directions
from multiprocessing.pool import Pool


class Play:

    def __init__(self, side, field: np.ndarray, my_player, enemy):
        self.side = side
        self.me = my_player
        self.enemy = enemy
        self.field = field
        print(self.field)

    def take_turn(self):
        next_field = self.next_field(self.me.position, self.me.direction)
        direction = self.me.direction
        if next_field == PublicFields.WALL:
            direction = Directions.RIGHT[direction]

        return "\"" + direction + "\""

    def next_field(self, position, direction):
        direction_array = DirectionConverter.convert(direction)
        next_field = self.field[int(position[0]) + direction_array[0]][int(position[1]) + direction_array[1]]
        return next_field

    def deepsearch(self, obj):
        found_object = False
        start_position = self.me.position
        start_direction = self.me.direction
        position = start_position
        direction = start_direction
        steps = 0
        best_steps = None
        a_star = AStar()
        enemy_avoid = not self.enemy.weakend
        a_star.astar(self.map_to_binaray(enemy_avoid), self.me.position, ArrayDistance.closetCapsule())

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
        return binary_field
