import requests
import urllib.parse as urllib


def coords_from_address(toponym):
    geocoder_api_server = 'http://geocode-maps.yandex.ru/1.x/'
    geocoder_params = {'geocode': toponym, 'format': 'json'}

    response = requests.get(geocoder_api_server, params=geocoder_params)

    if not response:
        response.raise_for_status()

    json_response = response.json()
    toponym = json_response['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']
    toponym_coordinates = toponym['Point']['pos']
    toponym_longitude, toponym_latitude = toponym_coordinates.split()

    return float(toponym_longitude), float(toponym_latitude)


def info_from_address(toponym):
    geocoder_api_server = 'http://geocode-maps.yandex.ru/1.x/'
    geocoder_params = {'geocode': toponym, 'format': 'json'}

    response = requests.get(geocoder_api_server, params=geocoder_params)

    if not response: 
        response.raise_for_status()

    json_response = response.json()
    toponym = json_response['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']
    toponym_coordinates = toponym['Point']['pos']
    toponym_longitude, toponym_latitude = toponym_coordinates.split()

    lower_corner = toponym['boundedBy']['Envelope']['lowerCorner']
    lower_corner = list(map(float, lower_corner.split()))
    upper_corner = toponym['boundedBy']['Envelope']['upperCorner']
    upper_corner = list(map(float, upper_corner.split()))
    size = (abs(upper_corner[0] - lower_corner[0]),
            abs(upper_corner[1] - lower_corner[1]))

    full_address = toponym['metaDataProperty']['GeocoderMetaData']['Address']['formatted']
    if 'postal_code' in toponym['metaDataProperty']['GeocoderMetaData']['Address'].keys():
        postal_code = toponym['metaDataProperty']['GeocoderMetaData']['Address']['postal_code']
    else:
        postal_code = None

    return float(toponym_longitude), float(toponym_latitude), size, full_address, postal_code


def url_from_params(longitude, latitude, width=None, height=None, map_type='map', traffic=False, pts=None):
    map_api_server = 'http://static-maps.yandex.ru/1.x/'
    map_params = {
        'll': '{0},{1}'.format(longitude, latitude),
        'l': map_type,
        'spn': '{},{}'.format(width, height),
        'size': '650,450',
        'pt': '{},{},comma'.format(longitude, latitude)
    }

    if width is None or height is None:
        del map_params['spn']

    if traffic:
        map_params['l'] += ',trf'

    if pts:
        for pt in pts:
            map_params['pt'] += '~{},{},pm2gnm'.format(pt[0], pt[1])

    url = map_api_server + '?' + urllib.urlencode(map_params)

    return url


def organizations_from_coords(long, lat, org_type):
    search_api_server = "https://search-maps.yandex.ru/v1/"
    api_key = "dda3ddba-c9ea-4ead-9010-f43fbc15c6e3"

    search_params = {
        "apikey": api_key,
        "text": org_type,
        "lang": "ru_RU",
        "ll": "{0},{1}".format(long, lat),
        "type": "biz"
    }

    response = requests.get(search_api_server, params=search_params)

    if not response:
        response.raise_for_status()

    json_response = response.json()
    organizations = json_response["features"]

    return organizations
