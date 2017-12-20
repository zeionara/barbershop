from json import JSONEncoder
from ming.odm import MappedClass
import bson
import datetime
# Usage: MappedClassJSONEncoder().encode(data)
class MappedClassJSONEncoder(JSONEncoder):
    """
    Returns a MappedClass object JSON representation.
    """

    def _get_document_properties(self, klass):
        """
        Returns the declared properties of the MappedClass's child class which represents Mongo Document
        Includes only the user declared properties such as tenantId, _id etc
        :param klass:
        :return:
        """
        return [k for k in dir(klass) if k not in dir(MappedClass)]

    def _get_attr_json_value(self, attr):
        if isinstance(attr, bson.objectid.ObjectId):
            return str(attr)
        elif isinstance(attr, datetime.datetime):
            return attr.isoformat()
        elif isinstance(attr, dict):
            dict_data = {}
            for member in attr:
                dict_data.update({member: self._get_attr_json_value(attr[member])})
            return dict_data
        else:
            return attr

    def default(self, o):
        mapped_class_attributes = self._get_document_properties(type(o))
        attributes_data = {}
        for attr_name in mapped_class_attributes:
            attr = o.__getattribute__(attr_name)
            attributes_data.update({attr_name: self._get_attr_json_value(attr)})
        return attributes_data
