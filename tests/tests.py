import unittest
import os
from io import StringIO
import sys

from classes.room import Room, Office, LivingSpace
from classes.person import Person, Fellow, Staff
from classes.amity import Amity


class CreateRoomTestCases(unittest.TestCase):
    """A class CreateRoom that has a collection of create_room testcases"""
    def setUp(self):
        """Keeps our code dry"""
        self.amity = Amity()
        self.bootcamp = self.amity.create_room("office", ["Bootcamp"])

    def tearDown(self):
        del self.amity
        Amity.offices = []
        Amity.livingspaces = []

    def test_create_room_type_office_successfully(self):
        """Test create a room_type office successfully"""
        response = self.amity.create_room("office", ["asmara"])
        self.assertEqual(response, "Asmara added successfully!\n")

    def test_create_multiple_rooms_of_type_livingspace_successfully(self):
        """Test create multiple rooms of type office successfully"""
        livingspace_intial_count = len(self.amity.livingspaces)
        likoni_tsavo = self.amity.create_room("livingspace",
                                              ["likoni", "tsavo"])
        self.assertEqual(len(self.amity.livingspaces),
                         livingspace_intial_count+2)

    def test_create_duplicate_room(self):
        """Test an existing room is not recreated"""
        response = self.amity.create_room("office", ["Bootcamp"])
        self.assertEqual(response, "Room Bootcamp already exists!\n")

    def test_create_invalid_room_type(self):
        """Test create invalid room type """
        response = self.amity.create_room("kitchen", ["hog_centre"])
        self.assertEqual(response, "Invalid room type. A room can either be of"
                         + " type office or living_space!\n")


class AddPersonTestCases(unittest.TestCase):
    """A class CreateRoom that has a collection of create_room testcases"""
    def setUp(self):
        """Keeps our code dry"""
        self.amity = Amity()

    def tearDown(self):
        del self.amity
        Amity.staffs = []
        Amity.fellows = []

    def test_add_person_staff_successfully(self):
        """Test add staff successfully"""
        self.amity.add_person("felistas", "staff", "no")
        response = sys.stdout.getvalue().strip()
        self.assertIn("Felistas added successfully! Your ID: SOO1", response)

    def test_add_person_staff_who_requires_accommodation(self):
        """Test reject accommodation for staff"""
        response = self.amity.add_person("felistas", "staff", "yes")
        self.assertIn("Staff cannot be accomodated!\n", response)

    def test_add_person_who_inputs_a_wrong_accomodation_value(self):
        """Test reject accommodation if option is neither yes/no"""
        response = self.amity.add_person("felistas", "staff", "who")
        self.assertIn("Invalid accomodate option. "
                      "It can either be yes or no.", response)

    def test_reject_invalid_role(self):
        """Rejects adding a person whose person type is not fellow/staff"""
        response = self.amity.add_person("alex", "techie", "no")
        self.assertIn("Invalid role. You can either be a fellow/staff.",
                      response)

    def test_if_it_accepts_string_only_in_person_name(self):
        """Tests if it rejects names with numbers"""
        response = self.amity.add_person("ti67ji#", "staff", "no")
        self.assertIn("Invalid name. Use letters only", response)


class AllocateRoomPersonTestCases(unittest.TestCase):
    """A collection of create_room testcases"""
    def setUp(self):
        """Keeps our code dry"""
        self.amity = Amity()

    def tearDown(self):
        del self.amity
        Amity.offices = []
        Amity.livingspaces = []
        Amity.fellows = []

    def test_allocate_office_successfully(self):
        """Tests if a person is successfully allocated an office"""
        self.amity.create_room("office", ["accra"])
        response = self.amity.add_person("oliver", "staff", "no")
        self.assertIn("Allocated office: accra\n", response)

    def test_allocate_livingspace_successfully(self):
        """Tests if a person is successfully allocated to a livingspace"""
        self.amity.create_room("livingspace", ["left_wing"])
        response = self.amity.add_person("oliver", "fellow", "yes")
        self.assertIn("Allocated livingspace: left_wing \n", response)

    def test_allocate_livingspace_if_no_available_livingspaces(self):
        """Test reject livingspace allocation if no livingspace available"""
        response = self.amity.add_person("oliver", "fellow", "yes")
        self.assertIn("No available livingspaces. "
                      "Added to the livingspaces waiting list\n", response)

    def test_allocate_office_if_no_available_offices(self):
        """Test reject allocation if room is full"""
        response = self.amity.add_person("Alex", "staff", "no")
        self.assertIn("No available offices. "
                      "Added to the office waiting list\n", response)


