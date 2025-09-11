#!/usr/bin/python

'''
@summary: Creates HTTP(S) connection and does HTTP(S) transactions.
Allows multipart form posts.

@organization: 
@author: michael.molien
@version: 1.1.0
@since: 07.30.2012
'''

__author__ = "michael.molien"
__version__ = "1.2.0"
__copyright__ = "07.30.2012"
__license__ = "New-style BSD"

import os
import re

import httplib
import urllib
import json
import base64
import hashlib
import mimetypes
import mimetools

class easyHTTP:
    def __init__(self, *args, **kwargs):
        """
        @summary:
        Allows for an easier interface to make HTTP(S) requests.
        Class initialization can take the following as parameters:

        @param self: Class Object.
        @param *args: 1 sets defaults to Secure HTTPS mode. (Optional) (Legacy)
        @param *args: Path with Parameter string. e.g.: '/index.php?foo=bar&test=yes'
        @param *args: Fully qualified URL. e.g.: 'https://www.google.com/search?q=Fully%20qualified%20URL'

        @keyword Headers: Needs a map of all of the desired default headers.
        @keyword Method: Can be any valid HTTP method type. e.g. [ GET, POST, HEAD, PUT, ... ]
        @keyword Path: The remote resource path.
        @keyword PortNumber: The port number that the remote web service is running on. e.g. [ 80, 443, ... ]
        @keyword Protocol: The HTTP protocol to use. e.g. [ http, https ]
        @keyword Secure: Is expected to be a binary true false. e.g. [ 0, 1 ]
        @keyword ServerName: The DNS or IP address of the remote web service. e.g. [ www.google.com, 127.0.0.1 ]
        @keyword TimeOut: The time out duration in seconds to wait for the return result to begin. e.g. [ 60 ]

        Description:
          First code block
            - initializes all variables to default values.
          Second code block
            - iterates over "*args" parameter values to and processes each of the three type.
          Third code block
            - iterates over "**kwargs" parameter values and applies keyword values as defaults.

        """

        _allowed_keywords = [ 'Headers', 'Method', 'Path', 'PortNumber', 'Protocol', 'Secure', 'ServerName', 'TimeOut' ]

        self._TimeOut = 60
        self._Protocol = 'http'
        self._Secure = 0
        self._ServerName = 'localhost'
        self._PortNumber = 80
        self._Path = '/index.html'
        self._Method = 'GET'
        self._Headers = { "Content-type": "application/x-www-form-urlencoded; charset=UTF-8", "Accept":"application/json, text/javascript, */*", "Accept-Charset":"ISO-8859-1,utf-8;q=0.7,*;q=0.7" }
        self._Parameters = {}
        self._GETPARAMS = None
        self._POSTPARAMS = None

        if 'Method' in kwargs.keys():
            self._Method = kwargs['Method']
        for arg in args:
            if str(arg) in ['1', '0', 1, 0]:
                if str(arg) in ['1', 1]:
                    self._Secure = int(1)
                    self._PortNumber = 443
                    self._Protocol = 'https'

            elif  re.match(r"^(?P<proto>http[s]?)\:\/\/(?P<serverName>[^\/\:\?\#]+)(\:(?P<portNumber>\d+))?(?P<path>\/[^\?\#]*)?(\?(?P<parameters>.*))?", arg):
                m = re.match(r"^(?P<proto>http[s]?)\:\/\/(?P<serverName>[^\/\:\?\#]+)(\:(?P<portNumber>\d+))?(?P<path>\/[^\?\#]*)?(\?(?P<parameters>.*))?", arg)
                self._Protocol = m.group('proto')
                self._ServerName = m.group('serverName')
                self._PortNumber = m.group('portNumber')
                self._Path = m.group('path')
                if m.group('parameters'):
                    if 'GET' == self._Method:
                        self.setParameter(m.group('parameters'))
                    else:
                        self._Path = (m.group('path') + '?' + m.group('parameters'))

            elif re.match(r"^(?P<path>[^?]*)(?P<parameters>\?.*)?", arg):
                    m = re.match(r"^(?P<path>[^?]*)(?P<parameters>\?.*)?", arg)

                    self._Path = m.group('path')
                    if m.group('parameters'):
                        if self._Method == 'GET':
                            self.setParameter(m.group('parameters'))
                        else:
                            self._Path = (m.group('path') + '?' + m.group('parameters'))

        sortedKeyList = sorted(kwargs.keys())
        for kw in sortedKeyList:
            if kw in _allowed_keywords:
                if 'Headers' == kw:
                    self._Headers = kwargs['Headers']
                if 'Method' == kw:
                    self._Method = kwargs['Method']
                if 'Path' == kw:
                    self._Path = kwargs['Path']
                if 'PortNumber' == kw:
                    self._PortNumber = kwargs['PortNumber']
                if 'Protocol' == kw:
                    self._Protocol = kwargs['Protocol']
                if 'Secure' == kw:
                    self._Secure = kwargs['Secure']
                if 'ServerName' == kw:
                    self._ServerName = kwargs['ServerName']
                if 'TimeOut' == kw:
                    self._TimeOut = kwargs['TimeOut']
            else:
                print "Unknown KeyWord: [%s] = %s" % (kw, kwargs[kw])



    def setBasicAuthorization(self, username='', password=''):
        self._Headers['Authorization'] = "Basic %s" % base64.encodestring('%s:%s' % (username, password))[:-1]
        self._Headers['realm'] = "Auth required"

    def setProtocol(self, value=None):
        if (value is not None):
            self._Protocol = value
        return self._Protocol

    def setServerName(self, value=None):
        if (value is not None):
            self._ServerName = value
        return self._ServerName

    def setTimeOut(self, value=None):
        if (value is not None and type(1) == type(value)):
            self._TimeOut = value
        else:
            self._PortNumber = 80
        return self._PortNumber

    def setPortNumber(self, value=None):
        if (value is not None and type(1) == type(value)):
            self._PortNumber = value
        else:
            self._PortNumber = 80
        return self._PortNumber

    def setPath(self, value=None):
        if (value is not None):
            self._Path = value
        return self._Path

    def setParameter(self, *args):
        """
            setParameter
            @summary:
            Used for setting parameters during HTTP(S) transactions.
            Function can take the following as parameters:

            @param *args: Pre-formatted parameter string. e.g.: 'foo=bar&test=yes'
            @param *args: Map of key value pairs. e.g.: '{ 'foo':'bar', 'test':'yes' }'
            @param *args: Single set of Key Value parameter to be set. e.g.: '"foo", "bar"'

            Description:
            First code block normalizes all given possible structures into a map.
            Second code block iterates over parameter values to verify string format.

        """

        tmp_map = {}
        if (len(args) == 1 and '=' in args[0]):
            temp = args[0].split('&')
            for items in temp:
                tmp_list = items.split('=', 2)
                tmp_map[ tmp_list[0] ] = tmp_list[1]
        elif (len(args) == 1 and type(args[0]) == type({"type":"map"})):
            tmp_map = args[0]
        elif (args[0] is not None):
            tmp_map[ args[0] ] = args[1]
        else:
            pass

        for tmp_key in tmp_map.keys():
            tmp_val = tmp_map[ tmp_key ]
            if type(tmp_val) == type(unicode('')):
