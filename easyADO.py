#!/usr/bin/python

'''
@summary: Allows for the creation of work tickets in the Azure Dev Ops system.

@author: michael.molien
@version: 1.2.0
@since: 06.01.2021
'''

__author__      = "michael.molien"
__version__     = "1.2.0"
__copyright__   = "2021 06 01"
__copyright__   = "2023 06 20"
__license__     = "New-style BSD"

import sys
import os
import re
import binascii
import requests
import base64

class easyADO:

    def __init__( self, **kwargs ):
        self._work_item_id      = -1
        self._azureURL          = "https://dev.azure.com/"
        self._organization      = "msbelfry"
        self._project           = "Belfry" # [ Sandbox | Belfry ]
        #   https://docs.microsoft.com/en-us/rest/api/keyvault/get-key/get-key
        self._PAToken           = "" # end points
        self._title             = "python script made this"
        self._work_item_type    = "Bug" # [ Task | Bug ]
        self._data              = []
        self._DEBUG             = 0

        _url        = self.URL()
        _method     = self.Method()
        _headers    = self.Headers()
        _param      = self.Params()
        _data       = self.Data()
        _backoff    = self._backoff
        _retry      = self._retry


    def __del__(self):
        pass

    def DEBUG( self, value = 0 ):
        """
            DEBUG
            @summary:
            Used to Get or Set the Value of the DEBUG flag.

            @param self, instance of class.
            @param value, equals either 0 or 1.

            Description:
            DEBUG will cause additonal logging to the console.
            Detects if value passed is in the allowed list. If it is the value of DEBUG will be updated.
            Value of DEBUG is returned.
        """
        if( value in [ 0, 1 ] ):
            self._DEBUG = value
        return self._DEBUG

    def AzureURL( self, value = None ):
        """
            AzureURL
            @summary:
            Used to Get or Set the Value of the Azure Dev Ops Base URL.

            @param self, instance of class.
            @param value, Default value is 'https://dev.azure.com/'.

            Description:
            Detects if value passed is in the allowed list. If it is the value of DEBUG will be updated.
            Value of DEBUG is returned. When enabled DEBUG will cause additonal logging to the console.
        """
        if( value is not None ):
            self._azureURL = value
        return self._azureURL

    def Organization( self, value = None ):
        if( value is not None ):
            self._organization = value
        return self._organization

    def Project( self, value = None ):
        if( value in [ "Sandbox", "Belfry" ] ):
            self._project = value
        return self._project

    def PAToken( self, value = None ):
        if( value is not None ):
            self._PAToken = value
        return self._PAToken

    def Title( self, value = None ):
        if( value is not None ):
            self._title = value
        return self._title

    def WorkItemTypes( self, value = None ):
        if( value in ["Bug","Task"] ):
            self._work_item_type = value
        return self._work_item_type

    def AddField( self, name = None, value = None ):
        if( name is None ):
            return 0
        if( value is None ):
            return 0

        _temp = {
             "op": "add",
             "path": "/fields/%s" % (name),
             "value": value
        }

        self._data.append( _temp )
        #print( _temp  )

    def SearchWorkItembyState( self, searchtext = None ):

        # _wiql = f"SELECT [System.Id] FROM WorkItemLinks WHERE ([Source].[System.Id] = {searchtext}) And ([System.Links.LinkType] = 'System.LinkTypes.Hierarchy-Reverse') And ([Target].[System.WorkItemType] = 'Feature') ORDER BY [System.Id] mode(MustContain"

        _wiql = f"Select [System.Id], [System.Title], [System.State] From WorkItems Where [System.State] = '{searchtext}'"
        return self.SearchWIQL( _wiql )

    def SearchWorkItem( self, searchtext = None ):
        # _wiql = "Select [System.Id], [System.Title], [System.State] From WorkItems Where [Custom.PyLogHashVal] = %s AND [System.Project] = %s" % ( searchtext, self._project )
        _wiql = f"Select [System.Id], [System.Title], [System.State] From WorkItems Where [Custom.PyLogHashVal] = {searchtext}"
        returned = self.SearchWIQL( _wiql )
        if( 'workItems' in returned.keys() ):
            if( len( returned['workItems'] ) > 0 ):
                self._work_item_id = returned['workItems'][0]['id']
                return 0
        return 1

    def ReadWorkItem( self, workItemID = 1 ):
        _wiql = f"Select [System.Id], [System.Title], [System.State], [System.AreaPath], [System.NodeName] From WorkItems Where [System.Id] = {workItemID}"
        returned = self.SearchWIQL( _wiql )
        if( 'workItems' in returned.keys() ):
            if( len( returned['workItems'] ) > 0 ):
                return returned['workItems'][0]
        return 0

    def SearchWIQL( self, wiql = None ):
        #  - https://docs.microsoft.com/en-us/rest/api/azure/devops/wit/wiql/query%20by%20wiql?view=azure-devops-rest-6.0
        #  POST https://dev.azure.com/fabrikam/_apis/wit/wiql?api-version=6.0
        #    {
        #        "query": "Select [System.Id], [System.Title], [System.State] From WorkItems Where [System.WorkItemType] = 'Task' AND [State] <> 'Closed' AND [State] <> 'Removed' order by [Microsoft.VSTS.Common.Priority] asc, [System.CreatedDate] desc"
        #    }

        _ret = []
        if(wiql != None):
            url = "%s/%s/%s/_apis/wit/wiql?api-version=6.0" % ( self._azureURL, self._organization, self._project)
            search_data = { "query": wiql }
            r = requests.post( url, json=search_data, headers={'Content-Type': 'application/json'}, auth=('', self._PAToken) )

            #basic_auth = 'mmolien' + ":" + self._PAToken
            #auth_token = 'Basic '+ base64.b64encode( basic_auth.encode('utf-8'))
            #r = requests.post( url, json=search_data, headers={'Content-Type': 'application/json'}, auth=('', auth_token) )


            if( self._DEBUG == 1):
                print(":: URL ::")
                print( url )
                print( r )
                print(":: SENT ::")
                print( search_data )
                print(":: RECEIVED ::")
                print( r.json() )
                print( "Search Code: " + str( r.status_code ) )

            if( r.status_code == 200 ):
                _ret = r.json()

        return _ret


    def ReadWorkItemAreaPath( self, workItemID = 1, FieldName = 'System.AreaPath' ):
        # https://learn.microsoft.com/en-us/rest/api/azure/devops/wit/work-items/get-work-item?view=azure-devops-rest-6.0&tabs=HTTP
        url = "%s/%s/%s/_apis/wit/workitems/%s?fields=%s,%s,%s&api-version=6.0" % ( self._azureURL, self._organization, self._project, workItemID, FieldName, 'System.WorkItemType', 'System.State' )
        try:
            r = requests.get( url, headers={'Content-Type': 'application/json'}, auth=('', self._PAToken) )
        except requests.exceptions.Timeout:
            # Maybe set up for a retry, or continue in a retry loop
            print( url )
            return 0

        except requests.exceptions.TooManyRedirects:
            # Tell the user their URL was bad and try a different one
            print( url )
            return 0

        except requests.exceptions.RequestException as e:
            print( url )
            print( e )
            return 0
        #basic_auth = 'mmolien' + ":" + self._PAToken
        #auth_token = 'Basic '+ base64.b64encode( basic_auth.encode('utf-8'))
        #r = requests.post( url, json=search_data, headers={'Content-Type': 'application/json'}, auth=('', auth_token) )

        if( self._DEBUG == 1):
            print(":: URL ::")
            print( url )
            print( r )
            print(":: RECEIVED ::")
            print( "Search Code: " + str( r.status_code ) )
            print( r )
        if( r.status_code == 200 ):
