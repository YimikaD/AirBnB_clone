#!/usr/bin/python3
"""This module contains the entry point of the command interpreter"""
import cmd
from models.base_model import BaseModel
import json
from models import storage
import re

class HBNBCommand(cmd.Cmd):

    """The class def for command interpreter"""

    prompt = "(hbnb) "

    def do_quit(self, line):
        """Quit command to exit the program"""
        
        if line:
            return True
        else:
            return True

    def do_EOF(self, line):
        """EOF command to handle End Of File character"""

        if line:
            return True
        else:
            print()
            return True

    def emptyline(self):
        """Dosen't execute anything on ENTER"""

        pass

    def do_create(self, line):
        """Creates new instance of BaseModel"""

        if line == "" or line is None:
            print("** class name missing **")
        elif line not in storage.classes():
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
                set_obj = "{}.{}".format(line_list[0], line_list[1])
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
                set_obj = "{}.{}".format(line_list[0], line_list[1])
                if set_obj not in storage.all():
                    print("** no instance found **")
                else:
                    del storage.all()[set_obj]
                    storage.save()

    def do_all(self, line):
        """Prints all string representation of all instances """

        if line != "":
            line_list = line.split(' ')
            if line_list[0] not in storage.classes():
                print("** class doesn't exist **")
            else:
                new_lt = [str(obj) for key, obj in storage.all().items()
                      if obj.__class__.__name__ == line_list[0]]
                print(new_lt)
        else:
            new_list = [str(obj) for key, obj in storage.all().items()]
            print(new_list)

    def do_update(self, line):
        """Updates an instance by adding or updating attribute """

        if line == "" or line is None:
            print("** class name missing **")
            return

        rex = r'^(\S+)(?:\s(\S+)(?:\s(\S+)(?:\s((?:"[^"]*")|(?:(\S)+)))?)?)?'
        match = re.search(rex, line)
        classname = match.group(1)
        uid = match.group(2)
        attribute = match.group(3)
        value = match.group(4)
        if not match:
            print("** class name missing **")
        elif classname not in storage.classes():
            print("** class doesn't exist **")
        elif uid is None:
            print("** instance id missing **")
        else:
            set_obj = "{}.{}".format(classname, uid)
            if set_obj not in storage.all():
                print("** no instance found **")
            elif not attribute:
                print("** attribute name missing **")
            elif not value:
                print("** value missing **")
            else:
                cast = None
                if not re.search('^".*"$', value):
                    if '.' in value:
                        cast = float
                    else:
                        cast = int
                else:
                    value = value.replace('"', '')
                attributes = storage.attributes()[classname]
                if attribute in attributes:
                    value = attributes[attribute](value)
                elif cast:
                    try:
                        value = cast(value)
                    except ValueError:
                        pass  # fine, stay a string then
                setattr(storage.all()[set_obj], attribute, value)
                storage.all()[set_obj].save()


if __name__ == '__main__':
    HBNBCommand().cmdloop()
