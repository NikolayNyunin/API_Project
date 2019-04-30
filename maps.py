import requests
import urllib.parse as urllib


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


def url_from_params(longitude, latitude, width, height, map_type='map', traffic=False):
    map_api_server = 'http://static-maps.yandex.ru/1.x/'
    map_params = {
        'll': '{0},{1}'.format(longitude, latitude),
        'l': map_type,
        'spn': '{},{}'.format(width, height),
        'size': '650,450',
        'pt': '{},{},comma'.format(longitude, latitude)
    }

    if traffic:
        map_params['l'] = map_params['l'] + ',trf'

    url = map_api_server + '?' + urllib.urlencode(map_params)

    return url
