from splinter import Browser
from collections import defaultdict
import itertools
import time
import urllib.request
import urllib.parse
import requests



class WebSoc:
    def __init__(self, URL: str) -> None:
        self.browser = Browser('chrome')
        self.browser.visit(URL)
        self.data = ''
        self.courses = [[]]
        self.course_list = []
        self.enrolled = []

    def dept_classes(self, department: str, courses: [[str]]) -> bool:
        self.courses = courses
        try:
            self.browser.select('Dept', department)
            return True
        except Exception as e:
            print(e)
            return False

    def submit(self) -> bool:
        try:
            button = self.browser.find_by_name('Submit')[0]
            button.click()
            return True
        except Exception as e:
            print(e)
            return False
        
    def check_courses(self) -> None:
        self.course_list = []
        data = self.browser.find_by_css('tr[valign="top"]')
        for i in data:
            self.course_list.append(i.find_by_css('td'))
        
        self.class_status = defaultdict(str)
        for i in self.course_list:
            if i[0].text in itertools.chain.from_iterable(self.courses):
                print(i[0].text, end ='   ')
                print(i[9].text, end ='  ')
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

        self.enroll(enroll_list)                
                
    def enroll(self, enroll_list):
        self.enrolled = []
        for i in enroll_list:
            print("enrolling in " + str(i))
            self.enrolled.append(i)

    def check_enrolled(self) -> None:
        for i in self.enrolled:
            if i in self.courses:
                self.courses.remove(i)
        print(self.courses)
                      

test = WebSoc("https://www.reg.uci.edu/perl/WebSoc")
try:
    if test.dept_classes('I&C SCI', [['36450','36451'],['36691'], ['36630']]):
        if test.submit():
            for i in range(5000):
                test.check_courses()
                time.sleep(10)
                test.check_enrolled()
                test.browser.reload()
                print('reloaded')
except Exception as e:
    print(e)
test.browser.quit()

            

