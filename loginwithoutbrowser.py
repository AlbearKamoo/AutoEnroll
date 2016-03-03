import requests, re
import urllib3.contrib.pyopenssl
from requests.auth import HTTPBasicAuth

#have to do this to handle HTTPS correctly
urllib3.contrib.pyopenssl.inject_into_urllib3()

def login(username,password,courses):

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

    that_young_login = re.search(r"/wramia(.*?)&",url)
    i_am_big_boy_login = 'http://webreg1.reg.uci.edu:8889/cgi-bin' + that_young_login.group(0)
    print(i_am_big_boy_login) # needs Auth token


    login_info['return_url'] = 'http%253A%252F%252Fwebreg1.reg.uci.edu%253A8889%252Fcgi-bin%252Fwramia%253Fpage%253Dlogin%253Fcall%253D' + i_am_big_boy_login[-5:-1]

    print(url)
    #logs me in bruh
    session.post(url, data=login_info, allow_redirects=False)
    #let's <>ing go into the log in page
    i_am_big_boy_login = i_am_big_boy_login + 'ucinetid_auth='+ session.cookies['ucinetid_auth']
    s = session.get(i_am_big_boy_login)


    with open('zzz.html', 'w') as f:
        f.write(s.content)

    for c in courses:
        enrollment_info = {'value' : 'add',
                           'courseCode' : c,
                           'gradeOption' : '',
                           'varUnits' : '',
                           'authCode' : ''}

        time_to_enroll = session.post('http://webreg2.reg.uci.edu:8889/cgi-bin/wramia', enrollment_info)
        logout = session.post('http://webreg2.reg.uci.edu:8889/cgi-bin/wramia', {'value' : 'exit'})

    print(logout.url)


login('zzzzzzzzzzzzzzzzzzzz','zzzzzzzzzzzzzzzzz',['36420', '36424'])