from src.core.page import Page, ResourceLoader
from src.core.r import Resource


class ConfirmationDialogPage(Page):
    
    actionConfirm = ResourceLoader(Resource.confirmDialogBtn)

    def __init__(self, box, settings):
        super(ConfirmationDialogPage, self).__init__(box, settings)
        self.box = box
        self.actionConfirm = self.box
        self.waitPageLoad()
        self.checkIfLoaded(['actionConfirm'])
        
    def confirm(self):
        self.actionConfirm.click()
        
    
class ConfirmationDialogPageAndroidHdpi(ConfirmationDialogPage):
    pass