import os
import platform
import marilla.utils.sockette
import time


def create_port_from_guerilla():
    """Inside guerilla write a random port
    """
    rdport = marilla.utils.sockette.get_open_port()
    if platform.system() == 'Linux':
        tmpdir = os.environ['TMPDIR']
    elif platform.system() == 'Windows':
        tmpdir = os.environ['TMP']
    else:
        raise EnvironmentError("Bad platform system")
    tmpportfile = file(tmpdir+'//port', 'w')
    tmpportfile.write(str(rdport))
    tmpportfile.close()

if __name__ == '__main__':
    create_port_from_guerilla()