# UTF-8 normalizes all unicode characters to be in \xFF format. 128 char map.
                tmp_val = tmp_val.encode('utf-8')
# UTF-8 normalizes all unicode characters to be in \xFF format. 256 char map.
#                tmp_val = tmp_val.encode( 'latin-1' )
# UTF-8 normalizes all unicode characters to be in \xFF format. 1024 char map.
#                tmp_val = tmp_val.encode( 'windows-1252' )
            else:
                tmp_val = str(tmp_val)

            try:
                urllib.quote(tmp_val)
                self._Parameters[ tmp_key ] = tmp_val
            except Exception, e:
#                print "Error Encoding String: ['%s'] - %s" % ( tmp_val, e )
                assert "Error Encoding String: ['%s'] - %s" % (tmp_val, e)

        return 1

    def delParameter(self, key=None):
        if (key is not None):
            del self._Parameters[ key ]
        return 1

    def delAllParameter(self):
        self._Parameters = {}
        return 1

    def setHeader(self, key=None, value=None):
        if (key is not None):
            self._Headers[ key ] = value
        return 1

    def delHeader(self, key=None):
        if (key is not None):
            del self._Headers[ key ]
        return 1

    def _encode_multipart_formdata(self, fields):
        BOUNDARY = mimetools.choose_boundary()
        CRLF = '\r\n'
        L = []
        for key in fields:

            L.append('--' + BOUNDARY)
            if not os.path.isfile(str(fields[ key ])):
                L.append('Content-Disposition: form-data; name="%s"' % key)
                L.append('')
                L.append(str(fields[ key ]))
            else:
                myWordList = fields[ key ].split('/')
                L.append('Content-Disposition: form-data; name="%s"; filename="%s"' % (key, myWordList[-1]))
                L.append('Content-Type: %s' % self._get_content_type(fields[ key ]))
                L.append('')
                fh = open(str(fields[ key ]), "rb")
                L.append(fh.read())
                fh.close()
        L.append('--' + BOUNDARY + '--')
        L.append('')
        body = CRLF.join(L)
        content_type = 'multipart/form-data; boundary=%s' % BOUNDARY
        return content_type, body

    def _get_content_type(self, filename):
        return mimetypes.guess_type(filename)[0] or 'application/octet-stream'

    def postRequest(self):
        self._Method = 'POST'
        self._GETPARAMS = ''
        self._POSTPARAMS = urllib.urlencode(self._Parameters)
        return self._request()

    def postMultiPartRequest(self):
        self._Method = 'POST'
        content_type, body = self._encode_multipart_formdata(self._Parameters)
        self._GETPARAMS = ''
        self._POSTPARAMS = body
        self.setHeader("Content-type", content_type)
        ret = self._request()
        self.setHeader("Content-type", "application/x-www-form-urlencoded; charset=UTF-8")
        return ret

    def getRequest(self):
        self._Method = 'GET'
        self._GETPARAMS = urllib.urlencode(self._Parameters)
        self._POSTPARAMS = ''
        return self._request()

    def headRequest(self):
        self._Method = 'HEAD'
        self._GETPARAMS = urllib.urlencode(self._Parameters)
        self._POSTPARAMS = ''
        return self._request()

