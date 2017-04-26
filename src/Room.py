class Room:
    max_space = None
    room_type = None
    occupants = []

    def set_max_space(self, value):
        if isinstance(value, int):
            self.max_space = value
        else:
            raise ValueError('max space value can only be an integer')


class Office(Room):

    def __init__(self, name):
        self.name = name
        self.room_type = 'office'
        self.max_space = 6
        self.occupants = []


class LivingSpace(Room):

    def __init__(self, name):
        self.name = name
        self.room_type = 'livingspace'
        self.max_space = 4
        self.occupants = []