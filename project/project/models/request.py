from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    Float,
    Boolean,
    Table,
    ForeignKey,
    Enum,
    Float,
    DateTime,
    )
 
from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    )
 
from sqlalchemy.ext.hybrid import (
    Comparator,
    hybrid_property,
    )
 
from sqlalchemy.orm import (
    validates,
    relationship,
    scoped_session,
    sessionmaker,
    )
 
from . import Base
 
class ValidationError(Exception):
    pass 
 
class Request(Base):
    """Database table Request.
 
    Attributes:
        id: Identificator of object
        user_id: Id of user
        song_id: Name of the song
    """
    __tablename__ = 'request'
    id = Column(Integer, primary_key=True)
    song_id = Column(Integer, ForeignKey('song.id'))
    song = relationship('Song', backref="request")
    user_id = Column(Integer, ForeignKey('uzer.id'))
    user = relationship('User', backref="request") 
 
    def __init__(self, user, song):
        """Initialization of class.
        """
        self.user = user
        self.user_id = user.id
        self.song = song
        self.song_id = song.id
 
    def __repr__(self):
        """Returns representative object of class User.
        """
        return "Request<{id}>".format(user_id=self.user_id, song_id=self.song_id)