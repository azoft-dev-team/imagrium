'''
Created on 20.05.2013

@author: Nosov Dmitriy
'''
from libs.sikuli import Sikuli
from src.core.page import ResourceLoader
from src.core.r import TestPlanConsts, Resource
from src.core.launch_page import LaunchPage
from subprocess import CalledProcessError
from telnetlib import Telnet
import logging
import os
import subprocess
import time

class AppLauncher(object):

    box = None  # The simulator box
    buildNum = None
    
    @staticmethod
    def completeBoot(settings):
        while True:
            try:
                time.sleep(3)
                isBootComplete = subprocess.check_output(["adb", "shell", "getprop", "dev.bootcomplete", "-s", settings.get("OS", "emulatorName")])
                logging.info("Waiting the boot to complete...")
                if int(isBootComplete):
                    logging.info("App booting -- DONE")
                    break
            except (ValueError, CalledProcessError):
                pass

    @staticmethod
    def prepareSnapshot(settings):
        if not settings.getboolean("OS", "debug"):
            AppLauncher.closeEmulator(settings)
            if settings.get("OS", "name") == TestPlanConsts.ANDROID_OS:
                apkFile = settings.get("App", "file")
                appName = settings.get("App", "shortname")
                time.sleep(5)
                subprocess.call(('vboxmanage controlvm %s poweroff' % settings.get("OS", "emulatorAvdName")).split())
                subprocess.call(('vboxmanage snapshot %s restore factory' % settings.get("OS", "emulatorAvdName")).split())
                subprocess.Popen(('player --vm-name %s' % settings.get("OS", "emulatorAvdName")).split())
                AppLauncher.completeBoot(settings)                
                subprocess.call(["adb", "-s", settings.get("OS", "emulatorName"), "uninstall", appName])
                logging.info("Uninstalling the app -- DONE")
                time.sleep(10)
                logging.info("Attempting to install the app...")
                subprocess.call(["adb", "-s", settings.get("OS", "emulatorName"), "install", apkFile])
                logging.info("Installing the app -- DONE")
                logging.info("The snapshot is ready, closing in 10 seconds...")
                time.sleep(5)
                subprocess.call(["adb", "-s", settings.get("OS", "emulatorName"),  "shell", "input", "keyevent", "82"])
                subprocess.call(["adb", "-s", settings.get("OS", "emulatorName"), "shell", "input", "keyevent", "4"])
                time.sleep(5)
                AppLauncher.closeEmulator(settings)
                logging.info("Waiting after closing the simulator to unmount the disk image")
                time.sleep(10)                
                import string
                import random
                AppLauncher.buildNum = 'build-' + ''.join([random.choice(string.lowercase + string.digits) for i in range(8)])
                subprocess.call(('vboxmanage controlvm %s poweroff' % settings.get("OS", "emulatorAvdName")).split())
                time.sleep(5)                
                subprocess.call(('vboxmanage snapshot %s take %s' % (settings.get("OS", "emulatorAvdName"), AppLauncher.buildNum)).split())
                time.sleep(5)                
                                
            if settings.get("OS", "name") == TestPlanConsts.X_OS:
                ''' Here we do nothing as the app changes can be easily rolled back
                    by copying the original copy of the app on top of the existing
                '''  
                pass
    
    @staticmethod
    def launchFromSnapshot(settings):
        
        box = Sikuli.Region(0, 0, Sikuli.Screen().w, Sikuli.Screen().h)
        
        if settings.get("OS", "name") == TestPlanConsts.ANDROID_OS:
            if not settings.getboolean("OS", "debug"):
                subprocess.call(('vboxmanage snapshot %s restore %s' % (settings.get("OS", "emulatorAvdName"), AppLauncher.buildNum)).split())
                subprocess.Popen(('player --vm-name %s' % settings.get("OS", "emulatorAvdName")).split())
                AppLauncher.completeBoot(settings)
                time.sleep(3)
                subprocess.call(["adb", "-s", settings.get("OS", "emulatorName"),  "shell", "input", "keyevent", "82"])
                time.sleep(3)
        
        if settings.get("OS", "name") == TestPlanConsts.X_OS:
            if not settings.getboolean("OS", "debug"):
                logging.info("Resetting all information on the simulator.")
                #Consider this is for just starting the simulator
                subprocess.call(["ssh", settings.get("SSH_ACCESS", "serverUrl"), "defaults write com.apple.iphonesimulator SimulateDevice -string \'%s\'" % settings.get("OS", "simulatorDevice")])                
                subprocess.call(["ssh", settings.get("SSH_ACCESS", "serverUrl"), settings.get("App", "appResetScript")])
                time.sleep(5)
                subprocess.call(["ssh", settings.get("SSH_ACCESS", "serverUrl"), settings.get("App", "appResetScript")])
                logging.info("Waiting 15 sec for the updates to be applied.")
                logging.info("Copying the app to launch location.")
                subprocess.call(["ssh", settings.get("SSH_ACCESS", "serverUrl"), "cp" , "-rf", settings.get("App", "appAbsolutePath"), settings.get("App", "launchLocation")])                                
                time.sleep(15)
        
        return LaunchPage.load(box, settings)
            
        raise AssertionError("No suitable app launcher found for the configuration")
    
    @staticmethod
    def closeEmulator(settings):
        if settings.get("OS", "name") == TestPlanConsts.ANDROID_OS:
            try:
                subprocess.check_output("taskkill /F /IM player.exe".split())
            except:
                logging.info("No emulators were found")
        if settings.get("OS", "name") == TestPlanConsts.X_OS:
            subprocess.call(["ssh", settings.get("SSH_ACCESS", "serverUrl"), "killall iPhone\ Simulator"])

