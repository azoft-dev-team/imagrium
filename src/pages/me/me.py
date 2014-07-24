from src.core.page import Page, ResourceLoader
from src.core.r import Resource
from src.pages.me.me_find_friends import MeFindFriends


class Me(Page):

    findFriendsListItem = ResourceLoader(Resource.findFriendsListItem)
       
    def __init__(self, box, settings):
        super(Me, self).__init__(box, settings)

        self.box = box
        self.settings = settings
        
        self.waitPageLoad()
        
        self.findFriendsListItem = self.box

        self.checkIfLoaded(['findFriendsListItem'])
    
    def actionFindFriends(self):
        self.findFriendsListItem.click()
        return MeFindFriends.load(self.box, self.settings)
    
    
class MeiOS(Me):
    pass
