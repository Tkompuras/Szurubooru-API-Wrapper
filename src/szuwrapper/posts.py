from .requests import Request
import requests
from json import dumps
from urllib.parse import quote


def get_posts_id(Request, query: str) -> list:
        """
        Returns a list containing the post ids corresponding to the query\n

        Positional arguments:\n
        query -- any supported query argument according to the Szurubooru API
        """
        initial_pos=0
        limit=100
        ids_list = []

        req = requests.get(f'{Request.api_url}/posts/?offset={initial_pos}&limit={limit}&query={quote(query)}', headers=Request.headers)
        json_response = req.json()
        while json_response['offset'] < json_response['total']:
            for item in json_response['results']:
                ids_list.append(item['id'])
            initial_pos += 100
            req = requests.get(f'{Request.api_url}/posts/?offset={initial_pos}&limit={limit}&query={quote(query)}', headers=Request.headers)
            json_response = req.json()
        else:
            return ids_list

def get_post(Request, post_id):
        req = requests.get(f'{Request.api_url}/post/{post_id}', headers=Request.headers)
        json_response = req.json()
        return json_response

def delete_post(Request, post_id):
        version_request = requests.get(f'{Request.api_url}/post/{post_id}', headers=Request.headers)
        json_response = version_request.json()
        request_input = {
            "version": json_response['version']
        }
        json_input = dumps(request_input)
        req = requests.delete(f'{Request.api_url}/post/{post_id}', headers=Request.headers, data=json_input)