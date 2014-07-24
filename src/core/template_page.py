from src.core.page import Page, ResourceLoader
from src.core.r import Resource
from src.pages.auth_page import AuthPage


class AuthPageLocation(Page):

    actionAllowUseLocation = ResourceLoader(Resource.actionAllowUseLocation)
       
    def __init__(self, box, settings):
        super(AuthPageLocation, self).__init__(box, settings)

        self.box = box
        self.settings = settings
        # It is necessary to assign a search area to all class fields
        self.actionAllowUseLocation = self.box
                
        self.checkIfLoaded(['actionAllowUseLocation'])
    
    def allowUseLocation(self):
        self.actionAllowUseLocation.click()
        return AuthPage.load(self.box, self.settings)
    
    
class AuthPageLocationiOS(AuthPageLocation):
    pass