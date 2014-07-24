from src.core.page import Page, ResourceLoader, iOSPage
from src.core.r import Resource
from src.pages.postauth.postauth_1_follow_people import PostauthFollowPeople



class FbConfirmPage(Page, iOSPage):
    
    actionConfirmAccount = ResourceLoader(Resource.fbConfirmBtniOS)
      
    def __init__(self, box, settings):
        super(FbConfirmPage, self).__init__(box, settings)

        self.box = box
        # It is necessary to assign a search area to all class fields
        self.actionConfirmAccount = self.box
        self.waitPageLoad()
        self.checkIfLoaded(['actionConfirmAccount'])

    def confirm(self):
        self.actionConfirmAccount.click()
        return PostauthFollowPeople.load(self.box, self.settings)

    
class FbConfirmPageiOS(FbConfirmPage):
    pass