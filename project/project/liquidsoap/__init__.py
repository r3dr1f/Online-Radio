import pkgutil
import sqlite3 as lite
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import logging
import os

#logging.basicConfig()
#logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)


"""
    vrati spojenie k databaze
"""

current_filedir_path = os.path.dirname(__file__)
engine_path = 'sqlite:///' + current_filedir_path + '/../../project.sqlite'
print (engine_path)

#db_path = "../../project.sqlite"

#engine_path = 'sqlite:///' + db_path
engine = create_engine(engine_path)
connection = engine.connect()

Session = sessionmaker(bind=connection)

_session = Session()

 
def load_modules():
    for loader, module_name, pkg in pkgutil.walk_packages(project.models.__path__, project.models.__name__ + '.'):
        __import__(module_name)
