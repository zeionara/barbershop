from ming import create_datastore
from ming.odm import ThreadLocalODMSession

def create_session(login, password, path):
    return ThreadLocalODMSession( bind = create_datastore('mongodb://%s:%s@%s' % (login, password, path)))