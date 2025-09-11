#!/usr/bin/python

'''
@summary: Parse Config info from JSON file.
@author: michael.molien
@version: 1.1.0
@since: 2024.08.28
@update: 2024.11.13
'''

__author__      = "michael.molien"
__version__     = "1.1.0"
__copyright__   = "2024-08-28"
__license__     = "New-style BSD"

from xml.dom import minidom
import os
import json

class easyConfig:
    def __init__( self, configFile = "./tokens.json" ):
        self._cfgFile    = "./tokens.json"
        self._cfgRAW     = ''
        self._cfgJSON    = ''

        self.ConfigFile(configFile)


    def ConfigFile( self, path_file = None ):
        #print(f"ConfigFile: FilePath FileName: {path_file}")
        if path_file is not None:
            if os.path.isfile( path_file ): self._cfgFile = path_file
        return self._cfgFile


    def ConfigRaw( self, contents = None ):
        if contents is not None : self._cfgRAW = contents
        return self._cfgRAW


    def ConfigJson( self, contents = None ):
        if contents is not None : self._cfgJSON = contents
        return self._cfgJSON


    def getConfig( self ):
        self._cfgFP = open( self._cfgFile, "r" )
        self._cfgJSON = self.ConfigJson( json.load( self._cfgFP ) )
        self._cfgFP.close()
        return self._cfgJSON


    def setConfig( self, contents = None ):
        if contents is not None : self._cfgRAW = json.dumps(contents)
        elif len(self._cfgJSON) > 0 : self._cfgRAW = json.dumps(self._cfgJSON)
        return self._cfgRAW


    def putConfig( self ):
        self._cfgFP = open( self._cfgFile, "w" )
        if self._cfgFP:
            self._cfgFP.write( self._cfgRAW )
            self._cfgFP.close()


def main():
    print("This class should not be executed directly.")

if __name__ == "__main__":
    main()
