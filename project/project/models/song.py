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

import datetime
 
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
    interpret = relationship('Interpret', backref="songs")
    name = Column(String(100))
    rating_max = Column(Float) # rating vyratany na zaklade hodnotenia vsetkych uzivatelov z tabulky rating
    #factor_played = Column(Float) # faktor vyratany na zaklade posledneho prehratia
    factor_age = Column(Float) # faktor vyratany na zaklade veku pesnicky
    current_rating = Column(Float) # aktualny rating pesnicky
    date_added = Column(DateTime) # cas pridania pesnicky do databazy
 
    def __init__(self, interpret, name, rating_max = 60, factor_age = 1,date_added = datetime.datetime.now()):
        """Initialization of class.
        """
        self.interpret_id = interpret.id
        self.interpret = interpret
        self.name = name
        self.rating_max = rating_max
        #self.factor_played = factor_played
        self.factor_age = factor_age
        self.current_rating = rating_max
        self.date_added = date_added
 
    def __repr__(self):
        """Returns representative object of class User.
        """
        return "Song<{id}>".format(id=self.interpret_id)
    
    def __json__(self, request):
        return {'id': self.id, 'name': self.name, 'interpret': self.interpret, 'rating_max': self.rating_max}
