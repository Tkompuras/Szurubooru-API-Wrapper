import base64

class Request():

    def __init__(self, username, token, api_url):

        auth_message = f'{username}:{token}'
        auth_message_ascii = auth_message.encode('ascii')
        auth_message_base64 = base64.b64encode(auth_message_ascii)
        auth_message_decoded = auth_message_base64.decode('ascii')

        self.api_url = api_url

        self.headers = {
            'Authorization': 'Token ' + auth_message_decoded,
            'Accept': 'application/json'
        }