from splinter import Browser


def loginIn(username, password):
    browser = Browser('chrome')
    browser.visit('https://www.reg.uci.edu/cgi-bin/webreg-redirect.sh')
    browser.fill('ucinetid', username)
    browser.fill('password', password)
    browser.find_by_name('login_button').click()
    return browser


def enroll(browser, listofClasses):
    if("UCInetID Secure Web Login" ==  browser.title):
        print("Invalid Login")
        browser.quit()
    else:
        print("Success")
        browser.find_by_name('Enrollment Menu').click()
        for courseID in listofClasses:
            browser.fill("<################>", courseID)
            browser.find_by_name('<###############>').click()



b = loginIn('username','password')

enroll(b)