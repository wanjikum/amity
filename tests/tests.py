import unittest
from classes.room import Room, Office, LivingSpace
from classes.person import Person, Fellow, Staff
from classes.amity import Amity


class CreateRoomTestCases(unittest.TestCase):
    """A class CreateRoom that has a collection of create_room testcases"""
    def setUp(self):
        """Keeps our code dry"""
        self.room = Room()
        self.office = Office()
        self.living_space = LivingSpace()

    def tearDown(self):
        del self.room
        del self.office
        del self.living_space

    def test_if_office_and_living_space_is_instance_of_class_room(self):
        """Tests if office and living space are instances of class Room"""
        self.assertTrue(isinstance(self.office, Room))
        self.assertTrue(isinstance(self.living_space, Room))


class AddPersonTestCases(unittest.TestCase):
    """A class CreateRoom that has a collection of create_room testcases"""
    def setUp(self):
        """Keeps our code dry"""
        self.person = Person()
        self.fellow = Fellow("Jamhuri Linnet", "yes")
        self.staff = Staff("Oliver")

    def tearDown(self):
        del self.person
        del self.fellow
        del self.staff

    def test_if_fellow_and_staff_is_instance_of_class_person(self):
        """Tests if fellow and staff are instances of class Person"""
        self.assertTrue(isinstance(self.fellow, Person))
        self.assertTrue(isinstance(self.staff, Person))

    def test_if_the_class_fellow_takes_in_correct_attributes(self):
        """Tests if class fellow takes in the attributes given"""
        self.assertListEquals(["Jamhuri Linnet", "yes"],
                              [self.fellow.person_name,
                               self.fellow.accommodate])

    def test_class_staff_takes_in_correct_attributes(self):
        """Tests if class staff takes in the attributes given"""
        self.assertEqual("Oliver", self.staff.person_name)
