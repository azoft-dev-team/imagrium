from src.core.page import Page, ResourceLoader
from src.core.r import Resource
from src.pages.explore import Explore


class PostauthDone(Page):

    doneBtniOS = ResourceLoader(Resource.doneBtniOS)
       
    def __init__(self, box, settings):
        super(PostauthDone, self).__init__(box, settings)

        self.box = box
        self.settings = settings
        # It is necessary to assign a search area to all class fields
        self.doneBtniOS = self.box
        self.waitPageLoad()
        self.checkIfLoaded(['doneBtniOS'])
    
    def completeWizard(self):
        self.doneBtniOS.click()
        return Explore.load(self.box, self.settings)
    
    
class PostauthDoneiOS(PostauthDone):
    pass
