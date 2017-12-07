import configparser
from connection import create_session

from ming import schema
from ming.odm import FieldProperty
from ming.odm.declarative import MappedClass

from commons import EnhancingClass
from commons import StringSingleForeignKeyUniqueProperty

from workers import Worker

collection_name = 'salaries'

config = configparser.ConfigParser()
config.read('C://Users//Zerbs//accounts.sec')

session = create_session(config['mongo']['login'], config['mongo']['password'], config['mongo']['path'])

class Salary(MappedClass, EnhancingClass):

    class __mongometa__:
        session = session
        name = collection_name

    _id = FieldProperty(schema.ObjectId)
    worker_id = StringSingleForeignKeyUniqueProperty(Worker, 'worker_id')

    common = FieldProperty(schema.Float(required=True))
    vacation = FieldProperty(schema.Float(required=True))
    sick = FieldProperty(schema.Float(required=True))

#salary = Salary(worker_id = "197", common = 3000.1, vacation = 2000.1, sick = 1000.1)

#session.clear()
