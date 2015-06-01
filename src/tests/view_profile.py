from src.core.testcase import AppTestCase
from src.precondition.before_auth import AuthProcess
from unittest.case import skip
      
@skip('Skipped for testing')
class FFL_3_EditProfile(AppTestCase):
       
    def testmasterEditProfile(self):
        (menuPage, findLunchPage) = AuthProcess.fbAuth(self, self.initialPage, self.settings.get("Facebook", "userAEmail"), self.settings.get("Facebook", "userAPassword"))
        menuPage.takeScreenShot(self)
        myProfilePage = menuPage.gotoMyProfile()
        myProfilePage.takeScreenShot(self)
        editProfilePage = myProfilePage.editProfile()
        editProfilePage.takeScreenShot(self)
        myProfilePage = editProfilePage.applyChanges()
        myProfilePage.takeScreenShot(self)
