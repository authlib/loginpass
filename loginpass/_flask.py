def create_flask_blueprint(backend, oauth, handle_authorize):
    """Create a Flask blueprint that you can register it directly to Flask
    app. The blueprint contains two route: ``/auth`` and ``/login``::

        from flask import Flask
        from authlib.integrations.flask_client import OAuth
        from loginpass import create_flask_blueprint, GitHub

        app = Flask(__name__)
        oauth = OAuth(app)


        def handle_authorize(remote, token, user_info):
            if token:
                save_token(remote.name, token)
            if user_info:
                save_user(user_info)
                return user_page
            raise some_error

        github_bp = create_flask_blueprint(GitHub, oauth, handle_authorize)
        app.register_blueprint(github_bp, url_prefix='/github')

        # visit /github/login
        # callback /github/auth

    :param backend: An OAuthBackend
    :param oauth: Authlib Flask OAuth instance
    :param handle_authorize: A function to handle authorized response
    :return: Flask Blueprint instance
    """
    from flask import Blueprint, request, url_for, current_app

    oauth.register(backend.NAME, overwrite=True, **backend.OAUTH_CONFIG)
    bp = Blueprint('loginpass_' + backend.NAME, __name__)

    @bp.route('/auth', methods=('GET', 'POST'))
    def auth():
        remote = oauth.create_client(backend.NAME)
        id_token = request.values.get('id_token')
        if request.values.get('code'):
            token = remote.authorize_access_token()
            if id_token:
                token['id_token'] = id_token
        elif id_token:
            token = {'id_token': id_token}
        elif request.values.get('oauth_verifier'):
            # OAuth 1
            token = remote.authorize_access_token()
        else:
            # handle failed
            return handle_authorize(remote, None, None)
        if 'id_token' in token:
            user_info = remote.parse_openid(token)
        else:
            remote.token = token
            user_info = remote.userinfo(token=token)
        return handle_authorize(remote, token, user_info)

    @bp.route('/login')
    def login():
        remote = oauth.create_client(backend.NAME)
        redirect_uri = url_for('.auth', _external=True)
        conf_key = '{}_AUTHORIZE_PARAMS'.format(backend.NAME.upper())
        params = current_app.config.get(conf_key, {})
        return remote.authorize_redirect(redirect_uri, **params)

    return bp
