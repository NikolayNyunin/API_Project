from flask import Flask, request, render_template

from maps import info_from_address, url_from_params
from wiki import search

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@app.route('/')
@app.route('/map_search', methods=['GET', 'POST'])
def map_search():
    text = request.args.get('search')
    if text:
        try:
            long, lat, (width, height), full_address, postal_code = info_from_address(text)
            image_url = url_from_params(long, lat, width, height)
            return render_template('map_search.html', title='Поиск на карте',
                                   image=image_url, address=full_address, code=postal_code)
        except Exception as e:
            return render_template('map_search.html', title='Поиск на карте',
                                   error='Ошибка: {}'.format(e))
    else:
        return render_template('map_search.html', title='Поиск на карте')


@app.route('/wiki_search')
def wiki_search():
    text = request.args.get('search')
    if text:
        try:
            data = search(text)
            if len(data) == 0:
                return render_template('wiki_search.html', title='Поиск в Википедии',
                                       error='Ничего не найдено')
            return render_template('wiki_search.html', title='Поиск в Википедии',
                                   data=data)
        except Exception as e:
            return render_template('wiki_search.html', title='Поиск в Википедии',
                                   error='Ошибка: '.format(e))
    else:
        return render_template('wiki_search.html', title='Поиск в Википедии')


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080)
