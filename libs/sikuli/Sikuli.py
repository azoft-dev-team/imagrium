# Copyright 2010-2013, Sikuli.org
# Released under the MIT License.
# modified RaiMan 2013

from __future__ import with_statement
from org.sikuli.basics import Debug
Debug.log(3, "Jython: sikuli: Sikuli: entering")
import time
import __builtin__
import __main__
import types
import sys
import os

Debug.log(3, "Jython: sikuli: Sikuli: constants")
import org.sikuli.script.FindFailed as FindFailed
from org.sikuli.script.FindFailedResponse import *
from org.sikuli.script.Constants import *
import org.sikuli.script.Button as Button
from org.sikuli.script.Button import WHEEL_UP, WHEEL_DOWN
from org.sikuli.basics import OS

Debug.log(3, "Jython: sikuli: Sikuli: import Region")
from org.sikuli.script import Region as JRegion
from Region import *

Debug.log(3, "Jython: sikuli: Sikuli: import Screen")
from org.sikuli.script import Screen as JScreen
from Screen import *

Debug.log(3, "Jython: sikuli: Sikuli: Env.addHotkey")
from Env import *

Debug.log(3, "Jython: sikuli: Sikuli: import Match")
from org.sikuli.script import Match
Debug.log(3, "Jython: sikuli: Sikuli: import Pattern")
from org.sikuli.script import Pattern
Debug.log(3, "Jython: sikuli: Sikuli: import Location")
from org.sikuli.script import Location
Debug.log(3, "Jython: sikuli: Sikuli: import ScreenUnion")
from org.sikuli.script import ScreenUnion
Debug.log(3, "Jython: sikuli: Sikuli: import Finder")
from org.sikuli.script import Finder

Debug.log(3, "Jython: sikuli: Sikuli: import App")
from org.sikuli.script import App
Debug.log(3, "Jython: sikuli: Sikuli: import Key")
from org.sikuli.script import Key
from org.sikuli.script import KeyModifier
from org.sikuli.script.KeyModifier import KEY_CTRL, KEY_SHIFT, KEY_META, KEY_CMD, KEY_WIN, KEY_ALT

Debug.log(3, "Jython: sikuli: Sikuli: import from Basics")
from org.sikuli.basics import ImageLocator
from org.sikuli.basics import Settings
from org.sikuli.basics import ExtensionManager

Debug.log(3, "Jython: sikuli: Sikuli: import from compare")
from org.sikuli.script.compare import DistanceComparator
from org.sikuli.script.compare import VerticalComparator
from org.sikuli.script.compare import HorizontalComparator

Debug.log(3, "Jython: sikuli: Sikuli: init SikuliImporter")
import SikuliImporter

Debug.log(3, "Jython: sikuli: Sikuli: import SikuliScript")
from org.sikuli.basics import SikuliScript
from org.sikuli.script import SikuliX

##
# some support for handling unicode and strings
#
## use instead of print if unicode strings present
# usage: uprint(s1, u1, u2, u3, s3, ...)
# 
def uprint(*args):
    for e in args[:-1]:
        if isinstance(e, str): print e,
        else: print e.encode("utf8"),
    if isinstance(args[-1], str): print args[-1]
    else: print args[-1].encode("utf8")

##
# to make an utf8-encoded string from a str object
#
def unicd(s):
    return (unicode(s, "utf8"))

##
# loads a Sikuli extension (.jar) from
#  1. user's sikuli data path
#  2. bundle path
#
def load(jar):
    def _load(abspath):
        if os.path.exists(abspath):
            if not abspath in sys.path:
                sys.path.append(abspath)
            return True
        return False
   
    if _load(jar):
        return True
    path = getBundlePath()
    if path:
        jarInBundle = os.path.join(path, jar)
        if _load(jarInBundle):
            return True
    path = ExtensionManager.getInstance().getLoadPath(jar)
    if path and _load(path):
        return True
    return False

def addModPath(path):
    if path[-1] == Settings.getFilePathSeperator():
        path = path[:-1]
    if not path in sys.path:
        sys.path.append(path)

def addImagePath(path):
    ImageLocator.addImagePath(path)

def getImagePath():
    return [e for e in ImageLocator.getImagePath() if e]

def removeImagePath(path):
    ImageLocator.removeImagePath(path)
   
def resetImagePath(path):
    ImageLocator.resetImagePath(path)

