class Person(object):
    """A class Person which is the super class of class fellow and staff.
    A person who can be allocated in the dojo facility. He can be a staff or
    a fellow.

    Attributes:
        person_name: A string that contains the person's name.
        person_type: The person type as a string.
        accommodate: A string that has information on whether to accomodate a
        person or not.
    """

    def __init__(self, person_name, person_type="none"):
        """Class person constructor"""
        self.person_name = person_name
        self.person_type = person_type
        self.person_id = ""


class Staff(Person):
    """A class Staff that inherits from class Person"""
    def __init__(self, person_name, person_type="staff"):
        Person.__init__(self, person_name, person_type)


class Fellow(Person):
    """A class Fellow that inherit from class Person"""
    def __init__(self, person_name, person_type="fellow", accommodate='no'):
        Person.__init__(self, person_name, person_type)
        self.accommodate = accommodate
