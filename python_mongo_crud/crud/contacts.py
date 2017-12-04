import configparser
from connection import create_session

from ming import schema
from ming.odm import FieldProperty
from ming.odm.declarative import MappedClass

from commons import EnhancingClass
from commons import PasswordProperty
from commons import SexProperty
from commons import ContactTypeProperty
from commons import StringForeignKeyProperty
from commons import PersonTypeProperty
from commons import ContactProperty

from clients import Client

collection_name = 'contacts'
config = configparser.ConfigParser()
config.read('C://Users//Zerbs//accounts.sec')

session = create_session(config['mongo']['login'], config['mongo']['password'], config['mongo']['path'])

class Contact(MappedClass, EnhancingClass):
    
    class __mongometa__:
        session = session
        name = collection_name
    
    _id = FieldProperty(schema.ObjectId)
    person_type = PersonTypeProperty()
    person_id = StringForeignKeyProperty([Client], ['client'], 'person_type')
    type = ContactTypeProperty()
    contact = ContactProperty('type')
    
    
contact = Contact(person_type = "client", person_id = "2bd", type = "phone", contact = "+7 (911) 111-11-11")

print("-ok")
session.flush_all()
#session.flush_all()