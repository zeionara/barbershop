import datetime

import sys
sys.path.insert(0, 'C:/Users/Zerbs/Desktop/databases_kursach/python_mongo_crud/crud/')

from worker_states import WorkerState
from commons import get_by_id

class State():
    def validate_state_id(self, state_id):
        state = get_by_id(WorkerState, state_id)
        if state == None:
            raise ValueError("No such state")
        return str(state._id)
    
    def __init__(self, date, state_id):
        self.date = date
        self.state_id = self.validate_state_id(state_id)
        
class StateSet():
    def __init__(self):
        self.states = []
    
    def get_by_date(self, date):
        for state in self.states:
            if state.date == date:
                return state
        return None
    
    def get_index_by_date(self, date):
        index = 0
        for state in self.states:
            if state.date == date:
                return index
            index += 1
        return None
    
    def add(self, state):
        if self.get_by_date(state.date) != None:
            raise ValueError("This date is already used")
        self.states.append(state)
        
    def remove(self, date):
        index = self.get_index_by_date(date)
        self.states = self.states[:index] + self.states[index + 1:]
        
    def update(self, date, state_id):
        index = self.get_index_by_date(date)
        self.states = self.states[:index] + [State(date, state_id)] + self.states[index + 1:]
        
        
    #def get_by_date():
        
        
stateset = StateSet()
print(WorkerState.query.find().all())
stateset.add(State(datetime.datetime(2017,10,10), "e88"))
stateset.add(State(datetime.datetime(2017,11,11), "e87"))
print(stateset.get_by_date(datetime.datetime(2017,10,10)))
#state1 = State(datetime.datetime(2017,10,10), "e88")
#state2 = State(datetime.datetime(2017,11,11), "e87")
#states = [state1, state2]

#print(state)
        