class PrintRoomTestCases(unittest.TestCase):
    """A collection of print_room testscases"""
    def setUp(self):
        self.amity = Amity()
        self.amity.create_room("living_space", ["left_wing"])
        self.amity.add_person("Kenneth", "fellow", "yes")
        self.amity.add_person("Larry", "fellow", "yes")

    def tearDown(self):
        self.amity
        Amity.offices = []
        Amity.livingspaces = []
        Amity.fellows = []

    def test_print_room_occupants_successfully(self):
        """Test if it prints the room occupants successfully"""
        response = self.amity.print_room("left_wing")
        self.assertIn("Room occupants printed successfully!\n", response)

    def test_print_room_reject_if_room_name_does_not_exist(self):
        """Test if rejects printing occupants in a unexisting room"""
        occupants = self.amity.print_room("kiki")
        self.assertIn("The room does not exist!\n", occupants)

    def test_print_room_if_empty(self):
        """Test response in print room empty if empty"""
        self.amity.create_room("living_space", ["right_wing"])
        response = self.amity.print_room("right_wing")
        self.assertIn("The room is empty!\n", response)


class RellocateRoomPersonTestCases(unittest.TestCase):
    """A collection of create_room testcases"""
    def setUp(self):
        """Keeps our code dry"""
        self.amity = Amity()
        self.amity.create_room("living_space", ["r_wing"])
        self.amity.add_person("Oliver", "fellow", "yes")
        self.amity.add_person("MaryAnne", "fellow", "yes")
        self.amity.add_person("Gideon", "fellow", "yes")
        self.amity.add_person("Kimokoti", "fellow", "yes")
        self.amity.create_room("office", ["dakar"])
        self.amity.create_room("living_space", ["l_wing"])
        self.amity.add_person("Taracha", "staff", "no")
        self.amity.create_room("office", ["accra"])

    def tearDown(self):
        del self.amity
        Amity.offices = []
        Amity.livingspaces = []
        Amity.staffs = []
        Amity.fellows = []

    def test_reallocate_room_reject_if_room_is_full(self):
        """Tests if rejects reallocate person to a room which is full"""
        self.amity.add_person("vanni", "fellow", "yes")
        response = self.amity.reallocate_person("FOO5", "r_wing")
        self.assertIn("Room capacity full!", response)

    def test_reallocate_room_successfully(self):
        """Tests if a person is successfully reallocated"""
        response = self.amity.reallocate_person("FOO1", "l_wing")
        self.assertIn("Oliver has been reallocated from r_wing to l_wing",
                      response)

    def test_reallocate_room_reject_a_person_with_invalid_identifier(self):
        """Tests if it rejects reallocate a person with an invalid personid"""
        response = self.amity.reallocate_person("omega", "kakamega")
        self.assertIn("The person identifier(id) used does not exist!",
                      response)

    def test_reallocate_room_reject_if_room_does_not_exist(self):
        """Tests if it rejects reallocation to a room which does not exist"""
        response = self.amity.reallocate_person("FOO3", "likoni")
        self.assertIn("The room does not exist!", response)

    def test_reallocate_staff_from_office_to_living_space(self):
        """Tests rejects reallocation of staff from office to livingspace"""
        response = self.amity.reallocate_person("SOO1", "l_wing")
        self.assertIn("Staff cannot be accomodated!", response)

    def test_reallocate_rejects_reallocation_to_the_same_room(self):
        """Test rejects reallocation to the same room"""
        response = self.amity.reallocate_person("FOO2", "r_wing")
        self.assertIn("A person cannot be reallocated to the same room",
                      response)

    def test_reallocate_rejects_reallocation_if_not_allocated_yet(self):
        """Test rejects reallocation to the same room"""
        response = self.amity.reallocate_person("FOO2", "accra")
        self.assertIn("Maryanne has not been allocated an office yet\n",
                      response)


class LoadsPeopleTestCases(unittest.TestCase):
    """A collection of reallocate_room testcases"""
    def setUp(self):
        self.amity = Amity()

    def tearDown(self):
        self.amity

    def test_loads_people_from_a_txt_file_successfully(self):
        """Tests if it loads people from a txt file successfully"""
        # remember to add the exten .txt
        cohort_15 = self.amity.loads_people("load")
        self.assertEqual(cohort_15, "People added successfully")

    def test_loads_an_empty_file(self):
        """Test if it loads people in an empty file and adds nothing"""
        empty_file = self.amity.loads_people("empty")
        self.assertEqual(empty_file, "Empty file. No one has been added.")

    def test_if_file_does_not_exist(self):
        """Tests if the file does not exist"""
        # Add the file path you said you wanted
        non_existing_file = self.amity.loads_people("non_existing")
        self.assertEqual(non_existing_file, "The file does not exist.")


