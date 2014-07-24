'''
@author: Nosov Dmitriy
'''
from src.core.page import Page, ResourceLoader
from src.core.r import Resource
from src.pages.postauth.postauth_2_follow_places import PostauthFollowPlaces



class PostauthFollowPeople(Page):

    actionNext = ResourceLoader(Resource.actionNextiOS)
       
    def __init__(self, box, settings):
        super(PostauthFollowPeople, self).__init__(box, settings)

        self.box = box
        self.settings = settings
        # It is necessary to assign a search area to all class fields
        self.actionNext = self.box
        self.waitPageLoad()
        self.checkIfLoaded(['actionNext'])
    
    def actionGoNext(self):
        self.actionNext.click()
        return PostauthFollowPlaces.load(self.box, self.settings)
    
    
class PostauthFollowPeopleiOS(PostauthFollowPeople):
    pass