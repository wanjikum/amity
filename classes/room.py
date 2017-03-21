class Room(object):
    """A class Room which is the blue print of class office and livingspace.

    Attributes:
        room_name: A string that contains the room's name.
        room_type: The room type as a string.
    """

    def __init__(self, room_name, room_type):
        """Class room constructor"""
        self.room_name = room_name
        self.room_type = room_type


class Office(Room):
    """A class Staff that inherits from class room"""
    def __init__(self, room_name, room_type):
        Room.__init__(self, room_name, room_type)
        self.room_capacity = 6
        self.room_type = "office"


class LivingSpace(Room):
    """A class Fellow that inherit from class room"""
    def __init__(self, room_name, room_type="living_space", accommodate='no'):
        Room.__init__(self, room_name, room_type)
        self.room_capacity = 4
        self.accommodate = accommodate
