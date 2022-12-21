import importlib
import os

import pymel.core as pm
from typing import Dict


class MyPlugin:
    def __init__(self, menu_path: str) -> None:
        """
        Initializes a new instance of the MyPlugin class.

        Parameters:
        - menu_path: The path of the menu in which to create the plugin's items.
        """
        # Split the menu path into separate menu labels
        menu_labels = menu_path.split("/")

        # Create the menu hierarchy by iterating over the menu labels
        parent_menu = None
        for label in menu_labels:
            # Check if a menu with this label already exists
            existing_menu = pm.menu(label, query=True, exists=True)
            if existing_menu:
                # Use the existing menu
                menu = existing_menu
            else:
                # Create a new menu
                menu = pm.menu(label, label=label, tearOff=True, parent=parent_menu)

            # Set the parent menu for the next iteration
            parent_menu = menu

        # Add a menu item
        pm.menuItem(parent=menu, label="Item 1", command=self.item1_command)

        # Attach the top-level menu to the main Maya menu bar
        pm.menu(menu_labels[0], edit=True, parent="MayaWindow")

    def item1_command(self, *args) -> None:
        """
        Handles the action for the "Item 1" menu item.
        """
        print("Item 1 command called")


def discover_plugins(directory: str) -> Dict[str, str]:
    """
    Discovers the Maya menu plugins in the specified directory.

    Parameters:
    - directory: The directory to search for plugins.

    Returns:
    A dictionary mapping module names to menu paths for each plugin.
    """
    # Get a list of all files in the directory
    file_names = os.listdir(directory)

    # Only include files that are prefixed with "mmp_" and have the .py extension
    mmp_files = []
    for file_name in file_names:
        if file_name.startswith("mmp_") and os.path.splitext(file_name)[1] == ".py":
            mmp_files.append(file_name)

    # Remove the .py extension from the file names
    module_names = []
    for mmp_file in mmp_files:
        module_names.append(os.path.splitext(mmp_file)[0])

    # Create the menu paths for each module based on the directory structure
    menu_paths = []
    for module_name in module_names:
        # Get the relative path of the module's directory
        module_path = os.path.relpath(os.path.dirname(module_name), directory)

        # Replace the directory separator with a forward slash
        menu_path = module_path.replace(os.sep, "/")

        menu_paths.append(menu_path)

    return dict(zip(module_names, menu_paths))


def import_module(module_name: str) -> object:
    """
    Imports a module by its name.

    Parameters:
    - module_name: The name of the module to import.

    Returns:
    The imported module.
    """
    return importlib.import_module(module_name)


def create_instance(module, class_name, menu_path):
    """
    Creates an instance of the specified class in the specified module.
    Args:
        module (object):
        class_name (str):
        menu_path (str):

    Returns:

    """
    # Get the class from the module
    cls = getattr(module, class_name)

    # Create an instance of the class
    return cls(menu_path)


if __name__ == "__main__":
    # Define the directory where the plugins are located
    plugin_directory = "/path/to/plugins"

    # Discover the plugins in the directory
    plugins = discover_plugins(plugin_directory)

    # Import and create instances of the plugins
    for module_name, menu_path in plugins:
        # Import the module
        module = import_module(module_name)

        # Create an instance of the plugin class
        instance = create_instance(module, "MyPlugin", menu_path)
