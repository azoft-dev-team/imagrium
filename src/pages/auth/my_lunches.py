from src.core.page import Page, ResourceLoader
from src.core.r import Resource
from src.pages.general.popup_dialog import ConfirmationDialogPage


class MyLunchesPage(Page):
    
    myLunchesTitle = ResourceLoader(Resource.myLunchesTitle)
    actionSelectLunch = ResourceLoader(Resource.lunchField)
    actionCreateLunch = ResourceLoader(Resource.createLunchIcon)
      
    def __init__(self, box, settings):
        super(MyLunchesPage, self).__init__(box, settings)

        self.box = box
        # It is necessary to assign a search area to all class fields
        
        self.myLunchesTitle = self.box
        self.actionSelectLunch = self.box
        self.actionCreateLunch = self.box
        
        self.waitPageLoad()
        self.checkIfLoaded(['myLunchesTitle'])
    
    def selectLunch(self):
        self.actionSelectLunch.click()
        return LunchDetailsPage.load(self.box, self.settings)

    
class MyLunchesPageAndroidHdpi(MyLunchesPage):
    pass


class LunchDetailsPage(Page):
    
    lunchDetailsTitle = ResourceLoader(Resource.lunchDetailsTitle)
    actionJoinLunch = ResourceLoader(Resource.joinLunchBtn)
    actionAcceptJoinRequest = ResourceLoader(Resource.acceptJoinRequestBtn)

    def __init__(self, box, settings):
        super(LunchDetailsPage, self).__init__(box, settings)
        self.box = box
        
        self.lunchDetailsTitle = self.box
        self.actionJoinLunch = self.box
        self.actionAcceptJoinRequest = self.box
        
        self.waitPageLoad()
        self.checkIfLoaded(['lunchDetailsTitle'])
        
    def joinLunch(self):
        self.actionJoinLunch.click()
        ConfirmationDialogPage.load(self.box, self.settings).confirm()
        return self
    
    def checkJoinRequest(self):
        self.actionAcceptJoinRequest.highlight(1)
        
    
class LunchDetailsPageAndroidHdpi(LunchDetailsPage):
    pass


