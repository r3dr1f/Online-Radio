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

from ..models.song import (
    Song,
    )

from ..models.interpret import (
    Interpret,
    )

from ..models.rating import (
    Rating,
    )

from ..models.request import (
    Request,
    )

from ..models.comment import (
    Comment,
    )

from ..models.image import (
    Image,
    )

from ..utils import valid_email

from mako.template import Template

from pkg_resources import resource_string

import os, shutil, mimetypes

import json, sys

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

from pyramid.security import remember

import PIL
from PIL import Image as Im

import time, datetime

import random
#}}}

def allowed_mime_type(mime_type):
    mime_types = {'audio/mpeg'}
    return mime_type[0] in mime_types

@notfound_view_config(append_slash=True)
def notfound(request):
    return HTTPNotFound("Hľadaná stránka neexistuje")

@view_config(route_name='home', renderer='project:templates/home.mako')
def main_page_view(request):
    """Shows a Home Page.
    """
    return {
        'page_title': 'HomePage',
        'logged': (request.userid is not None)
        }


class RegistrationError(Exception):
    pass


class DuplicateUserError(RegistrationError): 
    pass

def register_interpret(db_session, user_id, interpret_name):
    """Registers a new interpret
    
    """
    user = db_session.query(User).filter_by(id=user_id).first()
    interpret = Interpret(user, interpret_name)
    
    if db_session.query(Interpret).filter_by(name=interpret_name).count() != 0:
        raise DuplicateUserError

    db_session.add(interpret)
    db_session.flush()
    
    return {}

def register_user(db_session, email, password, role, uuid = 0):
    """Registers a new user and returns his ID (single number).

    """
    user = User(email, password, role, uuid)
    
    if db_session.query(User).filter_by(email=email).count() != 0:
        raise DuplicateUserError

    db_session.add(user)
    db_session.flush()

    return user.id

def register_fb(db_session, email, password, role, uuid):
    user = User(email, password, role, uuid)
    db_session.add(user)
    db_session.flush()

error_messages = {
    'invalid_email':'Zadajte správny e-mail.',
    'duplicate_email':'E-mail je už obsadený.',
    'invalid_password':'Zadajte heslo.',
    'dont_match':'Heslá sa nezhodujú.',
    }


@view_config(route_name='register', request_method='GET', renderer='json')
def register_view(request):
    """Displays registration form and processes form data.
    """
    return {'register': True}


@view_config(route_name='register', request_method='POST', renderer='json')
def register_submission(request):
    """Handles registration form submission.
    Creates PDF card in 'users_data/cards/{ID}.pdf'. CSS file for it is in 'templates/pdf_card.css'.
    """
    POST = request.POST
    errors = validate_registration_data(POST)
    if not errors:
        try:
            user_id = register_user(request.db_session, POST['email'], POST['password'], int(POST['role']))
            if POST['interpret_name'] and int(POST['role']) == 1:
                register_interpret(request.db_session, user_id ,POST['interpret_name'])
            return {'register_success': True}
        except DuplicateUserError:
            errors['email'] = 'duplicate_email'

    return {'errors': errors, 'error_messages': error_messages}

@view_config(route_name='login_fb', request_method='POST', renderer='json')
def login_fb(request):
    
    
    user = request.db_session.query(User).filter_by(email=request.POST['email']).first()
    errors = []
    if user is None:
        register_fb(request.db_session, request.POST['email'], "", 3, request.POST['uuid'])
    try:
        (headers, user) = request.authenticator.login_fb(request.POST['email'])
        request.response.headerlist.extend(headers)
        return {'user': user}
    except NonExistingUserError:
        errors.append('wrong-email')
    return {'error': errors}

@view_config(route_name='register_success', request_method='get', renderer='json')
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


@view_config(route_name='login', request_method='POST', renderer='json')
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
        request.response.headerlist.extend(headers)
        print(user);
        return {'user': user}
    except WrongPasswordError:
        errors.append('wrong-password')
    except NonExistingUserError:
        errors.append('wrong-email')
    return {'errors': errors}


@view_config(route_name='logout', request_method='POST', renderer='json')
def logout(request):
    """Unauthorizes user.
    """
    headers = request.authenticator.logout()
    request.response.headerlist.extend(headers)
    return {'user': None}


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
    return {}

@view_config(route_name='getsource', request_method='GET', renderer='json')
def get_source(request):
    song = request.db_session.query(Playlist).order_by(Playlist.play_time.desc()).first()
    song_name = request.db_session.query(Song).filter_by(id=song.song_id).first()
    playlist = request.db_session.query(Playlist).order_by(Playlist.id.desc())[0:15]
    return{'song': song_name, 'playlist': playlist}
    
