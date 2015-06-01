from src.core.page import Page, ResourceLoader
from src.core.r import Resource
from src.pages.auth.find_lunch import FindLunchPage
from src.pages.auth.menu_page import MenuPage


class SavePasswordPage(Page):
    
    actionSkipSavePassword = ResourceLoader(Resource.skipSavePasswordBtn)
      
    def __init__(self, box, settings):
        super(SavePasswordPage, self).__init__(box, settings)

        self.box = box
        # It is necessary to assign a search area to all class fields
        self.actionSkipSavePassword = self.box
        self.waitPageLoad()
        self.checkIfLoaded(['actionSkipSavePassword'])

    def skipSave(self):
        self.actionSkipSavePassword.click()
        return (MenuPage.load(self.box, self.settings), FindLunchPage.load(self.box, self.settings))

    
class SavePasswordPageAndroidHdpi(SavePasswordPage):
    pass