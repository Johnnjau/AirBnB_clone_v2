#!/usr/bin/python3
""" Console Module """
import cmd
import sys
from models.base_model import BaseModel
from models.__init__ import storage
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review


class FileStorage:
    def __init__(self):
        self.__file_path = "file.json"
        self.__objects = {}

    def create(self, obj):
        """Create a new object in the storage"""
        key = "{}.{}".format(obj.__class__.__name__, obj.id)
        self.__objects[key] = obj
        self.save()

    def save(self):
        """Save the objects to the file"""
        with open(self.__file_path, "w") as file:
            json.dump({key: obj.to_dict() for key, obj 
                       in self.__objects.items()}, file)

    def reload(self):
        """Reload the objects from the file"""
        try:
            with open(self.__file_path, "r") as file:
                objects_dict = json.load(file)
                self.__objects = {key: eval(value['__class__'])(**value) for key, value in objects_dict.items()}
        except FileNotFoundError:
            pass

# Modify the do_create method in your file.py
def do_create(self, arg):
    """Create a new instance of a specified class"""
    if not arg:
        print("** class name missing **")
        return

    args = arg.split()
    class_name = args.pop(0)
    if class_name not in ["BaseModel", "User", "Place", "State", "City", "Amenity", "Review"]:
        print("** class doesn't exist **")
        return

    param_dict = {}
    for param in args:
        if "=" not in param:
            continue
        key, value = param.split("=", 1)
        if len(value) < 2 or value[0] != '"' or value[-1] != '"':
            continue
        value = value[1:-1].replace("_", " ").replace('\\"', '"')
        if "." in value:
            try:
                value = float(value)
            except ValueError:
                continue
        else:
            try:
                value = int(value)
            except ValueError:
                continue
        param_dict[key] = value

    if not param_dict:
        print("** invalid input **")
        return

    try:
        new_instance = eval(class_name)(**param_dict)
    except NameError:
        print("** class doesn't exist **")
        return

    storage.create(new_instance)
    storage.save()
    print(new_instance.id)
