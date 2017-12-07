import configparser
from connection import create_session

from ming import schema
from ming.odm import FieldProperty
from ming.odm.declarative import MappedClass

from commons import EnhancingClass
from commons import PasswordProperty
from commons import SexProperty
from commons import ImageProperty
from commons import StringSingleForeignKeyProperty

from qualifications import Qualification
from positions import Position

collection_name = 'workers'
config = configparser.ConfigParser()
config.read('C://Users//Zerbs//accounts.sec')

session = create_session(config['mongo']['login'], config['mongo']['password'], config['mongo']['path'])

class Worker(MappedClass, EnhancingClass):

    class __mongometa__:
        session = session
        name = collection_name

    _id = FieldProperty(schema.ObjectId)
    name = FieldProperty(schema.String(required=True))
    surname = FieldProperty(schema.String(required=True))
    sex = SexProperty()
    address = FieldProperty(schema.String(required=True))
    login = FieldProperty(schema.String(required=True))
    passwd = PasswordProperty()

    qualification = StringSingleForeignKeyProperty(Qualification)
    position = StringSingleForeignKeyProperty(Position)

    patronymic = FieldProperty(schema.String(if_missing = ''))
    avatar = ImageProperty()

#worker = Worker(name = "Bill", surname = "Gates", sex = "m", address = "Silicon Valley, 25",
#                login = "bill",
#                passwd = "12345",
#                qualification = "7cbe",
#                position = "7e20")
#print("ok")
#session.flush_all()
