import requests


def generate_info(website, requirements):
    #website = string of webpage
    #requirements = dictionary of the form
    request = requests.post(website,requirements)
    print(request.url)
    with open('download_stuff2.html', 'w') as d:
        d.write(request.content)


#Must fill out all parts of the form in order to interact with a form on HTML
form_requirements = {'YearTerm' : '2016-14',
     'Breadth' : 'ANY',
     'Dept' : 'I&C SCI',
     'CourseNum' : '',
     'Division' : 'ANY',
     'CourseCodes' : '',
     'InstrName' : '',
     'CourseTitle' : '',
     'ClassType' : 'ANY',
     'Units' : '',
     'Days' : '',
     'StartTime' : '',
     'EndTime' : '',
     'FullCourses' : 'ANY',
     'FontSize' : '100',
     'CancelledCourses' : 'Exclude',
     'Bldg' : '',
     'Room' : '',
     }

generate_info("http://www.reg.uci.edu/perl/WebSoc", form_requirements)
