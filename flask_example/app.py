from flask import Flask, jsonify
from authlib.integrations.flask_client import OAuth
from loginpass import create_flask_blueprint
from loginpass import Twitter, GitHub, Google

app = Flask(__name__)
app.config.from_pyfile('config.py')


oauth = OAuth(app)

#: you can customize this part
backends = [Twitter, GitHub, Google]


@app.route('/')
def index():
    tpl = '<li><a href="/login/{}">{}</a></li>'
    lis = [tpl.format(b.NAME, b.NAME) for b in backends]
    return '<ul>{}</ul>'.format(''.join(lis))


def handle_authorize(remote, token, user_info):
    return jsonify(user_info)


bp = create_flask_blueprint(backends, oauth, handle_authorize)
app.register_blueprint(bp, url_prefix='')
