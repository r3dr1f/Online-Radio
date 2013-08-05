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

class Interpret(Base):
    """Database table Interpret.
 
    Attributes:
        id: Identificator of object
        user_id: id of user
        interpret_name: name of interpret
    """
    __tablename__ = 'interpret'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    interpret_name = Column(String(100))
    

    def __init__(self, user_id, interpret_name):
        """Initialization of class.
        """
        self.user_id = user_id
        self.interpret_name = interpret_name
 
    def __repr__(self):
        """Returns representative object of class interpret.
        """
        return "Interpret<{id}>".format(id=self.id)