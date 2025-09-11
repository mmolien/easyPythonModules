#!/usr/bin/python

'''
@summary: Facilitates generation and sending of email.
@author: michael.molien
@version: 1.0.0
@since: 2012.07.31
@copyright: 2012.07.31
@Create Date: 2012.07.31

Email to SMS Gateways:
    https://avtech.com/articles/138/list-of-email-to-sms-addresses/

'''

__author__      = "michael.molien"
__version__     = "1.1.1"
__copyright__   = "2012-07-31"
__license__     = "New-style BSD"


import smtplib
from email.mime.multipart   import MIMEMultipart
from email.mime.text        import MIMEText

# from modules.easyConfig import configParser

class easyMail:
    def __init__( self, env_map = {} ):
#        env_map['name'] = ''

        self._to_addr_list  = []
        self._to_addr       = ""
        self._from_addr     = ""
        self._from_pass     = ""
        self._subject       = ""
        self._message_txt   = ""
        self._message_htm   = ""
        self._sendmail_server = 'smtp.gmail.com'
        self._sendmail_port = '587'

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

    def Add_Recipient_list ( self, listValues = [] ):
        _tmp_list = []
        if isinstance( listValues, list ):
            _tmp_list = listValues
        for value in _tmp_list:
            self.Add_Recipient( value )
        self._to_addr = str( ', '.join( self._to_addr_list ) )
        return self._to_addr

    def Sender( self, value = None ):
        if ( value is not None ):
            self._from_addr = value
        return self._from_addr

    def Pass( self, value = None ):
        if ( value is not None ):
            self._from_pass = value
        return self._from_pass

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

    def SendmailPort( self, value = None ):
        if ( value is not None ):
            self._sendmail_port = value
        return self._sendmail_port

    def SendMail(self):
        result = '0'
        if ( self._from_addr is None ):     return 'From Value Not Set.'
        if ( self._to_addr is None ):       return 'Recipient Value Not Set.'
        if ( self._subject is None ):       return 'Subject Value Not Set.'

        msg = MIMEMultipart('alternative')
        msg['From']     = self._from_addr
        msg['To']       = self._to_addr
        msg['Subject']  = self._subject

        if self._message_txt != "": msg.attach( MIMEText(self._message_txt, 'plain') )
        if self._message_htm != "": msg.attach( MIMEText(self._message_htm, 'html') )

        try:
            # Start the server
            server = smtplib.SMTP( self._sendmail_server, self._sendmail_port )
            server.starttls()  # Secure the connection

            # Log in to your email account
            server.login( self._from_addr, self._from_pass )

            # Send the email
            result = server.send_message(msg)
            #print("Email sent successfully!")

        except Exception as e:
            print(f"Error: {e}")
        finally:
            server.quit()

        return result

def main():
    print("This class should not be executed directly.")

'''
# Example of use:
    Config     = configParser('..\tokens.json')
    _tokens    = Config.getConfig()

    mail = easyMail()
    mail.Sender( _tokens['email']['sender'] )
    mail.Pass( _tokens['email']['app'] )
    mail.Add_Recipient('test@mail.net')
    mail.Subject('Test')
    mail.MessageTEXT('Hello World!?')
    _result = mail.SendMail()

'''

if __name__ == "__main__":
    main()
