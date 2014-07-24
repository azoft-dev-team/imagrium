# -*- coding: utf-8 -*-
import org.sikuli.basics.SikuliXforJython
import os
from libs.sikuli import *
Sikuli.setBundlePath(os.getcwd())

from src.core.app_launcher import AppLauncher
from src.core.r import ClientMessageConsts
from src.core.testplan_loader import TestPlanLoader
from src.core.testplan_settings import TestPlanSettings
import logging
import os.path
import pika
import sys
import xmlrunner

# Set up logging
logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)


class TestCaseRunnerMaster:
    def __init__(self, settings):
        # Launch the app on the auth page
        self.settings = settings
        AppLauncher.prepareSnapshot(settings)        

        if settings.get("System", "testcaseFilter"):
            tPlan = TestPlanLoader.getTestCasesByName(settings, settings.get("System", "testcaseFilter"))
        else:
            tPlan = TestPlanLoader.getAllTC(settings)
            
        xmlrunner.XMLTestRunner(output='test-reports').run(tPlan)
        if settings.getboolean("Multiclient", "closeSecondaryOnFinish"):
            self.closeAllSlaves()
        
        if not settings.getboolean("OS", "debug"):
            AppLauncher.closeEmulator(settings) #if emulator is not recognized
        
    def closeAllSlaves(self):
        connection = pika.BlockingConnection(pika.ConnectionParameters(
        host=self.settings.get("Multiclient", "rabbitHostUrl")))
        channel = connection.channel()
        channel.exchange_declare(exchange='exitrequests', type='fanout')
        channel.basic_publish(exchange='exitrequests', routing_key='', body=ClientMessageConsts.TASK_EXIT)
        connection.close()


class TestCaseRunnerSlave:

    def testCaseRunRequestProcess(self, ch, method, properties, body):
        """
        Receives the request from a master node, executes a test and confirms the execution
        """
        ch.basic_ack(delivery_tag=method.delivery_tag)
        tCase = TestPlanLoader.getTestCaseByName(self.settings, body)
        if tCase:
            xmlrunner.XMLTestRunner(output='test-reports').run(tCase)
        self.sendResponse(ClientMessageConsts.TASK_DONE)

    def clientExit(self, ch, method, properties, body):
        """
        Receives the request from a master node, executes a test and confirms the execution
        """
        sys.exit()
    
    def __init__(self, settings):
        self.settings = settings
                
        #Prepare the emulator for test run
        AppLauncher.prepareSnapshot(settings)
        
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=settings.get("Multiclient", "rabbitHostUrl")))
        channel = connection.channel()
        channel.basic_qos(prefetch_count=1)
        
        #The queue for test case run requests
        channel.queue_declare(queue='requests', durable=True)
        channel.queue_purge(queue='requests')
        
        #The special queue for exit requests
        channel.exchange_declare(exchange='exitrequests', type='fanout')
        result = channel.queue_declare(exclusive=True)
        queue_name = result.method.queue
        channel.queue_bind(exchange='exitrequests', queue=queue_name)
        
        channel.basic_consume(self.testCaseRunRequestProcess, queue='requests')
        channel.basic_consume(self.clientExit, queue=queue_name, no_ack=True)
        
        channel.start_consuming()
    
    def sendResponse(self, message):
        connection = pika.BlockingConnection(pika.ConnectionParameters(
        host=self.settings.get("Multiclient", "rabbitHostUrl")))
        channel = connection.channel()
        channel.queue_declare(queue='responses', durable=True)
        channel.basic_publish(exchange='', routing_key='responses', body=message,
                      properties=pika.BasicProperties(
                         delivery_mode = 2, # make message persistent
                      ))
        connection.close()

class TestCaseRunnerFactory:
    MASTER = 'primary'
    SLAVE = 'secondary'
    
    def __init__(self, settings):
        if settings.get("System", "runType") == TestCaseRunnerFactory.MASTER:
            TestCaseRunnerMaster(settings)
        else:
            TestCaseRunnerSlave(settings)
            

# Get the initial configuration
TestCaseRunnerFactory(TestPlanSettings.getInstance())



