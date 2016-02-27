from splinter import Browser


def login(username, password):
    browser = Browser('chrome')
    browser.visit('https://www.reg.uci.edu/cgi-bin/webreg-redirect.sh')
    browser.fill('ucinetid', username)
    browser.fill('password', password)
    browser.find_by_name('login_button').click()
    return browser


def enroll(browser, courselist):
    if("UCInetID Secure Web Login" ==  browser.title):
        print("Invalid Login")
        browser.quit()
    else:
        print("Success")
        browser.find_by_css('input[value = "Enrollment Menu"]').first.click()
        for courseId in courselist:
            browser.choose('mode', 'add')
            browser.fill("courseCode", courseId)
            browser.find_by_css('input[value = "Send Request"]').first.click()
        browser.find_by_value("Logout").first.click()




b = login('####################','#################')

enroll(b, ["21020","21021"])