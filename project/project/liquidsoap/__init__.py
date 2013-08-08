import sqlite3 as lite
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import logging

#logging.basicConfig()
#logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)


"""
    vrati spojenie k databaze
"""

db_path = "../../project.sqlite"

engine_path = 'sqlite:///' + db_path
engine = create_engine(engine_path)
connection = engine.connect()

Session = sessionmaker(bind=connection)

_session = Session()

 
