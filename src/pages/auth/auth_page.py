'''
Created on 16.05.2013

@author: Nosov Dmitriy
'''
from org.sikuli.script import FindFailed, Button
from src.core.page import Page, ResourceLoader, AndroidPage
from src.core.r import Resource
from src.pages.fb_auth.fb_auth_page import FbAuthPage
from unittest.util import strclass
import logging




class AuthPage(Page):    

    actionSignUpFb = ResourceLoader(Resource.fbAuthBtniOS)
    actionAgreeTermsBtniOS = ResourceLoader(Resource.agreeTermsBtniOS)
           
    def __init__(self, box, settings):
        super(AuthPage, self).__init__(box, settings)

        self.box = box
        self.settings = settings
        # It is necessary to assign a search area to all class fields
        self.actionSignUpFb = self.box
        self.actionAgreeTermsBtniOS = self.box
                
        
    
    def signUpFb(self):
        self.actionAgreeTermsBtniOS.click()
        self.actionSignUpFb.click()
        return FbAuthPage.load(self.box, self.settings)
    
    
class AuthPageiOS(AuthPage):
    
    actionSignUpFb = ResourceLoader(Resource.fbAuthBtniOS)
    actionAgreeTermsBtniOS = ResourceLoader(Resource.agreeTermsBtniOS)
        
    def __init__(self, box, settings):
        super(AuthPageiOS, self).__init__(box, settings)
        self.checkIfLoaded(['actionSignUpFb', 'actionAgreeTermsBtniOS'])


class AuthPageAndroidHdpi(AuthPage):
    
    actionSignUpFb = ResourceLoader(Resource.fbAuthBtnAndroidHdpi)
    actionAgreeTermsBtniOS = ResourceLoader(Resource.fbAuthBtnAndroidHdpi)

    def __init__(self, box, settings):
        super(AuthPageAndroidHdpi, self).__init__(box, settings)
        self.checkIfLoaded(['actionSignUpFb'])
