from src.core.page import Page, ResourceLoader
from src.core.r import Resource


class Explore(Page):

    pageTitle = ResourceLoader(Resource.explorePageTitle)
       
    def __init__(self, box, settings):
        super(Explore, self).__init__(box, settings)

        self.box = box
        self.settings = settings
        # It is necessary to assign a search area to all class fields
        self.pageTitle = self.box
        
        self.waitPageLoad()
        
        self.checkIfLoaded(['pageTitle'])

    
class ExploreiOS(Explore):
    pass
