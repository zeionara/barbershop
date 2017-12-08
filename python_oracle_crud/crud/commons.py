import hashlib
from ming import schema
from ming.odm import FieldProperty
import re
import numpy as np
from scipy.misc import imread

import datetime


def get_by_id(class_obj, iden):
    return class_obj.query.find().all()[0].get_by_id(iden)


class EnhancingClass():
    def get_by_id(self, searched_id):
        for item in self.__class__.query.find().all():
            if (str(item._id)[-len(searched_id):] == searched_id):
                return item
        return None

class PasswordProperty(FieldProperty):
    def __init__(self):
        super(PasswordProperty, self).__init__(schema.String(required=True))

    def __get__(self, instance, cls=None):
        if instance is None: return self

        class Password(str):
            def __new__(cls, content):
                self = str.__new__(cls, '******')
                self.raw_value = content
                return self

        return Password(super(PasswordProperty, self).__get__(instance, cls))

    def __set__(self, instance, value):
        pwd = hashlib.md5(value.encode("utf-8")).hexdigest()
        super(PasswordProperty, self).__set__(instance, pwd)

class SexProperty(FieldProperty):
    def __init__(self):
        super(SexProperty, self).__init__(schema.String(required=True))

    def __get__(self, instance, cls=None):

        if instance is None: return self

        return super(SexProperty, self).__get__(instance, cls)

    def __set__(self, instance, value):
        if value not in ['m','w']:
            raise ValueError("Invalid value of property with type sex")
        super(SexProperty, self).__set__(instance, value)

class ContactTypeProperty(FieldProperty):
    def __init__(self):
        super(ContactTypeProperty, self).__init__(schema.String(required=True))

    def __get__(self, instance, cls=None):

        if instance is None: return self

        return super(ContactTypeProperty, self).__get__(instance, cls)

    def __set__(self, instance, value):
        if value not in ['e-mail','phone','vk']:
            raise ValueError("Invalid value of property with type contact type")
        super(ContactTypeProperty, self).__set__(instance, value)

class PersonTypeProperty(FieldProperty):
    def __init__(self):
        super(PersonTypeProperty, self).__init__(schema.String(required=True))

    def __get__(self, instance, cls=None):

        if instance is None: return self

        return super(PersonTypeProperty, self).__get__(instance, cls)

    def __set__(self, instance, value):
        if value not in ['worker', 'client']:
            raise ValueError("Invalid value of property with type person type")
        super(PersonTypeProperty, self).__set__(instance, value)

class ImageProperty(FieldProperty):
    def get_image_data(self, path):
        return imread(path).astype(np.float32)

    def __init__(self):
        super(ImageProperty, self).__init__(schema.Anything(if_missing = []))

    def __get__(self, instance, cls=None):

        if instance is None: return self

        return super(ImageProperty, self).__get__(instance, cls)

    def __set__(self, instance, path):
        super(ImageProperty, self).__set__(instance, self.get_image_data(path).tolist())

class StringForeignKeyProperty(FieldProperty):
    def __init__(self, referenced_classes, referenced_classes_keys, collection_name):
        self.referenced_classes = referenced_classes
        self.referenced_classes_keys = referenced_classes_keys
        self.collection_name = collection_name
        super(StringForeignKeyProperty, self).__init__(schema.String(if_missing = ''))

    def __get__(self, instance, cls=None):

        if instance is None: return self

        return super(StringForeignKeyProperty, self).__get__(instance, cls)

    def __set__(self, instance, key):
        referenced_object = self.referenced_classes[self.referenced_classes_keys.index(getattr(instance,self.collection_name))]\
        .query.find().first().get_by_id(key)
        if (referenced_object == None):
            raise ValueError("Foreign key is invalid")
        #instance._id = str(referenced_object._id)
        super(StringForeignKeyProperty, self).__set__(instance, str(referenced_object._id))

class ContactProperty(FieldProperty):
    def __init__(self, contact_type_property_name):
        self.contact_type_property_name = contact_type_property_name
        super(ContactProperty, self).__init__(schema.String(if_missing = ''))

    def __get__(self, instance, cls=None):

        if instance is None: return self

        return super(ContactProperty, self).__get__(instance, cls)

    def __set__(self, instance, contact):
        contact_type = getattr(instance,self.contact_type_property_name)
        result = None
        pattern = ""
        if (contact_type == "phone"):
            pattern = r'\+7 \(9[0-9]{2}\) [0-9]{3}\-[0-9]{2}\-[0-9]{2}'
        elif (contact_type == "e-mail"):
            pattern = r'[a-zA-Z][a-zA-Z0-9]{1,}@[a-zA-Z0-9]{3,}.[a-zA-Z0-9]{3,}'
        elif (contact_type == "vk"):
            pattern = r'[a-z0-9A-Z_]{5,}'
        result = re.match(pattern, contact)
        if (result == None):
            raise ValueError("Contact is invalid")
        super(ContactProperty, self).__set__(instance, contact)

class StringForeignKeyListProperty(FieldProperty):
    def __init__(self, referenced_class):
        self.referenced_class = referenced_class
        super(StringForeignKeyListProperty, self).__init__(schema.Array(str, required = True))

    def __get__(self, instance, cls=None):

        if instance is None: return self

        return super(StringForeignKeyListProperty, self).__get__(instance, cls)

    def __set__(self, instance, keys):
        extended_keys = []
        for key in keys:
            referenced_object = self.referenced_class.query.find().first().get_by_id(key)
            if (referenced_object == None):
                raise ValueError("Foreign key is invalid")
            extended_keys.append(str(referenced_object._id))

        super(StringForeignKeyListProperty, self).__set__(instance, list(set(extended_keys)))

