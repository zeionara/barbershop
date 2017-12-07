import datetime

def get_date(string_date):
    if (isinstance(string_date,datetime.datetime)):
        return string_date
    return datetime.datetime.strptime(string_date, '%d.%m.%Y').date()

def get_worker_date_state_list(value):
    #value = '12.12.2017,e88 ; 12.11.2017, e89 '
    result = []
    pre_result = value.replace(" ","").split(";")
    for item in pre_result:
        pair = item.split(",")
        result.append([get_date(pair[0]), pair[1]])
    return result

print(get_worker_date_state_list('12.12.2017,e88 ; 12.11.2017, e89 '))
