from src.core.app_launcher import AppLauncher
from src.core.testcase import AppTestCase
from src.pages.auth.auth_page_uselocation import AuthPageLocation
from src.pages.bottom_navigation import BottomNavigation
        

class HOP_325_Vihod_Is_Regima_Neaktivnosti(AppTestCase):
       
    def testmasterFbAuth(self):
        authPageLocation = self.initialPage
        authPage = authPageLocation.allowUseLocation()
        authPage.takeScreenShot(self)
        
        fbAuthPage = authPage.signUpFb()
        fbAuthPage.takeScreenShot(self)
        fbAuthPage.fillEmail(self.settings.get("Facebook", "email"))
        fbAuthPage.takeScreenShot(self)
        fbAuthPage.fillPassword(self.settings.get("Facebook", "password"))
        fbAuthPage.takeScreenShot(self)
        fbConfirmPage = fbAuthPage.login()
        
        postauthFollowPeople = fbConfirmPage.confirm()
        postauthFollowPlaces = postauthFollowPeople.actionGoNext()
        postauthContactsDialog = postauthFollowPlaces.actionGoNext()
        postauthDone = postauthContactsDialog.actionAllowContacts()
        postauthDone.completeWizard()
        
        #Using the bottom navigation
        nav = BottomNavigation.load(AppLauncher.box, self.settings)
        
        nav.actionGoMe()
        
        self.requestRunTestCase('testhelperFollowUser')
        
        nav.actionGoExplore()
                
        me = nav.actionGoMe()
        me.takeScreenShot(self)
        
        self.requestRunTestCase('testhelperUnfollowUser')
        
        nav.actionGoExplore()
                
        me = nav.actionGoMe()
        me.takeScreenShot(self)
                
    def testhelperFollowUser(self):
        authPageLocation = self.initialPage
        authPage = authPageLocation.allowUseLocation()
        authPage.takeScreenShot(self)
        
        fbAuthPage = authPage.signUpFb()
        fbAuthPage.takeScreenShot(self)
        fbAuthPage.fillEmail(self.settings.get("Facebook", "email"))
        fbAuthPage.takeScreenShot(self)
        fbAuthPage.fillPassword(self.settings.get("Facebook", "password"))
        fbAuthPage.takeScreenShot(self)
        fbConfirmPage = fbAuthPage.login()
        
        postauthFollowPeople = fbConfirmPage.confirm()
        postauthFollowPlaces = postauthFollowPeople.actionGoNext()
        postauthContactsDialog = postauthFollowPlaces.actionGoNext()
        postauthDone = postauthContactsDialog.actionAllowContacts()
        postauthDone.completeWizard()
        
        #Using the bottom navigation
        nav = BottomNavigation.load(AppLauncher.box, self.settings)
        
        me = nav.actionGoMe()
        
        findFriends = me.actionFindFriends()
        friendsSearch = findFriends.actionFindFromRegistered()
        friendsSearch = friendsSearch.actionFindFriend(self.settings.get("Extras", "HOP_325_SEARCH_USERNAME"))
        friendsSearch = friendsSearch.followFirstFriend()
        
        nav.actionGoMe(inactive=False)

    def testhelperUnfollowUser(self):
        authPageLocation = self.initialPage
        authPage = authPageLocation.allowUseLocation()
        authPage.takeScreenShot(self)
        
        fbAuthPage = authPage.signUpFb()
        fbAuthPage.takeScreenShot(self)
        fbAuthPage.fillEmail(self.settings.get("Facebook", "email"))
        fbAuthPage.takeScreenShot(self)
        fbAuthPage.fillPassword(self.settings.get("Facebook", "password"))
        fbAuthPage.takeScreenShot(self)
        fbConfirmPage = fbAuthPage.login()
        
        postauthFollowPeople = fbConfirmPage.confirm()
        postauthFollowPlaces = postauthFollowPeople.actionGoNext()
        postauthContactsDialog = postauthFollowPlaces.actionGoNext()
        postauthDone = postauthContactsDialog.actionAllowContacts()
        
        postauthDone.completeWizard()
 
        #Using the bottom navigation
        nav = BottomNavigation.load(AppLauncher.box, self.settings)
        
        me = nav.actionGoMe()
        
        findFriends = me.actionFindFriends()
        friendsSearch = findFriends.actionFindFromRegistered()
        friendsSearch = friendsSearch.actionFindFriend(self.settings.get("Extras", "HOP_325_SEARCH_USERNAME"))
        friendsSearch = friendsSearch.unfollowFirstFriend()
        
        nav.actionGoMe(inactive=False)
