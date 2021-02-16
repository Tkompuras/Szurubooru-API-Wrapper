from . import Request
import requests
from json import dumps
from urllib.parse import quote

def get_tags_names(Request, query: str) -> list:
        initial_pos=0
        limit=50
        names_list = []

        req = requests.get(f'{Request.api_url}/tags/?offset={initial_pos}&limit={limit}&query={quote(query)}', headers=Request.headers)
        json_response = req.json()
        while json_response['offset'] < json_response['total']:
            for item in json_response['results']:
                names_list.append(item['names'])
            initial_pos += 50
            req = requests.get(f'{Request.api_url}/tags/?offset={initial_pos}&limit={limit}&query={quote(query)}', headers=Request.headers)
            json_response = req.json()
        else:
            return names_list

def delete_tag(Request, tag_name):
    version_request = requests.get(f'{Request.api_url}/tag/{quote(tag_name)}', headers=Request.headers)
    json_response = version_request.json()
    request_input = {
        "version": json_response['version']
    }
    json_input = dumps(request_input)
    req = requests.delete(f'{Request.api_url}/tag/{tag_name}', headers=Request.headers, data=json_input)

def get_tag_usages(Request, tag_name):
    req = requests.get(f'{Request.api_url}/tag/{quote(tag_name)}', headers=Request.headers)
    json_response = req.json()
    return json_response['usages']