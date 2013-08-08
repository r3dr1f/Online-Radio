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
 
class Rating(Base):
    """Database table Rating.
 
    Attributes:
        id: Identificator of object
        user_id: Id of user
        song_id: Name of the song
        rating: Rating - 0,1,2,3,4
    """
    __tablename__ = 'rating'
    id = Column(Integer, primary_key=True)
    song_id = Column(Integer, ForeignKey('song.id'))
    song = relationship('Song', backref="ratings")
    user_id = Column(Integer, ForeignKey('uzer.id'))
    user = relationship('User', backref="ratings") 
    rating = Column(Integer)
 
    def __init__(self, user, song, rating):
        """Initialization of class.
        """
        self.user = user
        self.user_id = user.id
        self.song = song
        self.song_id = song.id
        self.rating = rating
 
    def __repr__(self):
        """Returns representative object of class User.
        """
        return "Rating<{id}>".format(user_id=self.user_id, song_id=self.song_id, rating=self.rating)
    
    def __json__(self, request):
        return {'id': self.id, 'rating': self.rating, 'song_id': self.song_id}
