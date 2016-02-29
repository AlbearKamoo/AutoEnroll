from bs4 import BeautifulSoup
from collections import defaultdict
import requests
import itertools
import time
import webreg


class WebSoc:
    def __init__(self, URL: str, dept: str,  courses: [[]], username: str, password: str) -> None:
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
        
        self.URL = URL
        self.data = ''
        self.userdata = (username, password)
        self.courses = courses
        self.course_list = []
        self.enrolled = []

    def get_search_results(self):
        try:
            request = requests.post(self.URL ,self.form_data)
            self.soup = BeautifulSoup(request.content, "html.parser")
            return True
        except:
            return False
        
        
    def check_courses(self) -> None:
        self.course_list = []
        data = self.soup.select('tr[valign="top"]')
        for i in data:
            self.course_list.append(i.select('td'))
        
        self.class_status = defaultdict(str)
        for i in self.course_list:
            if i[0].text in itertools.chain.from_iterable(self.courses):
                print(i[0].text, end ='   ')
                print(i[8].text, end ='  ')
                print(i[-1].text)
                self.class_status[i[0].text] = i[-1].text

        self.enrollment()
                
    def enrollment(self):
        enroll_list = []
        for l in self.courses:
            if self.class_status[l[0]] == 'OPEN':
                if len(l) == 1:
                    enroll_list.append(l)
                for c in range(1, len(l)):
                    if self.class_status[l[c]] == 'OPEN':
                        enroll_list.append(l)
                        break
        print(enroll_list)

        if enroll_list:
            webreg_browser = webreg.login(self.userdata[0], self.userdata[1])
            if webreg_browser.find_by_css('div[class="DivLogoutMsg"]'):
                print("Currently unable to access Webreg. Your account may be in use, or the system may not have updated yet.")
                webreg_browser.quit()
            else:
                self.enroll(enroll_list, webreg_browser)                
                
    def enroll(self, enroll_list, webreg_browser):
        print("enrolling in " + str(enroll_list))
        webreg.enroll(webreg_browser, itertools.chain.from_iterable(enroll_list))
        self.enrolled = enroll_list

    def check_enrolled(self) -> bool:
        for i in self.enrolled:
            if i in self.courses:
                self.courses.remove(i)
        return len(self.courses) == 0
        
if __name__ == "__main__":                      
    test = WebSoc("https://www.reg.uci.edu/perl/WebSoc", "PHILOS", [['30500', '30503'], ['30640']], "#####", "#####")
    try:
        if test.get_search_results():
            for i in range(40):
                test.check_courses()
                time.sleep(10)
                if test.check_enrolled():
                    break
                print('rechecking')
    except Exception as e:
        print(e)

            

