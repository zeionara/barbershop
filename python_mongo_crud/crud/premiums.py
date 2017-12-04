import configparser
from connection import create_session

import datetime

from ming import schema
from ming.odm import FieldProperty
from ming.odm.declarative import MappedClass
from ming.odm.mapper import MapperExtension

from commons import EnhancingClass
from commons import StringSingleForeignKeyProperty

from premium_sizes import PremiumSize
from workers import Worker
from commons import get_by_id

collection_name = 'premiums'

config = configparser.ConfigParser()
config.read('C://Users//Zerbs//accounts.sec')

session = create_session(config['mongo']['login'], config['mongo']['password'], config['mongo']['path'])

class PremiumTriggers(MapperExtension):
    
    def validate(self, obj):
        premium_size = get_by_id(PremiumSize, obj.premium_id)
        if (obj.size < premium_size.min) or (obj.size > premium_size.max):
            raise ValueError("Value must be between min and max")
    
    def before_insert(self, obj, st, sess):
        self.validate(obj)
        
    def before_update(self, obj, st, sess):
        self.validate(obj)

class Premium(MappedClass, EnhancingClass):
    
    class __mongometa__:
        session = session
        name = collection_name
        extensions = [PremiumTriggers]
    
    _id = FieldProperty(schema.ObjectId)
    
    premium_id = StringSingleForeignKeyProperty(PremiumSize)
    worker_id = StringSingleForeignKeyProperty(Worker)
    earning_date = FieldProperty(schema.DateTime(required=True))
    size = FieldProperty(schema.Float(required=True))
    
    note = FieldProperty(schema.String(if_missing = ""))
    
premium = Premium(premium_id = "39f", worker_id = "0197", 
                  earning_date = datetime.datetime(2017,2,2,0,0,0), size = 330)

session.flush_all()