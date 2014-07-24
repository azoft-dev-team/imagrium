from src.core.page import Page, ResourceLoader
from src.core.r import Resource
from src.pages.postauth.postauth_4_allow_contacts import PostauthContactsDialog


class PostauthInviteFriends(Page):

    actionNext = ResourceLoader(Resource.actionNextiOS)
       
    def __init__(self, box, settings):
        super(PostauthInviteFriends, self).__init__(box, settings)

        self.box = box
        self.settings = settings
        # It is necessary to assign a search area to all class fields
        self.actionNext = self.box                
        self.checkIfLoaded(['actionNext'])
    
    def actionGoNext(self):
        self.actionNext.click()
        return PostauthContactsDialog.load(self.box, self.settings)
    
    
class PostauthInviteFriendsiOS(PostauthInviteFriends):
    pass