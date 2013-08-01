import os
import sys
import transaction

from sqlalchemy import engine_from_config
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from pyramid.paster import (
    get_appsettings,
    setup_logging,
    )

from ..models import (
    DBSession,
    Base,
    set_up_tables,
    )

from ..models.song import (
    Song,                       
    )


def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri>\n'
          '(example: "%s development.ini")' % (cmd, cmd))
    sys.exit(1)


def main(argv=sys.argv):
    if len(argv) != 2:
        usage(argv)
    config_uri = argv[1]
    setup_logging(config_uri)
    settings = get_appsettings(config_uri)
    engine = engine_from_config(settings, 'sqlalchemy.')
    set_up_tables(engine)
    
    song = Song(1, "skuska")
    song2 = Song(1, "skuska2")
    song3 = Song(1, "skuska3")
    
    connection = engine.connect()
    Session = sessionmaker(bind=connection)
    db_session = Session()
    db_session.add(song)
    db_session.add(song2)
    db_session.add(song3)
    
    db_session.commit()
