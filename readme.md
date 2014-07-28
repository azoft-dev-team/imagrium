# About #
*Reflectico* is a Jython framework for cross-platform testing of mobile applications basing on the **image recognition** method. The core principles of the framework (which are reflected in its design) are:
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
 
 Before going deeply into the framework guts, I'd like you to watch the following video which outlines the Reflectico abilities:
 
 [![Mobile Test Automation of iOS and Android Applications](http://img.youtube.com/vi/IUJOzHMKZgo/0.jpg)](http://www.youtube.com/watch?v=IUJOzHMKZgo)

  [1]: http://www.sikuli.org/ "Sikuli"
  [2]: http://www.jython.org "Jython"
  [3]: http://ant.apache.org/ "Apache Ant"
  [4]: http://pydev.org/ "PyDev"
  [5]: http://jenkins-ci.org/ "Jenkins"
  [6]: http://www.genymotion.com "Genymotion"
  
 
 