class StringSingleForeignKeyProperty(FieldProperty):
    def __init__(self, referenced_class):
        self.referenced_class = referenced_class
        super(StringSingleForeignKeyProperty, self).__init__(schema.String(required = True))

    def __get__(self, instance, cls=None):

        if instance is None: return self

        return super(StringSingleForeignKeyProperty, self).__get__(instance, cls)

    def __set__(self, instance, key):
        referenced_object = self.referenced_class.query.find().first().get_by_id(key)
        if (referenced_object == None):
            raise ValueError("Foreign key is invalid")

        super(StringSingleForeignKeyProperty, self).__set__(instance, str(referenced_object._id))

class StringSingleForeignKeyUniqueProperty(FieldProperty):
    def __init__(self, referenced_class, attr_name):
        self.referenced_class = referenced_class
        self.attr_name = attr_name
        super(StringSingleForeignKeyUniqueProperty, self).__init__(schema.String(required = True))

    def __get__(self, instance, cls=None):

        if instance is None: return self

        return super(StringSingleForeignKeyUniqueProperty, self).__get__(instance, cls)

    def check_unique(self, current_class, key):
        #print(current_class.query.find().all())
        for item in current_class.query.find().all():
            #print([getattr(item, self.attr_name),key])
            if (getattr(item, self.attr_name) == key):
                raise ValueError("Given key is not unique")


    def __set__(self, instance, key):
        referenced_object = self.referenced_class.query.find().first().get_by_id(key)
        if (referenced_object == None):
            raise ValueError("Foreign key is invalid")
        self.check_unique(type(instance), str(referenced_object._id))
        super(StringSingleForeignKeyUniqueProperty, self).__set__(instance, str(referenced_object._id))

class HoldingsWithQuantityProperty(FieldProperty):
    def __init__(self, referenced_class):
        self.referenced_class = referenced_class
        super(HoldingsWithQuantityProperty, self).__init__(schema.Anything(required = True))

    def __get__(self, instance, cls=None):

        if instance is None: return self

        return super(HoldingsWithQuantityProperty, self).__get__(instance, cls)

    def __set__(self, instance, holdings):
        extended_holdings = []
        for holding in holdings:
            print(holding[0])
            referenced_object = self.referenced_class.query.find().first().get_by_id(holding[0])
            if (referenced_object == None):
                raise ValueError("Foreign key is invalid")
            extended_holdings.append([str(referenced_object._id), holding[1]])

        super(HoldingsWithQuantityProperty, self).__set__(instance, extended_holdings)

class VisitDateTimeProperty(FieldProperty):
    def __init__(self, worker_class, service_class):
        self.worker_class = worker_class
        self.service_class = service_class
        super(VisitDateTimeProperty, self).__init__(schema.DateTime(required = True))

    def __get__(self, instance, cls=None):

        if instance is None: return self

        return super(VisitDateTimeProperty, self).__get__(instance, cls)

    def get_request_duration(self, request):
        service_durations = []
        if (request.factical_durability == None):
            for service_id in request.service_ids:
                service = self.service_class.query.find().first().get_by_id(service_id)
                if (service.avg_duration != None):
                    service_durations.append(service.avg_duration)
        else:
            return request.factical_durability
        if (len(service_durations) == 0):
            print("taking default")
            return 100
        print(service_durations)
        return float(np.max(service_durations))

            #raise ValueError("Durability is not set")

    def __set__(self, instance, date_time):
        current_request_duration = self.get_request_duration(instance)
        end_service_date_time = date_time + datetime.timedelta(minutes = current_request_duration)
        for worker_id in instance.worker_ids:
            worker = self.worker_class.query.find().first().get_by_id(worker_id)
            for request in type(instance).query.find().all():
                if str(worker._id) in request.worker_ids:
                    if ((request.visit_date_time - datetime.timedelta(minutes = 5) <= date_time) and \
                    (date_time <= request.visit_date_time + datetime.timedelta(minutes = self.get_request_duration(request)) + datetime.timedelta(minutes = 5))) or \
                    ((request.visit_date_time - datetime.timedelta(minutes = 5) <= end_service_date_time) and \
                    (end_service_date_time <= request.visit_date_time + datetime.timedelta(minutes = self.get_request_duration(request)) + datetime.timedelta(minutes = 5))):
                        raise ValueError("Master is busy at that time")

        super(VisitDateTimeProperty, self).__set__(instance, date_time)


class DateStatesProperty(FieldProperty):
    def __init__(self, state_class):
        self.state_class = state_class
        super(DateStatesProperty, self).__init__(schema.Anything(required = True))

    def __get__(self, instance, cls=None):

        if instance is None: return self

        return super(DateStatesProperty, self).__get__(instance, cls)

    def validate_state_id(self, state_id):
        state = get_by_id(self.state_class, state_id)
        if state == None:
            raise ValueError("No such state")
        return str(state._id)

    def __set__(self, instance, datestates):
        j = 0
        for datestate in datestates:
            datestate[1] = self.validate_state_id(datestate[1])
            i = 0
            for i_datestate in datestates:
                if (i_datestate[0] == datestate[0]) and (i != j):
                    raise ValueError("This date is used multiple times")
                i += 1
            j += 1

        super(DateStatesProperty, self).__set__(instance, datestates)
