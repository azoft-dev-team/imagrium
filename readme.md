# About #
*Reflectico* is a Jython framework for cross-platform testing of mobile applications basing on the **image recognition** method (and distributed under the MIT License terms). The core principles of the framework (which are reflected in its design) are:
> Share test code base between platforms. 

In other words, a functional test should be agnostic about an app platform, it should run both on Android and iOS. 

 > Decouple resources from logic. 
 
The tools which provide the common API for different OSes typically do one of the following:
A. Implement middleware which translates common requests into OS-specific commands or 
B. use image-recognition technologies to identify UI elements and act on them.
Although I'm a great fan of the first approach, the implementations were way too buggy and unpolished back in 2012 pushing me to write something different. 

The second (image-based) approach is normally implemented as a record-and-replay tool. These tools are nice when you record tests from scratch, but later on the code base becomes enormously hard to maintain as these tools wrap images into tests. Given you have a new design/UX (new images for the most of UI elements), you have to shovel all the tests updating images. Soon it becomes unclear what is less costly - a manual testing round or a code update. That is why I added the *PageObject pattern* into the framework as it decouples resources (images) from operations a user performs on these resources.

 > Allow for CI support and convenient code debugging. 

This project stands on the shoulders of giants: [Sikuli][1] for actions on images, the [Jython][2] unittest library for running tests, and [Apache Ant][3] for test running and reporting, all wrapped into a [PyDev][4] project. You can use it as a template to write your own pages and tests, and of course you can run/debug it in Eclipse (in my view Eclipse is better than Sikuli IDE as it provides tools for collaboration, refactoring, debugging).
What's more, the framework is designed to be seamlessly integrated into [Jenkins][5], so that you can simply attach a worker with emulators and necessary SDKs installed and run an ant script to perform testing and collect results.

> Guarantee the same initial system state for all tests.

I borrowed the idea about independence of test cases run from jUnit as it eases the process of running tests in parallel or performing selective runs. One more thing to consider was handling of failed tests. I wanted a simple way to bring the system back to the initial state regardless of the test execution status (say, if a test failed somewhere in the middle). For this I used emulator snapshots on Android and the simulator reset feature on iOS.

> Ensure the mobile OS emulator responds in reasonable time.

I'm happy with the speed of the iOS simulator which comes with Xcode, but I cannot say the same for the Android out-of-the-box emulator. I had hopes for HAXM and x86 images provided by Intel, but their problem is that they do not provide Google API which is used in the majority of apps my company develops. Only the 4.4 image ships this API, but unfortunately it does not work as stable as I expect. That's why the current version of Reflectico uses [Genymotion][6] and VirtualBox to create and manipulate snapshots.


----------


If you share these principles and considering between frameworks which use them, I'd recommend you to give Reflectico a chance to become your testing automation tool.

