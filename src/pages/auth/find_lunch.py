from src.core.page import Page, ResourceLoader
from src.core.r import Resource
from src.pages.auth.my_lunches import LunchDetailsPage


class FindLunchPage(Page):
    
    findLunchTitle = ResourceLoader(Resource.findLunchTitle)
    actionViewLunchesList = ResourceLoader(Resource.viewLunchesListIcon)
      
    def __init__(self, box, settings):
        super(FindLunchPage, self).__init__(box, settings)

        self.box = box
        # It is necessary to assign a search area to all class fields
        self.findLunchTitle = self.box
        self.actionViewLunchesList = self.box
        
        self.waitPageLoad()
        self.checkIfLoaded(['findLunchTitle'])
    
    def viewLunchesList(self):
        self.actionViewLunchesList.click()
        return LunchesListPage.load(self.box, self.settings)

    
class FindLunchPageAndroidHdpi(FindLunchPage):
    pass


class LunchesListPage(Page):
    actionViewLunchDetails = ResourceLoader(Resource.viewLunchDetails)

    def __init__(self, box, settings):
        super(LunchesListPage, self).__init__(box, settings)

        self.box = box
        # It is necessary to assign a search area to all class fields
        self.actionViewLunchDetails = self.box
        self.waitPageLoad()
        self.checkIfLoaded(['actionViewLunchDetails'])
        
    def viewLunchDetails(self):
        self.actionViewLunchDetails.click()
        return LunchDetailsPage.load(self.box, self.settings)
        
    
class LunchesListPageAndroidHdpi(LunchesListPage):
    pass