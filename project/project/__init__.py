from pyramid.config import Configurator

from pyramid.events import (
    ContextFound,
    BeforeRender,
    )

from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.security import (
    authenticated_userid,
    Allowed,
    Denied,
    has_permission,
    )

from pyramid_mailer.mailer import Mailer

from sqlalchemy import engine_from_config

from .models import (
    DBSession,
    Base,
    )

from .models.user import User

from .models.interpret import Interpret

from .helpers import attr

from .authenticator import Authenticator

import random

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """

    def add_renderer_globals(event):
        """Adding renderer globals to event.
        """
        request = event['request']
        event['attr'] = attr
        event['user'] = request.user

    def prepare_request(event): #{{{
        """Add some additional information to the request object.
        """
        request = event.request
        request.settings = settings
        request.db_session = DBSession
        request.userid = authenticated_userid(request)
        request.interpretid = authenticated_userid(request)
#         request.without_interpret = True
        
        if request.userid is not None:
            request.user = request.db_session.query(User).\
                    filter(User.id == request.userid).\
                    first()
            if request.interpretid is not None:
                request.interpret = request.db_session.query(Interpret).filter(Interpret.user_id == request.userid).first()
            else:
                request.interpret = None
            
        else:
            request.user = None

        if request.registry and 'mailer' in request.registry:
            mailer = request.registry['mailer']
            request.mailer = mailer

        request.authenticator = Authenticator(request.db_session, request)

    # Settings
    authn_policy = AuthTktAuthenticationPolicy(secret=settings['auth_secret_key']) 
    authz_policy = ACLAuthorizationPolicy()
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine

    config = Configurator(settings=settings)
    config.add_subscriber(add_renderer_globals, BeforeRender)
    config.add_subscriber(prepare_request, ContextFound)
    config.registry['mailer'] = Mailer.from_settings(settings)

    config.set_authentication_policy(authn_policy)
    config.set_authorization_policy(authz_policy)

    config.add_static_view('static', 'static', cache_max_age=3600)

    # Routes
    config.add_route('home', '/')
    config.add_route('register', '/registracia')
    config.add_route('register_success', '/uspesna-registracia/{user_id}')
    config.add_route('login', '/login')
    config.add_route('logout', '/logout')
    config.add_route('beg_for_recovery', '/stratene-heslo')
    config.add_route('new_password', '/nove-heslo/{user_id}/{code}')
    config.add_route('get_user_info', '/get-user-info/{user_id}')
    config.add_route('recovery_small_success', '/stratene-heslo-uspech')
    config.add_route('admin', '/admin')
    config.add_route('getsource', '/getsource')
    config.add_route('upload', '/upload')
    config.add_route('getsong', '/getsong')
    config.add_route('getinterpret', '/getinterpret')
    config.add_route('rate', '/rate')
    config.add_route('search', '/search')
    config.add_route('request', '/request')
    config.add_route('login_fb', '/login_fb')
    config.add_route('comment', '/comment')

    config.scan()
    random.seed()

    return config.make_wsgi_app()
