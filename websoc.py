from bs4 import BeautifulSoup
from collections import defaultdict
import requests
import itertools
import time
import webreg


class WebSoc:
    ''' Class that handles interactions with UCI's Schedule of Classes interface. '''
    
    def __init__(self, dept: str,  courses: [[]], username: str, password: str) -> None:
        ''' Initiates WebSoc object with approriate fields

        keyword arguments:
        dept -- a string representing the user's chosen department
        courses -- nested lists of strings containing course codes and lecture/discussion relationships
        username -- the user's UCINetID
        password -- the user's UCINet password
        '''

        # Dictionary containing HTML form data for POST request
        self.form_data = {'YearTerm' : '2016-14',
         'Breadth' : 'ANY',
         'Dept' : dept,
         'CourseNum' : '',
         'Division' : 'ANY',
         'CourseCodes' : '',
         'InstrName' : '',
         'CourseTitle' : '',
         'ClassType' : 'ANY',
         'Units' : '',
         'Days' : '',
         'StartTime' : '',
         'EndTime' : '',
         'FullCourses' : 'ANY',
         'FontSize' : '100',
         'CancelledCourses' : 'Exclude',
         'Bldg' : '',
         'Room' : '',
         }

        # Object attributes assigned to initialization input
        self.userdata = (username, password)
        self.courses = courses

        # Internal object attributes with default values
        self.URL = "https://www.reg.uci.edu/perl/WebSoc"
        self.data = ''
        self.course_list = []
        self.enrolled = []

    def get_search_results(self) -> BeautifulSoup:
        ''' Sends POST request to URL and returns retrived content in parsed form '''
        request = requests.post(self.URL, self.form_data)
        soup = BeautifulSoup(request.content, "html.parser")
        return soup
        
        
    def check_courses(self, soup: BeautifulSoup) -> None:
        ''' Iterates through a course list to find courses codes specified by the user, 
        building a dictionary with the course codes as keys, and their enrollment satus
        as values. Calls the enrollment method after this process is complete.

        keyword arguments:
        soup -- parsed result from POST request
        '''

        # Build the available course list using HTML scraping on the soup object
        self.course_list = []
        data = soup.select('tr[valign="top"]')
        for i in data:
            self.course_list.append(i.select('td'))

        # Builds the course status dictionary with user specified courses and their status
        # Print statements are curretly for debugging purposes 
        class_status = defaultdict(str)
        for i in self.course_list:
            if i[0].text in itertools.chain.from_iterable(self.courses):
                print(i[0].text, end ='   ')
                print(i[8].text, end ='  ')
                print(i[-1].text)
                class_status[i[0].text] = i[-1].text

        # Call to enrollment method
        self.enrollment(class_status)
                
    def enrollment(self, class_status: dict):
        ''' Builds a list of enrollable (OPEN) courses, later calling the enroll method on
        those courses. Stores a list of succesfully enrolled courses as an object attribute.

        keyword arguments:
        class_status -- a dictionary with course codes as keys and their enrollment status as values
        '''

        # Builds a list that cointains courses specified by the user that are open for enrollment
        enroll_list = []
        for l in self.courses:
            if class_status[l[0]] == 'OPEN':
                if len(l) == 1:
                    enroll_list.append(l)
                for c in range(1, len(l)):
                    if class_status[l[c]] == 'OPEN':
                        enroll_list.append(l)
                        break
        print(enroll_list) # Print statement for debugging purposes

        # If there are enrollable courses, send enroll list to enroll method
        # Retrieve a list of successfully enrolled courses as an attribute
        if enroll_list:
            webreg_browser = webreg.login(self.userdata[0], self.userdata[1])
            if webreg_browser.find_by_css('div[class="DivLogoutMsg"]'):
                print("Currently unable to access Webreg. Your account may be in use, or the system may not have updated yet.")
                webreg_browser.quit()
            else:
                self.enrolled = self.enroll(enroll_list, webreg_browser)                
                
    def enroll(self, enroll_list, webreg_browser) -> [[str]]:
        ''' Sends enroll requests to the WebReg handler module, retrieving the enrolled courses list. '''
        # Print statement for debuggin purposes
        print("enrolling in " + str(enroll_list))
        return webreg.enroll(webreg_browser, enroll_list)

    def check_enrolled(self) -> bool:
        ''' Removes enrolled course from the object's course list.
        Returns True if the course list becomes empty, False otherwise.
        '''
        for i in self.enrolled:
            if i in self.courses:
                self.courses.remove(i)
        return len(self.courses) == 0
        
if __name__ == "__main__":
    # Test routine to be used when this module is executed independently
    # Hashtags are username and passwords fields
    dept = "PHILOS"
    test = WebSoc(dept, [['30500', '30503'], ['30640']], "mautran", "defence123")
    try:
        soup = test.get_search_results()
        if soup.find_all('li')[0].text == "Department: " + dept:
            for i in range(40):
                test.check_courses(soup)
                time.sleep(10)
                if test.check_enrolled():
                    break
                print('rechecking')
    except Exception as e:
        print(e)

            