##
# Sets the path for searching images in all Sikuli Script methods. <br/>
# Sikuli IDE sets this to the path of the bundle of source code (.sikuli)
# automatically. If you write Sikuli scripts by the Sikuli IDE, you should
# not call this method.
#
def setBundlePath(path):
    ImageLocator.setBundlePath(path)

def getBundlePath():
    return ImageLocator.getBundlePath()

##
# Sikuli shows actions (click, dragDrop, ... etc.) if this flag is set to <i>True</i>.
# The default setting is <i>False</i>.
#
def setShowActions(flag):
    Settings.setShowActions(flag)

##
# Shows a question-message dialog requesting input from the user.
# @param msg The message to display.
# @param default The preset text of the input field.
# @return The user's input string.
#
def input(msg="", default=""):
    return SikuliScript.input(msg, default)

def capture(*args):
    scr = ScreenUnion()
    if len(args) == 0:
        simg = scr.userCapture()
        if simg:
            return simg.getFilename()
        else:
            return None
    elif len(args) == 1:
        if __builtin__.type(args[0]) is types.StringType or __builtin__.type(args[0]) is types.UnicodeType:
            simg = scr.userCapture(args[0])
            if simg:
                return simg.getFilename()
            else:
                return None
        else:
            return scr.capture(args[0]).getFilename()
    elif len(args) == 4:
        return scr.capture(args[0], args[1], args[2], args[3]).getFilename()
    else:
        return None


def selectRegion(msg=None):
    if msg:
        r = ScreenUnion().selectRegion(msg)
    else:
        r = ScreenUnion().selectRegion()
    if r:
        return Region(r)
    else:
        return None


##
# Switches the frontmost application to the given application.
# If the given application is not running, it will be launched by openApp()
# automatically. <br/>
# Note: On Windows, Sikule searches in the text on the title bar
# instead of the application name.
# @param app The name of the application. (case-insensitive)
#
def switchApp(app):
    return App.focus(app)

##
# Opens the given application. <br/>
# @param app The name of an application if it is in the environment variable PATH, or the full path to an application.
#
def openApp(app):
    return App.open(app)

##
# Closes the given application. <br/>
# @param app The name of the application. (case-insensitive)
#
def closeApp(app):
    return App.close(app)

##
# Sleeps until the given amount of time in seconds has elapsed.
# @param sec The amount of sleeping time in seconds.
def sleep(sec):
    time.sleep(sec)

##
# Shows a message dialog containing the given message.
# @param msg The given message string.
def popup(msg, title="Sikuli"):
    SikuliScript.popup(msg, title)

def exit(code=0):
    SikuliX.cleanUp(code)
    sys.exit(code)

##
# Runs the given string command.
# @param msg The given string command.
# @return Returns the output from the executed command.
def run(cmd):
    return SikuliScript.run(cmd)
    
##
# display some help in interactive mode
def shelp():
    SikuliScript.shelp()
    
def byDistanceTo(m):
    """ Method to compare two Region objects by distance to m. This method is deprecated and should not be used. Use distanceComparator() instead """
    return DistanceComparator(m)

def byX(m):
    """ Method to compare two Region objects by x value. This method is deprecated and should not be used. Use horizontalComparator() instead """
    return m.x

def byY(m):
    """ Method to compare two Region objects by y value. This method is deprecated and should not be used. Use verticalComparator() instead """
    return m.y

def verticalComparator():
    """ Method to compare two Region objects by y value. """
    return VerticalComparator().compare

def horizontalComparator():
    """ Method to compare two Region objects by x value. """
    return HorizontalComparator().compare

def distanceComparator(x, y=None):
    """ Method to compare two Region objects by distance to a specific point. """
    if y is None:
        return DistanceComparator(x).compare # x is Region or Location
    return DistanceComparator(x, y).compare # x/y as coordinates


############### SECRET FUNCTIONS ################

def initSikuli(scr = None):
    dict = globals()
    dict['METHODCATALOG'] = sys.modules[__name__].__dict__
    if scr == None:
        Debug.log(3, "Jython: init SCREEN as ()")
        dict['SCREEN'] = Screen()
    else:
        Debug.log(3, "Jython: init SCREEN as", scr)
        dict['SCREEN'] = Screen(scr) 
    dict['SCREEN']._exposeAllMethods(__name__)


initSikuli()
