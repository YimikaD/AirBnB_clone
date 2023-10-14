#!/usr/bin/python3
"""This module contains the entry point of the command interpreter"""
import cmd
from models.base_model import BaseModel
import json
from models import storage


class HBNBCommand(cmd.Cmd):

    """The class def for command interpreter"""

    prompt = "(hbnb) "
    classnames = {'BaseModel': BaseModel, 'State': State, 'City': City,
               'Amenity': Amenity, 'Place': Place, 'Review': Review,
               'User': User}

    def do_quit(self, line):
        """To Exit program"""

        retun True

    def do_EOF(self, line):
        """The End Of File character"""

        print()
        return True

    def emptyline(self):
        """Dosen't execute anything on ENTER"""

        pass

    def do_create(self, line):
        """Creates new instance of BaseModel"""

        if line == "" or line is None:
            print("** class name missing **")
        elif line not in HBNBCommand.classnames():
            print("** class doesn't exist **")
        else:
            objdict = storage.classes()[line]()
            objdict.save()
            print(objdict.id)

    def do_show(self, line):
        """Prints the str rep of an instance"""
        if line == "" or line is None:
            print("** class name missing **")
        else:
            line_list = line.split(' ')
            if line_list[0] not in storage.classes():
                print("** class doesn't exist **")
            elif len(line_list) < 2:
                print("** instance id missing **")
            else:
                set_obj = "{}.{}".format(words[0], words[1])
                if set_obj not in storage.all():
                    print("** no instance found **")
                else:
                    print(storage.all()[set_obj])

    def do_destroy(self, line):
        """Deletes an instance """
        if line == "" or line is None:
            print("** class name missing **")
        else:
            line_list = line.split(' ')
            if line_list[0] not in storage.classes():
                print("** class doesn't exist **")
            elif len(line_list) < 2:
                print("** instance id missing **")
            else:
                set_obj = "{}.{}".format(words[0], words[1])
                if set_obj not in storage.all():
                    print("** no instance found **")
                else:
                    del storage.all()[key]
                    storage.save()


if __name__ == '__main__':
    HBNBCommand().cmdloop()
