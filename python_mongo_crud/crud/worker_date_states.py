import configparser
from connection import create_session

from ming import schema
from ming.odm import FieldProperty
from ming.odm.declarative import MappedClass

from commons import EnhancingClass
from commons import StringSingleForeignKeyUniqueProperty
from commons import DateStatesProperty

from workers import Worker
from worker_states import WorkerState

import datetime

collection_name = 'worker_date_states'

config = configparser.ConfigParser()
config.read('C://Users//Zerbs//accounts.sec')

session = create_session(config['mongo']['login'], config['mongo']['password'], config['mongo']['path'])

class WorkerDateStates(MappedClass, EnhancingClass):
    
    class __mongometa__:
        session = session
        name = collection_name
    
    _id = FieldProperty(schema.ObjectId)
    worker_id = StringSingleForeignKeyUniqueProperty(Worker, 'worker_id')
    
    date_states = DateStatesProperty(WorkerState)
    
workerdatestates = WorkerDateStates(worker_id = "197", date_states = [[datetime.datetime(2017,10,10), "e88"],
                                                                       [datetime.datetime(2017,11,10), "e87"],
                                                                       [datetime.datetime(2017,12,10), "e88"]])

session.flush_all()