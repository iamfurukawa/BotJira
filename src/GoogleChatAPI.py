from httplib2 import Http
from json import dumps

class GoogleChatAPI:
    __url = '<WEBHOOK URL>'
    
    def sendMessage(self, message):
        """Send a message for a chat on Google Chat.

        Keyword arguments:
        message -- The message that will send.
        """
        
        '''
        If you want to send a message to a single thread, you must change the request body as specified below and change the thread name.

        bot_message = {
            'text' : message,
            'thread': {
                'name': '<Insert the thread name here!>'
            }
        }
        '''

        Http().request(
            uri = self.__url,
            method = 'POST',
            headers = { 'Content-Type': 'application/json; charset=UTF-8'},
            body = dumps({ 'text' : message }),
        )

        