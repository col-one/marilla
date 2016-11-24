"""Ensembles des def lance depuis le menu mopa>guerilla
Peuvent etre utilise hors menu.
"""

import os
import subprocess
try:
    import pymel.core as pmc
except ImportError:
    pass
from functools import partial
import marilla.guegueTags
import marilla.utils.sockette
import marilla.maUtils
import marilla.marillaUi

"""All def call be guerilla menu command
"""
def auto_tags_selection(*args):
    """auto tag all selected objects
    """
    sl = pmc.ls(sl=True)
    for obj in sl:
        tt = marilla.guegueTags.GuegueTags(obj)
        tt.write_tags()

def remove_all_tags(*args):
    """remove all tags selected objects
    """
    sl = pmc.ls(sl=True)
    for obj in sl:
        tt = marilla.guegueTags.GuegueTags(obj)
        tt.tags = []
        tt.write_tags()

def add_custom_tags(*args):
    """add and remove custom tags on selection with \bGUI
    """
    def exec_add_button(*args):
        sl = pmc.ls(sl=True)
        for obj in sl:
            tt = marilla.guegueTags.GuegueTags(obj)
            tt.add_to_tags(tag=str(pmc.textField('tags', query=True, text=True)))
            tt.write_tags()
    def exec_remove_button(*args):
        sl = pmc.ls(sl=True)
        for obj in sl:
            tt = marilla.guegueTags.GuegueTags(obj)
            tt.remove_to_tags(tag=str(pmc.textField('tags', query=True, text=True)))
            tt.write_tags()
    marilla.marillaUi.ui_add_custom_tags(exec_add_button, exec_remove_button)

def export_selection(*args):
    """collect all export options for abc and send to guerilla with \bGUI
    """
    def exec_button(*args):
        path = pmc.fileDialog2(fileFilter='*.abc')
        if path:
            path = path[0]
        else:
            exit("Canceled")
        #query ui values
        framemode = pmc.radioCollection('framemode', query=True, sl=True)
        preroll = pmc.checkBox('preroll', q=True, value=True)
        qstart = pmc.intField('start', q=True, value=True)
        qend = pmc.intField('end', q=True, value=True)
        preframe = pmc.intField('prerollstart', q=True, value=True)
        step = pmc.intField('step', q=True, value=True)
        toguerilla = pmc.checkBox('guerilla', q=True, value=True)
        #export with maUtils abc_export
        marilla.maUtils.abc_export(path=path,framemode=framemode,preroll=preroll,
        qstart=qstart, qend=qend, preframe=preframe, step=step, nodes=pmc.ls(sl=True))
        #send to guerilla
        if toguerilla:
            command=("local mod = Document:modify(); mod.createref ('{filename}'"
            ",'{path}',nil,{{prefixnodes=false,containschildren=false}}); "
            "mod.finish()").format(
                filename=os.path.basename(path).split('.')[0], path=path)
            try:
                sock = marilla.utils.sockette.SendCommand(port=1978, 
                                                          command=command)
                sock.send()
            except:
                raise SystemError("Maybe Guerilla is closed ? ")
        if pmc.window('exportabc', exists=True):
            pmc.deleteUI('exportabc')
    marilla.marillaUi.ui_export_selection(exec_button)

def api_help(*args):
    """open firefox for display marilla's api help
    """
    import webbrowser
    webbrowser.open("{0}/doc/build/html/marilla.html".format(os.path.dirname(__file__)))


def create_geurilla_submenu(menu):
    """create all submenu guerilla
    """
    gue = pmc.menuItem("guerilla", subMenu=True, label='Guerilla',
                                                 parent = menu)
    pmc.menuItem("autoTagsSelection", subMenu=False, label='Auto Tags Selection',
                                         parent=gue, command=auto_tags_selection)
    pmc.menuItem("removeTagsSelection", subMenu=False,
         label='Remove All Tags Selection' , parent=gue, command=remove_all_tags)
    pmc.menuItem("extraTagsSelection", subMenu=False, 
         label='Add / Remove extra tags Selection' , parent=gue, 
                                                         command=add_custom_tags)
    pmc.menuItem("exportSelection", subMenu=False, label='Export Abc Selection',
                                            parent=gue, command=export_selection)
    pmc.menuItem("apiHelp", subMenu=False, label='Api help',
                                            parent=gue, command=api_help)
