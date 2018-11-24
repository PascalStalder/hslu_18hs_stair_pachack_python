from dto.HelperDTOs import PublicFields
import numpy as np


class ArrayDistance():
    def __init__(self, field, side):
        self.field = field
        self.side = side
        self.half_field = int(np.array(self.field).shape[1] / 2)

    def getCapsuleList(self):
        enemy_field = np.array(self.field)

        if self.side == 1:
            enemy_field = enemy_field[:, :self.half_field]
        else:
            enemy_field = enemy_field[:, -self.half_field:]
        print("field shape: ", np.array(enemy_field).shape)
        capsule_list = []
        for i in range(0, enemy_field.shape[0]):
            row = enemy_field[i]
            for j, obj in enumerate(row):
                if obj == PublicFields.CAPSULE:
                    if self.side == 0:
                        j += self.half_field
                    capsule_list.append([i, j])
        return capsule_list

    def closest_capsule(self, myPosition):
        capsulePosition = None
        capsule_list = self.getCapsuleList()
        if self.capsule_available():
            distances = [(myPosition[0] - capsule[0]) ** 2 + (myPosition[1] - capsule[1]) ** 2 for capsule in
                         capsule_list]
            result = capsule_list[np.argmin(distances)]
            print('closest capsule: ', result)
            capsulePosition = result
            print(myPosition)
            print(capsule_list)

        return capsulePosition


    def capsule_available(self):
        if len(self.getCapsuleList()) == 0:
            return False
        else:
            return True
