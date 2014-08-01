'''
Created on 26.06.2013

@author: Nosov Dmitriy
'''
from libs.sikuli import Sikuli
from src.core.app_launcher import AppLauncher
from unittest.util import strclass
import logging
import os
import pika
import shutil
import time
import unittest


class AppTestCase(unittest.TestCase):
    
    failuresCount = 0
    _context = {}
    
    def setUp(self):
        app = AppLauncher.launchFromSnapshot(self.settings)
        AppLauncher.box = app.box
        
        def _importClassByName(cl):
            d = cl.rfind(".")
            classname = cl[d+1:len(cl)]
            m = __import__(cl[0:d], globals(), locals(), [classname])
            return getattr(m, classname)
        
        app.launch(_importClassByName(self.settings.get("Page", "launchPageClass")), app.box)
         
    def tearDown(self):
        # I see this as the only way to apply a screenshot in case we have a failure before moving on to
        # the next test. 
        if len(self._resultForDoCleanups.failures) > AppTestCase.failuresCount:
            self.takeScreenShot()
            #wait a bit so that the system managed to take a screenshot
            time.sleep(2)
            AppTestCase.failuresCount += 1
        if not self.settings.getboolean("OS", "debug"):
            AppLauncher.closeEmulator(self.settings)

           
    def run(self, result):
        logging.info("STARTING TEST %s (%s)" % (strclass(self.__class__), self._testMethodName))
        super(AppTestCase, self).run(result)

    def takeScreenShot(self):
        imgFilename = "{}-{}-FAILURE.png".format(strclass(self.__class__), self._testMethodName)
        imgLocation = Sikuli.getBundlePath() + "/test-reports/screenshots/"
        if not os.path.isdir(imgLocation):
            os.makedirs(imgLocation)
        screenshotFilename = Sikuli.Screen().capture(Sikuli.Screen().getBounds())
        shutil.move(screenshotFilename, imgLocation + imgFilename)

    def onReceiveTestCaseRunResponse(self, ch, method, properties, body):
        logging.info("Received from the secondary client: %s " % body)
        ch.stop_consuming()
    
    def requestRunTestCase(self, testCaseNameFragment):
        
        connection = pika.BlockingConnection(pika.ConnectionParameters(
        host=self.settings.get("Multiclient", "rabbitHostUrl")))
        
        #First, send the message
        channel = connection.channel()
        channel.queue_declare(queue='requests', durable=True)
        channel.basic_publish(exchange='', routing_key='requests', body=testCaseNameFragment,
                      properties=pika.BasicProperties(
                         delivery_mode = 2, # make message persistent
                      ))

        #Then, wait for the response
        channel = connection.channel()
        channel.queue_declare(queue='responses', durable=True)
        channel.queue_purge(queue='responses')
        channel.basic_consume(self.onReceiveTestCaseRunResponse, queue='responses', no_ack=True)
        channel.start_consuming()
        
        connection.close()
