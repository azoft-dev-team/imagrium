import org.sikuli.basics.SikuliXforJython
import os
from libs.sikuli import *

#from src.pages.auth.my_friends import FindFriendsPage, MyFriendsPage
#from src.pages.auth.find_lunch import FindLunchPage
#from src.pages.auth.create_lunch import CreateLunchPage,SelectPlacePage

from src.pages.auth.menu_page import MenuPage

Sikuli.setBundlePath(os.getcwd())

import logging
logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%I:%M:%S %p', level=logging.INFO)

import ConfigParser


box = Sikuli.Region(701, 149, 484, 803)
config = ConfigParser.ConfigParser()
config.read("conf/android_settings.conf")


menuPage = MenuPage.load(box, config)
myProfilePage = menuPage.gotoMyProfile()
editProfilePage = myProfilePage.editProfile()
myProfilePage = editProfilePage.applyChanges()