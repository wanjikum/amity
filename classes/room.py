class Room(object):
    """A class Room which is the blue print of class office and livingspace.

    Attributes:
        room_names: A string that contains the room names.
        room_type: The room type as a string.
    """

    def __init__(self, room_type, room_names=[]):
        """Class room constructor"""
        self.room_type = room_type
        self.room_names = room_names


class Office(Room):
    """A class Staff that inherits from class room"""
    def __init__(self, room_type, room_names):
        Room.__init__(self, room_type, room_names)
        self.room_capacity = 6
        self.room_type = "office"


class LivingSpace(Room):
    """A class Fellow that inherit from class room"""
    def __init__(self, room_type, room_names, accommodate="no"):
        Room.__init__(self, room_type, room_names)
        self.room_type = "living_space"
        self.room_capacity = 4
        self.accommodate = accommodate
