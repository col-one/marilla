try:
    import pymel.core as pmc
except ImportError:
    pass

def abc_export(framemode='currentframe', qstart=0, qend=0, preroll=False,
                path='', preframe=0, nodes=[]):
    """wrapper the abcexport export abc file with abcexport maya command with
     some preset like uvwrite, world space, color groups, face groups

    :type framemode: string
    :param framemode: currentframe, timeslider, startend
    :type qstart: int
    :param qstart: precise start frame manualy for startend framemode option
    :type qend: int
    :param qend: precise end frame manualy for startend framemode option
    :type preroll: bool
    :param preroll: active a preroll compute frames
    :type preframe: int
    :param preframe: precise the preroll start frame
    :type nodes: list
    :param nodes: list of maya transform nodes
    :type path: string
    :param path: the alembic path file
    """
    if framemode == 'currentframe':
            start = int(pmc.currentTime(query=True))
            end = int(pmc.currentTime(query=True))
    elif framemode == 'timeslider':
        start = int(pmc.playbackOptions(q=True, ast=True))
        end = int(pmc.playbackOptions(q=True, aet=True))
    elif framemode == 'startend':
        start = qstart
        end = qend
    else:
        raise ValueError(("Wrong framemode, must be currentframe or timeslider"
                        " or startend"))
    if path == '':
        raise ValueError("Must precise a string path")
    prerollstring = ''
    if preroll:
        prerollstring = ('-frameRange {prerollstart} {startp} -step 1 -preRoll'
        ).format(prerollstart=preframe, startp=start-1)
    if len(nodes) == 0:
        raise ValueError("obj arg cant be an empty list of transform")
    objects = ''
    for obj in nodes:
        objects += ' -root |' + obj.name()
    abcstring = ('{prerollstring} -frameRange {start} {end} -attr GuerillaTags'
    ' -uvWrite -writeColorSets -writeFaceSets -worldSpace -dataFormat ogawa'
    ' {objects} -file {path}').format(
                    prerollstring=prerollstring, start=start, end=end, 
                    objects=objects, path=path)
    pmc.AbcExport(jobArg=abcstring, verbose=True)
    
