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
        if browser.find_by_value("Logout"):
            browser.find_by_value("Logout").first.click()
        browser.quit()
        print("Success")
        return True

def enroll(browser, courselist):
    print(courselist)
    enroll_list = []
    browser.find_by_css('input[value = "Enrollment Menu"]').first.click()
    for i in range(len(courselist)):
        enroll_list.append([])
        for courseId in courselist[i]:
            browser.choose('mode', 'add')
            browser.fill("courseCode", courseId)
            browser.find_by_css('input[value = "Send Request"]').first.click()
            if browser.find_by_css('table[class="studyList"]'):
                enroll_list[i].append(courseId)
                
    browser.find_by_value("Logout").first.click()
    browser.quit()
    print("enrolled in: " +str(enroll_list))
    return enroll_list


if __name__ == '__main__':
    b = login('####################','#################')
    enroll(b, ["21020","21021"])
