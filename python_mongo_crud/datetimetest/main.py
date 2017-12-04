import datetime

visit_date = datetime.datetime(2017,10,10,14,30,0)
print(visit_date + datetime.timedelta(minutes = 100))

#visit_date.add_minutes(100)