from src.core.page import Page, ResourceLoader
from src.core.r import Resource
from src.pages.me.me_find_friends_search import MeFindFriendsSearch


class MeFindFriends(Page):

    findFromRegisteredListItem = ResourceLoader(Resource.findFromRegisteredListItem)
       
    def __init__(self, box, settings):
        super(MeFindFriends, self).__init__(box, settings)

        self.box = box
        self.settings = settings

        self.findFromRegisteredListItem = self.box
        self.checkIfLoaded(['findFromRegisteredListItem'])
    
    def actionFindFromRegistered(self):
        self.findFromRegisteredListItem.click()
        return MeFindFriendsSearch.load(self.box, self.settings)
    
    
class MeFindFriendsiOS(MeFindFriends):
    pass
