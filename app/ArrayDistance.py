from dto.HelperDTOs import PublicFields
import numpy as np
from scipy.spatial.distance import cdist

class ArrayDistance():

    @staticmethod
    def distance(self, map, myPosition):

        for i, row in enumerate(map):
            for j,obj in enumerate(row):
                if obj == PublicFields.CAPSULE:
                    capsule_list = list.append([i,j])

        result = np.min(cdist(myPosition, capsule_list))



        capsulePosition = result
        return capsulePosition
