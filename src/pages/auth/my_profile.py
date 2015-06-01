from src.core.page import Page, ResourceLoader
from src.core.r import Resource


class ViewProfilePage(Page):
    
    actionEditProfile = ResourceLoader(Resource.editProfileIcon)
    viewProfileTitle = ResourceLoader(Resource.viewProfileTitle)
      
    def __init__(self, box, settings):
        super(ViewProfilePage, self).__init__(box, settings)

        self.box = box
        # It is necessary to assign a search area to all class fields
        
        self.actionEditProfile = self.box
        self.viewProfileTitle = self.box
        
        self.waitPageLoad()
        self.checkIfLoaded(['viewProfileTitle'])
    
    def editProfile(self):
        self.actionEditProfile.click()
        return EditProfilePage.load(self.box, self.settings)

  
class ViewProfilePageAndroidHdpi(ViewProfilePage):
    pass


class EditProfilePage(Page):
    
    editProfileTitle = ResourceLoader(Resource.editProfileTitle)
    actionApplyChanges = ResourceLoader(Resource.applyChangesBtn)
    
    def __init__(self, box, settings):
        super(EditProfilePage, self).__init__(box, settings)

        self.box = box
        # It is necessary to assign a search area to all class fields
        
        self.editProfileTitle = self.box
        
        self.waitPageLoad()
        self.checkIfLoaded(['editProfileTitle'])
                
    def applyChanges(self):
        self.actionApplyChanges.click()
        return ViewProfilePage.load(self.box, self.settings)


class EditProfilePageAndroidHdpi(EditProfilePage):
    pass