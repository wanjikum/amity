import unittest
from classes.room import Room, Office, LivingSpace
from classes.person import Person, Fellow, Staff
from classes.amity import Amity


class CreateRoomTestCases(unittest.TestCase):
    """A class CreateRoom that has a collection of create_room testcases"""
    def setUp(self):
        """Keeps our code dry"""
        self.amity = Amity()
        self.office = Office("office", "Tsavo")
        self.living_space = LivingSpace("livingspace", "Tsavo")

    def tearDown(self):
        del self.office
        del self.living_space

    def test_if_office_and_living_space_is_instance_of_class_room(self):
        """Tests if office and living space are instances of class Room"""
        self.assertTrue(isinstance(self.office, Room))
        self.assertTrue(isinstance(self.living_space, Room))

    def test_if_the_class_livingSpace_takes_in_correct_attributes(self):
        """Tests if class LivingSpace takes in correct attributes given"""
        self.assertListEqual(["Tsavo", "living_space", 4, "no"],
                             [self.living_space.room_names,
                              self.living_space.room_type,
                              self.living_space.room_capacity,
                              self.living_space.accommodate])

    def test_if_the_class_office_takes_in_correct_attributes(self):
        """Tests if class Office takes in correct attributes given"""
        self.assertListEqual(["Tsavo", "office", 6],
                             [self.office.room_names,
                              self.office.room_type,
                              self.office.room_capacity])

    def test_create_room_type_office_successfully(self):
        """Test create a room_type office successfully"""
        office_intial_count = len(self.amity.offices)
        bootcamp = self.amity.create_room("office", ["Bootcamp"])
        self.assertEqual(len(self.amity.offices), office_intial_count+1)

    def test_create_room_type_living_space_successfully(self):
        """Test create room_type living_space successfully"""
        bootcamp = self.amity.create_room("living_space", ["Bootcamp"])
        self.assertEqual(bootcamp,
                         "LivingSpace Bootcamp has been successfully created!")

    def test_create_multiple_rooms_of_type_office_successfully(self):
        """Test create multiple rooms of type office successfully"""
        likoni_tsavo = self.amity.create_room("office", ["likoni", "tsavo"])
        self.assertListEqual([likoni_tsavo],
                             ["Office likoni has been successfully created!",
                              "Office tsavo has been successfully created!"])

    def test_create_multiple_rooms_of_type_livingspace_successfully(self):
        """Test create multiple rooms of type livingspace successfully"""
        kigali_nairobi = self.amity.create_room("living_space",
                                                ["kigali", "nairobi"])
        self.assertListEqual([kigali_nairobi],
                             ["LivingSpace kigali has been" +
                              " successfully created!",
                              "LivingSpace nairobi has been" +
                              "successfully created!"])

    def test_duplicate_room(self):
        """Test an existing room is not recreated"""
        kigali_kigali = self.amity.create_room("living_space",
                                               ["kigali", "kigali"])
        self.assertListEqual([kigali_kigali],
                             ["LivingSpace kigali has been" +
                              " successfully created!",
                              "LivingSpace kigali already exists!"])

    def test_invalid_room_type(self):
        """Test create invalid room type """
        kitchen = self.amity.create_room("kitchen", ["hog_centre"])
        self.assertEqual(kitchen, "Invalid room type. A room can either be of "
                         + "type office or living_space")


class AddPersonTestCases(unittest.TestCase):
    """A class CreateRoom that has a collection of create_room testcases"""
    def setUp(self):
        """Keeps our code dry"""
        self.fellow = Fellow("Jamhuri Linnet")
        self.staff = Staff("Oliver")

    def tearDown(self):
        del self.fellow
        del self.staff

    def test_if_fellow_and_staff_is_instance_of_class_person(self):
        """Tests if fellow and staff are instances of class Person"""
        self.assertTrue(isinstance(self.fellow, Person))
        self.assertTrue(isinstance(self.staff, Person))

    def test_if_the_class_fellow_takes_in_correct_attributes(self):
        """Tests if class fellow takes in the attributes given"""
        self.assertListEqual(["Jamhuri Linnet", "fellow", "no"],
                             [self.fellow.person_name,
                              self.fellow.person_type,
                              self.fellow.accommodate])

    def test_class_staff_takes_in_correct_attributes(self):
        """Tests if class staff takes in the attributes given"""
        self.assertListEqual(["Oliver", "staff"],
                             [self.staff.person_name,
                              self.staff.person_type])
