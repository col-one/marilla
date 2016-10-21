"""Create a mopa menu, if it already exists it is delete and recreate 
from scratch.
"""

try:
    import pymel.core as pmc
except ImportError:
    pass
import marilla.defMenus

def get_main_window_name():
    """return the main maya window
    """
    w = pmc.MelGlobals()['gMainWindow']
    return w

def create_menu():
    """create menu mopa, delete it if already exists
    """
    main = get_main_window_name()
    if pmc.menu('Marilla', exists=True):
        pmc.deleteUI('Marilla')
    menu = pmc.menu('Marilla', parent=main)
    return menu

def exec_menu():
	menu = create_menu()
	marilla.defMenus.create_geurilla_submenu(menu)