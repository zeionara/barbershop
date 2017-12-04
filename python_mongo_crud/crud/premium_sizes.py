import configparser
from connection import create_session

from ming import schema
from ming.odm import FieldProperty
from ming.odm.declarative import MappedClass
from ming.odm.mapper import MapperExtension

from commons import EnhancingClass

collection_name = 'premium_sizes'

config = configparser.ConfigParser()
config.read('C://Users//Zerbs//accounts.sec')

session = create_session(config['mongo']['login'], config['mongo']['password'], config['mongo']['path'])

class PremiumSizeTriggers(MapperExtension):
    
    def validate(self, obj):
        if (obj.min >= obj.max):
            raise ValueError("Min value must be less than max")
    
    def before_insert(self, obj, st, sess):
        self.validate(obj)
        
    def before_update(self, obj, st, sess):
        self.validate(obj)

class PremiumSize(MappedClass, EnhancingClass):
    
    class __mongometa__:
        session = session
        name = collection_name
        extensions = [PremiumSizeTriggers]
    
    _id = FieldProperty(schema.ObjectId)
    name = FieldProperty(schema.String(required=True))
    min = FieldProperty(schema.Float(required=True))
    max = FieldProperty(schema.Float(required=True))
    description = FieldProperty(schema.String(if_missing = ''))
    
premsize = PremiumSize(name="Good work", min = 300, max = 400.3)

session.flush_all()