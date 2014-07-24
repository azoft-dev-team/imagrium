'''
Created on 20.05.2013

@author: Nosov Dmitriy
'''
from libs.sikuli import Sikuli
from org.sikuli.script import FindFailed
from src.core.page import Page, ResourceLoader, AndroidPage
from src.core.r import Resource, TestPlanConsts
from subprocess import CalledProcessError
import logging
import subprocess
import time


class LaunchPage(Page):

    verticalBorder = ResourceLoader(Resource.verticalBorderiOS)
    horizontalBorder = ResourceLoader(Resource.horizontalBorderiOS)    
        
    def __init__(self, box, settings):
        #This constructor does not have the super call as it does not yet know anything about its box.
        self.settings = settings
        originalSimilarity = Sikuli.Settings.MinSimilarity
        Sikuli.Settings.MinSimilarity = 0.87
        try:
            vRegion = self.verticalBorder
            hRegion = self.horizontalBorder
            leftX = vRegion.x
            leftY = vRegion.y
            width = hRegion.w
            height = vRegion.h
            Sikuli.Settings.MinSimilarity = originalSimilarity
            self.box = Sikuli.Region(leftX, leftY, width, height)
        except FindFailed, e:
            raise AssertionError("Unable to get the simulator frame")

    def launch(self, page, pageBox):
        try:
            if self.settings.get("OS", "name") == TestPlanConsts.ANDROID_OS:
                subprocess.check_call(["adb", "-s", self.settings.get("OS", "emulatorName"), "shell", "am", "start", "-n", self.settings.get("App", "name")])
            if self.settings.get("OS", "name") == TestPlanConsts.X_OS:
                subprocess.Popen(["ssh", self.settings.get("SSH_ACCESS", "serverUrl"), self.settings.get("System", "iosSimPath"), "launch", self.settings.get("App", "launchLocation") + '/' + self.settings.get("App", "appName")])
                logging.info("Waiting 10 sec for the updates to be applied.")
                time.sleep(10)
                
            isPageLoaded = False
            while not isPageLoaded:
                try:
                    page.load(pageBox, self.settings)
                    isPageLoaded = True
                    
                except AssertionError:
                    continue
        
        except CalledProcessError:
            raise AssertionError("Unable to run a script that launches the app")


class LaunchPageiOS(LaunchPage):
    
    verticalBorder = ResourceLoader(Resource.verticalBorderiOS)
    horizontalBorder = ResourceLoader(Resource.horizontalBorderiOS)


class LaunchPageAndroidHdpi(LaunchPage):
    
    verticalBorder = ResourceLoader(Resource.verticalBorderAndroidHdpi)
    horizontalBorder = ResourceLoader(Resource.horizontalBorderAndroidHdpi)