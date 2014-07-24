from src.core.app_launcher import AppLauncher
from src.core.testcase import AppTestCase
from src.pages.auth.auth_page import AuthPage
from unittest.case import skip
import unittest


#added comment
class LoginViaFB(AppTestCase):

    @skip("From poker")
    def testmasterfbAuth(self):
        authPage = AuthPage.load(AppLauncher.box, self.settings)
        fbAuthPage = authPage.signUpFb()
        
        fbAuthPage.fillEmail(self.settings.get("Facebook", "email"))
        fbAuthPage.fillPassword(self.settings.get("Facebook", "password"))
        fbConfirmPage = fbAuthPage.login()
        LobbyPage = fbConfirmPage.confirm()
        self.requestRunTestCase('testsecondaryfbAuth')
        GameTable = LobbyPage.play()
        
    @skip("From poker")
    def testsecondaryfbAuth(self):
        authPage = AuthPage.load(AppLauncher.box, self.settings)
        fbAuthPage = authPage.signUpFb()        
        fbAuthPage.fillEmail(self.settings.get("Facebook", "email"))
        fbAuthPage.fillPassword(self.settings.get("Facebook", "password"))
        fbConfirmPage = fbAuthPage.login()
        LobbyPage = fbConfirmPage.confirm()
        self.requestRunTestCase('some_testable')
        GameTable = LobbyPage.play()