from dto.HelperDTOs import PublicFields
import numpy as np
from scipy.spatial.distance import cdist

class ArrayDistance():

    @staticmethod
    def closest_capsule(map, myPosition, side):

        if side == 0:
            field = map[:, 17]
        else:
            field = map[:,-17:]

        for i, row in enumerate(field):
            for j,obj in enumerate(row):
                if obj == PublicFields.CAPSULE:
                    capsule_list = list.append([i,j])

        result = np.min(cdist(myPosition, np.array(capsule_list)))



        capsulePosition = result
        return capsulePosition
