import configparser
from connection import create_session

from ming import schema
from ming.odm import FieldProperty
from ming.odm.declarative import MappedClass

from commons import EnhancingClass
from commons import PasswordProperty
from commons import SexProperty
from commons import ImageProperty

collection_name = 'clients'
config = configparser.ConfigParser()
config.read('C://Users//Zerbs//accounts.sec')

session = create_session(config['mongo']['login'], config['mongo']['password'], config['mongo']['path'])

class Client(MappedClass, EnhancingClass):
    
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
    
    patronymic = FieldProperty(schema.String(if_missing = ''))
    avatar = ImageProperty()
    
client = Client(name = "Sweeney", surname = "Todd", sex = "w", address = "Flit-street, 13",
                login = "stodd", 
                passwd = "12345", 
                avatar = "C:\\Users\\Zerbs\\Desktop\\databases_kursach\\python_mongo_crud\\blob\\ava.png")
print("ok")
session.flush_all()