class PrintAllocatedUnallocated(unittest.TestCase):
    """A collection of print allocated and unallocated testcases"""
    def setUp(self):
        self.amity = Amity()
        self.amity.create_room("living_space", ["right_wing"])
        self.amity.add_person("Kenneth", "fellow", "yes")
        self.amity.add_person("Gideon", "fellow", "yes")
        self.amity.add_person("Kimokoti", "fellow", "yes")
        self.amity.add_person("Larry", "fellow", "yes")
        self.amity.add_person("MaryAnne", "fellow", "yes")
        self.amity.add_person("Sarah", "fellow", "yes")

    def tearDown(self):
        self.amity
        Amity.offices = []
        Amity.livingspaces = []
        Amity.staffs = []
        Amity.fellows = []

    def test_print_allocations_successfully(self):
        """Tests if it prints allocated people successfully"""
        response = self.amity.print_allocated(None)
        self.assertIn("\nData printed successfully\n", response)

    def test_print_unallocated_successfully(self):
        """Tests if it prints unallocated people successfully"""
        response = self.amity.print_unallocated()
        self.assertIn("Data printed successfully\n", response)

    def test_print_allocated_successfully_to_text_file(self):
        """Tests if it prints allocated people to the specified file"""
        response = self.amity.print_allocated("allocated")
        self.assertIn("Data saved in allocated successfully", response)

    def test_print_unallocated_successfully_to_text_file(self):
        """Tests if prints unallocated people to the specified file"""
        response = self.amity.print_unallocated("unallocated")
        self.assertIn("Data saved in unallocated successfully", response)


class AllocateUnallocated(unittest.TestCase):
    """A collection of allocate_person room"""
    def setUp(self):
        self.amity = Amity()
        self.amity.create_room("office", ["bootcamp"])
        self.amity.create_room("living_space", ["left"])
        self.amity.add_person("Oliver", "fellow", "yes")
        self.amity.add_person("Kenneth", "fellow", "yes")
        self.amity.add_person("Gideon", "fellow", "yes")
        self.amity.add_person("Kimokoti", "fellow", "yes")
        self.amity.add_person("Larry", "fellow", "yes")
        self.amity.add_person("MaryAnne", "fellow", "yes")
        self.amity.add_person("Ian", "fellow", "yes")

    def tearDown(self):
        self.amity
        Amity.offices = []
        Amity.livingspaces = []
        Amity.staffs = []
        Amity.fellows = []

    def test_allocate_person_to_a_random_office_from_the_waiting_list(self):
        """Tests if it allocates a person if no available offices"""
        response = self.amity.allocate_person_office("foo7")
        self.assertEqual(response,
                         "No available offices")

    def test_allocate_person_to_a_random_livingspace(self):
        """Tests if it allocates a person if no available livingspaces"""
        response = self.amity.allocate_person_livingspace("foo7")
        self.assertEqual(response,
                         "No available livingspaces")

    def test_allocate_person_to_an_office_successfully_from_waiting_list(self):
        """Tests if it allocates a person to a random office"""
        self.amity.create_room("office", ["asmara"])
        response = self.amity.allocate_person_office("foo7")
        self.assertEqual(response,
                         "Ian has been allocated to office asmara")

    def test_allocate_person_to_a_random_living_space_from_waiting_list(self):
        """Tests if it allocates a person to a random living_space"""
        self.amity.create_room("living_space", ["west"])
        response = self.amity.allocate_person_livingspace("foo7")
        self.assertEqual(response,
                         "Ian has been allocated to livingspace west")

    def test_allocate_office_if_allocated(self):
        response = self.amity.allocate_person_office("foo2")
        self.assertEqual(response,
                         "The person is not in the office waiting list")

    def test_allocate_livingspace_if_allocated(self):
        response = self.amity.allocate_person_livingspace("foo2")
        self.assertEqual(response,
                         "The person is not in the livingspace waiting list")


class SaveStateTestCases(unittest.TestCase):
    """A collection of loadstate testcases"""

    def setUp(self):
        self.amity = Amity()

    def tearDown(self):
        self.amity
        os.remove("database/amity_database.db")

    def test_save_state_successfully(self):
        """Test if it saves state successfully"""
        # look at this later and db extension
        response = self.amity.save_state("amity_database")
        self.assertEqual(response, "The state has been saved successfully!")

    def test_if_db_exists(self):
        """Tests if the db file exists"""
        self.amity.save_state("amity_database")
        file_path = os.path.abspath("database/amity_database.db")
        file_status = os.path.isfile(file_path)
        self.assertTrue(file_status)


class LoadStateTestCases(unittest.TestCase):
    """A collection of load state testcases"""

    def setUp(self):
        self.amity = Amity()

    def tearDown(self):
        self.amity

    def test_load_state_successfully(self):
        """Tests if load state successfully"""
        response = self.amity.load_state("amity")
        self.assertEqual(response,
                         "The database has loaded successfully!")

    def test_load_state_unsuccessfully(self):
        """Test if loads state unsuccessfully"""
        # This may be due to non existing db
        response = self.amity.load_state("dee")
        self.assertEqual(response,
                         "The database does not exist!")
