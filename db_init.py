import sqlite3
import sys

con = None

try:
    con = sqlite3.connect('files.db')

    cur = con.cursor()
    cur.execute('SELECT SQLITE_VERSION()')

    data = cur.fetchone()

    print 'SQLite Version : {}'.format(data)

except lite.Error, e:
    
    print 'Error! {}'.format(e.args[0])
    sys.exit(1)

finally:

    if con:
        con.close()
