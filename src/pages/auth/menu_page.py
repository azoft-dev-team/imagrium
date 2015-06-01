from src.core.page import Page, ResourceLoader
from src.core.r import Resource
from src.pages.auth.create_lunch import CreateLunchPage
from src.pages.auth.my_friends import MyFriendsPage
from src.pages.auth.my_profile import ViewProfilePage


class MenuPage(Page):
    
    actionOpenMenu = ResourceLoader(Resource.openMenuBtn)
    actionCreateLunch = ResourceLoader([Resource.createLunchBtnActive, Resource.createLunchBtnInactive])
    actionMyFriends = ResourceLoader([Resource.myFriendsBtnActive, Resource.myFriendsBtnInactive])
    actionMyProfile = ResourceLoader([Resource.myProfileBtnInactive, Resource.myProfileBtnActive])
      
    def __init__(self, box, settings):
        super(MenuPage, self).__init__(box, settings)

        self.box = box
        # It is necessary to assign a search area to all class fields
        self.actionOpenMenu = self.box
        self.actionCreateLunch = self.box
        self.actionMyFriends = self.box
        self.actionMyProfile = self.box
        
        self.waitPageLoad()
        self.checkIfLoaded(['actionOpenMenu'])   
    
    def open(self):
        self.actionOpenMenu.click()
        return self

    def gotoCreateLunch(self):
        self.open()
        self.waitPageLoad()
        self.actionCreateLunch.click()
        return CreateLunchPage.load(self.box, self.settings)

    def gotoMyFriends(self):
        self.open()
        self.waitPageLoad()
        self.actionMyFriends.click()
        return MyFriendsPage.load(self.box, self.settings)
    
    def gotoMyProfile(self):
        self.open()
        self.waitPageLoad()
        self.actionMyProfile.click()
        return ViewProfilePage.load(self.box, self.settings)
    
class MenuPageAndroidHdpi(MenuPage):
    pass
