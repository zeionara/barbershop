import configparser
from connection import create_session

from ming import schema
from ming.odm import FieldProperty
from ming.odm.declarative import MappedClass

from commons import EnhancingClass

collection_name = 'worker_states'

config = configparser.ConfigParser()
config.read('C://Users//Zerbs//accounts.sec')

session = create_session(config['mongo']['login'], config['mongo']['password'], config['mongo']['path'])

class WorkerState(MappedClass, EnhancingClass):
    
    class __mongometa__:
        session = session
        name = collection_name
    
    _id = FieldProperty(schema.ObjectId)
    name = FieldProperty(schema.String(required=True))
    
    description = FieldProperty(schema.String(if_missing = ''))
    
#worker_state_1 = WorkerState(name = "basic")
#worker_state_2 = WorkerState(name = "ill")
#worker_state_3 = WorkerState(name = "rest")

#session.flush_all()