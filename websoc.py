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
        self.dept = dept
        self.enrolled = []
              
        
    def check_courses(self, soup: BeautifulSoup) -> defaultdict(str):
        ''' Iterates through a scraped course list to find courses codes specified in the
        object, building a dictionary with the course codes as keys, and their enrollment
        status as values. Returns this dictionary.

        keyword arguments:
        soup -- parsed result from POST request
        '''

        # Builds available course list using HTML scraping on the soup object
        course_list = []
        data = soup.select('tr[valign="top"]')
        for i in data:
            course_list.append(i.select('td'))

        # Builds the course status dictionary with user specified courses and their status
        # Print statements are curretly for debugging purposes 
        course_status = defaultdict(str)
        for i in course_list:
            if i[0].text in itertools.chain.from_iterable(self.courses):
                print(i[0].text, end ='   ')
                print(i[8].text, end ='  ')
                print(i[-1].text)
                course_status[i[0].text] = i[-1].text

        # Return dictionary of course codes as keys and their availability as values
        return course_status
                
    def get_enroll_list(self, course_status: dict):
        ''' Builds a list of enrollable (OPEN) courses, mainting course/discussion
        relationships through sublists, and returns it.

        keyword arguments:
        class_status -- a dictionary with course codes as keys and their enrollment status as values
        '''

        # Builds a list that cointains courses specified by the user that are open for enrollment
        enroll_list = []
        for l in self.courses:
            if course_status[l[0]] == 'OPEN':
                if len(l) == 1:
                    enroll_list.append(l)
                for c in range(1, len(l)):
                    if course_status[l[c]] == 'OPEN':
                        enroll_list.append(l)
                        break
        print("Courses OPEN for enrollment: "+str(enroll_list)) # Print statement for debugging purposes

        return enroll_list               
                
    def enroll(self, enroll_list, webreg_browser) -> [[str]]:
        ''' Sends enroll requests to the WebReg handler module, retrieving the enrolled courses list.'''
    
        webreg_browser = webreg.login(self.userdata[0], self.userdata[1])
        if webreg_browser.find_by_css('div[class="DivLogoutMsg"]'):
            print("Currently unable to access Webreg. Your account may be in use, or the system may not have updated yet.")
            webreg_browser.quit()
        else:
            print("enrolling in " + str(enroll_list))
            self.enrolled = webreg.enroll(webreg_browser, enroll_list)

    def main_routine(self):
        soup = self.get_POST_results(self.URL, self.form_data)
        if soup.find_all('li')[0].text == "Department: " + self.dept: #Checks if the post request retrieved the right data
            course_status = self.check_courses(soup)
            enroll_list = self.get_enroll_list(course_status)
            if enroll_list:
                self.enroll(enroll_list)          
        else:
            print("POST request failed to retrieve correct data. Please contact an administrator =p")
            

    def check_enrolled(self) -> bool:
        ''' Removes enrolled course from the object's course list.
        Returns True if the course list becomes empty, False otherwise.
        '''
        for i in self.enrolled:
            if i in self.courses:
                self.courses.remove(i)
        return len(self.courses) == 0

def get_POST_results(URL, form_data) -> BeautifulSoup:
    ''' Sends POST request to URL and returns retrived content in parsed form '''
    request = requests.post(URL, form_data)
    soup = BeautifulSoup(request.content, "html.parser")
    return soup
        
if __name__ == "__main__":
    # Test routine to be used when this module is executed independently
    # Hashtags are username and passwords fields
    dept = "PHILOS"
    test = WebSoc(dept, [['30500', '30503'], ['30640']], "#####", "#####")
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

            

