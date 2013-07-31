#{{{
from pyramid.view import (
    view_config,
    notfound_view_config,
    forbidden_view_config,
    )

from pyramid.security import (
    remember,
    forget,
    )

from pyramid.httpexceptions import (
    HTTPException,
    HTTPNotFound,
    HTTPFound,
    HTTPForbidden,
    )

from pyramid.response import (
    FileResponse,
    Response,
    )

from pyramid.renderers import render

from pyramid_mailer.message import (
    Message,
    Attachment,
    )

from ..models.user import (
    User, 
    )

from ..models.playlist import (
    Playlist, 
    )

from ..utils import valid_email

from mako.template import Template

from pkg_resources import resource_string

import os.path

import json

from sqlalchemy import (
    asc,
    desc,
    )

from sqlalchemy.sql import func


from ..authenticator import (
    WrongPasswordError,
    NonExistingUserError,
    )

from subprocess import (
    Popen, 
    PIPE
    )

import time


import random
#}}}

@notfound_view_config(append_slash=True)
def notfound(request):
    return HTTPNotFound("Hľadaná stránka neexistuje")


import urllib
from bs4 import BeautifulSoup

def get_server_details(server, port, mount):
    server = "http://%s:%s/status.xsl?mount=/%s" % (server, port, mount)
    #print "Getting info for %s" % (server)
    try:
        response = urllib.request.urlopen(server)
        html = response.read()
        if html:
            soup = BeautifulSoup(html)
            print(soup)
            info = {}
            info['stream_title'] = soup.find(text="Stream Title:").findNext('td').contents[0]
            info['stream_description'] = soup.find(text="Stream Description:").findNext('td').contents[0]
            info['content_type'] = soup.find(text="Content Type:").findNext('td').contents[0]
            info['mount_started'] = soup.find(text="Mount started:").findNext('td').contents[0]
            info['quality'] = soup.find(text="Quality:").findNext('td').contents[0]
            info['current_listeners'] = soup.find(text="Current Listeners:").findNext('td').contents[0]
            info['peak_listeners'] = soup.find(text="Peak Listeners:").findNext('td').contents[0]
            info['stream_genre'] = soup.find(text="Stream Genre:").findNext('td').contents[0]
            info['stream_url'] = soup.find(text="Stream URL:").findNext('td').findNext('a').contents[0]
            info['current_song'] = soup.find(text="Current Song:").findNext('td').contents[0]

            return info 
        else:
            print ("Invalid content found")
            return None

    except urllib.request.URLError:
        print ("Unable to read url, please check your parameters")
        return None
    except:
        print ("MARHHHHHAAAAAAAAAAAAAAA")
        return info


@view_config(route_name='home', renderer='project:templates/home.mako')
def main_page_view(request):
    """Shows a Home Page.
    """
    ret = get_server_details('localhost', '8000', 'stream')
    return {
        'info': ret,
        'page_title': 'HomePage',
        'logged': (request.userid is not None)
        }


class RegistrationError(Exception):
    pass


class DuplicateUserError(RegistrationError): 
    pass


def register_user(db_session, email, password):
    """Registers a new user and returns his ID (single number).

    """
    user = User(email, password)
    
    if db_session.query(User).filter_by(email=email).count() != 0:
        raise DuplicateUserError

    db_session.add(user)
    db_session.flush()

    return user.id

error_messages = {
    'invalid_email':'Zadajte správny e-mail.',
    'duplicate_email':'E-mail je už obsadený.',
    'invalid_password':'Zadajte heslo.',
    'dont_match':'Heslá sa nezhodujú.',
    }


@view_config(route_name='register', request_method='GET', renderer='project:templates/register.mako')
def register_view(request):
    """Displays registration form and processes form data.
    """
    return {'errors': {}, 'error_messages': error_messages}


@view_config(route_name='register', request_method='POST', renderer='project:templates/register.mako')
def register_submission(request):
    """Handles registration form submission.
    Creates PDF card in 'users_data/cards/{ID}.pdf'. CSS file for it is in 'templates/pdf_card.css'.
    """
    POST = request.POST
    errors = validate_registration_data(POST)
    if not errors:
        try:
            user_id = register_user(request.db_session, POST['email'], POST['password'])
            return HTTPFound(request.route_path('register_success', user_id=user_id))
        except DuplicateUserError:
            errors['email'] = 'duplicate_email'


    return {'errors': errors, 'error_messages': error_messages}


@view_config(route_name='register_success', renderer='project:templates/register_success.mako')
def register_success(request):
    """Displays success message after registration
    """
    return {'user_id':request.matchdict['user_id']}




def validate_registration_data(form_data):
    """Checkes whether all datas are correct and returns dictionary of errors.
    """
    errors = {}
    if not valid_email(form_data['email']):
        errors['email'] = 'invalid_email'
    if form_data['password'] != form_data['password_repeat']:
        errors['password'] = 'dont_match'
    if form_data['password'] == "":
        errors['password'] = 'invalid_password'
    return errors
    