@view_config(route_name='upload', request_method='GET', renderer='project:templates/upload.mako')
def upload_song(request):
    if request.interpretid is None:
        return HTTPFound(location=request.route_url('home'))
    return {}

@view_config(route_name='upload', request_method='POST', renderer='project:templates/upload.mako')
def upload_song_post(request):
    if request.POST['name'] != '':
        if 'mp3' in request.POST and not hasattr(request.POST['mp3'], 'filename'):
            return {'ok': 0, 'error': 'mp3'}
        else:
            if not allowed_mime_type(mimetypes.guess_type(request.POST['mp3'].filename)):
                return {'ok': 0, 'error': 'mime'}
            else:
                song = Song(request.interpret.id, request.POST['name'])
                request.db_session.add(song)
                request.db_session.flush()
                
                filename = str(song.id) + ".mp3"
        
                input_file = request.POST['mp3'].file
        
                file_path = os.path.join(os.getcwd() + '/project/liquidsoap/songs/', filename)
                with open(file_path, 'wb') as output_file:
                    shutil.copyfileobj(input_file, output_file)
        
                return {'ok': 1}
    else:
        return {'ok': 0, 'error': 'name'}
    
@view_config(route_name='getinterpret', request_method='POST', renderer='json')
def get_interpret(request):
    request.without_interpret = True
    interpret = request.db_session.query(Interpret).filter_by(id=request.POST['id']).first()
    return{'interpret': interpret, 'songs': interpret.songs}

@view_config(route_name='getsong', request_method='POST', renderer='json')
def get_song(request):
    song = request.db_session.query(Song).filter_by(id=request.POST['id']).first()
    comments = request.db_session.query(Comment).filter_by(song_id=song.id).order_by(Comment.add_time.asc()).all()
    if not request.user is None:
        rating = request.db_session.query(Rating).filter_by(user_id = request.user.id, song_id = song.id).first()
        request_to_play = request.db_session.query(Request).filter_by(song_id = song.id, user_id = request.user.id).first()
        if request_to_play is None:
            request_to_play = False
        else:
            request_to_play = True
        if not rating is None:
            return{'song': song, 'rating': rating, 'user': request.user, 'request': request_to_play, 'comments': comments}
        else:
            return{'song': song, 'user': request.user, 'request': request_to_play, 'comments': comments}
    else:
        return{'song': song, 'comments': comments}
    
@view_config(route_name='rate', request_method='POST', renderer='json')
def rate_song(request):
    if not request.user is None:
        song = request.db_session.query(Song).filter_by(id=request.POST['id']).first()
        rating = request.db_session.query(Rating).filter_by(user_id = request.user.id, song_id = song.id).first()
        if rating is None:
            rating = int(request.POST['rating'])
            if rating > 4:
                rating = 4
            elif rating < 0:
                rating = 0
            rating_obj = Rating(request.user, song, rating)
            request.db_session.add(rating_obj)
            all_ratings = request.db_session.query(Rating).filter_by(song_id = song.id).all()
            all_who_rated = len(all_ratings)
            minimalna_hranica = 19
            if(all_who_rated > minimalna_hranica):
                count = 0
                for ratings in all_ratings:
                    count += ratings.rating
                multiply_to_hundred = 25 # nasobime 25 lebo hodnotenie je od 0 po 4
                average_rating = (count/all_who_rated)*multiply_to_hundred
                #update_song = Song(song.interpret, song.name, average_rating, song.factor_played, song.factor_age)
                request.db_session.query(Song).filter_by(id=song.id).update({"rating_max": average_rating})
            comments = request.db_session.query(Comment).filter_by(song_id=song.id).order_by(Comment.add_time.asc()).all()
            return{'song': song, 'rating': rating_obj, 'comments': comments, 'user': request.user}
        else:
            error = "Lutujeme ale tuto pesnicku ste uz raz hodnotili"
            return{'error': error}
    else:
        return{'error': "asd"}

@view_config(route_name='search', request_method='POST', renderer='json')
def search(request):
    songs = request.db_session.query(Song).filter(Song.name.like('%'+request.POST['search']+'%')).all()
    interprets = request.db_session.query(Interpret).filter(Interpret.name.like('%'+request.POST['search']+'%')).all()
    return {'songs': songs, 'interprets': interprets}

