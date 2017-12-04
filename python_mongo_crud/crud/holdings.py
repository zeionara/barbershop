import configparser
from connection import create_session

from ming import schema
from ming.odm import FieldProperty
from ming.odm.declarative import MappedClass
from ming.odm.mapper import MapperExtension

from commons import EnhancingClass

collection_name = 'holdings'

config = configparser.ConfigParser()
config.read('C://Users//Zerbs//accounts.sec')

session = create_session(config['mongo']['login'], config['mongo']['password'], config['mongo']['path'])

class HoldingTriggers(MapperExtension):
    
    def validate(self, obj):
        if (obj.quantity <= 0):
            raise ValueError("Quantity must be more than zero")
        if (obj.price <= 0):
            raise ValueError("Price must be more than zero")
    
    def before_insert(self, obj, st, sess):
        self.validate(obj)
        
    def before_update(self, obj, st, sess):
        self.validate(obj)

class Holding(MappedClass, EnhancingClass):
    
    class __mongometa__:
        session = session
        name = collection_name
        extensions = [HoldingTriggers]
    
    _id = FieldProperty(schema.ObjectId)
    name = FieldProperty(schema.String(required=True))
    quantity = FieldProperty(schema.Float(required=True))
    price = FieldProperty(schema.Float(required=True))
    
#holding = Holding(name = "small scissors", quantity = 50, price = 200.5)

#session.flush_all()
