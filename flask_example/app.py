from flask import Flask, jsonify
from authlib.flask.client import OAuth
from loginpass import create_flask_blueprint
from loginpass import OAUTH_BACKENDS

app = Flask(__name__)
app.config.from_pyfile('config.py')


class Cache(object):
    def __init__(self):
        self._data = {}

    def get(self, k):
        return self._data.get(k)

    def set(self, k, v, timeout=None):
        self._data[k] = v

    def delete(self, k):
        if k in self._data:
            del self._data[k]


# Cache is used for OAuth 1 services. You MUST use a real
# cache service like memcache/redis on production.
# THIS IS JUST A DEMO.
oauth = OAuth(app, Cache())


@app.route('/')
def index():
    tpl = '<li><a href="/{}/login">{}</a></li>'
    lis = [tpl.format(b.OAUTH_NAME, b.OAUTH_NAME) for b in OAUTH_BACKENDS]
    return '<ul>{}</ul>'.format(''.join(lis))


def handle_authorize(remote, token, user_info):
    return jsonify(user_info)


for backend in OAUTH_BACKENDS:
    bp = create_flask_blueprint(backend, oauth, handle_authorize)
    app.register_blueprint(bp, url_prefix='/{}'.format(backend.OAUTH_NAME))
