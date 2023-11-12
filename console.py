#!/usr/bin/python3
"""Module that contains entry point of the command interpreter."""

import cmd
from models.base_model import BaseModel
from models import storage
import re
import json


class HBNBCommand(cmd.Cmd):

    """The command interpreter class."""

    Prompt = "(hbnb)"

    def default(self, line):
        """Catch commands if nothing else matches then."""

        self._precmd(line)

    def _precmd(self, line):
        """Intercepts commands to test for class.syntax()"""

        Match = re.search(r"^(\w*)\.(\w+)(?:\(([^)]*)\))$", line)

        if not Match:
            return line

        Classname = Match.group(1)
        Method = Match.group(2)
        Args = Match.group(3)

        Match_Uid_and_Args = re.search('^"([^"]*)"(?:, (.*))?$', Args)

        if Match_Uid_and_Args:
            Uid = Match_Uid_and_Args.group(1)
            Attr_or_Dict = Match_Uid_and_Args.group(2)
        else:
            Uid = Args
            Attr_or_Dict = False

        Attr_and_Value = ""

        if Method == "update" and Attr_or_Dict:

            Match_Dict = re.search('^({.*})$', Attr_or_Dict)

            if Match_Dict:
                self.Update_Dict(Classname, Uid, Match_Dict.group(1))
                return ""

            Match_Attr_and_Value = re.search(
                '^(?:"([^"]*)")?(?:, (.*))?$', Attr_or_Dict)

            if Match_Attr_and_Value:
                Attr_and_Value = (Match_Attr_and_Value.group(
                    1) or "") + " " + (Match_Attr_and_Value.group(2) or "")
        Command = Method + " " + Classname + " " + Uid + " " + Attr_and_Value
        self.onecmd(Command)
        return Command

    def Update_dict(self, Classname, Uid, o_Dict):
        """Helper method for update() with a dictionary."""
        o = o_dict.replace("'", '"')
        e = json.loads(o)
        if not Classname:
            print("** class name missing **")
        elif Classname not in storage.classes():
            print("** class doesn't exist **")
        elif Uid is None:
            print("** instance id missing **")
        else:
            key = "{}.{}".format(Classname, Uid)
            if key not in storage.all():
                print("** no instance found **")
            else:
                Attributes = storage.Attributes()[Classname]
                for Attribute, Value in e.items():
                    if Attribute in Attributes:
                        Value = Attributes[Attribute](Value)
                    setattr(storage.all()[key], Attribute, Value)
                storage.all()[key].save()

    def do_EOF(self, line):
        """Handles End Of File character.
        """
        print()
        return True

    def do_quit(self, line):
        """Exits the program.
        """
        return True

    def emptyline(self):
        """Doesn't do anything on ENTER.
        """
        pass

    def do_create(self, line):
        """Creates an instance.
        """
        if not line:
            print("** class name missing **")
        elif line not in storage.classes():
            print("** class doesn't exist **")
        else:
            c = storage.classes()[line]()
            c.save()
            print(c.id)

    def do_show(self, line):
        """Prints the string representation of an instance.
        """
        if not line:
            print("** class name missing **")
        else:
            Words = line.split(' ')
            if Words[0] not in storage.classes():
                print("** class doesn't exist **")
            elif len(Words) < 2:
                print("** instance id missing **")
            else:
                key = "{}.{}".format(Words[0], Words[1])
                if key not in storage.all():
                    print("** no instance found **")
                else:
                    print(storage.all()[key])

    def do_destroy(self, line):
        """Deletes an instance based on the class name and id.
        """
        if not line:
            print("** class name missing **")
        else:
            Words = line.split(' ')
            if Words[0] not in storage.classes():
                print("** class doesn't exist **")
            elif len(Words) < 2:
                print("** instance id missing **")
            else:
                key = "{}.{}".format(Words[0], Words[1])
                if key not in storage.all():
                    print("** no instance found **")
                else:
                    del storage.all()[key]
                    storage.save()

    def do_all(self, line):
        """Prints all string representation of all instances.
        """
        if line != "":
            Words = line.split(' ')
            if Words[0] not in storage.classes():
                print("** class doesn't exist **")
            else:
                wl = [str(obj) for key, obj in storage.all().items()
                      if type(obj).__name__ == Words[0]]
                print(wl)
        else:
            Newlist = [str(obj) for key, obj in storage.all().items()]
            print(Newlist)

    def do_count(self, line):
        """Counts the instances of a class.
        """
        Words = line.split(' ')
        if not Words[0]:
            print("** class name missing **")
        elif Words[0] not in storage.classes():
            print("** class doesn't exist **")
        else:
            Matches = [
                r for r in storage.all() if r.startswith(
                    Words[0] + '.')]
            print(len(Matches))

    def do_update(self, line):
        """Updates an instance by adding or updating attribute.
        """
        if not line:
            print("** class name missing **")
            return

        Rex = r'^(\S+)(?:\s(\S+)(?:\s(\S+)(?:\s((?:"[^"]*")|(?:(\S)+)))?)?)?'
        Match = re.search(Rex, line)
        Classname = Match.group(1)
        Uid = Match.group(2)
        Attribute = Match.group(3)
        Value = Match.group(4)

        if not Match:
            print("** class name missing **")
        elif Classname not in storage.classes():
            print("** class doesn't exist **")
        elif Uid is None:
            print("** instance id missing **")
        else:
            key = "{}.{}".format(Classname, Uid)
            if key not in storage.all():
                print("** no instance found **")
            elif not Attribute:
                print("** attribute name missing **")
            elif not Value:
                print("** value missing **")
            else:
                cast = None
                if not re.search('^".*"$', Value):
                    if '.' in Value:
                        cast = float
                    else:
                        cast = int
                else:
                    Value = Value.replace('"', '')
                Attributes = storage.Attributes()[Classname]
                if Attribute in Attributes:
                    Value = Attributes[Attribute](Value)
                elif cast:
                    try:
                        Value = cast(Value)
                    except ValueError:
                        pass
                setattr(storage.all()[key], Attribute, Value)
                storage.all()[key].save()


if __name__ == '__main__':
    HBNBCommand().cmdloop()
