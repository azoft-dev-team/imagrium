from src.core.page import Page, ResourceLoader
from src.core.r import Resource
from src.pages.postauth.postauth_4_invite_friends import PostauthInviteFriends




class PostauthFollowFriends(Page):

    actionNext = ResourceLoader(Resource.actionNextiOS)
       
    def __init__(self, box, settings):
        super(PostauthFollowFriends, self).__init__(box, settings)

        self.box = box
        self.settings = settings
        # It is necessary to assign a search area to all class fields
        self.actionNext = self.box
        self.waitPageLoad()
        self.checkIfLoaded(['actionNext'])
    
    def actionGoNext(self):
        self.actionNext.click()
        return PostauthInviteFriends.load(self.box, self.settings)
    
    
class PostauthFollowFriendsiOS(PostauthFollowFriends):
    pass