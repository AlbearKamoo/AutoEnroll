from splinter import Browser
import urllib.request


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
        data = self.browser.find_by_css('tr[valign="top"][bgcolor="#FFFFCC"')
        for i in data:
            print(i.text)
            course_list.append(i.find_by_css('td'))
        for j in course_list:
            print(j[0].text, end ='   ')
            print(j[-1].text)      

            
##    def __setattr__(self, name, value):
##        if name not in ['browser', 'data']:
##            print("Additional attributes cannot be set for WebSoc objects")
##        else:
##            self.__dict__[name] = value
            
    


test = WebSoc("https://www.reg.uci.edu/perl/WebSoc")
if test.dept_classes('ARTS'):
    if test.submit():
        test.check_courses([1])
            

