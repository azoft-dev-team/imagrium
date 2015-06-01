'''
Created on 16.05.2013

@author: Nosov Dmitriy
'''
from src.core.page import Page, ResourceLoader
from src.core.r import Resource
from src.pages.preauth.fb_auth_page import FbAuthPage


class AuthPage(Page):

    actionSignUpFb = ResourceLoader(Resource.fbAuthBtnAndroidHdpi)
    actionAgreeTermsBtniOS = ResourceLoader(Resource.fbAuthBtnAndroidHdpi)
               
    def __init__(self, box, settings):
        super(AuthPage, self).__init__(box, settings)
        self.box = box
        self.settings = settings
        # It is necessary to assign a search area to all class fields
        
        self.actionSignUpFb = self.box
        self.actionAgreeTermsBtniOS = self.box
                
        self.waitPageLoad()
        self.checkIfLoaded(['actionSignUpFb'])
    
    def signUpFb(self):
        self.actionSignUpFb.click()
        return FbAuthPage.load(self.box, self.settings)
        

class AuthPageAndroidHdpi(AuthPage):
    pass
