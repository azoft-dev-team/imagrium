from src.core.testcase import AppTestCase
from src.precondition.before_auth import AuthProcess
from unittest.case import skip
      
      
class FFL_2_AddFriend(AppTestCase):
        
    def testmasterAddFriend(self):
        (menuPage, findLunchPage) = AuthProcess.fbAuth(self, self.initialPage, self.settings.get("Facebook", "userAEmail"), self.settings.get("Facebook", "userAPassword"))        
        myFriendsPage = menuPage.gotoMyFriends()
        myFriendsPage.takeScreenShot(self)
        findFriendsPage = myFriendsPage.findFriends()
        findFriendsPage.takeScreenShot(self)
        findFriendsPage = findFriendsPage.requestBeFriends()
        findFriendsPage.takeScreenShot(self)

        self.requestRunTestCase('testhelperAcceptFriendRequest')
        findFriendsPage.back()
        myFriendsPage.checkFriendExist()

                              
    def testhelperAcceptFriendRequest(self):
        (menuPage, findLunchPage) = AuthProcess.fbAuth(self, self.initialPage, self.settings.get("Facebook", "userBEmail"), self.settings.get("Facebook", "userBPassword"))
        myFriendsPage = menuPage.gotoMyFriends()
        myFriendsPage.takeScreenShot(self)
        myFriendsPage = myFriendsPage.addFriend()
        myFriendsPage.takeScreenShot(self)
