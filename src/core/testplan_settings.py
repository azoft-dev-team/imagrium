'''
Created on 29.01.2013

@author: Nosov Dmitriy
'''
from libs.sikuli import Sikuli
import ConfigParser
import os
import sys


class TestPlanSettings:
        
    instance = None

    @classmethod
    def getInstance(cls):
        if cls.instance != None:
            return cls.instance
        else:
            cls.instance = TestPlanSettings()
            try:
                configFile = sys.argv[1]
            except IndexError:
                exit("Please specify the configuration file")
            cls.instance._config = ConfigParser.ConfigParser()
            assert len(cls.instance._config.read(configFile)) > 0, "Unable to read the config file"
            return cls.instance

    def __init__(self):
        #The region where all subsequent searches will be conducted
        Sikuli.setBundlePath(os.getcwd())
        self.box = None

    def __getattr__(self, name):
        return getattr(self._config, name)