from bs4 import BeautifulSoup
from collections import defaultdict
import requests
import itertools


class WebSoc:
    ''' Class that handles interactions with UCI's Schedule of Classes interface. '''
    
    def __init__(self, dept: str) -> None:
        ''' Initiates WebSoc object with approriate fields

        keyword arguments:
        dept -- a string representing the user's chosen department
        courses -- nested lists of strings containing course codes and lecture/discussion relationships
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
        self.courses = courses
        self.dept = dept

        # Internal object attributes with default values
        self.URL = "https://www.reg.uci.edu/perl/WebSoc"
              
        
    def get_course_status(self, courses: []) -> defaultdict(str):
        ''' Iterates through a scraped course list to find courses codes specified in the
        object, building a dictionary with the course codes as keys, and their enrollment
        status as values. Returns this dictionary.
        '''
        course_status = defaultdict(str)
        soup = get_POST_as_soup(self.URL, self.form_data)
        if soup.find_all('li')[0].text == "Department: " + self.dept:
            # Builds available course list using HTML scraping on the soup object
            course_list = []
            data = soup.select('tr[valign="top"]')
            for i in data:
                course_list.append(i.select('td'))
                
            # Builds the course status dictionary with user specified courses and their status
            for i in course_list:
                if i[0].text in itertools.chain.from_iterable([x.get_course_as_list() for x in self.courses]):
                    course_status[i[0].text] = i[-1].text
        else:
            print("POST request failed to retrieve correct data. Please contact an administrator =p")
            
        # Return dictionary of course codes as keys and their availability as values
        return course_status

    def get_enroll_list(self) -> [[str]]:
        ''' Builds a list of enrollable (OPEN) courses, mainting course/discussion
        relationships through sublists, and returns it.

        keyword arguments:
        class_status -- a dictionary with course codes as keys and their enrollment status as values
        '''
        course_status = self.get_course_status()
        enroll_list = []
        if course_status:
            # Builds a list that cointains courses specified by the user that are open for enrollment
            for l in self.courses:
                if course_status[l.lecture_code] == 'OPEN':
                    if l.auxiliary_codes:
                        for c in l.auxiliary_codes:
                            if course_status[c] == 'OPEN':
                                enroll_list.append(l)
                                break
                    else:
                        enroll_list.append(l)                                  
                    
        print("Courses OPEN for enrollment: "+str(enroll_list)) # Print statement for debugging purposes
        
        return enroll_list 

    # Overloaded method with an external course dictionary         
    def get_enroll_list(self, course_status: dict) -> [[str]]:
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

def get_POST_as_soup(URL, form_data) -> BeautifulSoup:
    ''' Sends POST request to URL and returns retrived content in parsed form '''
    request = requests.post(URL, form_data)
    soup = BeautifulSoup(request.content, "html.parser")
    return soup
        
if __name__ == "__main__":
    # Test routine to be used when this module is executed independently
    # Hashtags are username and passwords fields
    dept = "PHILOS"
    test = WebSoc(dept)
    try:
        soup = get_POST_results(test.URL, test.form_data)
        if soup.find_all('li')[0].text == "Department: " + dept:
            for i in range(40):
                test.check_courses(soup)
                if test.check_enrolled():
                    break
                print('rechecking')
    except Exception as e:
        print(e)

            

