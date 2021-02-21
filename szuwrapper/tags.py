from . import Request
import requests
from json import dumps
from urllib.parse import quote

def get_tags_names(Request: object, query: str) -> tuple:
    """Returns tuple of tags returned from the specified query

    Args:
        Request (object): Request object
        query (str): Specific query, '*' as placeholder is supported

    Returns:
        tuple: Tuple with the tag names
    """
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
        return tuple(names_list)

def delete_tag(Request: object, tag_name: str) -> None:
    """Deletes tag

    Args:
        Request (object): Request object
        tag_name (str): Tag name

    Returns:
        None
    """
    version_request = requests.get(f'{Request.api_url}/tag/{quote(tag_name)}', headers=Request.headers)
    json_response = version_request.json()
    request_body = {
        "version": json_response['version']
    }
    req = requests.delete(f'{Request.api_url}/tag/{tag_name}', headers=Request.headers, data=dumps(request_body))
    return None

def get_tag_usages(Request: object, tag_name: str) -> int:
    """Returns number of tag usages

    Args:
        Request (object): Request object
        tag_name (str): Tag name

    Returns:
        int: Number of usages
    """
    req = requests.get(f'{Request.api_url}/tag/{quote(tag_name)}', headers=Request.headers)
    json_response = req.json()
    return json_response['usages']

def create_tag(Request: object, tag_name: str, tag_category: str) -> dict:
    """Creates tag

    Args:
        Request (object): Request object
        tag_name (str): Tag name
        tag_category (str): Tag category of tag

    Returns:
        dict: JSON response
    """
    request_body = {
        "names": tag_name,
        "category": tag_category
    }
    req = requests.post(f'{Request.api_url}/tags', headers=Request.headers, data=dumps(request_body))
    return req.json()

def get_tag(Request: object, tag_name: str) -> dict:
    """Returns info about tag

    Args:
        Request (object): Request object
        tag_name (str): Tag name

    Returns:
        dict: JSON response
    """
    req = requests.get(f'{Request.api_url}/tag/{quote(tag_name)}', headers=Request.headers)
    return req.json()

def get_tag_categories(Request: object) -> dict:
    """Returns tag categories

    Args:
        Request (object): Request object

    Returns:
        dict: JSON response
    """
    req = requests.get(f'{Request.api_url}/tag-categories', headers=Request.headers)
    return req.json()

def create_tag_category(Request: object, name: str, color: str = '#00ffff', order: int = 0) -> dict:
    """Creates tag category

    Args:
        Request (object): Request object
        name (str): Name of tag category
        color (str, optional): Hex color code. Defaults to '#00ffff'.
        order (int, optional): Tag category order. Defaults to 0.

    Returns:
        dict: JSON response
    """
    request_body = {
        "name": name,
        "color": color,
        "order": order
    }
    req = requests.post(f'{Request.api_url}/tag-categories', headers=Request.headers, data=dumps(request_body))
    return req.json()