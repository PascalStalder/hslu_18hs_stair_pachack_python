from dto.HelperDTOs import Directions


class DirectionConverter:

    dictionary = {'North': [1, 0], 'East': [0, 1], 'South': [-1, 0], 'West': [0, -1]}

    @staticmethod
    def convert(direction: str):
        return DirectionConverter.dictionary[direction]

    @staticmethod
    def revert(direction_array):
        for key, value in DirectionConverter.dictionary.items():
            if value[0] == direction_array[0] and value[1] == direction_array[1]:
                return key