# conn = httplib.HTTPSConnection( self.ceServerName, self.cePortNumber )

    def _request(self):
        httpResp = None
        ret = {}
        if (str(self._Secure) != str(0) or self._Protocol == 'https'):
            if(self._PortNumber == 80): self._PortNumber = 443
            conn = httplib.HTTPSConnection(self._ServerName, self._PortNumber, timeout=self._TimeOut)
        else:
            conn = httplib.HTTPConnection(self._ServerName, self._PortNumber, timeout=self._TimeOut)
        qmark = ''
        if self._GETPARAMS is not None and self._GETPARAMS is not '': qmark = '?'
        self._UrlString = "%s%s%s" % (self._Path, qmark, self._GETPARAMS)

        try:
            conn.request(self._Method, self._UrlString, self._POSTPARAMS, self._Headers)
#            print 'URL:%s %s://%s:%s%s' % ( self._Method, self._Protocol, self._ServerName, self._PortNumber, self._UrlString )
        except Exception, e :
            print "httpStuff EXCEPTION: %s" % (str(e))
            print '++RESPONSE++'
            print 'URL:%s %s://%s:%s%s' % (self._Method, self._Protocol, self._ServerName, self._PortNumber, self._UrlString)

        try:
            httpResp = conn.getresponse()
            if httpResp.status == 401:
                if 'Authorization' in self._Headers:
                    m1 = self._Headers['Authorization'].split(' ')
                    print "regex pass: %s" % (m1[1])
                    try:
                        tmp_str = base64.urlsafe_b64decode(str(m1[1]))
                        print tmp_str
                    except Exception, e:
                        print e
            if httpResp.status == 301 or httpResp.status == 302 :
                tmpDict = dict(httpResp.getheaders())
                try:
                    m = re.match(r"^(?P<proto>http[s]?)\:\/\/(?P<serverName>[^\/\:\?\#]+)(\:(?P<portNumber>\d+))?(?P<path>\/[^\?\#]*)?(\?(?P<parameters>.*))?", tmpDict['location'])
#                    m = re.match( r"^(?P<proto>http[s]?)\:\/\/(?P<serverName>[^\/\:]+)\:?(?P<portNumber>\d*)(?P<path>[^?]*)(\?(?P<parameters>.*))?", tmpDict['location'] )
                    self.setProtocol(m.group('proto'))
                    self.setServerName(m.group('serverName'))
                    self.setPortNumber(m.group('portNumber'))
                except Exception, e:
                    m = re.match(r"^(?P<path>[^?]*)(?P<parameters>\?.*)?", tmpDict['location'])
#                print "%s:%s%s" % ( m.group('serverName'), m.group('portNumber'), m.group('path') )

                self.setPath(m.group('path'))
                if m.group('parameters'):
                    if self._Method == 'GET':
                        self.setParameter(m.group('parameters'))
                    else:
                        self.setPath(m.group('path') + '?' + m.group('parameters'))

                ret = self._request()
                if (str(self._Secure) != str(0)):
                    self.setProtocol('http')
                    self.setPortNumber(80)
                return ret
            tmp_body = httpResp.read()
            ret['reqURL'] = self._UrlString
            ret['reqBody'] = self._POSTPARAMS
            ret['head'] = httpResp.msg
            ret['header'] = dict(httpResp.getheaders())
            ret['code'] = httpResp.status
            ret['status'] = httpResp.reason
            ret['md5sum'] = hashlib.md5(tmp_body).hexdigest()
            try:
                ret['body'] = json.loads(tmp_body)
            except Exception, e:
                ret['body'] = tmp_body

        except Exception, e:
            print "httpStuff EXCEPTION: %s" % (str(e))
            print '++RESPONSE++'
            print 'URL:%s %s://%s:%s%s' % (self._Method, self._Protocol, self._ServerName, self._PortNumber, self._UrlString)
            if httpResp is not None:
                print '%s %s %s %s' % (httpResp.version, self._Method, httpResp.status, httpResp.reason)
                print httpResp.msg
                print httpResp.read()
            print '++++'
        conn.close()
        return ret

def main():
    print("This class should not be executed directly.")

if __name__ == "__main__":
    main()
