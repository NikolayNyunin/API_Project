from flask import Flask, request, render_template, session

from maps import coords_from_address, info_from_address,\
    url_from_params, organizations_from_coords
from wiki import search_wiki

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@app.route('/', methods=['GET', 'POST'])
@app.route('/map_search', methods=['GET', 'POST'])
def map_search():
    if 'map_type' not in session:
        session['map_type'] = 'map'
        session['traffic'] = False
    if request.method == 'POST':
        session['map_type'] = request.form.get('map_type')
        traffic = request.form.get('trf')
        if traffic == 'trf':
            session['traffic'] = True
        else:
            session['traffic'] = False
    text = request.args.get('search')
    if text:
        try:
            long, lat, (width, height), full_address, postal_code = info_from_address(text)
            image_url = url_from_params(long, lat, width, height, session['map_type'], session['traffic'])
            return render_template('map_search.html', title='Поиск на карте',
                                   image=image_url, address=full_address,
                                   code=postal_code, text=text)
        except Exception as e:
            return render_template('map_search.html', title='Поиск на карте',
                                   error='Ошибка: {}'.format(e), text=text)
    else:
        return render_template('map_search.html', title='Поиск на карте')


@app.route('/wiki_search')
def wiki_search():
    text = request.args.get('search')
    if text:
        try:
            data = search_wiki(text)
            if len(data) == 0:
                return render_template('wiki_search.html', title='Поиск в Википедии',
                                       error='Ничего не найдено', text=text)
            return render_template('wiki_search.html', title='Поиск в Википедии',
                                   data=data, text=text)
        except Exception as e:
            return render_template('wiki_search.html', title='Поиск в Википедии',
                                   error='Ошибка: {}'.format(e), text=text)
    else:
        return render_template('wiki_search.html', title='Поиск в Википедии')


@app.route('/organization_search', methods=['GET', 'POST'])
def org_search():
    if 'map_type' not in session:
        session['map_type'] = 'map'
        session['traffic'] = False
    if request.method == 'POST':
        session['map_type'] = request.form.get('map_type')
        traffic = request.form.get('trf')
        if traffic == 'trf':
            session['traffic'] = True
        else:
            session['traffic'] = False
    text = request.args.get('search')
    if text:
        try:
            data = text.split('+')
            address = data[0].strip()
            org_type = data[1].strip()
            long, lat = coords_from_address(address)
            organizations = organizations_from_coords(long, lat, org_type)
            org_coords = [tuple(org['geometry']['coordinates']) for org in organizations]
            url = url_from_params(long, lat, map_type=session['map_type'],
                                  traffic=session['traffic'], pts=org_coords)
            return render_template('organization_search.html', title='Поиск по организациям',
                                   text=text, image=url)
        except Exception as e:
            return render_template('organization_search.html', title='Поиск по организациям',
                                   error='Ошибка: {}'.format(e), text=text)
    else:
        return render_template('organization_search.html', title='Поиск по организациям')


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080)