#            print( r.json() )
            returned = r.json()
            if( 'fields' in returned.keys() ):
                if( len( returned['fields'] ) > 0 ):
                    return returned['fields']
        return 0


    def EditWorkItem( self, workItemID = 0 ):
        url = "%s/%s/%s/_apis/wit/workitems/%s?api-version=5.1" % ( self._azureURL, self._organization, self._project, self._work_item_id )
        _temp = {
             "op": "test",
             "path": "/fields/System.WorkItemType",
             "value": self._work_item_type
        }
        self._data.append( _temp )

        r = requests.patch(url, json=self._data, headers={'Content-Type': 'application/json-patch+json'}, auth=('', self._PAToken))

        if( self._DEBUG == 1 ):
            print(":: URL ::")
            print( url )
            print(":: SENT ::")
            print( self._data )
            print(":: RECEIVED ::")
            print( r.json() )
            print( "Edit Code: " + str( r.status_code ) )
        if( r.status_code != 200 ):
            print(":: URL ::")
            print( url )
            print(":: SENT ::")
            print( self._data )
            print(":: RECEIVED ::")
            print( r.json() )


    def CreateWorkItem( self ):
        url = "%s/%s/%s/_apis/wit/workitems/$%s?api-version=5.1" % ( self._azureURL, self._organization, self._project, self._work_item_type )

        r = requests.post(url, json=self._data, headers={'Content-Type': 'application/json-patch+json'}, auth=('', self._PAToken))
        if( self._DEBUG == 1 ):
            print(":: URL ::")
            print( url )
            print(":: SENT ::")
            print( self._data )
            print(":: RECEIVED ::")
            print( r.json() )
            print( "Create Code: " + str( r.status_code ) )
        if( r.status_code != 200 ):
            print(":: URL ::")
            print( url )
            print(":: SENT ::")
            print( self._data )
            print(":: RECEIVED ::")
            print( r ) #<Response [401]>  == PAT is expired.
