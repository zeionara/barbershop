import sys
sys.path.insert(0, 'extra/')
sys.path.insert(0, 'crud/')


import get_schedule
import worker_states
import positions
import contacts
import services
import holdings
import salaries
import premium_sizes
import premiums
import nested_states

import commons


def get_handler(typed_command):
    for command in commands:
        if (typed_command == command[0]) or (typed_command == command[1]):
            return command[3]

commands = sorted((('get_schedule','gs', 'master_id [date_of_visit_in_format_10.10.2010]', get_schedule.execute),
            ('create_worker_state','cws','state_name [state_description]', worker_states.create),
            ('delete_worker_state','dws','state_id', worker_states.delete),
            ('update_worker_state','uws','state_id [-n new_name] [new_description]', worker_states.update),
            ('read_worker_state','rws',commons.get_column_shorts(worker_states.columns), worker_states.read),
            ('create_position','cp','position_name [position_description]', positions.create),
            ('delete_position','dp','state_id', positions.delete),
            ('update_position','up','state_id [-n new_name] [-d new_description]', positions.update),
            ('read_position','rp',commons.get_column_shorts(positions.columns), positions.read),
            ('create_contact','cc','person_id person_status contact_type contact', contacts.create),
            ('delete_contact','dc','contact_id', contacts.delete),
            ('read_contact','rc',commons.get_column_shorts(contacts.columns), contacts.read),
            ('update_contact','uc','contact_id [-i person_id] [-s person_status] [-t contact_type] [-c contact]', contacts.update),
            ('create_service','cs','service_name price [service_average_duration] [service_description]', services.create),
            ('update_service','us','service_id [-n service_name] [-p price] [-a service_average_duration] [-d service_description]', services.update),
            ('delete_service','ds','service_id', services.delete),
            ('read_service','rs',commons.get_column_shorts(services.columns), services.read),
            ('create_holding','ch',commons.get_column_shorts_insert(holdings.columns), holdings.create),
            ('update_holding','uh',commons.get_column_shorts_update(holdings.columns), holdings.update),
            ('delete_holding','dh','holding_id', holdings.delete),
            ('read_holding','rh',commons.get_column_shorts(holdings.columns), holdings.read),
            ('create_salary','csl','worker_id common vacation sick', salaries.create),
            ('update_salary','usl','salary_id [-w worker_id] [-c common] [-v vacation] [-s sick]', salaries.update),
            ('delete_salary','dsl','salary_id', salaries.delete),
            ('read_salary','rsl',commons.get_column_shorts(salaries.columns), salaries.read),
            ('create_premium_size','cps','premium_name minimal_value maximal_value [description]', premium_sizes.create),
            ('update_premium_size','ups','premium_id [-n name] [-min minimal_value] [-max maximal_value] [-d description]', premium_sizes.update),
            ('delete_premium_size','dps','premium_id', premium_sizes.delete),
            ('read_premium_size','rps',commons.get_column_shorts(premium_sizes.columns), premium_sizes.read),
            ('create_premium','cpr','worker_id premium_id earning_date_in_format_10.10.2010 premium_size [note]', premiums.create),
            ('update_premium','upr','premium_id [-w worker_id] [-p preium_id] [-e earning_date in format 10.10.2010] [-s premium_size] [-d note]', premiums.update),
            ('delete_premium','dpr','premium_id', premiums.delete),
            ('read_premium','rpr',commons.get_column_shorts(premiums.columns), premiums.read),
            ('create_worker_day_state','cwds','worker_id date_in_format_10.10.2010 state_id', nested_states.create),
            ('delete_worker_day_state','dwds','worker_id date_in_format_10.10.2010', nested_states.delete),
            ('read_worker_day_state','rwds','worker_id '+commons.get_column_shorts(nested_states.columns), nested_states.read)))
