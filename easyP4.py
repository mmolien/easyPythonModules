#!/usr/bin/python

'''
@summary: P4 helper class.
@author: michael.molien
@version: 1.0.0
@since: 2023.11.01
'''

__author__      = "michael.molien"
__version__     = "1.0.0"
__copyright__   = "2023-11-01"
__license__     = "New-style BSD"

from P4 import P4,P4Exception

class easyP4:
    def __init__( self, **kwargs ):
        self._P4 = P4()
        self._P4Client  = None
        self._P4Host    = 'p4-west.stoic.id'
        self._P4Port    = '1668' #"1666"
        self._P4User    = None
        self._P4Pass    = None
        self._P4Serv    = 'ssl:p4-west.stoic.id:1668'
        self._P4Conn    = None
        self._P4Command = []

    def __del__(self):
        self.P4Close()

    def P4Client(self, P4Client=None):
        if P4Client is not None : self._P4Client = str(P4Client)
        return self._P4Client

    def P4Host(self, P4Host=None):
        if P4Host is not None : self._P4Host = str(P4Host)
        return self._P4Host

    def P4Port(self, P4Port=None):
        if P4Port is not None : self._P4Port = str(P4Host)
        return self._P4Port

    def P4User(self, P4User=None):
        if P4User is not None : self._P4User = str(P4User)
        return self._P4User

    def P4Pass(self, P4Pass=None):
        if P4Pass is not None : self._P4Pass = str(P4Pass)
        return self._P4Pass

    def P4Serv(self, P4Serv=None):
        if P4Serv is not None :
            self._P4Serv = P4Serv
        else:
            self._P4Serv = ("ssl:%s:%d") % ( self.P4Host(), int( self.P4Port() ) )
        return self._P4Serv

    def P4Connect (self):
        try:
            self._P4 = P4()
#            _P4.host       = self.P4Host()
#            _P4.port       = self.P4Port()
#            _P4.user       = self.P4User()
#            _P4.password   = self.P4Pass()
#            _P4.client     = self.P4Client()
#            print("Try connect.")
            self._P4.connect()

#            print("Try login.")
#            _P4.run_login()
#            opened = self._P4.run_opened()

        except P4Exception:
            print( self._P4.errors )
            for e in self._P4.errors:          # Display errors
                print("%s" % (e) )
            return 0
        return self._P4

    def P4Close (self):
        try:
            self._P4.disconnect()
        except P4Exception:
            for e in self._P4.errors:          # Display errors
                print(e)
            return 0
        return 1

    def P4Run(self, cmd=[] ):
        results = []
        cmd = self.P4Command(cmd)
        try:
            results = self._P4.run( cmd )
        except P4Exception:
            for e in self._P4.errors:          # Display errors
                print(e)
        return results

    def P4FileLog(self, cmd ):
        results = 0
        try:
            results = self._P4.run_filelog( cmd )
        except P4Exception:
            for e in self._P4.errors:          # Display errors
                print(e)
        return results

    def P4Command( self, cmd_list = [] ):
        if type(cmd_list) == type(list()) :
            if (len(cmd_list) > 0 ):
                self._P4Command = cmd_list
        return self._P4Command

    def get_p4_change_results( self ):
        _ret_changes_list = []
        _command = self.P4Command()
        try:
            _ret_changes_list = self._P4.run( _command )
        except P4Exception:
            for e in self._P4.errors:          # Display errors
                print(e)
        return _ret_changes_list

    def get_changes_between_changelists( self, _repo, _first, _last):
        _command = [ "changes", '-l', '-L', '-s', 'submitted', f"//wt/{_repo}/...@{_first},{_last}" ]
        return self.P4Run( _command )

def main():
    print("This class should not be executed directly.")

if __name__ == "__main__":
    main()
