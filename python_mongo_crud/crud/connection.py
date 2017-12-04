from ming import create_datastore
from ming.odm import ThreadLocalODMSession

session = None

def create_session(login, password, path):
    global session
    if session == None:
        session = ThreadLocalODMSession( bind = create_datastore('mongodb://%s:%s@%s' % (login, password, path)))
    return session