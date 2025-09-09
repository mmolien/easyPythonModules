#!/usr/bin/python

'''
Makes it easier to connect and interact with a MySQL database.
@author: michael.molien
@version: 1.0.0
@since: 07.30.2012
'''

__author__ = "michael.molien"
__version__ = "1.0.0"
__license__ = "New-style BSD"

import MySQLdb

class easyMySQL:
    def __init__(self, configName=None):

        self._DBName = "test"
        self._DBHost = "localhost"
        self._DBUser = "root"
        self._DBPass = "root"

        self._DBConn = None
        self._DBCStr = None
        self._DBCursor = None
        self._Action = None

    def __del__(self):
        self.dbClose()

### DATABASE - Stuff ###
    def setDatabaseName(self, DBName=None):
        if DBName is not None : self._DBName = str(DBName)
        return self._DBName

    def setDatabaseHost(self, DBHost=None):
        if DBHost is not None : self._DBHost = str(DBHost)
        return str(self._DBHost)

    def setDatabaseUser(self, DBUser=None):
        if DBUser is not None : self._DBUser = str(DBUser)
        return str(self._DBUser)

    def setDatabasePass(self, DBPass=None):
        if DBPass is not None : self._DBPass = str(DBPass)
        return str(self._DBPass)

    def dbConnect (self):
        if self._DBConn is None :
            self._DBConn = MySQLdb.connect(host=self._DBHost, user=self._DBUser, passwd=self._DBPass, db=self._DBName)
            self._DBCStr = "%s:%s:%s:%s" % (self._DBHost, self._DBUser, self._DBPass, self._DBName)
        else:
            if self._DBCStr != ("%s:%s:%s:%s" % (self._DBHost, self._DBUser, self._DBPass, self._DBName)):
                self.dbClose()
                self._DBConn = MySQLdb.connect(host=self._DBHost, user=self._DBUser, passwd=self._DBPass, db=self._DBName)
                self._DBCStr = "%s:%s:%s:%s" % (self._DBHost, self._DBUser, self._DBPass, self._DBName)
        return self._DBConn

    def dbClose (self):
        if self._DBConn is None :
            return 1
        else:
            try:
                self._DBConn.close ()
            except( MySQLdb.Error, e ):
                print( "Server: '%s' Database: '%s'." % (self._DBHost, self._DBName) )
                print( "Error %d: %s" % (e.args[0], e.args[1]) )
                return 0
        return 1

    def dbCursor(self):
        if self._DBCursor is not None :
            self._DBCursor.close()
        self.dbConnect()
        self._DBCursor = self._DBConn.cursor(MySQLdb.cursors.DictCursor)
        self._DBCursor.execute("SET AUTOCOMMIT=1")
        return self._DBCursor

    def dbExec(self, queryStr):
        results = []
        try:
            self.dbCursor()
            self._DBCursor.execute(queryStr)
            results = self._DBCursor.fetchall ()
            self._DBCursor.close ()
            self._DBConn.commit()
        except( MySQLdb.Error, e ):
            print( "MySQL ERROR - Server: %s Database: %s" % (self._DBHost, self._DBName) )
            print( str(e) )
            print( queryStr )
        return results
