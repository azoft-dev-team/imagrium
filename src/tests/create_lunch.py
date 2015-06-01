from src.core.testcase import AppTestCase
from src.precondition.before_auth import AuthProcess
from unittest.case import skip
      

@skip('Skipped for testing')
class FFL_1_CreateLunch(AppTestCase):
        
    def testmasterCreateLunch(self):
        (menuPage, findLunchPage) = AuthProcess.fbAuth(self, self.initialPage, self.settings.get("Facebook", "userAEmail"), self.settings.get("Facebook", "userAPassword"))
        createLunchPage = menuPage.gotoCreateLunch()
        createLunchPage.takeScreenShot(self)
        citiesListPage = createLunchPage.openCities()
        citiesListPage.takeScreenShot(self)
        createLunchPage = citiesListPage.selectCity("Moscow")
        createLunchPage.takeScreenShot(self)
        selectPlacePage = createLunchPage.openPlaces()
        selectPlacePage.takeScreenShot(self)
        createLunchPage = selectPlacePage.selectPlace()
        createLunchPage.takeScreenShot(self)
        myLunchesPage = createLunchPage.createLunch()
        myLunchesPage.takeScreenShot(self)
        self.requestRunTestCase('testhelperJoinLunch')
        lunchDetailsPage = myLunchesPage.selectLunch()
        lunchDetailsPage.checkJoinRequest()
        lunchDetailsPage.takeScreenShot(self)
                
    def testhelperJoinLunch(self):
        (menuPage, findLunchPage) = AuthProcess.fbAuth(self, self.initialPage, self.settings.get("Facebook", "userBEmail"), self.settings.get("Facebook", "userBPassword"))
        lunchesListPage = findLunchPage.viewLunchesList()
        lunchDetailsPage = lunchesListPage.viewLunchDetails()
        lunchDetailsPage = lunchDetailsPage.joinLunch()

