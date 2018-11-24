from dto.HelperDTOs import PublicFields
import numpy as np


class ArrayDistance():
    def __init__(self, map, side):
        self.map = map
        self.side = side


    def getCapsuleList(self):
        if self.side == 0:
            field = self.map[:][:int(len(map[:][0]) / 2)]
        else:
            field = self.map[:][-17:]
        capsule_list = []
        field = np.array(field)
        for i in range(0, field.shape[0]):
            row = field[i]
            for j, obj in enumerate(row):
                if obj == PublicFields.CAPSULE:
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
