'''
Created on 13.05.2013

@author: Nosov Dmitriy
'''
from libs.sikuli import Sikuli, Settings
from org.sikuli.script import FindFailed
from src.core.r import Resource, TestPlanConsts
from unittest.util import strclass
import importlib
import logging
import os
import shutil
import subprocess
import time


class ResourceLoader(object):
    
    def __init__(self, resourceUrl, pageBox=None, minSimilarity=0.7):
        self.resourceUrl = resourceUrl
        self.pageBox = pageBox
        self.minSimilarity = minSimilarity
        
    def __get__(self, instance, owner):
        originalSimilarity = Sikuli.Settings.MinSimilarity 
        Sikuli.Settings.MinSimilarity = self.minSimilarity
        logging.info("Loading resource: %s" % self.resourceUrl)
        res = None
        
        def findInListOrSingle(source):
            res = None
            if isinstance(self.resourceUrl, list):
                for item in self.resourceUrl:
                    try:
                        res = source.find(item)
                        break
                    except FindFailed:
                        pass
                if not res:
                    raise FindFailed("Could not find resource: %s" % self.resourceUrl)
            else:
                res = source.find(self.resourceUrl)
            return res
        
        try:
            if self.pageBox:
                res = findInListOrSingle(self.pageBox)
            else:
                res = findInListOrSingle(Sikuli.Screen())

        except FindFailed:
            raise AssertionError("Could not find resource: %s" % self.resourceUrl)
        
        finally:
            Sikuli.Settings.MinSimilarity = originalSimilarity
        self.res = res
        return self

    def __set__(self, obj, value):
        self.pageBox = value
    
    def __getattr__(self, name):
        logging.info("OPERATION: %s, RESOURCE: %s" % (name, self.resourceUrl))
        return getattr(self.res, name)


class Page(object):
   
    keyboardiOsTop = ResourceLoader(Resource.keyboardiOsTop)
    
    def __init__(self, box, settings):
        super(Page, self).__init__(box, settings)
        logging.info("Starting page initialization: %s" % self.__class__)
        self.box = box
        self.settings = settings        
        Settings.OcrTextSearch = True
        Settings.OcrTextRead = True
        self.loadingChangePixelsMdpi = self.settings.getint("Page", "loadingChangePixelsMdpi")
        self.loadingTimeout = self.settings.getint("Page", "loadingTimeout")
        self.loadingBox = Sikuli.Region(self.box.getX(), self.box.getY(), self.box.getW(), self.box.getH())
        
        
    def checkIfLoaded(self, fields):
        try:
            [getattr(self, field) for field in fields]
        except AssertionError, e:
            logging.info(e.message)
            raise AssertionError("Unable to load page %s" % strclass(self.__class__))
            
         

    @classmethod
    def load(cls, box, settings):
        logging.info("Loading page %s..." %  cls.__name__)        
        if settings.get("OS", "name") == TestPlanConsts.ANDROID_OS:
            if settings.get("OS", "density") == TestPlanConsts.MDPI:
                pageDensity = "Mdpi"
            if settings.get("OS", "density") == TestPlanConsts.HDPI:
                pageDensity = "Hdpi"                
                # First, try a version-specific class. If fails, try common for this density.
            try:
                verMajor, verMinor = settings.get("OS", "version").split(".")
                genClass = getattr(importlib.import_module(cls.__module__), cls.__name__ + "_" + verMajor + "_" + verMinor + "_" + "Android" + pageDensity)
                logging.info("Loading version-specific class.")
                return genClass(box, settings)
            except AttributeError:
                logging.info("Loading generic class for this density.")
                                
            try:
                genClass = getattr(importlib.import_module(cls.__module__), cls.__name__ + "Android" + pageDensity)
                return genClass(box, settings)
            except AttributeError:
                raise AssertionError("Could not find the page from configuration, please add it.")
        
        if settings.get("OS", "name") == TestPlanConsts.X_OS:
            try:
                genClass = getattr(importlib.import_module(cls.__module__), cls.__name__ + "iOS")
                return genClass(box, settings)
            except AttributeError, e:
                logging.info(e)
                raise AssertionError("Could not find the page from configuration, please add it.")
    
    def takeScreenShot(self, testcase):
        stepNum = testcase.screenShotsCaptured
        imgFilename = "{}-{}-step_{:02d}.png".format(strclass(testcase.__class__), testcase._testMethodName, stepNum)
        imgLocation = Sikuli.getBundlePath() + self.settings.get("System", "screenshotsPath")
        if not os.path.isdir(imgLocation):
            os.makedirs(imgLocation)
        screenshotFilename = Sikuli.Screen().capture(self.box)
        shutil.move(screenshotFilename, imgLocation + imgFilename)
        testcase.screenShotsCaptured += 1
       
    def waitPageLoad(self, name=None, raiseIfDidntStart=False):
        """
        Set parameters for a precise search and then scan for an image which shows after page loading completes.
        """
        if not name:
            name = strclass(self.__class__)
        else:
            name = strclass(name)
        similarity = Sikuli.Settings.MinSimilarity
        Sikuli.Settings.MinSimilarity = 0.95
        global boxUpdateTime
        global updatesHappened
        boxUpdateTime = time.time()
        updatesHappened = False
                
        def loadingHappens(event):
            global boxUpdateTime
            global updatesHappened
            updatesHappened = True
            boxUpdateTime = time.time()
            logging.info("Loading page %s..." % name)
        self.loadingBox.onChange(self.loadingChangePixelsMdpi, loadingHappens) #the number of changed pixels
        self.loadingBox.observe(self.loadingTimeout, background=True) #the number of seconds to wait
            
        delayBetweenLoadings = int(self.settings.get("Page", "delayBetweenLoadings"))
            
        while True:
            if abs(boxUpdateTime - time.time()) > delayBetweenLoadings and not updatesHappened:
                self.loadingBox.stopObserver()
                if raiseIfDidntStart:
                    raise AssertionError("Unable to find the loading element or it is not spinning")
                break
                
            if abs(boxUpdateTime - time.time()) > delayBetweenLoadings and updatesHappened:
                self.loadingBox.stopObserver()
                break
        Sikuli.Settings.MinSimilarity = similarity
            
    def swipeDown(self):
        center = self.box.getCenter()
        bottom = self.box.getBottomLeft()
        self.box.dragDrop(center, bottom)
        
    def swipeUp(self):
        center = self.box.getCenter()
        top = self.box.getTopLeft()
        self.box.dragDrop(center, top) 
        
    def waitKeyboardAppears(self):
        timeout = self.box.getAutoWaitTimeout()
        self.box.setAutoWaitTimeout(Sikuli.FOREVER)
        self.keyboardTopMdpi = self.box
        self.keyboardTopMdpi
        self.box.setAutoWaitTimeout(timeout)
            
        
