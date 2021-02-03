import requests
import json
from flask import Flask, render_template, Response, stream_with_context, url_for
import settings

app = Flask(__name__)


# https://flask.palletsprojects.com/en/1.1.x/patterns/streaming/
# https://www.geeksforgeeks.org/use-yield-keyword-instead-return-keyword-python/
# https://flask.palletsprojects.com/en/1.1.x/quickstart/
# @app.route('/')
# def hello():
#     def generate_menus():
#         for menu in requests.get('http://localhost:8080/api/v1/drinklists/').json():
#             yield render_template('menu.html', menu=menu)
#
#     doc = render_template('menus.html', menus=generate_menus())
#     return doc

@app.route('/')
def get_tree():
    tree = requests.get('http://localhost:8080/api/v1/ingredients/tree').json()

    for tag, node in tree.items():
        print(tag)

    def _render_node(node):
        return render_template('ingredients/tree/node.html', node=node, _render_node=_render_node)

    doc = render_template('ingredients/tree/tree.html', tree=tree, _render_node=_render_node)

    return doc


@app.route('/me')
def me():
    inventories = json.loads(requests.get('http://localhost:8080/api/v1/inventories/').text)
    inventory_id = inventories[0].get('id')

    print("Found inventory ID %s" % inventory_id)

    recipes = json.loads(requests.get("http://localhost:8080/api/v1/inventories/%s/recipes/search" % inventory_id, params={'missing': 0}).text)

    # https://www.geeksforgeeks.org/ways-sort-list-dictionaries-values-python-using-lambda-function/
    sort = sorted(recipes, key=lambda x: x.get('hit').get('cocktail_slug'))

    return render_template('recipes/recipes.html', recipes=sort)


if __name__ == '__main__':
    app.run(debug=settings.FLASK_DEBUG, host='0.0.0.0', port=3000)
