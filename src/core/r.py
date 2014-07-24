'''
Created on 15.05.2013

@author: Nosov Dmitriy
'''


class Resource:
    
    #auth_page_location
    actionAllowUseLocation = "res/pages/ios/auth_page_location/useLocationBtniOS.png"
       
    #auth_page    
    fbAuthBtniOS = "res/pages/ios/auth_page/fbAuthBtniOS.png"
    fbAuthBtnAndroidHdpi = "res/pages/android/hdpi/auth_page/fbAuthBtn.png"
    authSelectionTitleAndroiHdpi = "res/pages/android/hdpi/auth_page/authSelectionLabel.png"
    agreeTermsBtniOS = "res/pages/ios/auth_page/agreeTermsBtniOS.png"
    
    # fb_auth_page (iOS)
    fbEmailFieldiOS        = "res/pages/ios/fb_auth/fbEmailFieldiOS.png"
    fbPasswordFieldiOS    = "Password"
    fbLoginBtniOS         = "res/pages/ios/fb_auth/fbLoginBtniOS.png"
    fbConfirmBtniOS       = "res/pages/ios/fb_auth/fbConfirmBtniOS.png"
    
    fbEmailFieldiOS_ru = "res/pages/ios/fb_auth/fbEmailFieldiOS_ru.png"
    fbPasswordFieldiOS_ru    = "res/pages/ios/fb_auth/fbPasswordFieldiOS_ru.png"
    fbLoginBtniOS_ru         = "res/pages/ios/fb_auth/fbLoginBtniOS_ru.png"
    
    # fb_auth_page (Android)
    fbEmailFieldAndroidHdpi        = "res/pages/android/hdpi/fb_auth/fbEmailField.png"
    fbPasswordFieldAndroidHdpi    = "Password"
    fbLoginBtnAndroidHdpi         = "res/pages/android/hdpi/fb_auth/fbLoginBtn.png"
    fbConfirmBtnAndroidHdpi       = "res/pages/android/hdpi/fb_auth/fbConfirmBtn.png"
    
    fbEmailFieldAndroidHdpi_ru =       "res/pages/android/hdpi/fb_auth/fbEmailField_ru.png"
    fbPasswordFieldAndroidHdpi_ru    = "res/pages/android/hdpi/fb_auth/fbPasswordField_ru.png"
    fbLoginBtnAndroidHdpi_ru         = "res/pages/android/hdpi/fb_auth/fbLoginBtn_ru.png"

        
    #core
    # iOS 7
    verticalBorderiOS   = "res/pages/ios/core/verticalBorder.png"
    horizontalBorderiOS = "res/pages/ios/core/horizontalBorder.png"

    #Android Hdpi
    verticalBorderAndroidHdpi   = "res/pages/android/hdpi/core/verticalBorder.png"
    horizontalBorderAndroidHdpi = "res/pages/android/hdpi/core/horizontalBorder.png"
    
    actionNextiOS = "res/pages/ios/core/nextBtniOS.png"
    dialogOkBtniOS = "res/pages/ios/core/dialogOkBtniOS.png"
    doneBtniOS = "res/pages/ios/core/doneBtniOS.png"
    followUserBtn = "res/pages/ios/core/followUserBtn.png"
    unfollowUserBtn = "res/pages/ios/core/unfollowUserBtn.png"
    searchUsersBtn = "res/pages/ios/core/searchUsersBtn.png"
  
    #feed
    explorePageTitle = "res/pages/ios/explore/pageTitle.png"
    
    #me
    findFriendsListItem = "res/pages/ios/me/findFriendsListItem.png"
    
    #me_find_friends
    findFromRegisteredListItem = "res/pages/ios/me_find_friends/findFromRegisteredListItem.png"
    
    #navigation icons inactive
    meNavIconInactive = "res/pages/ios/bottom_navigation/meNavIconInactive.png"
    meNavIconActive = "res/pages/ios/bottom_navigation/meNavIconActive.png"
    exploreNavIconInactive = "res/pages/ios/bottom_navigation/exploreNavIconInactive.png"
    exploreNavIconActive = "res/pages/ios/bottom_navigation/exploreNavIconActive.png"    
  
    # keyboard_iOs
    
    keyboardiOs = "res/pages/ios/keyboard/keyboardiOS.png"
    keyboardiOsTop = "res/pages/ios/keyboard/keyboardiOSTop.png"
    runSearchBtn = "res/pages/ios/keyboard/searchBtn.png"    
    btnA = "res/pages/ios/keyboard/aLetteriOS.png"
    btnB = "res/pages/ios/keyboard/bLetteriOS.png"    
    btnZ = "res/pages/ios/keyboard/zLetteriOS.png"
    btnO = "res/pages/ios/keyboard/oLetteriOS.png"
    btnF = "res/pages/ios/keyboard/fLetteriOS.png"
    btnT = "res/pages/ios/keyboard/tLetteriOS.png"
    btnE = "res/pages/ios/keyboard/eLetteriOS.png"
    btnS = "res/pages/ios/keyboard/sLetteriOS.png"
    btnH = "res/pages/ios/keyboard/hLetteriOS.png"
    btnR = "res/pages/ios/keyboard/rLetteriOS.png"
    btnD = "res/pages/ios/keyboard/dLetteriOS.png"
    btnP = "res/pages/ios/keyboard/pLetteriOS.png"
    btnK = "res/pages/ios/keyboard/kLetteriOS.png"    
    

    #lost
    hophopLogoMdpi = "res/pages/android/mdpi/core/keyboardTop.png"
    inviteFriendsTabMdpi = "res/pages/android/mdpi/core/keyboardTop.png"
    upgdadeAppBtn_4_2_Mdpi = ""
    remindBtn_4_2_Mdpi = ""    
  
    
    


class ClientMessageConsts:
    TASK_DONE = "done"
    TASK_EXIT = "~exit~" #in case we need to stop all clients


class TestPlanConsts:
    ANDROID_OS = "Android"
    MDPI = "mdpi"
    HDPI = "hdpi"
    X_OS = "iOS"    
    