import http.client
import json
import requests

api_short = 'api.scryfall.com'
headers = {
    "User-Agent": "MTGExampleApp/1.0",  # Your app's name and version
    "Accept": "application/json;q=0.9,*/*;q=0.8"  # Generic preference for JSON
}

test_id = "3364dd1b-df21-48a9-9059-f26b992ce7af"  # the card ~Absorb~
api_conn = http.client.HTTPSConnection(api_short)


# using http.client
def get_sf_card(scryfall_id: str):
    endpoint = '/cards/' + scryfall_id
    api_conn.request("GET", endpoint, headers=headers)
    response = api_conn.getresponse()
    out = response.read().decode()

    return out


# requests version

def get_scry_card(scryfall_id: str):
    address = "https://" + api_short + '/cards/' + scryfall_id
    response = requests.get(address, headers=headers).json()
    return response


# -----------------------------------

# extraction json info

jsonx = json.loads(get_sf_card(test_id))
jsonx.get("name")

print(json.dumps(jsonx, indent=2))


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

jsonx.get("image_uris").get("normal")

api_conn.close()
