from splinter import Browser


class WebSoc:
    def __init__(self, URL: str) -> None:
        self.browser = Browser()
        self.browser.visit(URL)

    def dept_classes(self, department: str) -> bool:
        try:
            self.browser.select('Dept', department)
            return True
        except Exception as e:
            print(e)
            return False

    def submit(self) -> None:
        button = self.browser.find_by_name('Submit')[1]
        button.click()


test = WebSoc("https://www.reg.uci.edu/perl/WebSoc")
if test.dept_classes('ARTS'):
    test.submit()
