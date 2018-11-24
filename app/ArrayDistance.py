from dto.HelperDTOs import PublicFields
import numpy as np
from scipy.spatial.distance import cdist

class ArrayDistance():

    @staticmethod
    def clostst_capsule(map, myPosition):

        for i, row in enumerate(map):
            for j,obj in enumerate(row):
                if obj == PublicFields.CAPSULE:
                    capsule_list = list.append([i,j])

        result = np.min(cdist(myPosition, np.array(capsule_list)))



        capsulePosition = result
        return capsulePosition
