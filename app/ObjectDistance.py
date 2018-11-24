from dto.HelperDTOs import PublicFields
import numpy as np


class ObjectDistance():
    def __init__(self, field, side):
        self.field = field
        self.side = side
        self.half_field = int(np.array(self.field).shape[1] / 2)


    def get_object_list(self, target):
        enemy_field = np.array(self.field)

        if self.side == 1:
            enemy_field = enemy_field[:, :self.half_field]
        else:
            enemy_field = enemy_field[:, -self.half_field:]
        capsule_list = []
        for i in range(0, enemy_field.shape[0]):
            row = enemy_field[i]
            for j, obj in enumerate(row):
                if obj == target:
                    if self.side == 0:
                        j += self.half_field
                    capsule_list.append([i, j])
        return capsule_list

    def closest_object(self, myPosition, target):
        object_position = None
        object_list = self.get_object_list(target)
        if self.object_available(target):
            distances = [(myPosition[0] - capsule[0]) ** 2 + (myPosition[1] - capsule[1]) ** 2 for capsule in
                         object_list]
            result = object_list[np.argmin(distances)]
            object_position = result

        return object_position

    def object_available(self, target):
        if len(self.get_object_list(target)) == 0:
            return False
        else:
            return True
