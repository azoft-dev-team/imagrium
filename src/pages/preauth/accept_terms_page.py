'''
@author: Nosov Dmitriy
'''
from src.core.page import Page, ResourceLoader
from src.core.r import Resource
from src.pages.preauth.auth_page import AuthPage


class AcceptTermsPage(Page):

    actionAcceptAndContinue = ResourceLoader(Resource.acceptAndContinueBtn)
       
    def __init__(self, box, settings):
        super(AcceptTermsPage, self).__init__(box, settings)

        self.box = box
        self.settings = settings
        # It is necessary to assign a search area to all class fields
        self.actionAcceptAndContinue = self.box
        self.waitPageLoad()
        self.checkIfLoaded(['acceptAndContinue'])
    
    def acceptAndContinue(self):
        self.actionAcceptAndContinue.click()
        return AuthPage.load(self.box, self.settings)
    
    
class AcceptTermsPageAndroidHdpi(AcceptTermsPage):
    pass