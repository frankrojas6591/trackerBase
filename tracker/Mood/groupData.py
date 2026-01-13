'''
Manage group instance Data 

- each group has a profile : groups/{grpID}/profile.json
- defines: grpID, pw,  whoList
- manages access to all filename: profile.json, mood_data.json
'''
import os
import json

class groupData(object):
    def __init__(self, **kwargs):
        self.oID = self.__class__.__name__
        self.debug = kwargs.get('debug', False)
        self.grpID = kwargs['grpID']
        self.ext = kwargs.get('ext', None)

    def grpDIR(self):
        return os.path.join(self.ext.appDataDir, str(self.grpID))
    
    def moodFN(self):
        # Data file for storing mood entries
        #DATA_FILE = f'groups/{profDict['name']}/mood_data.json'
        return os.path.join(self.grpDIR(), 'mood_data.json')

    def _loadProfile(self):
        '''
        Initialize appData with values from profile
        '''
        with open(os.path.join(self.grpDIR(), 'profile.json'),'r') as fio:
            pDict =  json.load(fio)
        for k,v in pDict.items():
            setattr(self, k, v)

    def __repr__(self):
        return str(self.__dict__)


    def loadHistDict(self):
        """Load mood entries from JSON file."""
        if os.path.exists(self.moodFN()):
            with open(self.moodFN(), 'r') as f:
                return json.load(f)
        return {}
    
    def saveHistDict(self, entries):
        """Save mood entries to JSON file."""
        with open(self.moodFN(), 'w') as f:
            json.dump(entries, f, indent=2)
    
    def loadMoodList(self, whoID):
        hDict = self.loadHistDict()
        try: return hDict[whoID]
        except: return []
