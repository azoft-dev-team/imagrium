# Copyright 2010-2013, Sikuli.org
# Released under the MIT License.
# modified RaiMan 2013

import inspect
import types
import sys

from org.sikuli.script import Screen as JScreen
from org.sikuli.basics import Debug
from Region import *

class Screen(Region):
    def __init__(self, id=None):
        try:
            if id != None:
                r = JScreen.getBounds(id)
                s = JScreen.getScreen(id)
            else:
                id = JScreen.getPrimaryId()
                r = JScreen.getBounds(id)
                s = JScreen.getScreen(id)
            (self.x, self.y, self.w, self.h) = (int(r.getX()), int(r.getY()), \
                            int(r.getWidth()), int(r.getHeight()))
            self.initScreen(s)
        except:
            Debug.log(3, "Jython: init: exception while initializing Screen\n%s", sys.exc_info(0))
            sys.exit(1)

    @classmethod
    def getNumberScreens(cls):
        return JScreen.getNumberScreens()

    def resetROI(self):
        self.setRect(self.getScreen().getBounds())

    def getBounds(self):
        return self.getScreen().getBounds()

    def selectRegion(self, msg=None):
        if msg:
            r = self.getScreen().selectRegion(msg)
        else:
            r = self.getScreen().selectRegion()
        if r:
            return Region(r)
        else:
            return None

    ##
    # Enters the screen-capture mode asking the user to capture a region of
    # the screen if no arguments are given.
    # If any arguments are specified, capture() automatically captures the given
    # region of the screen.
    # @param *args The args can be 4 integers: x, y, w, and h, a <a href="org/sikuli/script/Match.html">Match</a> object or a {@link #Region} object.
    # @return The path to the captured image.
    #
    def capture(self, *args):
        scr = self.getScreen()
        if len(args) == 0:
            simg = scr.userCapture("Select an image")
            if simg:
                return simg.getFile()
            else:
                return None
        elif len(args) == 1:
            if isinstance(args[0], (types.StringType, types.UnicodeType)):
                simg = scr.userCapture(args[0])
                if simg:
                    return simg.getFile()
                else:
                    return None
            else:
                return scr.capture(args[0]).getFile()
        elif len(args) == 4:
            return scr.capture(args[0], args[1], args[2], args[3]).getFile()
        else:
            return None

    def _exposeAllMethods(self, mod):
        exclude_list = [ 'class', 'classDictInit', 'clone', 'equals', 'finalize',
                        'getClass', 'hashCode', 'notify', 'notifyAll',
                        'toGlobalCoord', 'toString', 'getLocationFromPSRML', 'getRegionFromPSRM',
                       'capture', 'selectRegion', 'create', 'observeInBackground', 'waitAll',
                        'updateSelf', 'findNow', 'findAllNow', 'getEventManager']
        dict = sys.modules[mod].__dict__
        for name in dir(self):
            if name in exclude_list: continue
            try:
                if not inspect.ismethod(getattr(self,name)): continue
            except:
                continue
            if name[0] != '_' and name[:7] != 'super__':
                dict[name] = eval("self."+name)
                if name == 'checkWith': Debug.log(3, "%s %s", name, str(dict[name])[1:])

    def toString(self):
        return self.getScreen().toString()

