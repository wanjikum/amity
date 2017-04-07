class Room(object):
    """A class Room which is the blue print of class office and livingspace.

    Attributes:
        room_names: A string that contains the room names.
        room_type: The room type as a string.
    """
    def __init__(self, room_name):
        """Class room constructor"""
        self.room_type = None
        self.room_name = room_name


class Office(Room):
    """A class Staff that inherits from class room"""
    def __init__(self, room_name):
        Room.__init__(self, room_name)
        self.room_capacity = 6
        self.room_type = "office"


class LivingSpace(Room):
    """A class Fellow that inherit from class room"""
    def __init__(self, room_name):
        Room.__init__(self, room_name)
        self.room_type = "living_space"
        self.room_capacity = 4
