try:
    import pymel.core as pmc
except ImportError:
    pass

def ui_add_custom_tags(exec_add_button, exec_remove_button):
    """create ui window for add and remove guerilla tags
    """
    if pmc.window('extratags', exists=True):
        pmc.deleteUI('extratags')
    pmc.window('extratags', menuBar=True, width=200, height=50 )
    pmc.columnLayout()
    pmc.separator()
    pmc.text('title', label='extra tags, separated them by a coma : ')
    pmc.separator()
    pmc.textField('tags', width=200)
    pmc.separator()
    pmc.button('add', label='add', width=200, command=exec_add_button)
    pmc.separator()
    pmc.button('remove', label='remove', width=200, command=exec_remove_button)
    pmc.showWindow()

def ui_export_selection(exec_button):
    """create ui window for export to abc and guerilla
    """
    if pmc.window('exportabc', exists=True):
        pmc.deleteUI('exportabc')
    pmc.window('exportabc', menuBar=True, width=200, height=50 )
    pmc.columnLayout()
    pmc.radioCollection('framemode')
    pmc.radioButton('currentframe', label='Current frame')
    pmc.radioButton('timeslider', label='Time Slider')
    pmc.radioButton('startend', label='Start / End')
    pmc.separator()
    pmc.text(label='Start frame')
    pmc.intField('start')
    pmc.text(label='End frame')
    pmc.intField('end')
    pmc.separator()
    pmc.checkBox('preroll', label='Pre roll')
    pmc.intField('prerollstart')
    pmc.text(label='Step')
    pmc.floatField('step', value=1.0)
    pmc.separator()
    pmc.checkBox('guerilla', label='Send to Guerilla')
    pmc.separator()
    pmc.button('export', label='Export', width=250, c=exec_button)
    pmc.showWindow()
