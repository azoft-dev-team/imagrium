from src.core.page import Page, ResourceLoader
from src.core.r import Resource
from src.pages.postauth.postauth_5_done import PostauthDone




class PostauthContactsDialog(Page):

    dialogOkBtniOS = ResourceLoader(Resource.dialogOkBtniOS)
       
    def __init__(self, box, settings):
        super(PostauthContactsDialog, self).__init__(box, settings)

        self.box = box
        self.settings = settings
        # It is necessary to assign a search area to all class fields
        self.dialogOkBtniOS = self.box
        self.waitPageLoad()
        self.checkIfLoaded(['dialogOkBtniOS'])
    
    def actionAllowContacts(self):
        self.dialogOkBtniOS.click()
        return PostauthDone.load(self.box, self.settings)
    
    
class PostauthContactsDialogiOS(PostauthContactsDialog):
    pass