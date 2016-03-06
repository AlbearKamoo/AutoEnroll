## Overview
AutoEnroll is an application that aims to aid UCI students in the somewhat obtuse enrollment process that the university offers. Sometimes students simply aren't able to enroll at their given enrollment times, or maybe there is a desired class that's full but has no waitlist, forcing the student to be constantly checking the system for an opening. AutoEnroll solves these problems and offers a quick and intuitive way to add classes without constant worry.

## Program Capabilities
#### Features:
- Automated enrollment for multiple classes in the same program instance
- Preservation of lecture/discussion/lab course relationships
- Enrollment time option to adhere to enrollment windows and non-prime time enrollment
- Email option that notifies users of successfull enrollment

#### Limitations:
- Only enrolls in classes of one department per program instance
- Enrollment time option is limited to the 24h of the day it is set on
- If too many users utilize the email service, some emails may not get sent out or received
- May be too intensive on the UCI servers

## Development History
My partner [WhatsEmo](https://github.com/WhatsEmo) and I initially started this project on a whim to see if we could monitor and automatically enroll in a desired course once seats opened up. As such, our first version of AutoEnroll was very rudimentary. We started building the program using Python and a tool called [Splinter](https://splinter.readthedocs.org/en/latest/) which literaly simulated button clicks and form entries on an active browser window. Many problems arose with this setup. The WebSoc browser window had to be active for as long as the program was running. Once a desired course was found to be open, a new window would launch, possibily disrupting the user's use of the computer. Not to mention how inneficient and memory/processor intensive it was.

Unsatisfied, we decided to take up the challenge of fully automizing the program without relying on browser programs. We began to read up on HTTP, something that we had barely come across during our time in college. Over the span of a weekend we became familiar with POST and GET requests and how responses, cookies and authentication worked. Continuing with Python, we dropped the splinter module and began to rely on the [Requests](http://docs.python-requests.org/en/master/) package to mediate our form submissions and responses. Our new version applied HTML scraping to the WebSoc response using [BeautifulSoup](http://www.crummy.com/software/BeautifulSoup/) to retrieve course data. This data was sent to the webreg module that would handle login/logouts and submit forms for course enrollment.

Somewhere throghout this process I decided to implement a GUI to faciliate navigation. I used the [PyQt](https://riverbankcomputing.com/software/pyqt/intro) framework since I was already familiar with it, and quickly had a basic interface set up. This new addition led us to go back and refactor a bunch of our code, improving its workflow and strengthening its object-orientedness. Lastly, I whipped up an executable using [PyInstaller](http://www.pyinstaller.org/) in case we ever want to distribute the program to others who don't have Python on their machines. 

Our current version is comprised of the GUI module, the legacy module (an improved version of the old webreg module that uses Session objects) and the websoc module. Features we have recently added are enrollment time configuration and email notification options. Looking forward we might add other enrollment capabilites such as dropping courses and waitlist handling, provided we decide to continue developing the program (enrollment season is going to end soon!).
