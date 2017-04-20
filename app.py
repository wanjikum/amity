#!/usr/bin/env python
"""
This example uses docopt with the built in cmd module to demonstrate an
interactive command application.
Usage:
    app.py create_room <room_type> <room_name>...
    app.py add_person <first_name> <last_name> <role> [<accommodate>]
    app.py reallocate_person <person_identifier> <new_room_name>
    app.py load_people <file_name>
    app.py print_allocations [--o=filename]
    app.py print_unallocated [--o=filename]
    app.py print_room <room_name>
    app.py save_state [--db=sqlite_database]
    app.py load_state <sqlite_database>
    app.py (-i | --interactive)
    app.py (-h | --help | --version)
Options:
    -i, --interactive  Interactive Mode
    -h, --help  Show this screen and exit.
"""

import os
import sys
import cmd
import re
from termcolor import cprint, colored
from pyfiglet import Figlet
from docopt import docopt, DocoptExit
from classes.amity import Amity

amity = Amity()
amity.load_state("amity")


def docopt_cmd(func):
    """
    This decorator is used to simplify the try/except block and pass the result
    of the docopt parsing to the called action.
    """
    def fn(self, arg):
        try:
            opt = docopt(fn.__doc__, arg)

        except DocoptExit as e:
            # The DocoptExit is thrown when the args do not match.
            # We print a message to the user and the usage block.

            print('Invalid Command!')
            print(e)
            return

        except SystemExit:
            # The SystemExit exception prints the usage for --help
            # We do not need to do the print here.

            return

        return func(self, opt)

    fn.__name__ = func.__name__
    fn.__doc__ = func.__doc__
    fn.__dict__.update(func.__dict__)
    return fn


def start():
    """Clears the screen and prints the amity user interface"""
    os.system("clear")
    font = Figlet(font='cosmic')
    title = font.renderText(' Amity ')
    cprint("-" * 100, 'white')
    cprint(title,  'yellow')
    cprint("-" * 100, 'white')
    cprint(__doc__, 'green')


class MyInteractiveAmity (cmd.Cmd):
    intro = colored('Welcome to my interactive program!', "yellow")
    prompt = colored('amity>>>', "yellow")

    @docopt_cmd
    def do_create_room(self, arg):

        """
        Creates rooms in Amity. Using this command you can able to create
        as many rooms as possible by specifying multiple room names after the
        create_room  command. The room type is either of type office or
        livingspace

        Usage: create_room <room_type> <room_name>...

        e.g create_room office dakar accra

        """

        room_type = arg["<room_type>"]
        room_names = arg["<room_name>"]
        for room in room_names:
            if not re.match(r'^[A-Za-z]{1,15}$', room):
                cprint("Invalid input {}!".format(room), 'red')
                room_names.remove(room)
        cprint(amity.create_room(room_type, room_names), 'green')

    @docopt_cmd
    def do_add_person(self, arg):
        """
         Adds a person to the system and allocates the person to a random room.
         accommodate here is an optional argument which can be either
         Y or N . The default value if it is not provided is  N .

        Usage: add_person <first_name> <last_name> <role> [<accommodate>]

        e.g add_person millicent njuguna f y

        """
        if not re.match(r'^[A-Za-z]{1,15}$', arg["<first_name>"]):
            cprint("Invalid input! Use letters only in first name.", 'red')
        elif not re.match(r'^[A-Za-z]{1,15}$', arg["<last_name>"]):
            cprint("Invalid input! Use letters only in last name.", 'red')
        elif not re.match(r'^[A-Za-z]{1,10}$', arg["<role>"]):
            cprint("Invalid input! Use letters only in role.", 'red')
        elif not re.match(r'^[A-Za-z]{1,5}$', arg["<accommodate>"]):
            cprint("Invalid input! Use letters only in accommodate.", 'red')
        else:
            person_name = arg["<first_name>"] + " " + arg["<last_name>"]
            person_type = arg["<role>"]
            wants_accommodation = arg["<accommodate>"]
            cprint(amity.add_person(person_name, person_type,
                   wants_accommodation),
                   'blue', attrs=['bold'])

    @docopt_cmd
    def do_reallocate_person(self, arg):
        """
        Reallocates the person with  person_identifier  to  new_room_name.

        Usage: reallocate_person <person_identifier> <new_room_name>

        e.g reallocate_person FOO1 accra
        """
        if not re.match(r'^[A-Za-z0-9]{1,10}$', arg["<person_identifier>"]):
            cprint("Invalid input! Use letters or digits in person identifier",
                   'red')
        if not re.match(r'^[A-Za-z0-9]{1,10}$', arg["<new_room_name>"]):
            cprint("Invalid input! Use letters only in room name.", 'red')
        person_id = arg["<person_identifier>"]
        room_name = arg["<new_room_name>"]
        cprint(amity.reallocate_person(person_id, room_name), 'green')

    @docopt_cmd
    def do_load_people(self, arg):
        """
        Adds people to rooms from a txt file

        Usage: load_people <file_name>

        e.g load_people load
        """
        file_name = arg["<file_name>"]
        if not re.match(r'^[A-Za-z0-9]{1,10}$', file_name):
            cprint("Invalid input! Use letters only in file name.", 'red')
        cprint(amity.loads_people(file_name), 'yellow')

    @docopt_cmd
    def do_print_allocations(self, arg):
        """
        Prints a list of allocations onto the screen. Specifying the optional
         -o  option outputs the registered allocations to a txt file

        Usage: print_allocations [--o=filename]

        e.g print_allocations --o=allocated
        """
        file_name = arg["--o"]
        cprint(amity.print_allocated(file_name), 'green')

    @docopt_cmd
    def do_print_unallocated(self, arg):
        """
        Prints a list of unallocated people to the screen. Specifying the  -o
        option outputs the information to the txt file provided.

        Usage: print_unallocated [--o=filename]

        e.g print_unallocated --o=unallocated
        """
        file_name = arg["--o"]
        cprint(amity.print_unallocated(file_name), 'blue')

    @docopt_cmd
    def do_print_room(self, arg):
        """
        Prints the names of all the people in  room_name  on the
        screen.
        Usage: print_room <room_name>

        e.g print_room accra
        """
        room_name = arg["<room_name>"]
        cprint(amity.print_room(room_name), 'green')

    @docopt_cmd
    def do_save_state(self, arg):
        """
         Persists all the data stored in the app to a SQLite database.
         Specifying the --db  parameter explicitly stores the data in the
         sqlite_database  specified.

         Usage: save_state [--db=sqlite_database]

         e.g save_state --db=amity
         """
        database_name = arg["--db"]
        cprint(amity.save_state(database_name), 'yellow')

    @docopt_cmd
    def do_load_state(self, arg):
        """
        Loads data from a database into the application.

        Usage: load_state <sqlite_database>

        e.g load_state amity
        """
        database_name = arg["<sqlite_database>"]
        cprint(amity.load_state(database_name), 'blue')

    def do_quit(self, arg):
        """Quits out of Interactive Mode."""

        print('Good Bye!')
        exit()


opt = docopt(__doc__, sys.argv[1:])

if __name__ == "__main__":
    try:
        start()
        MyInteractiveAmity().cmdloop()
    except KeyboardInterrupt:
        os.system("clear")
        print('Application Exiting')