# Quick Demo #
 
 Before going deeply into the framework guts, I'd like you to watch the following video which showcases the Reflectico abilities.
 This video demonstrates iOS and Android test runs of the same app called **HopHop**.

 [![Mobile Test Automation of iOS and Android Applications](http://img.youtube.com/vi/IUJOzHMKZgo/0.jpg)](http://www.youtube.com/watch?v=IUJOzHMKZgo)

# Installation #

(1) Clone the git repo to the directory of your liking (versions for Win x64 and MacOS are available in the *win* and *ios* branches respectively).
 
(2) Install [JDK 1.7.0\_55+][7]. The **JAVA_HOME** environment varialbe should be correctly set.
 
(3) **(win)** If you wish to use Reflectico for Windows, make sure the following software is installed and configured:

- Install [VirtualBox 4.2+][8]. 

- Include the bin directory of VirtualBox in your PATH environment variable (otherwise, the `vboxmanage` utility will not be found).
- Install [Genymotion 2.2+][9].
- Include the genymotion in your PATH environemnt variable (we need this to run the `player` utility).
- Install [Android SDK][10].
- Include the platform-tools directory in your PATH environemnt variable (we need this to use the `adb` utility).
- Install [Tesseract OCR][11].
- Install [Apache Ant][12].


----------

(3) **(mac)** If you wish to use Reflectico for MacOS, make sure the following software is installed and configured:

- [ios-sim][13]. Use [npm][14], [brew][15], or other ways to install it (visit the project and read the related docs). We use this utility to launch apps in the simulator.

- We use the Apple Script snippets to reset and rotate the Simulator, so copy the `reset` and `rotateScreen` scripts from the `scripts` directory in the repo root to the place where you can execute them.

- Ensure the user who launches the test run has a permission to execute these scripts (if this is your current user, run  <code>chmod +x reset rotateScreen </code>).

- **IMPORTANT!** Run `reset` and `rotateScreen` directly from *Terminal* under the user who will later run tests. Accept the pop-ups asking the permission to manipulate the system through the Terminal app.

We're done with installing things, let's configure the system.
          
# Configuration (Bare Minimum) #
Before running tests, you need to configure the system by providing paths to the app under test and accompanying scripts, simulator name, port, and other misc settings.

The sample config files are kept in the `conf` directory within the repo root. Provide the appropriate values for the following parameters to fit your needs.

## Configuration of Android/Win ##

This minimum info should be correctly substituted with your values in `conf/android_settings.conf`:

[OS]

`emulatorAvdName`. String. The name of your Genymotion emulator (preferrably without spaces). If you do not have it, create one.
Example: 
emulatorAvdName = and-4.2-hdpi_1

`emulatorName`. String. The device name of the emulator (the output of the `adb devices` command when the emulator is launched). Usually the name is the IP address and port pair. 
Example: 
emulatorName = 169.254.215.108:5555

----------

[App]

`shortname`. String. The *package* name in your manifest file.
Example:
shortname = mobi.hophop

`name`. String. The name of the launch activity.
Example:
name = mobi.hophop/.ui.activities.SplashActivity

`file`. String. The absolute path to the apk file. For testing purposes, you may grab the HopHop apk [here][16].
Example:
file = C:\tmp\apps\HopHop-debug-1.1.6.2407-11072014-1541.apk

----------

[Page]

`launchPageClass`. String. The Jython class of the page which should be initially launched (if this confuses you, please read more about how Reflectico works with pages). In other words, it is the start point for the app (the class which represents the first page after the app launch).
Example:
launchPageClass = src.pages.auth.auth\_page\_uselocation.AuthPageLocation

## Configuration of iOS ##

This minimum info should be correctly substituted with your values in `conf/ios_settings.conf`:

[SSH_ACCESS]

`serverUrl`. String. The user and host which will be used for running tests. **IMPORTANT**: You must preliminarily add the user's public key to the `authorized_keys` file on the host to allow the authorization by key for this user (without entering any passwords). To check that the auth by key works, simply try to log in to the host by firing `ssh user@host`
Example: 
serverUrl = helpadmin@172.16.0.173

----------

[App]

`appAbsolutePath`. String. The path to the app directory (here we suppose that you already have an Xcode build for simulator). You can use [the HopHop app][17] for testing purposes.
Example:
appAbsolutePath = /Users/Shared/apps/myEvents.app

`launchLocation`. String. The absolute path to a directory, to which the app files will be copied (and from which the `ios-sim` will launch the app).
Example: 
launchLocation = /Users/Shared/appsRun

`appName`. String. The application name.
Example:
appName = myEvents.app

`appResetScript`. String. The absolute path to the script which resets the simulator data and settings. Must be executable by a user who runs tests.
Example:
appResetScript = /Users/Shared/scripts/reset

`appRotateScript`. String. The absolute path to the script which rotates the simulator. Must be executable by a user who runs tests.
Example:
appRotateScript = /Users/Shared/scripts/rotateScreen

`iosSimPath`. String. The absolute path to the app launching utility. Check that the correct path is provided.
Example:
iosSimPath = /usr/local/bin/ios-sim

Once you're done with the settings, you can run the tests.

# How to Run Tests #
If you've decided to use the demo app (HopHop) and configured the basic parameters, you should be able to run the sample test on Android+win/iOS+mac simulators or both.

To do it, locate the git repo root from the command line and run:

`ant`

The system will start preparing the snapshot giving the valuable output on the progress to the stdout. If the test has passed at least a couple of steps, your system is correctly configured, and you can use it to write tests for your own apps.
**Congratulations!**

If you look in the related `build.xml` file, you'll notice what actually happens there. The test case run start point is the `run.py` file in the root directory of the project. it requires the config file as the first and the only one input parameter. Additionally, it requires some Sikuli dependencies to be added to the PATH and CLASSPATH environment variables (this should not be so important for Eclipse as long as you use the ready project file). So basically the ant runs

`run.py conf/android_settings.conf`

spiced up by some context.

**P.S.** If you wish to dig line by line to understand the guts of the system, start from `run.py`.

# How to Write Tests #
## About Pages ##
After the demo app test runs as charm, you generally would like to write some tests for your own app. It's time to do it!

The code you'll typically write when creating tests for an app can be divided into two groups: **Pages** and **Tests**. A *test* in this grouping is a sequence of operations on certain pages, for example:
``` python
authPage = AuthPage.load(AppLauncher.box, self.settings)
fbAuthPage = authPage.signUpFb()
fbAuthPage.fillEmail(self.settings.get("Facebook", "email"))
fbAuthPage.fillPassword(self.settings.get("Facebook", "password"))
fbConfirmPage = fbAuthPage.login()
LobbyPage = fbConfirmPage.confirm() 
```
As we can read from the snippet, the test first loads the *Authorization* page, then follows from it to the *Facebook Authorization* page, fills in the necessary data to log in, confirms the user, and finally loads the *Lobby* page. In other words, it just surfs through pages and performs requested operations, leaving all juicy details on how to do this to pages.

Thus, you'll get the 80% of success once you understand how to create pages. Hopefully, this is not that hard:)

A *page* is a Jython presentation of an app page/screen/activity. Technically it is a class with fields and methods to operate on these fields.

The most complex page looks as follows: 
``` python
class FbAuthPage(Page):

    email = ResourceLoader([Resource.fbEmailFieldiOS, Resource.fbEmailFieldiOS_ru])
    password = ResourceLoader([Resource.fbPasswordFieldiOS, Resource.fbPasswordFieldiOS_ru])
    actionLogin = ResourceLoader([Resource.fbLoginBtniOS, Resource.fbLoginBtniOS_ru])
        
    def __init__(self, box, settings):
        super(FbAuthPage, self).__init__(box, settings)
        
        self.email = self.box
        self.password = self.box
        self.actionLogin = self.box
        
        self.settings = settings
        self.waitPageLoad()

        self.checkIfLoaded(['email', 'password'])
        
    def fillEmail(self, text):
        self.email.click()
        self.waitPageLoad()
        self.inputText(text)
```
It actually uses almost all the sweeties of Reflectico, so let's discuss them one by one.
## Field Definition and Localization ##
Let's start from this line:
``` python
    email = ResourceLoader([Resource.fbEmailFieldiOS, Resource.fbEmailFieldiOS_ru])
```
The snippet associates a page field (in our case, the email input field) with one of the graphic assets (images or text labels). Here we provide two resources - one for English and one for Russian language. When a page requests the input field, the system will try to sequentially find one of these resources and will stop after the first success.

By convention, app resources are kept under the `res` directory in the repo root. You may call them directly, like this, 
``` python
    email = ResourceLoader("res/pages/ios/fb_auth/fbEmailFieldiOS.png")
```
or something like this:
``` python
    email = ResourceLoader(["res/pages/ios/fb_auth/fbEmailFieldiOS.png", "res/pages/ios/fb_auth/fbEmailFieldiOS_ru.png"])
```

but for maintenance convenience the Resource class keeps resource paths mapping.

**Brief summary**: If you want to manipulate a page field (an icon, a label, an input, or something else), first create a page class and define the field using the `ResourcesLoader` instance.

## Fields Initialization and Check-up ##
... and we continue with stumbling on our feature-rich page (the `FbAuthPage` class)
First to note, it is **necessary to inherit each page from the Page class**.
``` python
class FbAuthPage(Page):
```
as it enables some neat page-generic stuff like the method for waiting till a page loads.


Another mandatory rule is to **call the parent constructor** on the page initialization.

``` python
    def __init__(self, box, settings):
        super(FbAuthPage, self).__init__(box, settings)
```

The last peculiarity is that we normally want to limit the screen area where the system will search for a resource.
... and normally we do it by these lines:
``` python        
        self.email = self.box
        self.password = self.box
```
The box parameter itself is initially calculated shortly after the snapshot is started but before launching the app under test (the system does this under the hood). The parameter defines the borders of the emulator/simulator by finding the horizontal line and vertical line and calculating the rectangle basing on these two values. 

**IMPORTANT 1**: If you see something like the *"Unable to get the simulator frame"* error while running the tests, you need to make sure the horizontal and vertical borders present on the screen (see respective images in `res/pages/android/hdpi/core` or `res/pages/ios/core` and update them as necessary to fit your emulator presentation).

**IMPORTANT 2**: The system searches for resources only on the first display (Screen 0), so it may not find the emulator frame if you have the emulator on a different display.

This rectange is kept in the `AppLauncher.box` class field, so you can use it in tests, for instance.

In some exotic cases you may want to locate an element beyond the emulator frame (say, a hardware button). In this casejust don't assign anything to the fields on the page initialization.

As soon as you have fields at hands, you may need to verify that they actually present in the page. Looking at this under a different angle, this is the only way for you to verify that the loaded page is the one you actually need. For this verification, use the following one-liner:

``` python
self.checkIfLoaded(['email', 'password'])
```

Note that not all fields are necessarily visible on the page launch, specify only those that are visible.

If the system does not find all the fields, it will throw the *AssertionError* exception which ends the test with a failure (and of course say some swear words to stdout).

**Brief summary**: If you want the system to find elements within the emulator borders, assign the elements to `self.box`. It is a good practice to identify the page by its elements using `self.checkIfLoaded()`.

## Attributes and Methods of a Field ##
If you looked attentively at the `FbAuthPage` code, you could notice this line:
``` python
self.email.click()
```
Actually each field is a Sikuli [Match][18] object which exposees the corresponding methods and attributes. You can do whatever the specification says with page fields (in our example, we click the element).

## Access to Configuration ##
In the code snippet of the `FbAuthPage` class, we can see this line:
``` python
self.settings = settings
```
The `settings` attribute is a [ConfigParser][19] instance associated with the current configuration file (with which you launch your tests, either *android\_settings.conf* or *ios\_settings.conf*), so you can work with it using the standard methods like `get()`.

Example: 
``` python
self.settings.get("Facebook", "email")
```
This instance is passed from page to page.

## OS-Dependent Functions ##
Eventually you'll need to enter a text, emulate the Back hardware button on Android or do some other OS-specific work. In the `FbAuthPage` class we used the `inputText()` method to enter the text, but it is not found either in the class or in its parent classes. 

Instead, it is included into the parent mixin of OS-dependent pages. To be more precise:

for iOS (as `iOSPage`) ...
``` python
class FbAuthPageiOS(FbAuthPage, iOSPage):
    pass
```
and for Android (as `AndroidPage`)...
``` python
class FbAuthPageAndroidHdpi(FbAuthPage, AndroidPage):
```
**Brief summary**: to use OS-dependent functions like text enter, add the corresponding classes into your OS-dependent pages. 

## Pages Organization ##
Now you know almost everything you need about pages, the last question is how to correctly load pages and navigate between them.

To make things easy to maintain, Reflectico offers the specifically formatted organization of classes which represent pages. The big idea of this organization is to let the system decide which exactly page to load (iOS or Android page? which density? for which version?) when one page tries to load another page (by the `load()` method). The system makes this decision examining the configuration file, the [OS] section.

The classes organization has the following two levels connected by a child-parent dependency:

 1. A *generic* page which contains all the common page logic (the `FbAuthPage` class in our example). It has implementations of all methods and default fields (like `email`, `password`, or `fillEmail()`). The methods are deemed to perform the same operations on iOS and Android (filling a form in our example).
 
 2.  OS-dependent pages declare resource deviations (OS-specific colors, UI widgets, sizes, etc.). These pages must have specifically-formatted names:
 * An iOS page **is required** to be named **[GENERIC PAGE NAME] + "iOS"**, example: `FbAuthPageiOS`. This class must inherit from the generic page (`FbAuthPage`).

 * An Android page presentation depends on two factors - density and OS version. First, the system tries to load the **[GENERIC PAGE NAME] + "\_" +"[MAJOR VER]" + "\_"+"MINOR\_VER" + "Android" + "SCREEN\_DENSITY"** class. Example: `FbAuthPage_4_2_AndroidHdpi`. If it didn't find the class, it tries the Android-generic class pattern: **[GENERIC PAGE NAME] + "Android" + "SCREEN\_DENSITY"**. For example: `FbAuthPageAndroidhdpi`.

If a system fails to find a page class, it throws an AssertionError exception with the text: *Could not find the page from configuration, please add it*.

Here how it looks like in practice:

In a test (fragment)...
``` python
fbAuthPage = authPage.signUpFb()
```
In the generic page class for `authPage`...
``` python
def signUpFb(self):
    self.actionAgreeTermsBtniOS.click()
    self.actionSignUpFb.click()
    return FbAuthPage.load(self.box, self.settings)

```
and `load()` is a system page-wide method which decides on a page to actually load depending on the run configuration (`FbAuthPageiOS` or `FbAuthPageAndroidHdpi`).


**Brief summary**: The page load mechanism unveils the common way of thinking when creating pages. **First, create a generic page, add all necessary logic, and then expand it according to your needs**. When you complete creating the pages for a new platform/density, run the same test with a different configuration, and the system does all the heavy lifting for you.

# Tutorial: The Hello, World! Project #
The given above information is enough to write test code, but to wire up all these details into a clear picture, I offer you a small tutorial which writes a test from the grounds up.

First of all, the PyDev project setup for dummies. Skip it if you know how to do it. I use Eclipse 4.3, check specs for other versions though I think the steps should be similar.

## 1. Set Up the PyDev Project ##

### 1.1. Add the project to workspace ###
Start from **File** > **Import** > **Git** > **Projects from git** and providing these details:
![Provide the repo settings][20]

During the wizard, specify the project destination inside your workspace:
![Add the path within your workspace][21]

Click **Next** like hell and **Finish** in the end.

The sad news is that this wizard will fail to complete (crash-boom-bang). The good news is that it has created the directory and cloned the code into it, so we only need to create a new project associated with the code.

Do it by running **File** > **PyDev Project**. In the form that opens specify _Jython_ as the interpreter. The interpreter executable (`jython.jar`) is found in the `env/` directory within the project root, you need to provide it when configuring the project interpreter.

**Note**: I add the pysrc package as I believe it serves for debugging purposes, so please add it too.

![The interpreter settings][22]

This time it creates the project we need, but it reports the problem with the interpreter. Go to **Properties** (right-click the project root) > **PyDev - Interpreter/Grammar** and provide the interpreter you've just configured. Again :)

### 1.2. Add a Run Configuration ###

Check that Eclipse uses the x64 JVM by navigating to **Window** > **Preferences** > **Java** > **Installed JREs** (the x64 version must be given in bold).

Create a Run Configuration by navigating to **Run options (the arrow next to the green icon with a triangle)** > **Run Configurations**. Click **Jython run** and provide these parameters:

![Run configuration parameters][23]

... and in the **Arguments**, specify the config file you'll use:

![enter image description here][24]

Click **Run**. Weeee! I've created your first project! Good work so far! 

Enough for buttons and windows! Let's get busy with coding!

  [1]: http://www.sikuli.org/ "Sikuli"
  [2]: http://www.jython.org "Jython"
  [3]: http://ant.apache.org/ "Apache Ant"
  [4]: http://pydev.org/ "PyDev"
  [5]: http://jenkins-ci.org/ "Jenkins"
  [6]: http://www.genymotion.com "Genymotion"
  [7]: http://www.oracle.com/technetwork/java/javase/downloads/jdk7-downloads-1880260.html
  [8]: https://www.virtualbox.org/wiki/Downloads
  [9]: http://www.genymotion.com "Genymotion"
  [10]: http://developer.android.com/sdk/index.html
  [11]: https://code.google.com/p/tesseract-ocr/ "Tesseract OCR"
  [12]: http://ant.apache.org/ "Apache Ant"
  [13]: https://github.com/phonegap/ios-sim
  [14]: https://www.npmjs.org/
  [15]: http://brew.sh/
  [16]: https://drive.google.com/file/d/0B0RtsuDjIW5BQ0ZVYUNVQlZqMms/edit?usp=sharing
  [17]: https://drive.google.com/file/d/0B0RtsuDjIW5BdFJma3lVSTdmT0k/edit?usp=sharing
  [18]: http://doc.sikuli.org/match.html
  [19]: https://docs.python.org/2/library/configparser.html
  [20]: http://i.imgur.com/6zpDrDr.png "Create a git project dialog"
  [21]: http://i.imgur.com/Ro3VwAf.png
  [22]: http://i.imgur.com/vSuFKLH.png
  [23]: http://i.imgur.com/fI0x6P6.png
  [24]: http://i.imgur.com/GYLWqFm.png