#!/usr/bin/env python
"""
This example uses docopt with the built in cmd module to demonstrate an
interactive command application.
Usage:
    app.py create_room <OFFICE|LIVING_SPACE> <room_name>...
    app.py add_person <first_name> <last_name> <role> [<accommodate>]
    app.py reallocate_person <person_identifier> <new_room_name>
    app.py load_people <file_name>
    app.py print_allocations [--o=filename]
    app.py print_unallocated [--o=filename]
    app.py print_room <room_name>
    app.py save_state [--db=<sqlite_database>]
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
from docopt import docopt, DocoptExit
from classes.amity import Amity

amity = Amity()


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
    os.system("clear")
    print(__doc__)


class MyInteractiveAmity (cmd.Cmd):
    intro = 'Welcome to my interactive program!'
    prompt = 'amity>>>'

    @docopt_cmd
    def do_create_room(self, arg):
        """Usage: create_room <room_type> <room_name>..."""
        room_type = arg["<room_type>"]
        room_names = arg["<room_name>"]
        amity.create_room(room_type, room_names)

    @docopt_cmd
    def do_add_person(self, arg):
        """Usage: add_person <first_name> <last_name> <role> [<accommodate>]"""
        # the role should either be a fellow or a staff
        # the accomadation should either be yes or no
        # hoe to use pipe and how to pass arguments in it
        # join first name and second name inorder to fit in my persons name arg
        person_name = arg["<first_name>"] + " " + arg["<last_name>"]
        person_type = arg["<role>"]
        accommodate = arg["<accommodate>"]
        amity.add_person(person_name, person_type, accommodate)

    @docopt_cmd
    def do_reallocate_person(self, arg):
        """Usage: reallocate_person <person_identifier> <new_room_name>"""
        person_id = arg["<person_identifier>"]
        room_name = arg["<new_room_name>"]
        amity.reallocate_person(person_id, room_name)

    @docopt_cmd
    def do_load_people(self, arg):
        """Usage: load_people <file_name>"""
        file_name = arg["<file_name>"]
        amity.loads_people(file_name)

    @docopt_cmd
    def do_print_allocations(self, arg):
        """Usage: print_allocations [--o=filename]"""
        file_name = arg["--o"]
        amity.print_allocated(file_name)

    @docopt_cmd
    def do_print_unallocated(self, arg):
        """Usage: print_unallocated [--o=filename]"""
        file_name = arg["--o"]
        amity.print_unallocated(file_name)

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
