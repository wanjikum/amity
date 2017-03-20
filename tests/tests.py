from unittest import TestCase
from classes.room import Office, LivingSpace
from classes.amity import Amity


class CreateRoomTestCases(unittest.TestCase):
    """A class CreateRoom that has a collection of create_room testcases"""
    def setUp(self):
        """Keeps our code dry"""
        self.room = Room()
        self.office = Office()
        self.living_space = LivingSpace()

    def tearDown(self):
        """"""
        del self.room
        del self.office
        del self.living_space

    def test_office_and_living_space_is_instance_of_room(self):
        """Tests if office and living space are instances of class Room"""
        self.assertTrue(isinstance(self.office, Room))
        self.assertTrue(isinstance(self.living_space, Room))
