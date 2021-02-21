from . import Request
from .pools import create_pool, create_pool_category

import requests
import json

from hentai.hentai import Format, Hentai
from tqdm import tqdm


def get_global_info(Request: object) -> dict:
    """Retrieves general stats about the site

    Args:
        Request (object): Request object

    Returns:
        dict: JSON response
    """
    req = requests.get(f'{Request.api_url}/info', headers=Request.headers)
    return req.json()

def upload_nhentai_doujin(Request: object, nh_id: int, pool_creation: bool = False) -> tuple:
    """Uploads a doujin from nhentai using only its ID number

    Args:
        Request (object): Request object
        nh_id (int): The doujin ID, found commonly in the URL
        pool_creation (bool, optional): If True creates a pool with the doujin posts for better organization, name same as the doujin and in the doujinshi pool category. Defaults to False.

    Returns:
        tuple: Tuple with the IDs of the posts created
    """
    # More work for tag categories to work properly
    doujin = Hentai(nh_id)
    tags = [tag.name.replace(" ", "_") for tag in doujin.tag]
    artist = [f'{artist.name.replace(" ", "_")}' for artist in doujin.artist]
    title_tag = [f'{doujin.title((Format.Pretty)).replace(" ", "_").split("|")[0]}']
    parody_tag = [f'{parody.name.replace(" ", "_")}' for parody in doujin.parody]
    char_tag = [f'{character.name.replace(" ", "_")}' for character in doujin.character]
    category_tag = [f'{category.name.replace(" ", "_")}' for category in doujin.category]

    all_tags = tags + artist + title_tag + parody_tag + char_tag + category_tag + ['doujinshi']

    id_list = []

    for page in tqdm(doujin.pages):
        request_input = {
        "tags": all_tags,
        "safety": "unsafe",
        "contentUrl": page.url
        }
        json_input = json.dumps(request_input)
        req = requests.post(f'{Request.api_url}/posts', headers=Request.headers, data=json_input)

        json_response = req.json()
        id_list.append(json_response['id'])
    
    req = requests.get(f'{Request.api_url}/pool-category/doujinshi', headers=Request.headers)
    if req.json()["name"] == "PoolCategoryNotFoundError":
        create_pool_category(Request, 'doujinshi')

    if pool_creation == True:
        create_pool(Request, title_tag, category='doujinshi', posts=id_list)

    return tuple(id_list)