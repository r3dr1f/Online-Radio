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
 
from bcrypt import (hashpw, gensalt)
 
from ..utils import valid_email
from . import Base

class Playlist(Base):
    """Database table User.
 
    Attributes:
        id: Identificator of object
        email: User email, used as a login, so it's must be unique
        password: User Password
        active: Indicates, whether user-account is active
        games: relationship to table Game
    """
    __tablename__ = 'playlist'
    id = Column(Integer, primary_key=True)
    song_id = Column(Integer)
    play_time = Column(DateTime)

    def __init__(self, id, play_time):
        """Initialization of class.
        """
        self.id = id
        self.play_time = play_time
 
    def __repr__(self):
        """Returns representative object of class User.
        """
        return "Song<{id}>".format(id=self.id)