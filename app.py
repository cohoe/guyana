import requests
import json
from flask import Flask, render_template, Response, stream_with_context, url_for
app = Flask(__name__)


def _get_menus():
    return requests.get('https://jamaica.grantcohoe.com/api/v1/menus/').json()

# https://flask.palletsprojects.com/en/1.1.x/patterns/streaming/
# https://www.geeksforgeeks.org/use-yield-keyword-instead-return-keyword-python/
# https://flask.palletsprojects.com/en/1.1.x/quickstart/
@app.route('/')
def hello():

    def generate_menus():
        for menu in _get_menus():
            yield render_template('menu.html', display_name=menu.get('display_name'), items=menu.get('items'))
    doc = render_template('menus.html', menus=generate_menus())
    return doc


if __name__ == '__main__':
    app.run()
