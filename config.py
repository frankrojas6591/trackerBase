'''
App config

read from ~/profile_{appNm}.json

This json file needs to be uploaded to web server
'''

import os
import json
from tracker.util.util import loadProfile

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    # Use basename as Base appNm
    appNm = os.path.basename(basedir)
    # Load profile
    pDict = loadProfile(appNm)

    # Copy master profile into os.environ
    for k,v in pDict.items():
        if k not in os.environ:
            try: os.environ[k] = v.replace('HOME', str(Path.home())).replace('appNm', appNm)
            except: 
                # handle bool
                os.environ[k] = str(v)

    appDataDir = os.environ.get('appDataDir')
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI')\
        or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False if os.environ.get('SQL_TRACK_MOD') == 'False' else True

    def __repr__(self):
        s = f"{Config.appNm} Config.py\n"
        s += f"appDataDir : {Config.appDataDir}\n"
        s += f"SECRET_KEY: hiddeb\n"
        s += f"SQLALCHEMY_DATABASE_URI: {Config.SQLALCHEMY_DATABASE_URI}\n"
        s += f"SQLALCHEMY_TRACK_MODIFICATIONS: {Config.SQLALCHEMY_TRACK_MODIFICATIONS}"
        return s
