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
 
from bcrypt import (hashpw, gensalt)
 
from ..utils import valid_email
from . import Base

class Comment(Base):
    """Database table Interpret.
 
    Attributes:
        id: Identificator of object
        user_id: id of user
        interpret_name: name of interpret
    """
    __tablename__ = 'comment'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('uzer.id')) #one to one vztah s userom
    user = relationship('User', backref="comments")
    song_id = Column(Integer, ForeignKey('song.id'))
    song = relationship('Song', backref="comments")
    add_time = Column(DateTime)
    

    def __init__(self, user, song, add_time):
        """Initialization of class.
        """
        self.user = user;
        self.user_id = user.id
        self.song = song
        self.song_id = song.id
        self.add_time = add_time
 
    def __repr__(self):
        """Returns representative object of class comment.
        """
        return "Comment<{id}>".format(id=self.id)
    
    def __json__(self, request):
        return {'id': self.id, 'user': self.user, 'song': self.song, 'add_time': self.add_time}
