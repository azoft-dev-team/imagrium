'''
Created on 29.01.2013

@author: Nosov Dmitriy
'''
from glob import glob
from itertools import repeat
from unittest import TestSuite
import inspect
import os.path
import pkgutil
import src.tests as tests
import unittest
import itertools


class TestPlanLoader:
    _tCase = None
    
    def __init__(self):
        pass

    @staticmethod
    def getTestCaseByName(settings, nameFragment):
        TestPlanLoader._tCase = None

        def filterTestCaseByName(testInstance):
            if TestPlanLoader._tCase:
                return
            else:
                if isinstance(testInstance, TestSuite):
                    try:
                        TestPlanLoader._tCase = next(itertools.ifilter(lambda x: nameFragment in x.__str__(), testInstance))
                    except StopIteration: #in case we didn't find anything
                        pass
        
        TestPlanLoader._getTests((settings.get("System", "testsRootPath"), filterTestCaseByName))
        TestPlanLoader._tCase.settings = settings
        return TestPlanLoader._tCase


    @staticmethod
    def getTestCasesByName(settings, nameFragment):
        testPlanFiltered = unittest.TestSuite()        

        def filterTestCaseByName(testInstance):
            for testItem in testInstance._tests:
                testItem.settings = settings
            if isinstance(testInstance, TestSuite):
                try:
                    [testPlanFiltered.addTest(x) for x in filter(lambda x: nameFragment in x.__str__(), testInstance)]
                except StopIteration: #in case we didn't find anything
                    pass
        
        TestPlanLoader._getTests(('src.tests', filterTestCaseByName))
        return testPlanFiltered

    
    @staticmethod
    def getAllTC(settings):
        #Resulting test plan
        testPlanAll = unittest.TestSuite()
        
        def addTest(testInstance):
            for testItem in testInstance._tests:
                testItem.settings = settings
            testPlanAll.addTest(testInstance)
            
        TestPlanLoader._getTests(('src.tests', addTest))
        return testPlanAll

    @staticmethod
    def _getTests(args):
        '''
                
        @param args: A tuple (module, testSuiteCallable) that contains the root package to search into for test cases and a callable to call with a found test case class.
        @return: Nothing 
        '''
        (module, testSuiteCallable) = args
        
        def isTestSuite(candidateClass):
            return isinstance(candidateClass, TestSuite) and candidateClass.countTestCases() > 0

        def getTestsuitesFromModule(module):
            testSuiteCandidates = inspect.getmembers(module, inspect.isclass)
            testSuiteList = filter(isTestSuite, map(unittest.TestLoader().loadTestsFromTestCase, map(lambda x: x[1], testSuiteCandidates)))
            if testSuiteList:
                map(testSuiteCallable, testSuiteList)
        
        def isPackage(d):
            d = os.path.join(moduleHomeDir, d)
            return os.path.isdir(d) and glob(os.path.join(d, '__init__.py*'))
     
        def importPackageModules(packageName):
            modulesIter = pkgutil.iter_modules(packageName.__path__)
            for (moduleLoader, moduleName, isPackage) in modulesIter:
                module = importAndReturnModule(packageName.__name__ + "." + moduleName)
                getTestsuitesFromModule(module)
     
        def importAndReturnModule(name):
            m = __import__(name)
            for n in name.split(".")[1:]:
                m = getattr(m, n)
            return m
        
        def importAndCollectTestSuites(name):
            m = __import__(name)
            for n in name.split(".")[1:]:
                m = getattr(m, n)
            importPackageModules(m)
            return m
        
        def setPackageName():
            return map(lambda x: module.__name__ + "." + x, packagesList)
        
        def setFullPackageName(package):
            return module.__name__ + "." + package        

        module = importAndReturnModule(module)            
        moduleHomeDir = os.path.dirname(module.__file__)
        importPackageModules(module)
        packagesList = filter(isPackage, os.listdir(moduleHomeDir))
        map(TestPlanLoader._getTests, zip(map(setFullPackageName, packagesList), repeat(testSuiteCallable)))
        #map(TestPlanLoader._getTests, zip(map(importAndCollectTestSuites, setPackageName()), repeat(testSuiteCallable)))