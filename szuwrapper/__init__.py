import base64

class Request():
    """A class representing requests to be sent to the Szurubooru API, containing the required headers.

    Attributes:
        `api_url : str`
            the url to make the api calls to, default `http://localhost:8080/api`
        `headers : dict`
            the required headers for every call
    """
    def __init__(self, username: str, token: str, api_url: str):
        """Constructs the necessary attributes

        Args:
            username (str): the account username in the szurubooru server
            token (str): login token found in the account tab
            api_url (str): the url to make the api calls to, default `http://localhost:8080/api`
        """
        auth_message = f'{username}:{token}'
        auth_message_ascii = auth_message.encode('ascii')
        auth_message_base64 = base64.b64encode(auth_message_ascii)
        auth_message_decoded = auth_message_base64.decode('ascii')

        self.api_url = api_url

        self.headers = {
            'Authorization': 'Token ' + auth_message_decoded,
            'Accept': 'application/json'
        }