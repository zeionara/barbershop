import configparser
from connection import create_session

from ming import schema
from ming.odm import FieldProperty
from ming.odm.declarative import MappedClass

from commons import EnhancingClass

collection_name = 'services'

config = configparser.ConfigParser()
config.read('C://Users//Zerbs//accounts.sec')

session = create_session(config['mongo']['login'], config['mongo']['password'], config['mongo']['path'])

class Service(MappedClass, EnhancingClass):
    
    class __mongometa__:
        session = session
        name = collection_name
    
    _id = FieldProperty(schema.ObjectId)
    name = FieldProperty(schema.String(required=True))
    price = FieldProperty(schema.Float(required=True))
    
    description = FieldProperty(schema.String(if_missing = ''))
    avg_duration = FieldProperty(schema.Float(if_missing = None))
    
serv = Service(name = "Short hairing", price = 200, avg_duration = 25)

session.flush_all()