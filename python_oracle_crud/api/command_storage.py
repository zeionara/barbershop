import holdings_ as h
import contacts_ as c
import commons_ as cms
import worker_states_ as ws
import positions_ as p
import clients_ as cl
import services_ as s
import qualifications_ as q
import workers_ as w
import worker_date_states_ as wds
import salaries_ as sl
import premium_sizes_ as ps
import premiums_ as pr
import requests_ as r


def get_handler(typed_command):
    for command in commands:
        if (typed_command == command[0]) or (typed_command == command[1]):
            return command[3]

#print(list(cl.field_status))
#positions
commands = sorted((('read_positions','rp', cms.get_read_delete_rules('rp', p.field_status, p.field_shorts, p.field_names, p.field_descriptions), p.read),
('create_position','cp', cms.get_create_rules('cp',  p.field_status, p.field_shorts, p.field_names, p.field_descriptions), p.create),
('update_positions','up', cms.get_update_rules('up',  p.field_status, p.field_shorts, p.field_names, p.field_descriptions), p.update),
('delete_positions','dp', cms.get_update_rules('dp',  p.field_status, p.field_shorts, p.field_names, p.field_descriptions), p.delete),
#contacts
('read_contacts','rc', cms.get_read_delete_rules('rc', c.field_status, c.field_shorts, c.field_names, c.field_descriptions), c.read),
('create_contact','cc', cms.get_create_rules('cc', c.field_status, c.field_shorts, c.field_names, c.field_descriptions), c.create),
('update_contacts','uc', cms.get_update_rules('uc', c.field_status, c.field_shorts, c.field_names, c.field_descriptions), c.update),
('delete_contacts','dc', cms.get_update_rules('dc', c.field_status, c.field_shorts, c.field_names, c.field_descriptions), c.delete),
#worker states
('read_worker_states','rws', cms.get_read_delete_rules('rws', ws.field_status, ws.field_shorts, ws.field_names, ws.field_descriptions), ws.read),
('create_worker_state','cws', cms.get_create_rules('cws',  ws.field_status, ws.field_shorts, ws.field_names, ws.field_descriptions), ws.create),
('update_worker_states','uws', cms.get_update_rules('uws',  ws.field_status, ws.field_shorts, ws.field_names, ws.field_descriptions), ws.update),
('delete_worker_states','dws', cms.get_update_rules('dws',  ws.field_status, ws.field_shorts, ws.field_names, ws.field_descriptions), ws.delete),
#holdings
('create_holding','ch', cms.get_create_rules('ch', h.field_status, h.field_shorts, h.field_names, h.field_descriptions), h.create),
('read_holding','rh', cms.get_read_delete_rules('rh', h.field_status, h.field_shorts, h.field_names, h.field_descriptions), h.read),
('update_holding','uh', cms.get_update_rules('uh', h.field_status, h.field_shorts, h.field_names, h.field_descriptions), h.update),
('delete_holding','dh', cms.get_read_delete_rules('dh', h.field_status, h.field_shorts, h.field_names, h.field_descriptions), h.read),
#clients
('read_clients','rcl', cms.get_read_delete_rules('rcl', cl.field_status, cl.field_shorts, cl.field_names, cl.field_descriptions), cl.read),
('create_client','ccl', cms.get_create_rules('ccl', tuple(list(cl.field_status) + [2]), tuple(list(cl.field_shorts) + ["-ph"]),
        tuple(list(cl.field_names) + ["phone"]), tuple(list(cl.field_descriptions) + ["phone number"])), cl.create),
('update_clients','ucl', cms.get_update_rules('ucl',  cl.field_status, cl.field_shorts, cl.field_names, cl.field_descriptions), cl.update),
('delete_clients','dcl', cms.get_update_rules('dcl',  cl.field_status, cl.field_shorts, cl.field_names, cl.field_descriptions), cl.delete),
#services
('read_services','rs', cms.get_read_delete_rules('rs', s.field_status, s.field_shorts, s.field_names, s.field_descriptions), s.read),
('create_service','cs', cms.get_create_rules('cs',  s.field_status, s.field_shorts, s.field_names, s.field_descriptions), s.create),
('update_services','us', cms.get_update_rules('us',  s.field_status, s.field_shorts, s.field_names, s.field_descriptions), s.update),
('delete_services','ds', cms.get_update_rules('ds',  s.field_status, s.field_shorts, s.field_names, s.field_descriptions), s.delete),
#qualifications
('read_qualifications','rq', cms.get_read_delete_rules('rq', list(q.field_status) + list(q.extra_field_status),
                                                             list(q.field_shorts) + list(q.extra_field_shorts),
                                                             list(q.field_names) + list(q.extra_field_names),
                                                             list(q.field_descriptions) +list(q.extra_field_descriptions)),
                                                             q.read),
('create_qualification','cq', cms.get_create_rules('cq',  list(q.field_status) + list(q.extra_field_status),
                                                             list(q.field_shorts) + list(q.extra_field_shorts),
                                                             list(q.field_names) + list(q.extra_field_names),
                                                             list(q.field_descriptions) +list(q.extra_field_descriptions)),
                                                          q.create),
('update_qualifications','uq', cms.get_update_rules('uq',  list(q.field_status) + list(q.extra_field_status),
                                                             list(q.field_shorts) + list(q.extra_field_shorts),
                                                             list(q.field_names) + list(q.extra_field_names),
                                                             list(q.field_descriptions) +list(q.extra_field_descriptions)),
                                                           q.update),
('delete_qualifications','dq', cms.get_update_rules('dq',  list(q.field_status) + list(q.extra_field_status),
                                                             list(q.field_shorts) + list(q.extra_field_shorts),
                                                             list(q.field_names) + list(q.extra_field_names),
                                                             list(q.field_descriptions) +list(q.extra_field_descriptions)),
                                                           q.delete),
#workers
('read_workers','rw', cms.get_read_delete_rules('rw', w.field_status, w.field_shorts, w.field_names, w.field_descriptions), w.read),
('create_worker','cw', cms.get_create_rules('cw', tuple(list(w.field_status) + [2]), tuple(list(w.field_shorts) + ["-ph"]),
        tuple(list(w.field_names) + ["phone"]), tuple(list(w.field_descriptions) + ["phone number"])), w.create),
('update_workers','uw', cms.get_update_rules('uw',  w.field_status, w.field_shorts, w.field_names, w.field_descriptions), w.update),
('delete_workers','dw', cms.get_update_rules('dw',  w.field_status, w.field_shorts, w.field_names, w.field_descriptions), w.delete),
#worker date states
('read_worker_date_states','rwds', cms.get_read_delete_rules('rwds', wds.field_status, wds.field_shorts, wds.field_names, wds.field_descriptions), wds.read),
('create_worker_date_states','cwds', cms.get_create_rules('cwds',  wds.field_status, wds.field_shorts, wds.field_names, wds.field_descriptions), wds.create),
('update_worker_date_states','uwds', cms.get_update_rules('uwds',  wds.field_status, wds.field_shorts, wds.field_names, wds.field_descriptions), wds.update),
('delete_worker_date_states','dwds', cms.get_update_rules('dwds',  wds.field_status, wds.field_shorts, wds.field_names, wds.field_descriptions), wds.delete),
#salaries
('read_salaries','rsl', cms.get_read_delete_rules('rsl', sl.field_status, sl.field_shorts, sl.field_names, sl.field_descriptions), sl.read),
('create_salary','csl', cms.get_create_rules('csl',  sl.field_status, sl.field_shorts, sl.field_names, sl.field_descriptions), sl.create),
('update_salaries','usl', cms.get_update_rules('usl',  sl.field_status, sl.field_shorts, sl.field_names, sl.field_descriptions), sl.update),
('delete_salaries','dsl', cms.get_update_rules('dsl',  sl.field_status, sl.field_shorts, sl.field_names, sl.field_descriptions), sl.delete),
#premium_sizes
('read_premium_sizes','rps', cms.get_read_delete_rules('rps', ps.field_status, ps.field_shorts, ps.field_names, ps.field_descriptions), ps.read),
('create_premium_size','cps', cms.get_create_rules('cps',  ps.field_status, ps.field_shorts, ps.field_names, ps.field_descriptions), ps.create),
('update_premium_sizes','ups', cms.get_update_rules('ups',  ps.field_status, ps.field_shorts, ps.field_names, ps.field_descriptions), ps.update),
('delete_premium_sizes','dps', cms.get_update_rules('dps',  ps.field_status, ps.field_shorts, ps.field_names, ps.field_descriptions), ps.delete),
#premiums
('read_premiums','rpr', cms.get_read_delete_rules('rpr', pr.field_status, pr.field_shorts, pr.field_names, pr.field_descriptions), pr.read),
('create_premium','cpr', cms.get_create_rules('cpr',  pr.field_status, pr.field_shorts, pr.field_names, pr.field_descriptions), pr.create),
('update_premiums','upr', cms.get_update_rules('upr',  pr.field_status, pr.field_shorts, pr.field_names, pr.field_descriptions), pr.update),
('delete_premiums','dpr', cms.get_update_rules('dpr',  pr.field_status, pr.field_shorts, pr.field_names, pr.field_descriptions), pr.delete),
#requests
('read_requests','rr', cms.get_read_delete_rules('rr', list(r.field_status) + list(r.extra_field_status),
                                                             list(r.field_shorts) + list(r.extra_field_shorts),
                                                             list(r.field_names) + list(r.extra_field_names),
                                                             list(r.field_descriptions) +list(r.extra_field_descriptions)), r.read),
('create_request','cr', cms.get_create_rules('cr',  list(r.field_status) + list(r.extra_field_status),
                                                             list(r.field_shorts) + list(r.extra_field_shorts),
                                                             list(r.field_names) + list(r.extra_field_names),
                                                             list(r.field_descriptions) +list(r.extra_field_descriptions)), r.create),
('update_requests','ur', cms.get_update_rules('ur',  list(r.field_status) + list(r.extra_field_status),
                                                             list(r.field_shorts) + list(r.extra_field_shorts),
                                                             list(r.field_names) + list(r.extra_field_names),
                                                             list(r.field_descriptions) +list(r.extra_field_descriptions)), r.update),
('delete_requests','dr', cms.get_update_rules('dr',  list(r.field_status) + list(r.extra_field_status),
                                                             list(r.field_shorts) + list(r.extra_field_shorts),
                                                             list(r.field_names) + list(r.extra_field_names),
                                                             list(r.field_descriptions) +list(r.extra_field_descriptions)), r.delete)))
