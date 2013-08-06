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
 
class Song(Base):
    """Database table Song.
 
    Attributes:
        id: Identificator of object
        interpret_id: Id of interpret who uploaded the song
        name: Name of the song
    """
    __tablename__ = 'song'
    id = Column(Integer, primary_key=True)
    interpret_id = Column(Integer, ForeignKey('interpret.id'))
    interpret = relationship('Interpret', backref="song")
    name = Column(String(100))
 
    def __init__(self, interpret, name):
        """Initialization of class.
        """
        self.interpret_id = interpret.id
        self.interpret = interpret
        self.name = name
 
    def __repr__(self):
        """Returns representative object of class User.
        """
        return "Song<{id}>".format(interpret_id=self.interpret_id, name=self.name)
    
    def __json__(self, request):
        return {'id': self.id, 'name': self.name, 'interpret': self.interpret}
