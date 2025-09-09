#!/usr/bin/python

'''
@author: michael.molien
@version: 1.0.0
@since: 07.30.2012
'''

__author__ = "michael.molien"
__version__ = "1.0.0"
__license__ = "New-style BSD"

import zipfile
import os

class easyZipper:
    def __init__( self, zip_name = None ):

        self._archive_in_directory = None
        self._archive_out_directory = None
        self._archive_handle = None
        self._zip_file_name = None
        self._compression = zipfile.ZIP_STORED
        self._tmpFileName = None
        self._tmpFileData = None

        if zip_name is not None:
            self.ZipFileName( zip_name )
            if os.path.isfile( self.ZipFileName() ):
                self.OpenArchive()

    def __del__ ( self ):
        self.CloseArchive()

    def SourceDirectory( self, value = None ):
        return self.SrcDir( value )

    def SrcDir( self, value = None ):
        if value is not None:
            if os.path.isdir( value ):
                self._archive_in_directory = str( value )
            else:
                self._archive_in_directory = str( './' )
        return self._archive_in_directory

    def DestinationDirectory( self, value = None ):
        return self.DstDir( value )

    def DstDir( self, value = None ):
        if value is not None:
            if os.path.isdir( value ):
                self._archive_out_directory = str( value )
            else:
                try:
                    os.mkdir( value )
                    self._archive_out_directory = str( value )
                except Exception:
                    self._archive_out_directory = str( './' )
        return self._archive_out_directory

    def ZipFileName( self, value = None ):
        if value is not None:
            self._zip_file_name = str( value )
        return self._zip_file_name

    def SaveFile( self ):
        return self.WriteFile( self._tmpFileName, self._tmpFileData )

    def WriteFile( self, fileName = "", fileContent = "" ):
        try:
            myFile = open( fileName, "w" )
            myFile.write( fileContent )
            myFile.close()
        except( IOError, e ):
            print( f"There was an error writing to file '{fileName}'" )
            return 0
        return 1

    def ArchiveDirectory ( self ):
        zout = zipfile.ZipFile( self.ZipFileName(), "w" )
        for _fileName in os.listdir( self.SrcDir() ):
            _fullFileName = os.path.join( self.SrcDir(), _fileName )
            if os.path.isfile( _fullFileName ):
#                print "File: %s Fullname: %s" % ( fname, _fullFileName )
                zout.write( _fullFileName, _fileName, self._compression )
        zout.close()

    def OpenArchive ( self, value = None ):
        if self._archive_handle is not None:
            self.CloseArchive()
        if value is not None:
            self.ZipFileName( value )
        if os.path.isfile( self.ZipFileName() ):
            if zipfile.is_zipfile( self.ZipFileName() ):
                self._archive_handle = zipfile.ZipFile( self.ZipFileName(), "r" )
                return self._archive_handle

    def CloseArchive( self ):
        if self._archive_handle is not None:
            self._archive_handle.close()
            self._archive_handle = None

    def InArchive ( self, value = None ):
        if value is None:
            return None
        if self._archive_handle is not None:
            try:
                _zipInfo = self._archive_handle.getinfo( str( value ) )
                self._tmpFileName = str( value )
                return _zipInfo
            except KeyError:
                return None
        return None

    def ListArchive ( self ):
        out_list = []
        for item in self._archive_handle.infolist():
            out_list.append( item.filename )
        return out_list


    def AddToArchive ( self, filename, NameInArchive = None ):
        if os.path.isfile( filename ):
            return self._archive_handle.write( filename, NameInArchive, self._compression )
        return None
    def ReadFromArchive ( self, value = None ):
        _zipInfo = self.InArchive( value )
        if _zipInfo is not None:
            self._tmpFileName = str( value )
            _tmpFile = self._archive_handle.open( _zipInfo ).read()
            self._tmpFileData = _tmpFile
#            if type( _tmpFile ) == type( str ):
#                print _tmpFile
#                pass
            return _tmpFile
        return None
