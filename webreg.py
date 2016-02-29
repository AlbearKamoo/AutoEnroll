from splinter import Browser


def login(username, password):
    browser = Browser('chrome')
    browser.visit('https://www.reg.uci.edu/cgi-bin/webreg-redirect.sh')
    browser.fill('ucinetid', username)
    browser.fill('password', password)
    browser.find_by_name('login_button').click()
    return browser

def login_check(browser):
    if("UCInetID Secure Web Login" ==  browser.title):
        print("Invalid Login")
        browser.quit()
        return False
    else:
        print("Success")
        return True

def enroll(browser, courselist):
    if login_check(browser):
        browser.find_by_css('input[value = "Enrollment Menu"]').first.click()
        for courseId in courselist:
            browser.choose('mode', 'add')
            browser.fill("courseCode", courseId)
            browser.find_by_css('input[value = "Send Request"]').first.click()
        browser.find_by_value("Logout").first.click()
        browser.quit()


if __name__ == '__main__':
    b = login('####################','#################')
    enroll(b, ["21020","21021"])
