class AuthProcess:
    
    @staticmethod
    def fbAuth(testObj, initPage, email, password):
        acceptTermsPage = initPage
        authPage = acceptTermsPage.acceptAndContinue()
        authPage.takeScreenShot(testObj)
        fbAuthPage = authPage.signUpFb()
        fbAuthPage.takeScreenShot(testObj)
        fbAuthPage.fillEmail(email)
        fbAuthPage.takeScreenShot(testObj)
        fbAuthPage.fillPassword(password)
        fbAuthPage.takeScreenShot(testObj)
        savePasswordPage = fbAuthPage.login()
        savePasswordPage.takeScreenShot(testObj)
        (menuPage, findLunchPage) = savePasswordPage.skipSave()
        menuPage.takeScreenShot(testObj)
        return (menuPage, findLunchPage)