class AndroidPage(object):
    """
    This mixin adds Android-specific methods to a page object.
    """
    def __init__(self, box, settings):
        super(AndroidPage, self).__init__(self, box, settings)
    
    def inputText(self, text):
        subprocess.check_call(["adb", "-s", self.settings.get("OS", "emulatorName"), "shell", "input", "text", text])

    def submitForm(self):
        subprocess.check_call(["adb", "-s", self.settings.get("OS", "emulatorName"), "shell", "input", "keyevent", "66"])

    def unlockScreen(self):
        subprocess.check_call(["adb", "-s", self.settings.get("OS", "emulatorName"), "shell", "input", "keyevent", "86"])
        
    def back(self):
        subprocess.check_call(["adb", "-s", self.settings.get("OS", "emulatorName"), "shell", "input", "keyevent", "4"])
        
    @staticmethod
    def home(self):
        subprocess.check_call(["adb", "shell", "input", "keyevent", "3"])
        

class iOSPage(object):
    
    btnA  = ResourceLoader(Resource.btnA)
    btnB  = ResourceLoader(Resource.btnB)    
    btnZ  = ResourceLoader(Resource.btnZ)
    btnO  = ResourceLoader(Resource.btnO)
    btnF  = ResourceLoader(Resource.btnF)
    btnT  = ResourceLoader(Resource.btnT)
    btnE  = ResourceLoader(Resource.btnE)
    btnS  = ResourceLoader(Resource.btnS)
    btnH  = ResourceLoader(Resource.btnH)
    btnR  = ResourceLoader(Resource.btnR)
    btnD  = ResourceLoader(Resource.btnD)
    btnP  = ResourceLoader(Resource.btnP)
    btnK  = ResourceLoader(Resource.btnK)        
    
    @staticmethod
    def rotateScreen(settings):
        subprocess.call(["ssh", settings.get("SSH_ACCESS", "serverUrl"), settings.get("App", "appRotateScript")])

    def __init__(self, box, settings):
        super(iOSPage, self).__init__(box, settings)
        self.recognizedLetters = ["A", "B", "Z", "O", "F", "T", "E", "S", "H", "R", "D", "P", "K"]
        self.btnNamesList = ['btn' + letter for letter in self.recognizedLetters]
        [setattr(self, btnName, self.box) for btnName in self.btnNamesList]
    
    def inputText(self, text):
        letterImages = zip(self.recognizedLetters, [getattr(self, btn) for btn in self.btnNamesList])
        letterImagesDict = dict(letterImages) 
        for char in text:
            letterImagesDict[char.upper()].click()



    
    
    











