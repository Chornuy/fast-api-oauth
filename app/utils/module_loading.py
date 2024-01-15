import inspect
import pathlib
import sys
from importlib import import_module
from importlib.util import find_spec
from types import ModuleType
from typing import Type, Any


def get_module_subclasses(models_module: ModuleType, base_cls_list: tuple) -> list[tuple[str, Type]]:
    """Function to retrieve list of cls that inherited from base cls

    Args:
        models_module:
        base_cls_list:

    Returns:

    """

    def func(element):
        return (
            inspect.isclass(element)
            and issubclass(element, base_cls_list)
            and element not in base_cls_list
        )
    return inspect.getmembers(models_module, func)


def module_has_submodule(package: str, module_name: str) -> bool:
    """See if 'module' is in 'package'."""
    try:
        package_name = package.__name__
        package_path = package.__path__
    except AttributeError:
        # package isn't a package.
        return False

    full_module_name = package_name + "." + module_name
    try:
        return find_spec(full_module_name, package_path) is not None
    except ModuleNotFoundError:
        # When module_name is an invalid dotted path, Python raises
        # ModuleNotFoundError.
        return False


def convert_folder_path_to_module(app_dir: pathlib.Path, base_dir: pathlib.Path) -> str:
    """

    Args:
        app_dir:
        base_dir:

    Returns:

    """
    return str(app_dir).replace(str(base_dir), "").replace("/", ".")[1:]


def cached_import_module(module_path: str):
    """

    Args:
        module_path:

    Returns:

    """
    if not (
        (module := sys.modules.get(module_path))
        and (spec := getattr(module, "__spec__", None))
        and getattr(spec, "_initializing", False) is False
    ):
        module = import_module(module_path)
    return module


def cached_import_class(module_path: str, class_name: str) -> Any | None:
    """

    Args:
        module_path:
        class_name:

    Returns:

    """
    module = cached_import_module(module_path)
    return getattr(module, class_name)


def import_string(dotted_path: str, class_separator: str = "."):
    """
    Import a dotted module path and return the attribute/class designated by the
    last name in the path. Raise ImportError if the import failed.
    """
    try:
        module_path, class_name = dotted_path.rsplit(class_separator, 1)

    except ValueError as err:
        raise ImportError("%s doesn't look like a module path" % dotted_path) from err

    try:
        return cached_import_class(module_path, class_name)
    except AttributeError as err:
        raise ImportError('Module "%s" does not define a "%s" attribute/class' % (module_path, class_name)) from err
