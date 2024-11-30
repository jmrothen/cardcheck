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


# Results

print(get_sf_card(test_id))
print(get_scry_card(test_id))

# extraction json info

jsonx = json.loads(get_sf_card(test_id))
jsonx.get("name")

print(json.dumps(jsonx, indent=2))


jsonx.get("image_uris").get("normal")

api_conn.close()
