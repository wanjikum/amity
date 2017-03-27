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
        del self.amity

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
        bootcamp = self.amity.create_room("office", "Bootcamp")
        self.assertEqual(len(self.amity.offices), office_intial_count+1)

    def test_create_room_type_living_space_successfully(self):
        """Test create room_type living_space successfully"""
        bootcamp = self.amity.create_room("living_space", "Bootcamp")
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
        kitchen = self.amity.create_room("kitchen", "hog_centre")
        self.assertEqual(kitchen, "Invalid room type. A room can either be of "
                         + "type office or living_space")


class AddPersonTestCases(unittest.TestCase):
    """A class CreateRoom that has a collection of create_room testcases"""
    def setUp(self):
        """Keeps our code dry"""
        self.amity = Amity()
        self.fellow = Fellow("Jamhuri Linnet")
        self.staff = Staff("Oliver")

    def tearDown(self):
        del self.fellow
        del self.staff
        del self.amity

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

    def test_add_staff_successfully(self):
        """Test add staff successfully"""
        kigali = self.amity.create_room("office", "kigali")
        felistas = self.amity.add_person("felistas", "staff", "no")
        self.assertListEqual([felistas],
                             ["felistas has been successfully created!",
                              "felistas has been allocated to the " +
                              "office kigali"])

    def test_add_staff_successfully_who_requires_accommodation(self):
        """Test reject accommodation for staff"""
        kigali = self.amity.create_room("office", "kigali")
        kisumu = self.amity.create_room("living_space", "kisumu")
        felistas = self.amity.add_person("felistas", "staff", "yes")
        self.assertListEqual([felistas],
                             ["felistas has been successfully created!",
                              "felistas has been allocated to the " +
                              "office kigali",
                              "You can't be accommodated since you are a" +
                              "staff member"])

    def test_add_fellow_successfully_who_requires_accomodation(self):
        """Adds fellow successfully and is allocated room and livingspace"""
        kigali = self.amity.create_room("office", "kigali")
        mombasa = self.amity.create_room("living_space", "mombasa")
        larry = self.amity.add_person("larry", "fellow", "yes")
        self.assertListEqual([larry],
                             ["larry has been successfully added",
                              "larry has been allocated to the office kigali",
                              "larry has been allocated to the " +
                              "livingspace mombasa"])

    def test_add_fellow_successfully_who_does_not_require_accomodation(self):
        """Adds fellow successfully and is allocated room only"""
        kigali = self.amity.create_room("office", "kigali")
        larry = self.amity.add_person("larry", "fellow", "no")
        self.assertListEqual([larry],
                             ["larry has been successfully added",
                              "larry has been allocated to the office kigali"])

    def test_reject_invalid_role(self):
        """Rejects adding a person whose person type is not fellow/staff"""
        alex = self.amity.add_person("alex", "techie", "no")
        self.assertEqual(alex,
                         "Invalid role. You can either be a fellow/staff.")

    def test_if_it_accepts_string_only_in_person_name(self):
        """Tests if it rejects names with numbers"""
        tina = self.amity.add_person("ti67ji", "staff", "no")
        self.assertEqual(tina, "Invalid name. Use letters only")

    def test_if_it_accepts_a_registered_user(self):
        """Tests if it rejects a registered user"""
        george = self.amity.add_person("george kiarie", "fellow", "no")
        george_kiarie = self.amity.add_person("george kiarie", "fellow", "no")
        self.assertEqual(george_kiarie,
                         "The person already exists!")


class ReallocatePersonTestCases(unittest.TestCase):
    """A collection of create_room testcases"""
    def setUp(self):
        """Keeps our code dry"""
        self.amity = Amity()
        kakamega = self.amity.create_room("office", "kakamega")
        charity = self.amity.add_person("charity", "staff", "no")
        kisii = self.amity.create_room("office", "kisii")
        kiambu = self.amity.create_room("living_space", "kiambu")

    def tearDown(self):
        del self.amity

    def test_reallocate_a_person_successfully(self):
        """Tests if a person is successfully reallocated"""
        charity_kisii = self.amity.reallocate_person("1", "kisii")
        self.assertEqual(charity_kisii,
                         "charity has been reallocated from kakamega to kisii")

    def test_reallocate_reject_a_person_with_invalid_identifier(self):
        """Tests if it does not reallocate a person with an invalid personid"""
        charity_kisii = self.amity.reallocate_person("78", "kisii")
        self.assertEqual(charity_kisii,
                         "The person identifier(id) used does not exist!")

    def test_reallocate_reject_if_room_does_not_exist(self):
        """Tests if it rejects reallocation to a room which does not exist"""
        charity_kisii = self.amity.reallocate_person("1", "likoni")
        self.assertEqual(charity_kisii,
                         "The room does not exist!")

    def test_reallocate_reject_if_a_room_which_is_full(self):
        """Tests if rejects reallocate person to a room which is full"""
        self.amity.add_person("vannidiah", "fellow", "yes")
        self.amity.add_person("vannidia", "fellow", "yes")
        self.amity.add_person("vannidi", "fellow", "yes")
        self.amity.add_person("vannid", "fellow", "yes")
        self.amity.create_room("living_space", "marsabit")
        vanni = self.amity.add_person("vanni", "fellow", "yes")
        vanni_reallocate = self.amity.reallocate_person("6", "kiambu")
        self.assertEqual(vanni_reallocate,
                         "You cannot be reallocated to a full room!" +
                         "Try another room.")

    def test_reallocate_staff_from_office_to_living_space(self):
        """Tests rejects reallocation of staff from office to livingspace"""
        charity_kiambu = self.amity.reallocate_person("1", "kiambu")
        self.assertEqual(charity_kiambu,
                         "You can't be accommodated since you are a" +
                         "staff member")

    def test_reallocate_rejects_reallocation_to_the_same_room(self):
        """Test rejects reallocation to the same room"""
        charity_kakamega = self.amity.reallocate_person("1", "kakamega")
        self.assertEqual(charity_kakamega,
                         "You can't reallocate a person to the same room" +
                         "he was before")


class LoadsPeopleTestCases(unittest.TestCase):
    """A collection of reallocate_room testcases"""
    def setUp(self):
        self.amity = Amity()

    def tearDown(self):
        self.amity

    def test_loads_people_from_a_txt_file_successfully(self):
        """Tests if it loads people from a txt file successfully"""
        # remember to add the exten .txt
        cohort_15 = self.amity.loads_people("cohort15")
        self.assertEqual(cohort_15, "People added successfully")

    def test_loads_an_empty_file(self):
        """Test if it loads people in an empty file and adds nothing"""
        empty_file = self.amity.loads_people("empty.txt")
        self.assertEqual(empty_file, "Empty file. No one has been added.")

    def test_if_file_does_not_exist(self):
        """Tests if the file does not exist"""
        # Add the file path you said you wanted
        non_existing_file = self.amity.loads_people("non_existing.txt")
        self.assertEqual(non_existing_file, "The file does not exist.")


class PrintAllocatedUnallocated(unittest.TestCase):
    """A collection of print allocated and unallocated testcases"""
    def setUp(self):
        self.amity = Amity()

    def tearDown(self):
        self.amity

    def test_print_allocated_successfully(self):
        """Tests if it prints allocated people successfully"""
        pass

    def test_print_unallocated_successfully(self):
        """Tests if it prints unallocated successfully"""
        pass

    def test_if_it_prints_allocated_people_successfully(self):
        """Tests if it prints allocated people to the specified file"""
        pass

    def test_if_it_prints_unallocated_people_to_the_unspecified_file(self):
        """Tests if prints unallocated people to the sspecified file"""
        pass
