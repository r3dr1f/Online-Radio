import sqlite3 as lite

def connect():

    con = lite.connect('../project/project.sqlite')
    return con