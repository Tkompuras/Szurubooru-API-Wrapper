from . import Request
import requests
from json import dumps
from urllib.parse import quote

def create_pool(Request: object, names: list, category: str = 'default', posts: list = []) -> dict:
    """Create pool

    Args:
        Request (object): Request object
        names (list): List of names, at least one. ['test']
        category (str, optional): Pool category. Defaults to 'default'.
        posts (list, optional): List of posts IDs to be included in the pool. Defaults to [].

    Returns:
        dict: JSON response
    """
    request_body = {
        "names": names,
        "category": category,
        "posts": posts
    }
    req = requests.post(f'{Request.api_url}/pool', headers=Request.headers, data=dumps(request_body))
    return req.json()

def create_pool_category(Request: object, name: str, color: str = '#00ffff') -> dict:
    """Create pool category

    Args:
        Request (object): Request object
        name (str): Name of the pool category
        color (str, optional): Hex color code. Defaults to '#00ffff'.

    Returns:
        dict: JSON response
    """
    request_body = {
            "name": name,
            "color": color
    }
    req = requests.post(f'{Request.api_url}/pool-categories', headers=Request.headers, data=dumps(request_body))
    return req.json()