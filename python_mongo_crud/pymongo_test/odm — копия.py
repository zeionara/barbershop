import configparser
import pymongo
import datetime

from ming import create_datastore
from ming.odm import ThreadLocalODMSession

from ming import schema
from ming.odm import FieldProperty
from ming.odm import ForeignIdProperty
from ming.odm import RelationProperty
from ming.odm.declarative import MappedClass
import ming
from ming.odm.mapper import MapperExtension

from ming.schema import ObjectId

config = configparser.ConfigParser()
config.read('C://Users//Zerbs//accounts.sec')

session = ThreadLocalODMSession(
    bind=create_datastore('mongodb://%s:%s@%s' % (config["mongo"]["login"], 
                                                   config["mongo"]["password"],
                                                   config["mongo"]["path"]))
)

def get_by_id(class_obj, id):
    return class_obj.query.find().all()[0].get_by_id(id)
    
class MyExtension(MapperExtension):
    def before_insert(self, obj, st, sess):
        worker = get_by_id(TWorker, str(obj.worker_id))
#        obj.worker_id = "str(worker._id)"
#        premium_size = get_by_id(TPremiumSize, str(obj.premium_id))
#        obj.premium_id = "str(premium_size._id)"
#        
#       if (worker == None):
#            raise ValueError("Worker id must match an id in table with workers")
            
#        if (premium_size == None):
#            raise ValueError("Premium id must match an id in table with premium sizes")
#        
#        if (obj.premium_size > premium_size.max) or (obj.premium_size < premium_size.min):
#            raise ValueError("Premium size must be between %i and %i" % (premium_size.min, premium_size.max))

class HelloWorld(MappedClass):
    class __mongometa__:
        session = session
        name = 'testcollection'
    
    _id = FieldProperty(schema.ObjectId)
    title = FieldProperty(schema.String(required=True))
    text = FieldProperty(schema.String(if_missing='empty...'))

class EnhancingClass():
    def get_by_id(self, searched_id):
        for item in self.__class__.query.find().all():
            if (str(item._id)[-len(searched_id):] == searched_id):
                return item
        return None
##
    
class TWorker(MappedClass, EnhancingClass):
    class __mongometa__:
        session = session
        name = 'testworkers'
    
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
        extensions = [ MyExtension ]
    
    #primary key
    _id = FieldProperty(schema.ObjectId)
    
    #foreign keys
    premium_id = FieldProperty(schema.String(required = True))
    worker_id = FieldProperty(schema.String(required = True))
    
    #properties
    earning_date = FieldProperty(schema.DateTime(required=True))
    premium_size = FieldProperty(schema.Int(required=True))
    note = FieldProperty(schema.String(if_missing = ''))
    


#tp = TPremiumSize.query.find().all()[0]
#tw = TWorker.query.find().all()[0]    
#print(TPremiumSize.query.find().all())
#print(tp.get_by_id("4e8")._id)
#print(tw.get_by_id("4c0")._id)
#print(get_by_id(TPremium, 100))
tpr = TPremium(premium_id = "4e8", worker_id = "4c0", earning_date = datetime.datetime(2017, 11, 10),
               premium_size = 4100, note = "the best worker!")


session.flush_all()

