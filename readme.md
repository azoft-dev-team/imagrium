About
------
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

This project stands on the shoulders of giants: Sikuli for actions on images, the Jython unittest library for running tests, and Apache Ant for test running and reporting, all wrapped into a PyDev project. You can use it as a template to write your own pages and tests, and of course you can run/debug it in Eclipse (in my view Eclipse is better than Sikuli IDE as it provides tools for collaboration, refactoring, debugging).