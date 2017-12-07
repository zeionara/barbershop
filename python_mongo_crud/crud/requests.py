import configparser
from connection import create_session

import datetime

from ming import schema
from ming.odm import FieldProperty
from ming.odm.declarative import MappedClass

from commons import EnhancingClass
from commons import StringForeignKeyListProperty
from commons import HoldingsWithQuantityProperty
from commons import VisitDateTimeProperty


from workers import Worker
from clients import Client
from services import Service
from holdings import Holding

collection_name = 'requests'

config = configparser.ConfigParser()
config.read('C://Users//Zerbs//accounts.sec')

session = create_session(config['mongo']['login'], config['mongo']['password'], config['mongo']['path'])

class Request(MappedClass, EnhancingClass):

    class __mongometa__:
        session = session
        name = collection_name
        custom_indexes = [
            dict(fields=('worker_id',), unique = False),
            dict(fields=('client_id',), unique = False),
            dict(fields=('service_id',), unique = False)
        ]

    _id = FieldProperty(schema.ObjectId)

    visit_date_time = VisitDateTimeProperty(Worker, Service)

    worker_ids = StringForeignKeyListProperty(Worker)
    client_ids = StringForeignKeyListProperty(Client)
    service_ids = StringForeignKeyListProperty(Service)
    holdings = HoldingsWithQuantityProperty(Holding)

    note = FieldProperty(schema.String(if_missing = ""))
    factical_durability = FieldProperty(schema.Float(if_missing = None))

#request = Request(worker_ids = ["0197"], client_ids = ["fa25"], service_ids = ["3fe9"], holdings = [["414f", 10]],
#                  visit_date_time = datetime.datetime(2017,10,10,14,40,0))

session.flush_all()
