import requests, re
import urllib3.contrib.pyopenssl
from requests.auth import HTTPBasicAuth

#have to do this to handle HTTPS correctly
urllib3.contrib.pyopenssl.inject_into_urllib3()

class Legacy:

    def __init__(self) -> None:


def login(username,password):

    login_info = {'ucinetid' : username,
                  'password' : password,
                  'submit_type' : '',
                  'login_button' : 'Login',
                  'referer' : 'http%253A%252F%252Fwebreg1.reg.uci.edu%253A8889%252Fcgi-bin%252Fwramia%253Fpage%253DstartUp%2526call%253D',
                  'return_url' : 'http%253A%252F%252Fwebreg1.reg.uci.edu%253A8889%252Fcgi-bin%252Fwramia%253Fpage%253Dlogin%253Fcall%253D'}
    session = requests.Session()

    session.headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36'}

    #begin automated login set up
    session.get('http://www.reg.uci.edu/cgi-bin/webreg-redirect.sh')
    login_request = session.get('http://webreg4.reg.uci.edu:8889/cgi-bin/wramia?page=startUp&call=')

    that_sweet_redirect = re.search(r"\"0; url=(.*?)>", login_request.content)
    url = that_sweet_redirect.group(0)[8:-2]

    #Use this to help use locate the 4 digits ex: 0012
    that_young_login = re.search(r"/wramia(.*?)&",url)
    session_id = 'http://webreg1.reg.uci.edu:8889/cgi-bin' + that_young_login.group(0)[-5:-1]

    #This is part of the form we submit to login
    login_info['return_url'] = 'http%253A%252F%252Fwebreg1.reg.uci.edu%253A8889%252Fcgi-bin%252Fwramia%253Fpage%253Dlogin%253Fcall%253D' + session_id

    #logs me in bruh
    get_auth_link = session.post(url, data=login_info, allow_redirects=False)
    regex_link = re.search(r"\"0;url=(.*?)\"", get_auth_link.content)
    login_confirmation_redirect = regex_link.group(0)[7:-1]

    #let's <>ing go into the log in page
    session.get(login_confirmation_redirect)

    #To remove the '&'
    session_link = re.search(r"http(.*?)&", login_confirmation_redirect)[-1]

    #digits are gonna be important if we want to access menus
    return session, session_id, session_link
"""
    for c in courses:
        enrollment_info = {'value' : 'add',
                           'courseCode' : c,
                           'gradeOption' : '',
                           'varUnits' : '',
                           'authCode' : ''}

        time_to_enroll = session.post('http://webreg2.reg.uci.edu:8889/cgi-bin/wramia', enrollment_info)
        logout = session.post('http://webreg2.reg.uci.edu:8889/cgi-bin/wramia', {'value' : 'exit'})

    print(logout.url)
"""

def enrollment(courselist, session, session_id, session_link):
     #click Enrollment Button
     enroll_button = {'page' : 'enrollQtrMenu',
                      'mode' : 'enrollmentMenu',
                      'call' : session_id,
                      'submit' : 'Enrollment Menu'}

     session.post(session_link, data=enroll_button)

     for class_id in courselist:
        join_class = {'page' : 'enrollmentMenu',
                      'call' : session_id,
                      'mode' : 'add',
                      'button' : 'Send Request',
                      'courseCode' : class_id,
                      'gradeOption' : '',
                      'varUnits' : '',
                      'authCode' : '',
                      'courseCode' : ''}
        session.post('zzz')




session, session_id, session_link = login('##############','####################')

enrollment([],session, session_id,session_link)