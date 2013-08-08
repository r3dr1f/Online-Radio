import sqlite3 as lite
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


"""
    vrati spojenie k databaze
"""

db_path = "../../project.sqlite"

def connect():
    engine_path = 'sqlite:///' + db_path
    engine = create_engine(engine_path)
    connection = engine.connect()
    
    trans = connection.begin()
    Session = sessionmaker(bind=connection)
    db_session = Session()
    return db_session 

    #con = lite.connect('../project/project.sqlite')
    #return con