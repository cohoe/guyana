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

    # def _render_node(tag, children):
    #     return render_template('ingredients/tree/node.html', tag=tag, children=children, _render_node=_render_node)

    def _render_node(node):
        return render_template('ingredients/tree/node.html', node=node, _render_node=_render_node)

    # for key in tree.keys():
    #
    #
    doc = render_template('ingredients/tree/tree.html', tree=tree, _render_node=_render_node)

    return doc


if __name__ == '__main__':
    app.run(debug=settings.FLASK_DEBUG, host='0.0.0.0', port=3000)
