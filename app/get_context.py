import inspect
from os import listdir
from os.path import join
import importlib
from zsquirrel.entities import Entity
from zsquirrel.context import ApplicationInterface

CLASSES = "classes"
LAYERS = "layers"
SPRITES = "sprites"
INTERFACES = "interfaces"
METHODS = "methods"
APP = "app"


def get_classes_from_module(module):
    return list(filter(
        lambda cls: inspect.getmodule(cls) is module,   # exclude imported classes
        [member[1] for member in inspect.getmembers(module, inspect.isclass)]
    ))


def get_methods_from_module(module):
    return list(filter(
        lambda m: inspect.getmodule(m) is module,       # exclude imported methods
        [member[1] for member in inspect.getmembers(module, inspect.isfunction)]
    ))


def get_modules_from_directory(directory):
    path = join(APP, directory)
    file_names = listdir(path)
    file_names = list(filter(
        lambda f: f not in ("__pycache__", "__init__.py"),
        file_names
    ))

    modules = []

    for file_name in file_names:
        file_name = "".join(file_name.split(".")[:-1])
        name = "{}.{}.{}".format(APP, directory, file_name)
        modules.append(importlib.import_module(name))

    return modules


def get_context_classes():
    entity_classes = get_code_objects(
        CLASSES, SPRITES, LAYERS
    )
    entity_classes = [
        e for e in entity_classes if issubclass(e, Entity)
    ]

    interface_classes = get_code_objects(
        CLASSES, INTERFACES
    )
    interface_classes = [
        i for i in interface_classes if issubclass(i, ApplicationInterface)
    ]

    return entity_classes, interface_classes


def get_code_objects(obj_type, *dirs, module_name=""):
    output = []
    ve = False

    for directory in dirs:
        modules = get_modules_from_directory(directory)

        if module_name:
            modules = [
                m for m in modules if m.__name__.split(".")[-1] == module_name
            ]

        if obj_type == CLASSES:
            classes = []
            for m in modules:
                classes += get_classes_from_module(m)

            output += classes

        elif obj_type == METHODS:
            methods = []
            for m in modules:
                methods += get_methods_from_module(m)

            output += methods

        else:
            ve = True

    if ve:
        raise ValueError("obj_type must be 'methods' or 'classes'")

    return output
