# Office Space Allocation(Amity)
A room allocation system for Andela's Amity facility


**Constraints**

Amity has rooms which can be offices or living spaces. An office can accommodate a maximum of 6 people. A living space can accommodate a maximum of 4 people.

A person to be allocated could be a fellow or staff. Staff cannot be allocated living spaces. Fellows have a choice to choose a living space or not.

This system is used to automatically allocate spaces to people at random.

**Installation**

`$ git clone https://github.com/wanjikum/amity`

`$ cd amity`

 Create and activate a virtual environment.

 ```
 $ virtualenv --python=python3 amity-venv
 $ source amity-venv/bin/activate
 ```

 Install `requirements.txt`

 `$ pip install requirements.txt`

 Run the application using the following commands:
 ```
 $ python app.py -i
   app.py create_room <room_type> <room_name>...
   app.py add_person <first_name> <last_name> <role> [<accommodate>]
   app.py reallocate_person <person_identifier> <new_room_name>
   app.py load_people <file_name>
   app.py print_allocations [--o=filename]
   app.py print_unallocated [--o=filename]
   app.py print_room <room_name>
   app.py allocate_office <person_identifier>
   app.py allocate_livingspace <person_identifier>
   app.py save_state [--db=sqlite_database]
   app.py load_state <sqlite_database>
   app.py (-i | --interactive)
   app.py (-h | --help | --version)
Options:
   -i, --interactive  Interactive Mode
   -h, --help  Show this screen and exit.
"""
 ```
