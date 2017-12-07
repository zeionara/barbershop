import configparser
from connection import create_session

from ming import schema
from ming.odm import FieldProperty
from ming.odm.declarative import MappedClass

from commons import EnhancingClass
from commons import StringForeignKeyListProperty


from services import Service

collection_name = 'qualifications'

config = configparser.ConfigParser()
config.read('C://Users//Zerbs//accounts.sec')

session = create_session(config['mongo']['login'], config['mongo']['password'], config['mongo']['path'])

class Qualification(MappedClass, EnhancingClass):

    class __mongometa__:
        session = session
        name = collection_name

    _id = FieldProperty(schema.ObjectId)
    name = FieldProperty(schema.String(required=True))

    description = FieldProperty(schema.String(if_missing = ''))
    rendered_services = StringForeignKeyListProperty(Service)

#qualification = Qualification(name = "daemon-hairdresser", rendered_services = ["fa10"])

session.flush_all()
#session.flush_all()