@view_config(route_name='request', request_method='POST', renderer='json')
def request_to_play(request):
    if not request.user is None:
        song = request.db_session.query(Song).filter_by(id=request.POST['id']).first()
        request_to_play = request.db_session.query(Request).filter_by(song_id = song.id, user_id = request.user.id).first()
        if request_to_play is None:
            request_play = Request(request.user, song)
            request.db_session.add(request_play)
            request_koeficient = 2
            request.db_session.query(Song).filter_by(id=song.id).update({"current_rating": song.current_rating*request_koeficient})
            return {'request': True}
    return {'request': False}

@view_config(route_name='comment', request_method='POST', renderer='json')
def add_comment(request):
    if not request.user is None:
        song = request.db_session.query(Song).filter_by(id=request.POST['id']).first()
        user = request.db_session.query(User).filter_by(id=request.user.id).first()
        comment = Comment(user, song, datetime.datetime.now(), request.POST['comment'])
        request.db_session.add(comment)
        request.db_session.flush()
        comments = request.db_session.query(Comment).filter_by(song_id=song.id).order_by(Comment.add_time.asc()).all()
        return {'comments': comments}
        
@view_config(route_name='image', request_method='GET', renderer='json')
def image(request):
    return {}

@view_config(route_name='image', request_method='POST', renderer='json')
def upload_image(request):
    if request.user is None:
        return {}
    #check uploaded file
    file = request.POST['photoimg'].file
    filename = request.POST['photoimg'].filename
    if file is not None:
        
        img = request.db_session.query(Image).filter_by(user_id = request.user.id).first()
    
        #create image if current user doesn't have one already
        if img is None:
            img = Image(request.user, filename)
            request.db_session.add(img)
            request.db_session.flush()
            
        #else update
        else:
            try:
                os.remove(os.getcwd() + '/project/static/uploaded/' + str(img.user_id) + '/' + img.name)
            except:
                pass
            request.db_session.query(Image).filter_by(user_id=request.user.id).update({"name": filename})
            
        #get image file type
        file_type = filename.split('.')[-1]
        
        #create directories on file path, if they don't exist yet
        directory = os.getcwd() + '/project/static/tmp/' + str(img.user_id) + '/'
        if not os.path.exists(directory):
            os.makedirs(directory)

        #upload image to the directory
        file_path = os.path.join(directory, filename)
        with open(file_path, 'wb') as output_file:
            shutil.copyfileobj(file, output_file)
        
        #resize width to 800, if it is higher    
        image = Im.open(file_path)
        width, height = image.size
        maxwidth = 800
        if width > maxwidth:
            ratio = maxwidth / width
            image = image.resize((int(width*ratio), int(height*ratio)), Im.ANTIALIAS)
            #rewrite image
            if file_type == "jpg":      
                image.save(file_path, "JPEG")
            elif file_type == "gif":
                image.save(file_path, "GIF")
            elif file_type == "png":
                image.save(file_path, "PNG")    
        
    return {'image': img}
        
@view_config(route_name='cropimage', request_method='POST', renderer='json')
def crop_image(request):
    #load image
    img = Im.open(os.getcwd() + '/project/static/tmp/' + request.POST['src'])
    file_type = request.POST['src'].split('.')[-1]
    
    #get image dimensions
    src_width, src_height = img.size
    src_ratio = float(src_width) / float(src_height)
    dst_width, dst_height = 300, 300
    dst_ratio = 1
    
    #load crop variables - x,y = start coordinates, w = width, h = height
    x = int(request.POST['x'])
    y = int(request.POST['y'])
    w = int(request.POST['w'])
    h = int(request.POST['h'])
    
    #crop image
    img = img.crop((x, y, x+w, y+h))
    
    #resize image to 300x300 + antialias
    img = img.resize((dst_width, dst_height), Im.ANTIALIAS)
    
    directory = os.getcwd() + '/project/static/uploaded/' + str(request.userid) + '/'
    
    if not os.path.exists(directory):
            os.makedirs(directory)
    
    #rewrite image
    file_path = os.getcwd() + '/project/static/uploaded/' + request.POST['src']
    if file_type == "jpg":      
        img.save(file_path, "JPEG")
        ok = True
    elif file_type == "gif":
        img.save(file_path, "GIF")
        ok = True
    elif file_type == "png":
        img.save(file_path, "PNG")
        ok = True
        
    if ok:
        try:
            #delete image from tmp
            os.remove(os.getcwd() + '/project/static/tmp/' + request.POST['src'])
            #remove folder from tmp
            os.rmdir(os.getcwd() + '/project/static/tmp/' + str(request.userid))
        except:
            pass
        
    return {'ok': True}