@view_config(route_name='get_user_info', renderer='json')
def get_user_info(request):
    """Shows user's data in json format.
    Expects request.matchdict['user_id'].
    Return error='no-user-error' if user doesn't exist.
    Data is represented by dict with keys: 'email', 'password'.
    """
    user_id = request.matchdict['user_id']
    user = request.db_session.query(User).filter_by(id=user_id).first()
    data = {'error':'no-user-error'}
    if not user is None:
        data = {'email':user.email}
    return data



@view_config(route_name='login', request_method='GET', renderer='project:templates/login.mako')
@forbidden_view_config(renderer='project:templates/login.mako')
def login(request):
    """Shows login form.
    """
    return {'errors':[]}


@view_config(route_name='login', request_method='POST', renderer='project:templates/login.mako')
def login_submit(request):
    """Processes submit of login data.

    If they are correct, then authorizes and redirect to homepage. Otherwise, shows error.
    """
    POST = request.POST

    email = POST['email']
    password = POST['password']
    errors = []

    try:
        (headers, user) = request.authenticator.login(email, password)
        return HTTPFound(location=request.route_path('home'), headers=headers)
    except WrongPasswordError:
        errors.append('wrong-password')
    except NonExistingUserError:
        errors.append('wrong-email')
    return {'errors': errors}


@view_config(route_name='logout')
def logout(request):
    """Unauthorizes user.
    """
    headers = request.authenticator.logout()
    return HTTPFound(location=request.route_path('home'), headers=headers)


@view_config(route_name='beg_for_recovery', request_method='GET', renderer='project:templates/lost_password.mako')
def beg_for_recovery(request):
    """Shows form for email of user's account.
    """
    return {'error':[]}


@view_config(route_name='beg_for_recovery', request_method='POST', renderer='project:templates/lost_password.mako')
def begged_for_recovery(request):
    """Gets email. If exists, generates `recovery_code` and send a recovery link to user and redirect to 
    "success_beg". If not, shows error.
    """
    POST = request.POST
    email = POST['email']
    user = request.db_session.query(User).filter_by(email=email).first()
    if user == None:
        return {'error':['no-email']}

    user.recovery_code = str(random.getrandbits(50))

    link = request.route_url('new_password', user_id=str(user.id), code=user.recovery_code)

    message = Message(subject='Zmena hesla',  
                        recipients=[email],
                        body='Ak si chcete zmeniť heslo, kliknite na nasledovný odkaz:' + link + '.')

    request.mailer.send(message)

    return HTTPFound(location=request.route_url('recovery_small_success'))


@view_config(route_name='recovery_small_success', renderer='project:templates/small_success.mako')
def recovery_small_success(request):
    """Shows a message with an offer to check email for a link to advance in passweord recovery process.
    """
    return {}


@view_config(route_name='new_password', request_method='GET', renderer='project:templates/new_password.mako')
def recovery_final(request):
    """Shows form for new password. if user_id or recovery code doesn't match, then shows 404.
    """
    user_id = int(request.matchdict['user_id'])
    user = request.db_session.query(User).filter_by(id=user_id).first()
    
    if user == None:
        return HTTPNotFound("Neplatná obnovovacia URL. Skontrolujte odkaz na zmenu hesla a skúste znova.")
    if request.matchdict['code'] != user.recovery_code:
        return HTTPNotFound("Neplatná obnovovacia URL. Skontrolujte odkaz na zmenu hesla a skúste znova.")

    return {'error':[]}


@view_config(route_name='new_password', request_method='POST', renderer='project:templates/new_password.mako')
def recovery_final_submit(request):
    """Takes two passwords. If they match, then changes it in database and redirect to homepage. 
    Otherwise shows error.
    """
    POST = request.POST
    password = POST['password']
    password_repeat = POST['password_repeat']
    if password != password_repeat:
        return {'error':['nonequal-passwords']}
    user = request.db_session.query(User).filter_by(id=request.matchdict['user_id']).first()
    user.password = password
    return HTTPFound(location=request.route_url('home'))

@view_config(route_name='admin', request_method='GET', renderer='project:templates/admin.mako')
def admin_show(request):
    request.isOpenedStream = None
    return {}

@view_config(route_name='admin', request_method='POST', renderer='project:templates/admin.mako')
def admin_start_stream(request):
    print('#####'*20)
    process = Popen(['liquidsoap', '/home/r3dr1f/OnlineRadio/liquidsoap/script.liq', '-v'], stdout=PIPE)
    stdout, stderr = process.communicate()
    print(stdout)
    print(stderr)
    return {}

@view_config(route_name='getsource', request_method='GET', renderer='project:templates/getsource.mako')
def get_source(request):
    songinfo = request.db_session.query(Playlist).order_by(Playlist.play_time.desc()).first()
    return{'songinfo': songinfo}
    