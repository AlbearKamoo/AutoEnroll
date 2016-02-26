from splinter import Browser
import time
import urllib.request
import urllib.parse
import requests


class WebSoc:
    def __init__(self, URL: str) -> None:
        self.browser = Browser('chrome')
        self.browser.visit(URL)
        self.data = ''

    def dept_classes(self, department: str) -> bool:
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

    def check_courses(self, courses: dict):
        course_list = []
        data = self.browser.find_by_css('tr[valign="top"]')
        for i in data:
            course_list.append(i.find_by_css('td'))
        for j in course_list:
            if j[0].text in courses:
                print(j[0].text, end ='   ')
                print(j[9].text, end ='  ')
                print(j[-1].text)      

            
##    def __setattr__(self, name, value):
##        if name not in ['browser', 'data']:
##            print("Additional attributes cannot be set for WebSoc objects")
##        else:
##            self.__dict__[name] = value
            
    



test = WebSoc("https://www.reg.uci.edu/perl/WebSoc")
if test.dept_classes('I&C SCI'):
    if test.submit():
        for i in range(5000):
            test.check_courses(['36680','36681', '36691' ])
            time.sleep(5)
            test.browser.reload()
            print('reloaded')
test.browser.quit()

##values = {"Dept": "ARTS"}
##data = urllib.parse.urlencode(values)
##data = data.encode('ascii')
##request = urllib.request.Request("https://www.reg.uci.edu/perl/WebSoc", data)
##with (urllib.request.urlopen(req)) as response:
##        result = response.readlines()
##for i in result:
##    print(i)

            

