import requests, re
from requests.auth import HTTPBasicAuth


class Legacy:
    def __init__(self, username: str, password: str) -> None:
        '''
        :param username: str that is a user's ID
        :param password: str that is user's password
        :param courselist: [str] of desired classes to enroll in
        :return: Nothing
        '''
        self.username = username
        self.password = password
        self.session_id = ''
        self.session_link = ''
        self.session = requests.Session()
        self.session_token = ''

        #tells us which menu we're in so we can log out properly
        self.which_menu = ''

        #define base link
        self.logout_link = ''

        self.enrolled_classes = []

    def login(self) -> bool:
        '''
            This method will be used to log the user into webreg and obtain a session object
            that will be used to navigate through WebReg
        :return: Nothing
        '''

        print('Start Login')

        login_info = {'ucinetid' : self.username,
                    'password' : self.password,
                    'submit_type' : '',
                    'login_button' : 'Login',
                    'referer' : 'http%253A%252F%252Fwebreg1.reg.uci.edu%253A8889%252Fcgi-bin%252Fwramia%253Fpage%253DstartUp%2526call%253D',
                     'return_url' : 'http%253A%252F%252Fwebreg1.reg.uci.edu%253A8889%252Fcgi-bin%252Fwramia%253Fpage%253Dlogin%253Fcall%253D'}

        self.session.headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36'}

        #begin automated login set up
        self.session.get('http://www.reg.uci.edu/cgi-bin/webreg-redirect.sh')
        login_request = self.session.get('http://webreg4.reg.uci.edu:8889/cgi-bin/wramia?page=startUp&call=')

        that_sweet_redirect = re.search(r"\"0; url=(.*?)>", str(login_request.content))
        url = that_sweet_redirect.group(0)[8:-2]

        #Use this to help use locate the 4 digits ex: 0012
        that_young_login = re.search(r"/wramia(.*?)&",url)
        self.session_id = that_young_login.group(0)[-5:-1]

        #This is part of the form we submit to login
        login_info['return_url'] = 'http%253A%252F%252Fwebreg1.reg.uci.edu%253A8889%252Fcgi-bin%252Fwramia%253Fpage%253Dlogin%253Fcall%253D' + self.session_id

        #logs me in bruh
        get_auth_link = self.session.post(url, data=login_info, allow_redirects=False)

        regex_link = re.search(r"\"0;url=(.*?)\"", str(get_auth_link.content))

        #First check.
        if(regex_link is None):
            print('Login failed: You need to correct login information')
            return False
        login_confirmation_redirect = regex_link.group(0)[7:-1]

        #To remove the '&'
        #something like: http://webreg4.reg.uci.edu:8889/cgi-bin/wramia?page=login?call=####
        self.session_link = re.match(r"http(.*?)&", login_confirmation_redirect).group(0)[:-1]
        print("Use this link if program failed to logout: " + self.session_link)

        self.logout_link = re.match(r"(.*?)wramia", self.session_link).group(0)

        #let's <>ing go into the log in page
        self.landing_page = self.session.get(login_confirmation_redirect)
    
        #Checks if user is logged in
        #IF ucinetid_auth cookie is given to us
        if(self.session.cookies.__contains__('ucinetid_auth')):

            #Now check if ucinetid_auth that is given to us isn't a "no_key" value
            #or if the ucinetid_auth is not equal to the current session_token (that would mean we didn't finish a log in)
            if(self.session.cookies['ucinetid_auth'] != 'no_key' and self.session.cookies['ucinetid_auth'] != self.session_token):
                self.session_token = self.session.cookies['ucinetid_auth']
                print('Finished Login')
                return True

        print('Login Failed')
        self.session_link = ''
        return False

    def enroll(self, course_list: []) -> []:
        '''
        Starting from the WebReg Main Menu:
            User will be entering Enrollment Menu and this will register for user's specified classes
        :return: Nothing
        '''
        #tells us which menu we're in so we can log out properly
        print('Start Enrollment...')
        self.enrolled_classes = []

        #This self variables are given in the login() method. If it is empty that means user hasn't logged in
        if(self.session_link == ''):
            print('You never logged on.')
            return

        self.which_menu = 'enrollmentMenu'

        #click Enrollment Button
        enroll_button = {'page' : 'enrollQtrMenu',
                         'mode' : 'enrollmentMenu',
                         'call' : self.session_id}

        print('Enrolling')
        x = self.session.post(self.session_link, data=enroll_button)
        for course in course_list:

            #Use this variable to check if we wanna add the course to the "enrolled class list"
            is_enrolled = False

            join_class = {'page' : 'enrollmentMenu',
                          'call' : self.session_id,
                          'mode' : 'add',
                          'button' : 'Send Request',
                          'courseCode' : course.lecture_code,
                          'gradeOption' : '',
                          'varUnits' : '',
                          'authCode' : ''}
            enrollment_response = self.session.post(self.session_link, join_class)

            #checks if we successfully enrolled in the lecture
            if('studyList' in str(enrollment_response.content)):
                print('Successfully Enrolled In Lecture : ' + course.lecture_code)
                if(len(course.auxiliary_codes) == 0):
                    is_enrolled = True

            for discussion_code in course.auxiliary_codes:
                join_class = {'page' : 'enrollmentMenu',
                              'call' : self.session_id,
                              'mode' : 'add',
                              'button' : 'Send Request',
                              'courseCode' : discussion_code,
                              'gradeOption' : '',
                              'varUnits' : '',
                              'authCode' : ''}
                enrollment_response = self.session.post(self.session_link, join_class)

                #checks if we successfully enrolled in the discussion
                if('studyList' in str(enrollment_response.content)):
                    is_enrolled = True
                    print('Successfully Enrolled In Discussion : ' + course.lecture_code)
                    break

            if(is_enrolled):
                self.enrolled_classes.append(course)

        return self.enrolled_classes
        print('Enrollment Complete')

    def logout(self) -> None:
        '''
        Logs the user out. YOU MUST CALL THIS METHOD EVERYTIME
        enrollmentMenu
        enrollQrtMenu
        waitlistMenu
        :return: Nothing
        '''
        print('Logging Out....')
        #This self variables are given in the login() method. If it is empty that means user hasn't logged in
        if(self.session_link == ''):
            print('You never logged on.')
            return

        #use this to help post the log out
        #Tried using a dictionary, but it didn't work
        logout_hyperlink = self.logout_link + "?page="+ self.which_menu + "&mode=exit&call=" + self.session_id + "&submit=Logout"
        self.session.post(logout_hyperlink)
        print('Successfully Logged Out')


    def waitlist(self) -> None:
        '''
        Probably never gonna do this.
        :return:
        '''

        #tells us which menu we're in so we can log out properly
        self.which_menu = 'waitlistMenu'


    #Have to be Courses Class
    def remove_enrolled_courses(self, courses: []) -> []:
        for classes in self.enrolled_classes:
            if classes in courses:
                courses.remove(classes)
        return courses

if __name__ == '__main__':
    legacy = Legacy('#####', '#####')
    legacy.login()
    legacy.logout()
