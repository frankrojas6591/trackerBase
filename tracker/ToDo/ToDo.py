'''
ToDo task manager services

- List
- Add
- Complete
- delete
'''
import os
from pathlib import Path
import json
from tracker.util.appBase import appBase
import datetime
import uuid


class task(object):
    def __init__(self, **kwargs):
        for k,v in kwargs.items():
            setattr(self, k, v)
    def to_dict(self):
        return self.__dict__

class ToDo(appBase):
    '''
    Manage list of taskDict

    FIXME: need to fix DB per user, update to DB per multiple sessions, each save resets the unique taskID
    
    '''
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.loadProfile(obj=self)
        self.taskList = self.load()

    def FN(self):
        '''
        FIXME: add per_userID to FN DB
        '''
        return os.path.join(self.appDataDir, 'todo.json')

    def load(self):        
        if os.path.exists(self.FN()):
            with open(self.FN(),'r') as fio:
                taskList = json.load(fio)
            return taskList
        return []

    def fetch(self, view='home', sortBy='lifo'):
        self.taskList = self.load()
        
        """Get all items (AJAX endpoint)."""
        if view == 'home':  
            # default home view : exclude Done, Del
            dispOrder = ['Prio', 'Active', 'Hidden']
        elif view == 'All':
            dispOrder = ['Prio', 'Active', 'Hidden', 'Done', 'Del']
    
        # ------ filter view : Merge lists in order of dispOrder
        itemList = self.taskList
        dispList = []
        for s in dispOrder:
            dispList += [t for t in itemList if t['status'] == s]
        
        # Add any items not in sOrder
        if view == 'All' :
            dispList += [t for t in itemList if t['status'] not in dispOrder]
    
        #-------- sort -----

        # Sort using a lambda function
        if sortBy == 'LIFO': return sorted(dispList, key=lambda d: d['dt'], reverse=True)
        if sortBy == 'Category': return sorted(dispList, key=lambda d: d['category'])
        return dispList

    def save(self):
        FN = self.FN()
        todoDIR = Path(FN).parent
        if ~ todoDIR.is_dir():
            todoDIR.mkdir(parents=True, exist_ok=True)
        with open(FN,'w') as fio:
            json.dump(self.taskList, fio)

    def updateTaskList(self, taskDict):
        '''
        Do instantious update to DB
        FIXME : make update with DB lock across sessions
        '''
        self.taskList.append(taskDict)
        self.save()

    def add(self, taskDict):
        '''
        Input
        :dict(desc:str, category:str)       
        
        category: Home, Honey, LLC, Financial,...
        
        Add members: dt:str,status:str, taskID:uuid
        
        status: Prio2not3, Active, Hidden
        '''
        if taskDict:
            newDict = dict(desc=taskDict['desc'],
                           category = taskDict['category'],
                           taskID = uuid.uuid4().hex,
                           dt = datetime.datetime.now().strftime('%Y%m%d'),
                           status = 'Active'
                          )                
            self.updateTaskList(newDict)
            return newDict
        else:
            return None

    def find(self, taskDict):
        for i in range(len(self.taskList)):
            if self.taskList[i]['taskID'] == taskDict['taskID']:
                return i
        return None

    def get(self, taskID):
        for tDict in self.taskList:
            if tDict['taskID'] == taskID :
                return tDict
        return None

    def setStatus(self, taskID, status):
        tDict = self.get(taskID)
        if tDict: 
            tDict['status'] = status
            return tDict
        return None
            
        

        
        


    