'''
Base app class - common across all apps
'''
import os
from pathlib import Path
from typing import Any
import json

from flask import Flask, Blueprint
from tracker.util.util import loadProfile

class appBase(object):
    def __init__(self, **kwargs):
        self.oID = str(self.__class__.__name__)
        self.ui = kwargs.get('app', None)
        self.bp = Blueprint(self.oID, __name__)
        try: 
            # Load profile (if exists) into class values
            _ = loadProfile(self.oID, obj=self)
        except:
            pass

    def init_app(app):
        if self.ui : return
            
        if app  : 
            self.ui = app
            return

        # Standalone flask app
        self.ui = Flask(self.oID)
        
        # Initialize  app - ie. persistant store
        #self.flaskApp.before_request()

    def _val(self, v):
        '''
        Return value with substitutions
        '''
        try:
            # Handle string values
            return v.replace('HOME', str(Path.home())).replace('appNm', self.oID)
        except: 
            # handle non string, e.g. bool
            return str(v)

    def loadProfile(self, appNm=None, **kwargs):
        '''
        Load profile into os.environ

        :appNm - name of object
        :obj=None 
        :obj=sef

        Example:
        pDict = loadProfile('Mood')
        pDict = ext.loadProfile(ext.oID, obj=ext)
        
        '''
        if appNm is None : appNm = self.oID
    
        fnProfile = os.path.join(Path.home(),'tracker', f'profile_{appNm}.json')

        
        # Load the profile json
        try:
            with open(fnProfile,'r') as fio:
                pDict = json.load(fio)
        except:
            # No profile exist
            return {}

        # Check if Copy is needed?
        obj = kwargs.get('obj', None)
        if obj is None : return pDict

        oDict = obj.__dict__

        # Else copy pDict into class members
        for k,v in pDict.items():
            if k not in oDict:
                oDict[k] = self._val(v)

        return pDict



    def __repr__(self):
        s = f"{self.oID} Class Attributes"
        for k,v in self.__dict__.items():
            if 'SECRET' in k : continue
            try:
                s += f"\n{k} : {self._val(v)}"
            except:
                s += f"\n{k} : non-jsonify"
        return s