from ming import create_datastore
from ming.odm import ThreadLocalODMSession
import pymongo

session = None
db = None

def create_session(login, password, path):
    global session
    if session == None:
        session = ThreadLocalODMSession( bind = create_datastore('mongodb://%s:%s@%s' % (login, password, path)))
    return session

def create_db_connection(login, password, path):
    global db
    if db == None:
        db = pymongo.MongoClient('mongodb://%s:%s@%s' % (login, password, path))
    return db
