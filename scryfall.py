import http.client
import json
import requests

"""
Quick overview of the json dump:
~ aka what might be helpful ~

GENERAL INFO
- name:                     name of the card
- released_at:              date of release
- scryfall_uri:             link to the scryfall entry
- image_uris:               specific jpg/png of the card
    - small / normal / large
    - png / art_crop / border_crop

GAMEPLAY INFO
- mana_cost, cmc
- type_line
- oracle_text
- colors, color_identity
- keywords
- legalities
- rulings_uri

FINISH/QUALITY
- foil, nonfoil, finishes, 
- oversized, promo, reprint, variation
- rarity
- artist, artist_ids
- border_color, frame, security_stamp, full_art, textless, 

SET-INFO
- set_id, set, set_name, set_type, set_uri
- collector_number

OTHER SITES
- edhrec_rank
- penny_rank
- prices
    - usd, usd_foil, usd_etched

"""

test_id = "3364dd1b-df21-48a9-9059-f26b992ce7af"  # the card ~Absorb~


# using http.client
def get_sf_card(scryfall_id: str):
    api_short = 'api.scryfall.com'
    headers = {
        "User-Agent": "MTGExampleApp/1.0",  # Your app's name and version
        "Accept": "application/json;q=0.9,*/*;q=0.8"  # Generic preference for JSON
    }
    api_conn = http.client.HTTPSConnection(api_short)
    endpoint = '/cards/' + scryfall_id
    api_conn.request("GET", endpoint, headers=headers)
    response = api_conn.getresponse()
    out = response.read().decode()
    api_conn.close()
    return out


# requests version
def get_scry_card(scryfall_id: str):
    api_short = 'api.scryfall.com'
    headers = {
        "User-Agent": "MTGExampleApp/1.0",  # Your app's name and version
        "Accept": "application/json;q=0.9,*/*;q=0.8"  # Generic preference for JSON
    }
    address = "https://" + api_short + '/cards/' + scryfall_id
    response = requests.get(address, headers=headers).json()
    return response


# more directly grab the image for display
def get_card_image(card_id: str, image_type):
    """
    :param card_id: scryfall id
    :param image_type: one of {small, normal, large, png, art_crop, border_crop}
    :return: image link
    """
    info = json.loads(get_sf_card(card_id))
    if info.get('card_faces'):
        if info.get('card_faces').__len__() >= 2:
            return info.get('card_faces')[0].get('image_uris').get(image_type)
    return info.get('image_uris').get(image_type)


# more directly grab the price
def get_card_prices(card_id: str):
    info = json.loads(get_sf_card(card_id))
    usd = info.get('prices').get('usd')
    usd_hollow = info.get('prices').get('usd_foil')
    purchase_uri = info.get('purchase_uris').get('tcgplayer')
    scryfall_uri = info.get('scryfall_uri')
    return usd, usd_hollow, purchase_uri, scryfall_uri

# -----------------------------------
# extraction json info

# jsonx = json.loads(get_sf_card(test_id))
# jsonx.get("name")

# print(json.dumps(jsonx, indent=2))
# jsonx.get("image_uris").get("normal")
