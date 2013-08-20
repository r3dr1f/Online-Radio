from .models.user import User

from pyramid.security import (remember, forget)
from sqlalchemy.sql import not_

class Authenticator:

    def __init__(self, session, request):
        self._session = session
        self._request = request

    def login(self, email, password):
        """Logs user into a system.
        
        Args:
            email: User's email
            password: User's password
        """

        user = self._session.query(User).filter(User.email==email).filter(User.role!="fb").first()
        if user is None: raise NonExistingUserError('This user doesn\'t exist.')
        if (user.password != password): raise WrongPasswordError('Passwords don\'t match.') 
        
        return (
            remember(self._request, user.id),
            user,
            )
                             
    def login_fb(self, email):
        """
            Logs user into system.
        """
        user = self._session.query(User).filter_by(email=email).first()
        if user is None: raise NonExsitingUserError('This user doesn\'t exist.')
        
        return (
            remember(self._request, user.id),
            user,
            )
                             
    def logout(self):
        return forget(self._request)
        
class AuthenticationError(Exception):
    pass        
class WrongPasswordError(AuthenticationError):
    pass
class NonExistingUserError(AuthenticationError):
    pass
