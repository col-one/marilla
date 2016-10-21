import socket
import platform
import os

def get_open_port():
    """generate an empty port number and return it
        
        :returns: port number
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("",0))
    s.listen(1)
    port = s.getsockname()[1]
    s.close()
    return port

def read_tmp_port():
    """read port from tmp port file 
        
        todo:: wip
    """
    if platform.system() == 'Linux':
        tmpdir = os.environ['TMPDIR']
    elif platform.system() == 'Windows':
        tmpdir = os.environ['TMP']
    else:
        raise EnvironmentError("Bad platform system")
    tmpportfile = file(tmpdir+'//port', 'r')
    port = tmpportfile.read()
    tmpportfile.close()
    return int(port)

class SendCommand():
    """Send command to a server
    
        :type ip: string
        :param ip: ip of the local server
        :type port: int
        :param port: port number
        :type command: string
        :param command: command to execute by server
    """
    def __init__(self, ip='127.0.0.1', port=None, command=''):
        self.command = command
        if port is None:
            port = get_open_port()
        addr=(ip,port)
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(addr)
        self.data = None

    def send(self):
        """send the command to server
        """
        self.client.send(self.command)
        self.data = self.client.recv(1024)
        self.close()

    def close(self):
        """Close the protocol
        """
        self.client.close()
        print 'socket closed'