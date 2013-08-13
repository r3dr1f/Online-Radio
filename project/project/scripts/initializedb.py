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

from ..models.interpret import (
    Interpret,                      
    )

from ..models.user import (
    User,                      
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
    
    user1 = User("admin@mail.com","heslo","admin")
    user2 = User("mail1@mail.com","heslo","interpret")
    interpret1 = Interpret(user2,"smajdova manka1")
    user3 = User("mail2@mail.com","heslo","interpret")
    interpret2 = Interpret(user3,"sladke slyze2")
    user4 = User("user4@mail.com","heslo","user")
    interpret3 = Interpret(user4,"vyprazane kotrmelce")
    user5 = User("user5@mail.com","heslo","user")
    interpret4 = Interpret(user5,"zamracene keksy")
    
    
    song = Song(interpret1, "jalovica", 50)
    song2 = Song(interpret2, "dubdubdubstep")
    song3 = Song(interpret3, "rachot", 40)
    song4 = Song(interpret4, "zastavka", 30)
    song5 = Song(interpret4, "autolak")
    song6 = Song(interpret3, "pomodoro", 40)
    song7 = Song(interpret2, "taktytaktotytiktak", 70)
    song8 = Song(interpret1, "slanaHmla")
    song9 = Song(interpret1, "paprikovyMrak", 40)
    song10 = Song(interpret1, "Zodiac", 40)
    song11 = Song(interpret3, "zelenaBarbie")
    song12 = Song(interpret3, "papaliAnanas", 40)
    song13 = Song(interpret4, "somZabeu", 20)
    song14 = Song(interpret2, "parniky")
    song15 = Song(interpret4, "otrokJooozi", 50)
    song16 = Song(interpret1, "voxPopapuli", 30)
    song17 = Song(interpret3, "Dazd")
    song18 = Song(interpret2, "sychravaPerina", 60)
    song19 = Song(interpret1, "utocnyMraz", 30)
    song20 = Song(interpret2, "zloVkvetinaci")
    song21 = Song(interpret2, "agresivnaKalkulacka", 20)


    
    connection = engine.connect()
    Session = sessionmaker(bind=connection)
    db_session = Session()
    db_session.add(user1)
    
    db_session.add(user2)
    db_session.add(interpret1)
    
    db_session.add(user3)
    db_session.add(interpret2)
    
    db_session.add(user4)
    
    db_session.add(song)
    db_session.add(song2)
    db_session.add(song3)
    
    db_session.commit()
