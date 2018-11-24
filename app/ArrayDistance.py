from dto.HelperDTOs import PublicFields
import numpy as np
from scipy.spatial.distance import cdist

class ArrayDistance():

    @staticmethod
    def closest_capsule(map, myPosition, side):
        if side == 0:
            field = map[:][:int(len(map[:][0])/2)]
        else:
            field = map[:][-17:]
        capsule_list = []
        field = np.array(field)
        for i in range(0, field.shape[0]):
            row = field[i]
            for j, obj in enumerate(row):
                if obj == PublicFields.CAPSULE:
                    capsule_list.append([i, j])
        print(myPosition)
        print(capsule_list)
        distances = [(myPosition[0]-capsule[0])**2 + (myPosition[1]-capsule[1])**2 for capsule in capsule_list]
        result = capsule_list[np.argmin(distances)]
        print('closest capsule: ', result)
        capsulePosition = result
        return capsulePosition
