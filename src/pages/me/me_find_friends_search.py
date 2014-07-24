from src.core.page import Page, ResourceLoader, iOSPage
from src.core.r import Resource


class MeFindFriendsSearch(Page, iOSPage):

    followUserBtn = ResourceLoader(Resource.followUserBtn)
    unfollowUserBtn = ResourceLoader(Resource.unfollowUserBtn)
    searchUsersBtn = ResourceLoader(Resource.searchUsersBtn)
    runSearchBtn = ResourceLoader(Resource.runSearchBtn)
       
    def __init__(self, box, settings):
        super(MeFindFriendsSearch, self).__init__(box, settings)

        self.box = box
        self.settings = settings
        
        self.followUserBtn = self.box
        self.unfollowUserBtn = self.box
        self.searchUsersBtn = self.box

        self.checkIfLoaded(['searchUsersBtn'])
    
    def actionFindFriend(self, friendName):
        self.searchUsersBtn.click()
        self.inputText(self, friendName)
        self.runSearchBtn.click()
        self.waitPageLoad()
        return self
    
    def followFirstFriend(self):
        self.followUserBtn.click()
        return self
    
    def unfollowFirstFriend(self):
        self.unfollowUserBtn.click()
        return self

    
class MeFindFriendsSearchiOS(MeFindFriendsSearch):
    pass
