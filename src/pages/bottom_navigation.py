from src.core.page import ResourceLoader, Page
from src.core.r import Resource
from src.pages.explore import Explore
from src.pages.me.me import Me


class BottomNavigation(Page):

    meNavIconInactive = ResourceLoader(Resource.meNavIconInactive)
    meNavIconActive = ResourceLoader(Resource.meNavIconActive)

    exploreNavIconInactive = ResourceLoader(Resource.exploreNavIconInactive)
    exploreNavIconActive = ResourceLoader(Resource.exploreNavIconActive)
       
    def __init__(self, box, settings):
        super(Page, self).__init__(box, settings)

        self.box = box
        self.settings = settings
        # It is necessary to assign a search area to all class fields
        self.meNavIconInactive = self.box
        self.meNavIconActive = self.box
    
    def actionGoMe(self, inactive=True):
        if inactive:
            self.meNavIconInactive.click()
        else:
            self.meNavIconActive.click()
        return Me.load(self.box, self.settings)

    def actionGoExplore(self, inactive=True):
        if inactive:
            self.exploreNavIconInactive.click()
        else:
            self.exploreNavIconActive.click()
        return Explore.load(self.box, self.settings)


class BottomNavigationiOS(BottomNavigation):
    pass
