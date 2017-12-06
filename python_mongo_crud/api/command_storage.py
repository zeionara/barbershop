import holdings_ as h
import contacts_ as c
import commons_ as cms


def get_handler(typed_command):
    for command in commands:
        if (typed_command == command[0]) or (typed_command == command[1]):
            return command[3]

commands = sorted((('create_holding','ch', cms.get_create_rules('ch', h.field_status, h.field_shorts, h.field_names, h.field_descriptions), h.create),
('read_holding','rh', cms.get_read_delete_rules('rh', h.field_status, h.field_shorts, h.field_names, h.field_descriptions), h.read),
('update_holding','uh', cms.get_update_rules('uh', h.field_status, h.field_shorts, h.field_names, h.field_descriptions), h.read),
('delete_holding','dh', cms.get_read_delete_rules('dh', h.field_status, h.field_shorts, h.field_names, h.field_descriptions), h.read),
('read_contacts','rc', cms.get_read_delete_rules('rc', c.field_status, c.field_shorts, c.field_names, c.field_descriptions), c.read),
('create_contacts','cc', cms.get_create_rules('cc', c.field_status, c.field_shorts, c.field_names, c.field_descriptions), c.create),
('update_contacts','uc', cms.get_update_rules('uc', c.field_status, c.field_shorts, c.field_names, c.field_descriptions), c.update),
('delete_contacts','dc', cms.get_update_rules('dc', c.field_status, c.field_shorts, c.field_names, c.field_descriptions), c.delete)))