#            print( r.json() )

    def CommentAdd( self, comment = None ):
        # POST https://dev.azure.com/{organization}/{project}/_apis/wit/workItems/{workItemId}/comments?api-version=6.0-preview.3
        url = "%s/%s/%s/_apis/wit/workitems/%s?api-version=5.1" % ( self._azureURL, self._organization, self._project, self._work_item_id )
        _temp = {
             "text": "test"
        }
        self._data.append( _temp )

        if(comment == None): return
        r = requests.patch(url, json=self._data, headers={'Content-Type': 'application/json-patch+json'}, auth=('', self._PAToken))

        if( self._DEBUG == 1 ):
            print(":: URL ::")
            print( url )
            print(":: SENT ::")
            print( self._data )
            print(":: RECEIVED ::")
            print( r.json() )
            print( "Edit Code: " + str( r.status_code ) )
        if( r.status_code != 200 ):
            print(":: URL ::")
            print( url )
            print(":: SENT ::")
            print( self._data )
            print(":: RECEIVED ::")
            print( r.json() )

    def Method( self, value='' ):
        allowed_method_list = ['GET','POST','PUT','DELETE','HEAD','PATCH']
        if ( value.upper() in allowed_method_list ):
            self._method = value.upper()
        return self._method


    def URL( self, value=None ):
        if (value is not None):
            self._url = value
        return self._url


    def Headers( self, value=None ):
        if ( value is not None ):
            self._headers = value
        return self._headers


    def Params( self, value=None ):
        if ( value is not None ):
            self._params = value
        return self._params

    def Data( self, value=None ):
        if ( value is not None ):
            self._data = value
        return self._data


    def Requestor( self ):
        if( self._DEBUG):
            # FOR DEBUG ONLY
            import logging
            try:
                import http.client as http_client
            except ImportError:
                # Python 2
                import httplib as http_client
            http_client.HTTPConnection.debuglevel = 1

            # You must initialize logging, otherwise you'll not see debug output.
            logging.basicConfig()
            logging.getLogger().setLevel(logging.DEBUG)
            requests_log = logging.getLogger("requests.packages.urllib3")
            requests_log.setLevel(logging.DEBUG)
            requests_log.propagate = True
            # FOR DEBUG ONLY


        _url        = self.URL()
        _method     = self.Method()
        _headers    = self.Headers()
        _param      = self.Params()
        _data       = self.Data()
        _backoff    = self._backoff
        _retry      = self._retry

        _lresponse   = None

        for _try in range( _retry ):
            try:
                _resp = requests.request( _method, _url, params=_param, headers=_headers, json=_data )
                self.LogEvent( f"Method:{_method}, URL: {_url}, params={_param}, headers={_headers}, json={_data} \n \n", 'INFO' )

                if _resp.status_code in [ 200 ]:
                    self.LogEvent( f"Response Code:{_resp.status_code} Response:{_resp.json()} \n\n", 'INFO' )
                    return _resp

                elif _resp.status_code in self._status:
                    delay =  ( _backoff * _try )
                    time.sleep( delay )
                    _lresponse = _resp
                    continue

                else:
                    self.LogEvent( f"Response Code:{_resp.status_code} Not Found in Status:{self._status} \n\n", 'WARN' )
                    return _resp

            except requests.exceptions.ConnectionError:
                pass

        return _lresponse


def main():
    print("This class should not be executed directly.")

if __name__ == "__main__":
    main()
