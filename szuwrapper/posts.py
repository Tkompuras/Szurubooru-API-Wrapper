from . import Request
import requests
from json import dumps
from urllib.parse import quote


def get_posts_id(Request: object, query: str) -> tuple:
    """Returns tuple of posts IDs returned from the specified query

    Args:
        Request (object): Request object
        query (str): Specific query, '*' as placeholder is supported

    Returns:
        tuple: Tuple with the IDs
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
        return tuple(ids_list)

def get_post(Request: object, post_id: int) -> dict:
    """Returns info about a specific post from its ID

    Args:
        Request (object): Request object
        post_id (int): The ID of the post

    Returns:
        dict: JSON response
    """
    req = requests.get(f'{Request.api_url}/post/{post_id}', headers=Request.headers)
    return req.json()

def delete_post(Request: object, post_id: int) -> None:
    """Delete a post using its ID

    Args:
        Request (object): Request object
        post_id (int): The post ID

    Returns:
        None
    """
    version_request = requests.get(f'{Request.api_url}/post/{post_id}', headers=Request.headers)
    json_response = version_request.json()
    request_body = {
        "version": json_response['version']
    }
    req = requests.delete(f'{Request.api_url}/post/{post_id}', headers=Request.headers, data=dumps(request_body))
    return None

def upload_post(Request: object, tags: list, safety: str, file_path: str) -> dict:
    """Upload a post

    Args:
        Request (object): Request post
        tags (list): List of tags
        safety (str): Safety tag. 'safe', 'sketchy', 'unsafe'
        file_path (str): The file path of the file to be uploaded

    Returns:
        dict: JSON response
    """
    metadata = {
        "tags": tags,
        "safety": safety
    }
    multipart_form_data = {
        'content': ('test.jpg', open(file_path, 'rb')),
        'metadata': dumps(metadata),
    }
    req = requests.post(f'{Request.api_url}/posts', headers=Request.headers, files=multipart_form_data)
    return req.json()
