class Dojo:
    '''This class creates rooms, adds people and randomly allocates people
       to the rooms'''

    rooms = []  # list of rooms in the Dojo
    people = []  # list of people in Dojo

    def __init__(self):
        
        self.room = []
        self.people = []

    def create_room(self, room_type, room_name):
        """Create a new room in Dojo"""
        try:
            if not isinstance(room_type, str) or not \
                    isinstance(room_name, str):
                raise ValueError('Room name and type must be a string and ' +
                                 'not an integer or float!')
            elif room_type.lower() not in ('livingspace', 'office'):
                raise ValueError('Room type is incorrect. Must be office or ' +
                                 'livingspace!')
            elif not room_name.isalpha():
                raise ValueError('Room name cannot be empty or have special ' +
                                 'characters.\n{} is not a valid name!\n'
                                 .format(room_name))
            if self.room_exists(room_name):
                raise ValueError('Room with name {} already exists!'.format(
                    room_name))
            elif room_type == 'office':
                return self.create_office(room_name)
            elif room_type == 'livingspace':
                return self.create_livingspace(room_name)
        except Exception:
            raise

    def room_exists(self, name):
        '''Check that a room with the specified name exists'''
        if self.rooms:
            for room in self.rooms:
                if name == room['name']:
                    return room
        return None