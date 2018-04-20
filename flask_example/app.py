from flask import Flask, jsonify
from authlib.flask.client import OAuth
from loginpass import create_flask_blueprint
from loginpass.twitter import Twitter
from loginpass.facebook import Facebook
from loginpass.google import Google
from loginpass.github import GitHub
from loginpass.dropbox import Dropbox
from loginpass.reddit import Reddit

OAUTH_BACKENDS = [
    Twitter, Facebook, Google, GitHub, Dropbox,
    Reddit
]

app = Flask(__name__)
app.config.from_pyfile('config.py')
oauth = OAuth(app)


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
