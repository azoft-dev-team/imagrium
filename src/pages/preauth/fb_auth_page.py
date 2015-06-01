'''
Created on 23.05.2013

@author: Nosov Dmitriy
'''
from src.core.page import Page, ResourceLoader, iOSPage, AndroidPage
from src.core.r import Resource
from src.pages.general.save_password_page import SavePasswordPage


class FbAuthPage(Page):
    """
    This page (web view) appears when a user wants to authorize against Facebook.
    """

    email = ResourceLoader([Resource.fbEmailFieldAndroidHdpi, Resource.fbEmailFieldAndroidHdpi_ru])
    password = ResourceLoader([Resource.fbPasswordFieldAndroidHdpi, Resource.fbPasswordFieldAndroidHdpi_ru])
    actionLogin = ResourceLoader([Resource.fbLoginBtnAndroidHdpi, Resource.fbLoginBtnAndroidHdpi_ru])
        
    def __init__(self, box, settings):
        super(FbAuthPage, self).__init__(box, settings)
        
        # It is necessary to assign a search area to all class fields
        self.email = self.box
        self.password = self.box
        self.actionLogin = self.box
        self.settings = settings
        self.waitPageLoad()

        self.checkIfLoaded(['email', 'password'])
        
    def fillEmail(self, text):
        self.email.click()
        self.waitPageLoad()
        self.inputText(text)
            
    def fillPassword(self, text):
        self.password.click()
        self.waitPageLoad()
        self.inputText(text)
        
    def login(self):
        self.actionLogin.click()
        return SavePasswordPage.load(self.box, self.settings)

        
class FbAuthPageiOS(FbAuthPage, iOSPage):
    pass


class FbAuthPageAndroidHdpi(FbAuthPage, AndroidPage):
    pass