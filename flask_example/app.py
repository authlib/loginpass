from flask import Flask, jsonify
from authlib.flask.client import OAuth
from loginpass import create_flask_blueprint
from loginpass import OAUTH_BACKENDS, Azure, create_azure_backend

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
    # As the Azure tenant name, e.g. 'common', is hard-coded
    # into the code of the 'azure.py' file, if a non-common
    # tenant is to be specified, it'll have to be specified
    # using the Azure values found in the config.py file.

    # If this backend is
    # NOT an Azure backend
    if backend.OAUTH_NAME != Azure.OAUTH_NAME:
        # initialize the blueprint of non-Azure backends as normal
        bp = create_flask_blueprint(backend, oauth, handle_authorize)
    # otherwise
    else:
        # re-initialize the Azure backend using
        # the Azure values found in the config.py file
        backend = create_azure_backend(Azure.OAUTH_NAME,
                                       app.config['AZURE_TENANT_NAME'],
                                       app.config['AZURE_OAUTH_VERSION'])
        # initialize the blueprint with the re-initialized Azure backend
        bp = create_flask_blueprint(backend, oauth, handle_authorize)
    # register the blueprint
    app.register_blueprint(bp, url_prefix='/{}'.format(backend.OAUTH_NAME))

if __name__ == '__main__':
    app.run(debug=True)
