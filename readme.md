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