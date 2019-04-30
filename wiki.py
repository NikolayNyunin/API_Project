import requests


def search_wiki(text):
    wiki_api_server = 'https://ru.wikipedia.org/w/api.php'
    wiki_params = {
        'action': 'opensearch',
        'format': 'json',
        'prop': 'info',
        'inprop': 'url',
        'search': text
    }

    response = requests.get(wiki_api_server, params=wiki_params)

    if not response:
        response.raise_for_status()

    data = response.json()
    res = []
    for i in range(len(data[1])):
        item = dict()
        item['title'] = data[1][i]
        item['description'] = data[2][i]
        item['link'] = data[3][i]
        res.append(item)

    return res
