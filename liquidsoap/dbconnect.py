import sqlite3 as lite

"""
    vrati spojenie k databaze
"""

def connect():

    con = lite.connect('../project/project.sqlite')
    return con