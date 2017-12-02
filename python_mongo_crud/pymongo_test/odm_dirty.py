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
    
    
class MyExtension(MapperExtension):
    def before_insert(self, obj, st, sess):
        print("--"*20)
        #print(str(obj.worker_id))
        print(obj)
        if (TWorker.query.find().all()[0].get_by_id(str(obj.worker_id)) == None):
            raise ValueError("Worker id must match an id in table with workers")
        premium_size = TPremiumSize.query.find().all()[0].get_by_id(str(obj.premium_id))
        if (premium_size == None):
            raise ValueError("Premium id must match an id in table with premium sizes")
        
        if (obj.premium_size > premium_size.max) or (obj.premium_size < premium_size.min):
            raise ValueError("Premium size must be between %i and %i" % (premium_size.min,
                                                                         premium_size.max))

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
    #premiums = RelationProperty(TPremium)
    
class TPremiumSize(MappedClass, EnhancingClass):
    class __mongometa__:
        session = session
        name = 'testpremiumssizes'
    
    _id = FieldProperty(schema.ObjectId)
    name = FieldProperty(schema.String(required=True))
    min = FieldProperty(schema.Int(required=True))
    max = FieldProperty(schema.Int(required=True))
    description = FieldProperty(schema.String(if_missing = ''))
    
    #worker = ForeignIdProperty(TWorker)
    #premiums = RelationProperty('TPremium')
    
    
class TPremium(MappedClass, EnhancingClass):
    class __mongometa__:
        session = session
        name = 'testpremiums'
        extensions = [ MyExtension ]
    
    _id = FieldProperty(schema.ObjectId)
    premium_id = ForeignIdProperty(TPremiumSize)
    worker_id = ForeignIdProperty(TWorker)
    earning_date = FieldProperty(schema.DateTime(required=True))
    premium_size = FieldProperty(schema.Int(required=True))
    note = FieldProperty(schema.String(if_missing = '')) 
    
    worker = RelationProperty(TWorker)
    premium = RelationProperty(TPremiumSize)
    
    

class WikiPage(MappedClass):
    class __mongometa__:
        session = session
        name = 'testcollection'
        extensions = [ MyExtension ]

    _id = FieldProperty(schema.ObjectId)
    title = FieldProperty(schema.String(required=True))
    text = FieldProperty(schema.String(if_missing=''))


class WikiComment(MappedClass):
    class __mongometa__:
        session = session
        name = 'wiki_comment'
        

    _id = FieldProperty(schema.ObjectId)
    page_id = ForeignIdProperty(WikiPage, uselist=True)
    text = FieldProperty(schema.String(if_missing=''))

    page = RelationProperty(WikiPage)
    


print('1')
wp = WikiPage.query.get(title='MmyFirstPage')
print(wp)
print('2')
#WikiComment(page_id = wp._id, text='A comment')
print('3')

#HelloWorld(title='Hello',text='World')
#print(session.db.)
    
#TWorker(name="John",surname="Whilliams")
#TWorker(name="Bill",surname="White")
#tp = TPremiumSize(name="first",description="For good work",min=1000,max=5000)
tp = TPremiumSize.query.find().all()[0]
tw = TWorker.query.find().all()[0]    
print(TPremiumSize.query.find().all())
print(tp.get_by_id("4e8")._id)
print(tw.get_by_id("4c0")._id)

tpr = TPremium(premium_id = tp._id, worker_id = tw._id, 
               earning_date = datetime.datetime(2017, 11, 10), premium_size = 2100,
               note = "the best worker!")
#print(tw.get_by_id("4c9"))
#print(TWorker.query.find())
#for item in TWorker.query.find().all():
#    print(str(item._id) == "5a22f36e89ad9319709cd4c0")

session.flush_all()

#class SampleDocument(Document):

        #def my_sum(self):
                #return self["a"] + self["b"]

#class SampleCollection(Collection):
        #document_class = SampleDocument

        #def find_by_a(self, a_value):
                #return self.find_one({"a": a_value})

# Then use it in your code like this:

#print(config["mongo"]["login"])

#client = MongoClient()

#Sample = SampleCollection(collection=client.barbershopdb.testcollection)

#Sample.insert({"a": 1, "b": 2})
#Sample.insert({"a": 2, "b": 3})

#assert Sample.count() == 2

#five = Sample.find_by_a(2)
#assert five.my_sum() == 5
