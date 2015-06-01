from src.core.page import Page, ResourceLoader, AndroidPage
from src.core.r import Resource


class MyFriendsPage(Page):
    
    myFriendsTitle = ResourceLoader(Resource.myFriendsTitle)
    actionFindFriends = ResourceLoader(Resource.findFriendsBtn)
    actionAddFriend = ResourceLoader(Resource.addFriendIcon)
    actionRemoveFromFriends = ResourceLoader(Resource.removeFromFriendsIcon)
    

    def __init__(self, box, settings):
        super(MyFriendsPage, self).__init__(box, settings)

        self.box = box
        # It is necessary to assign a search area to all class fields
        
        self.myFriendsTitle = self.box
        self.actionFindFriends = self.box
        self.actionAddFriend = self. box
        self.actionRemoveFromFriends = self.box
        
        self.waitPageLoad()
        self.checkIfLoaded(['myFriendsTitle'])
    
    def findFriends(self):
        self.waitPageLoad()
        self.actionFindFriends.click()
        return FindFriendsPage.load(self.box, self.settings)
    
    def addFriend(self):
        self.waitPageLoad()
        self.actionAddFriend.click()
        return self
    
    def checkFriendExist(self):
        self.actionRemoveFromFriends.highlight(1)
    
class MyFriendsPageAndroidHdpi(MyFriendsPage):
    pass


class FindFriendsPage(Page):
    findFriendsTitle = ResourceLoader([Resource.findFriendsTitle, Resource.findFriendsListTitle])
    actionAddToFriends = ResourceLoader(Resource.addToFriendsIcon)
    
    def __init__(self, box, settings):
        super(FindFriendsPage, self).__init__(box, settings)

        self.box = box
        # It is necessary to assign a search area to all class fields
        self.actionAddToFriends = self.box
        self.findFriendsTitle = self.box
        
        self.waitPageLoad()
        self.checkIfLoaded(['findFriendsTitle'])
        
    def requestBeFriends(self):
        self.waitPageLoad()
        self.actionAddToFriends.click()
        return self
        
        
class FindFriendsPageAndroidHdpi(FindFriendsPage, AndroidPage):
    pass
