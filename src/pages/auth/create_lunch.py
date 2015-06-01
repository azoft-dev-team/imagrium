from libs.sikuli import Sikuli
from src.core.page import Page, ResourceLoader
from src.core.r import Resource
from src.pages.auth.my_lunches import MyLunchesPage

class CreateLunchPage(Page):
    
    actionOpenCities = ResourceLoader(Resource.openCitiesField)
    actionSelectPlace = ResourceLoader(Resource.selectPlaceField)
    actionCreateLunch = ResourceLoader(Resource.createLunchIcon)
      
    def __init__(self, box, settings):
        super(CreateLunchPage, self).__init__(box, settings)

        self.box = box
        # It is necessary to assign a search area to all class fields
        self.actionOpenCities = self.box
        self.actionSelectPlace = self.box
        self.actionCreateLunch = self.box
        self.waitPageLoad()
        self.checkIfLoaded(['actionOpenCities'])

    def openCities(self):
        r = self.actionOpenCities.res
        Sikuli.Region(r.x, r.y + 235, r.w, r.h).click() #hardcode for now as GPS outputs random cities, cannot give any predictions on them
        return CitiesListPage.load(self.box, self.settings)
    
    def openPlaces(self):
        self.actionSelectPlace.click()
        return SelectPlacePage.load(self.box, self.settings)
    
    def createLunch(self):
        self.actionCreateLunch.click()
        return MyLunchesPage.load(self.box, self.settings)

    
class CreateLunchPageAndroidHdpi(CreateLunchPage):
    pass


class CitiesListPage(Page):
    
    moscow = ResourceLoader(Resource.moscowField)
    actionSelectPlace = ResourceLoader(Resource.placeField)
      
    def __init__(self, box, settings):
        super(CitiesListPage, self).__init__(box, settings)

        self.box = box
        # It is necessary to assign a search area to all class fields
        self.moscow = self.box
        self.actionSelectPlace = self.box
        self.waitPageLoad()
        self.checkIfLoaded(['moscow'])

    def selectCity(self, city):
        if city == 'Moscow':
            self.moscow.click()
            return CreateLunchPage.load(self.box, self.settings)
        else:
            AssertionError("There is no handler corresponding to this name yet")

    
class CitiesListPageAndroidHdpi(CitiesListPage):
    pass


class SelectPlacePage(Page):
    
    actionSelectPlace = ResourceLoader(Resource.placeField)
      
    def __init__(self, box, settings):
        super(SelectPlacePage, self).__init__(box, settings)

        self.box = box
        # It is necessary to assign a search area to all class fields
        self.actionSelectPlace = self.box

        self.waitPageLoad()
        self.checkIfLoaded(['actionSelectPlace'])

    def selectPlace(self):
        self.actionSelectPlace.click()
        return CreateLunchPage.load(self.box, self.settings)

    
class SelectPlacePageAndroidHdpi(SelectPlacePage):
    pass
