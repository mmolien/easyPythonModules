#!/usr/bin/python

'''
Allow the easy generation and sending of email.
@author: michael.molien
@version: 1.0.0
@since: 07.31.2012
'''

__author__ = "michael.molien"
__version__ = "1.0.0"
__license__ = "New-style BSD"

import smtplib
from email.mime.multipart   import MIMEMultipart
from email.mime.text        import MIMEText

class easyMail:
    def __init__( self, env_map = {} ):
#        env_map['name'] = ''

        self._to_addr_list  = []
        self._to_addr       = ""
        self._from_addr     = "Test <no-reply@gmail.com>"
        self._subject       = "subject"
        self._message_txt   = ""
        self._message_htm   = ""
        self._sendmail_server = '127.0.0.1'

    def Remove_Recipient ( self, value = None ):
        if ( value is not None and value in self._to_addr_list ):
            self._to_addr_list.remove( value )
            self._to_addr.join( self._to_addr_list, ',')
        return self._to_addr

    def Add_Recipient ( self, value = None ):
        if ( value is not None and value not in self._to_addr_list ):
            self._to_addr_list.append( value )
            self._to_addr = str( ', '.join( self._to_addr_list ) )
        return self._to_addr

    def Sender( self, value = None ):
        if ( value is not None ):
            self._from_addr = value
        return self._from_addr

    def Subject( self, value = None ):
        if ( value is not None ):
            self._subject = value
        return self._subject

    def MessageTEXT( self, value = None ):
        if ( value is not None ):
            self._message_txt = value
        return self._message_txt

    def MessageHTML( self, value = None ):
        if ( value is not None ):
            self._message_htm = value
        return self._message_htm

    def SendmailServer( self, value = None ):
        if ( value is not None ):
            self._sendmail_server = value
        return self._sendmail_server

    def SendMail(self):
        if ( self._from_addr is None ): return 'From Value Not Set.'
        if ( self._to_addr is None ): return 'Recipient Value Not Set.'
        if ( self._subject is None ): return 'Subject Value Not Set.'
        msg = MIMEMultipart('alternative')
        msg['Subject'] = self._subject
        msg['From'] = self._from_addr
        msg['To'] = self._to_addr

        if self._message_txt != "": msg.attach( MIMEText(self._message_txt, 'plain') )
        if self._message_htm != "": msg.attach( MIMEText(self._message_htm, 'html') )

        s = smtplib.SMTP( self._sendmail_server )
#        s.starttls()
#        s.login("","")
        result = s.sendmail( self._from_addr, self._to_addr_list, msg.as_string() )
        s.quit()
        return result

if __name__ == '__main__':
    mail = easyMail()
    mail.Sender('')
    mail.Add_Recipient('')
    print( mail.Add_Recipient() )
    mail.Subject('Test')
    mail.MessageTEXT('Hello!?')
    print( mail.SendMail() )
