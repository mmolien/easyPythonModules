#!/usr/bin/python

'''
@author: michael.molien
@version: 1.0.0
@since: 07.30.2012
'''

__author__ = "michael.molien"
__version__ = "1.0.0"
__license__ = "New-style BSD"

from xml.dom import minidom
import os

class easyConfig:
    def __init__( self, configFile = "../envConfig/config.xml" ):
        self.cfgFile = configFile
        if not os.path.isfile( configFile ):
            self.cfgFile = "./envConfig/config.xml"
        self.config = minidom.parse( self.cfgFile )

    def getConfigValue( self, tagName = 'root' ):
        if tagName == 'active':
            if 'ACTIVE_OVERIDE' in os.environ and os.environ['ACTIVE_OVERIDE'] is not None:
                return os.environ['ACTIVE_OVERIDE']

        return self._getText( self.config.getElementsByTagName( tagName )[0] )

    def _getText( self, Node ):
        try:
            if Node.nodeType == Node.TEXT_NODE:
                return Node.wholeText
            elif Node.nodeType == Node.ELEMENT_NODE:
                rc = []
                for subNode in Node.childNodes:
                    rc.append( self._getText( subNode ) )
                return ''.join( rc )
            else:
                return ''
        except( Exception, e ):
            print( "XML DOM ERROR: %s :: %s" % ( type( Node ), Node ) )

    def getGroupInfo( self, parentName, tagName ):
        NodeList = self.config.getElementsByTagName( parentName )
        for NodeSr in NodeList :
            if NodeSr.attributes['name'].value == tagName :
                if NodeSr.nodeType == NodeSr.ELEMENT_NODE:
                    retMap = {}
                    for NodeJr in NodeSr.childNodes:
                        retMap[ NodeJr.localName ] = self._getText( NodeJr )
                    return retMap
                return self._getText( NodeSr )
#            return { 'host':'', 'user':'', 'pass':'', 'name':'' }
        return { 'host':'', 'user':'', 'pass':'', 'name':'' }
