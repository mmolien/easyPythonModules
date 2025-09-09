#!/usr/bin/python

'''
@author: michael.molien
@version: 1.0.0
@since: 07.30.2012
'''

__author__ = "michael.molien"
__version__ = "1.0.0"
__license__ = "New-style BSD"

from Crypto.Cipher import AES
import base64
import hashlib

class easyAES:
    def __init__( self ):
        self.aesKey = "1234567890123456"
        self.aesMode = AES.MODE_CBC
        self.srcStr = None
        self.encStr = None
        self.pickleStr = None
        self.md5Key = str( hashlib.md5( self.aesKey ).hexdigest() )
        self.saltIVStr = self.md5Key[0:len( self.aesKey )]
#        UTF8 = False
        __c = 0

#***
#   Getter / Setters
#***

# MODE_ECB = 1 #    Electronic Code Book (ECB). See blockalgo.MODE_ECB.
# MODE_CBC = 2 #    Cipher-Block Chaining (CBC). See blockalgo.MODE_CBC.
# MODE_CFB = 3 #    Cipher FeedBack (CFB). See blockalgo.MODE_CFB.
# MODE_PGP = 4 #    This mode should not be used.
# MODE_OFB = 5 #    Output FeedBack (OFB). See blockalgo.MODE_OFB.
# MODE_CTR = 6 #    CounTer Mode (CTR). See blockalgo.MODE_CTR.
# MODE_OPENPGP = 7 # OpenPGP Mode. See blockalgo.MODE_OPENPGP.

    def Mode( self, mode = 'cbc' ):
        my_mode_map = {
            'ecb':     AES.MODE_ECB,
            'cbc':     AES.MODE_CBC,
            'cfb':     AES.MODE_CFB,
#            'pgp':     AES.MODE_PGP,
            'ofb':     AES.MODE_OFB,
            'ctr':     AES.MODE_CTR,
#            'openpgp':     AES.MODE_OPENPGP,
        }

        if ( mode.lower() in my_mode_map.keys() ): # 32 byte key
            self.aesMode = my_mode_map[ mode.lower() ]
        else:
            self.aesMode = AES.MODE_CBC
        return 1

    def Key( self, aesKey = None ):
        if aesKey != None :
            self.aesKey = str( aesKey )
            self.md5Key = str( hashlib.md5( self.aesKey ).hexdigest() )
            self.saltIVStr = self.md5Key[0:len( self.aesKey )]
        return str( self.aesKey )

    def DecryptedString( self, srcStr = None ):
        if srcStr != None :
            self.srcStr = str( srcStr )
        return str( self.srcStr )

    def EncryptedString( self, encStr = None ):
        if encStr != None :
            self.encStr = str( encStr )
        return str( self.encStr )

    def SaltIVStr( self, saltIVStr = None ):
        if saltIVStr != None :
            self.saltIVStr = str( saltIVStr )
        return str( self.saltIVStr )

    def apKeySet( self, aesKey = None ):
        if aesKey != None :
            self.aesKey = str( aesKey )
            self.md5Key = str( hashlib.md5( self.aesKey ).hexdigest() )
            self.saltIVStr = self.md5Key[0:len( self.aesKey )]
        return str( self.aesKey )

#***
#   Functions
#***

    def encrypt( self, srcStr = None ):
        _buffer = self.DecryptedString( srcStr );
        blocksize = len( self.Key() )
        _buffer += ( blocksize - ( len( _buffer ) % blocksize ) ) * "\0";
        obj = AES.new( self.Key(), self.aesMode, self.SaltIVStr() )
        return self.EncryptedString( str( obj.encrypt( _buffer ) ) )

    def decrypt( self, encStr = None ):
        self.EncryptedString( encStr )
        obj = AES.new( self.Key(), self.aesMode, self.SaltIVStr() )
        return self.DecryptedString( obj.decrypt( self.EncryptedString() ) )

    def decode ( self, encStr = None ):
        self.EncryptedString( encStr )
        self.EncryptedString( self.b64decode( self.EncryptedString() ) )
        return self.decrypt()

    def encode ( self, srcStr = None ):
        self.DecryptedString( srcStr )
        self.encrypt()
        return self.EncryptedString( self.b64encode( self.EncryptedString() ) )

    def b64encode( self, string ):
        data = base64.b64encode( string )
        data += ( 4 - ( len( data ) % 4 ) ) * '='
        return data

    def b64decode( self, data ):
        data += ( 4 - ( len( data ) % 4 ) ) * '='
        return base64.b64decode( data )

    def str2hex( self, s ):
        lst = []
        for ch in s:
            hv = hex( ord( ch ) ).replace( '0x', '' )
            if len( hv ) == 1:
                hv = '0' + hv
            lst.append( 'x' + hv )
        return lst
