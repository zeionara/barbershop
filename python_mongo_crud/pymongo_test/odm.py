import configparser
import datetime

from ming import create_datastore
from ming.odm import ThreadLocalODMSession
from ming import schema
from ming.odm import FieldProperty
from ming.odm.declarative import MappedClass
from ming.odm.mapper import MapperExtension


config = configparser.ConfigParser()
config.read('C://Users//Zerbs//accounts.sec')

session = ThreadLocalODMSession(
    bind = create_datastore('mongodb://%s:%s@%s' % (config["mongo"]["login"], 
                                                  config["mongo"]["password"],
                                                  config["mongo"]["path"]))
)

class EnhancingClass():
    def get_by_id(self, searched_id):
        for item in self.__class__.query.find().all():
            if (str(item._id)[-len(searched_id):] == searched_id):
                return item
        return None
    
class PremiumTriggers(MapperExtension):
    def before_insert(self, obj, st, sess):
        
        worker = get_by_id(TWorker, obj.worker_id)        
        premium_size = get_by_id(TPremiumSize, obj.premium_id)
        
        if (worker == None):
            raise ValueError("Worker id must match an id in table with workers")
            
        obj.worker_id = str(worker._id)
        
        if (premium_size == None):
            raise ValueError("Premium id must match an id in table with premium sizes")
        
        obj.premium_id = str(premium_size._id)
        
        if (obj.premium_size > premium_size.max) or (obj.premium_size < premium_size.min):
            raise ValueError("Premium size must be between %i and %i" % (premium_size.min,
                                                                         premium_size.max))
    def before_update(self, obj, st, sess):
        print("upd")
        print(obj)
        
class WorkerTriggers(MapperExtension):     
    def before_update(self, obj, st, sess):
        print("upd")
        print(obj)
    
class TWorker(MappedClass, EnhancingClass):
    class __mongometa__:
        session = session
        name = 'testworkers'
        extensions = [ WorkerTriggers ]
    
    _id = FieldProperty(schema.ObjectId)
    name = FieldProperty(schema.String(required=True))
    surname = FieldProperty(schema.String(required=True))
    
class TPremiumSize(MappedClass, EnhancingClass):
    class __mongometa__:
        session = session
        name = 'testpremiumssizes'
        
    
    _id = FieldProperty(schema.ObjectId)
    name = FieldProperty(schema.String(required=True))
    min = FieldProperty(schema.Int(required=True))
    max = FieldProperty(schema.Int(required=True))
    description = FieldProperty(schema.String(if_missing = ''))
    
class TPremium(MappedClass, EnhancingClass):
    class __mongometa__:
        session = session
        name = 'testpremiums'
        extensions = [ PremiumTriggers ]
    
    #primary key
    _id = FieldProperty(schema.ObjectId)
    
    #foreign keys
    premium_id = FieldProperty(schema.String(required = True)) 
    worker_id = FieldProperty(schema.String(required = True)) 
    
    #properties
    earning_date = FieldProperty(schema.DateTime(required=True))
    premium_size = FieldProperty(schema.Int(required=True))
    note = FieldProperty(schema.String(if_missing = '')) 


def get_by_id(class_obj, iden):
    return class_obj.query.find().all()[0].get_by_id(iden)
    

tp = TPremiumSize.query.find().all()[0]
tw = TWorker.query.find().all()[0]

tpr = TPremium(premium_id = "4e8", worker_id = "4c0", 
               earning_date = datetime.datetime(2017, 11, 10), premium_size = 3100,
               note = "the best worker!")

tw.name = "name"


session.flush_all()

#tpr = TPremium.query.find().all()
#print(tpr)
#tpr.note = "the best of the bests!"

#session.flush_all()