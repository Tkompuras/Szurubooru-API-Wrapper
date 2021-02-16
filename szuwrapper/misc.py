from . import Request
import requests
import json
from hentai.hentai import Format, Hentai
from tqdm import tqdm

def get_global_info(Request):
    req = requests.get(f'{Request.api_url}/info', headers=Request.headers)
    json_response = req.json()
    return json.dumps(json_response, indent=4, sort_keys=True)

def download_nhentai_doujin(Request, nh_id):
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
        
        return id_list