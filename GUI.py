import sys
from time import sleep
from datetime import datetime, time
from collections import defaultdict
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from course import Course
import sender
import websoc
import webreg
import legacy


# Dictionary containing WebSoc string representations as keys, and the corresponding form data as values
dept_dict = {"AC ENG . . . . . .Academic English and ESL (started 2012 Fall)" : "AC ENG",
"AFAM . . . . . . . African American Studies" : "AFAM",
"ANATOMY . . . .Anatomy and Neurobiology" : "ANATOMY",
"ANESTH . . . . . Anesthesiology" : "ANESTH",
"ANTHRO . . . . . Anthropology" : "ANTHRO",
"ARABIC . . . . . .Arabic" : "ARABIC",
"ART . . . . . . . . .Art (started 2013 Fall)" : "ART",
"ART HIS . . . . . .Art History" : "ART HIS",
"ART STU . . . . . Art (until 2013 FSm)" : "ART STU",
"ARTS . . . . . . . Arts" : "ARTS",
"ARTSHUM . . . . Arts and Humanities" : "ARTSHUM",
"ASIANAM . . . . Asian American Studies" : "ASIANAM",
"BATS . . . . . . . Biomedical and Translational Science (started 2012 Fall)" : "BATS",
"BIO SCI . . . . . .Biological Sciences" : "BIO SCI",
"BIOCHEM . . . . Biological Chemistry" : "BIOCHEM",
"BME . . . . . . . . Biomedical Engineering" : "BME",
"BSEMD . . . . . .Bio Sci & Educational Media Design (started 2011 Fall)" : "BSEMD",
"CAMPREC . . . .Campus Recreation" : "CAMPREC",
"CBEMS . . . . . .Chemical Engr and Materials Science" : "CBEMS",
"CEM . . . . . . . . Community and Environmental Medicine" : "CEM",
"CHC/LAT . . . . . Chicano/Latino Studies" : "CHC/LAT",
"CHEM . . . . . . .Chemistry" : "CHEM",
"CHINESE . . . . .Chinese" : "CHINESE",
"CLASSIC . . . . .Classics" : "CLASSIC",
"CLT&THY . . . . .Culture & Theory" : "CLT&THY",
"COM LIT . . . . . Comparative Literature" : "COM LIT",
"COMPSCI . . . . Computer Science" : "COMPSCI",
"CRITISM . . . . . Criticism" : "CRITISM",
"CRM/LAW . . . . Criminology, Law and Society" : "CRM/LAW",
"CSE . . . . . . . . Computer Science and Engineering" : "CSE",
"DANCE . . . . . . Dance" : "DANCE",
"DERM . . . . . . .Dermatology" : "DERM",
"DEV BIO . . . . . Developmental and Cell Biology" : "DEV BIO",
"DRAMA . . . . . .Drama" : "DRAMA",
"E ASIAN . . . . . East Asian Languages and Literatures" : "E ASIAN",
"EARTHSS . . . . Earth System Science" : "EARTHSS",
"ECO EVO . . . . Ecology and Evolutionary Biology" : "ECO EVO",
"ECON . . . . . . . Economics" : "ECON",
"ED AFF . . . . . .Educational Affairs (Sch of Med)" : "ED AFF",
"EDUC . . . . . . . Education" : "EDUC",
"EECS . . . . . . . Electrical Engineering &amp; Computer Science" : "EECS",
"EHS . . . . . . . . Environmental Health Sciences (started 2013 Fall)" : "EHS",
"ENGLISH . . . . .English" : "ENGLISH",
"ENGR . . . . . . . Engineering" : "ENGR",
"ENGRCEE . . . .Engineering, Civil and Environmental" : "ENGRCEE",
"ENGRMAE . . . .Engineering, Mechanical and Aerospace" : "ENGRMAE",
"ENGRMSE . . . .Chemical Engr and Materials Science (grads)" : "ENGRMSE",
"ENVIRON . . . . .Environmental Health, Science, and Policy (until 2011 Spg)" : "ENVIRON",
"EPIDEM . . . . . .Epidemiology" : "EPIDEM",
"ER MED . . . . . Emergency Medicine" : "ER MED",
"EURO ST . . . . .European Studies" : "EURO ST",
"FAM MED . . . . Family Medicine" : "FAM MED",
"FLM&MDA . . . .Film and Media Studies" : "FLM&MDA",
"FRENCH . . . . . French" : "FRENCH",
"GEN&SEX . . . . Gender and Sexuality Studies (started 2014 Fall)" : "GEN&SEX",
"GERMAN . . . . .German" : "GERMAN",
"GLBLCLT . . . . .Global Cultures" : "GLBLCLT",
"GREEK . . . . . . Greek" : "GREEK",
"HEBREW . . . . .Hebrew" : "HEBREW",
"HINDI . . . . . . . .Hindi" : "HINDI",
"HISTORY . . . . .History" : "HISTORY",
"HUMAN . . . . . .Humanities" : "HUMAN",
"HUMARTS . . . . Humanities and Arts" : "HUMARTS",
"I&C SCI . . . . . . Information and Computer Science" : "I&C SCI",
"IN4MATX . . . . . Informatics" : "IN4MATX",
"INT MED . . . . . Internal Medicine" : "INT MED",
"INTL ST . . . . . . International Studies" : "INTL ST",
"ITALIAN . . . . . .Italian" : "ITALIAN",
"JAPANSE . . . . Japanese" : "JAPANSE",
"KOREAN . . . . .Korean" : "KOREAN",
"LATIN . . . . . . . Latin" : "LATIN",
"LAW . . . . . . . . Law" : "LAW",
"LINGUIS . . . . . .Linguistics" : "LINGUIS",
"LIT JRN . . . . . . Literary Journalism" : "LIT JRN",
"LPS . . . . . . . . .Logic and Philosophy of Science" : "LPS",
"M&MG . . . . . . .Microbiology and Molecular Genetics" : "M&MG",
"MATH . . . . . . . Mathematics" : "MATH",
"MED . . . . . . . . Medicine (started 2011 Spg)" : "MED",
"MED ED . . . . . Medical Education" : "MED ED",
"MGMT . . . . . . .Management" : "MGMT",
"MGMT EP . . . . Executive MBA" : "MGMT EP",
"MGMT FE . . . . Fully Employed MBA" : "MGMT FE",
"MGMT HC . . . . Health Care MBA" : "MGMT HC",
"MGMTMBA . . . Management MBA" : "MGMTMBA",
"MGMTPHD . . . .Management PhD" : "MGMTPHD",
"MIC BIO . . . . . .Microbiology" : "MIC BIO",
"MOL BIO . . . . . Molecular Biology and Biochemistry" : "MOL BIO",
"MPAC . . . . . . .Accounting (started 2013 SS1)" : "MPAC",
"MUSIC . . . . . . .Music" : "MUSIC",
"NET SYS . . . . .Networked Systems" : "NET SYS",
"NEURBIO . . . . .Neurobiology and Behavior" : "NEURBIO",
"NEUROL . . . . . Neurology" : "NEUROL",
"NUR SCI . . . . . Nursing Science" : "NUR SCI",
"OB/GYN . . . . . Obstetrics and Gynecology" : "OB/GYN",
"OPHTHAL . . . . Ophthalmology" : "OPHTHAL",
"PATH . . . . . . . Pathology and Laboratory Medicine" : "PATH",
"PED GEN . . . . Pediatrics Genetics" : "PED GEN",
"PEDS . . . . . . . Pediatrics" : "PEDS",
"PERSIAN . . . . .Persian" : "PERSIAN",
"PHARM . . . . . .Medical Pharmacology" : "PHARM",
"PHILOS . . . . . .Philosophy" : "PHILOS",
"PHRMSCI . . . . Pharmaceutical Sciences" : "PHRMSCI",
"PHY SCI . . . . . Physical Science" : "PHY SCI",
"PHYSICS . . . . .Physics" : "PHYSICS",
"PHYSIO . . . . . .Physiology and Biophysics" : "PHYSIO",
"PLASTIC . . . . . Plastic Surgery (started 2014 Fall)" : "PLASTIC",
"PM&R . . . . . . .Physical Medicine and Rehabilitation" : "PM&R",
"POL SCI . . . . . Political Science" : "POL SCI",
"PORTUG . . . . . Portuguese" : "PORTUG",
"PP&D . . . . . . . Planning, Policy, and Design" : "PP&D",
"PSY BEH . . . . .Psychology and Social Behavior" : "PSY BEH",
"PSYCH . . . . . . Cognitive Sciences" : "PSYCH",
"PUB POL . . . . .Public Policy (started 2013 Wtr)" : "PUB POL",
"PUBHLTH . . . . Public Health" : "PUBHLTH",
"RAD SCI . . . . . Radiological Sciences (until 2012 Spg)" : "RAD SCI",
"RADIO . . . . . . .Radiology" : "RADIO",
"REL STD . . . . . Religious Studies" : "REL STD",
"ROTC . . . . . . . Reserve Officers' Training Corps (started 2011 Fall)" : "ROTC",
"RUSSIAN . . . . .Russian" : "RUSSIAN",
"SOC SCI . . . . . Social Science" : "SOC SCI",
"SOCECOL . . . . Social Ecology" : "SOCECOL",
"SOCIOL . . . . . .Sociology" : "SOCIOL",
"SPANISH . . . . .Spanish" : "SPANISH",
"SPPS . . . . . . . Social Policy & Public Service (started 2016 Wtr)" : "SPPS",
"STATS . . . . . . .Statistics" : "STATS",
"SURGERY . . . .Surgery" : "SURGERY",
"TAGALOG . . . . Tagalog" : "TAGALOG",
"TOX . . . . . . . . .Toxicology" : "TOX",
"UCDC . . . . . . . UC Washington DC (started 2011 Fall)" : "UCDC",
"UNI AFF . . . . . .University Affairs" : "UNI AFF",
"UNI STU . . . . . .University Studies" : "UNI STU",
"VIETMSE . . . . .Vietnamese" : "VIETMSE",
"VIS STD . . . . . .Visual Studies" : "VIS STD",
"WOMN ST . . . . Women's Studies (until 2014 SS2)" : "WOMN ST",
"WRITING . . . . . Writing" : "WRITING"}

class Main(QWidget):
     ''' Main GUI platform for handling auto enrollment configuration and launch. '''
     
     def __init__(self, username, password):
          ''' Initiates the Main window and builds its layout.

          keyword arguments:
          username -- user's UCINetID
          password -- user's UCINet password
          '''
          
          super().__init__()

          # Stores user information and initialiazes internal attributes
          self.username = username
          self.password = password
          self.course_count = 0
          self.input_list = []
          self.checkbox_list = []
          self.course_list = []
          self.discussions = defaultdict(QLineEdit)

          # Grid layout setup
          self.grid = QGridLayout()
          self.setLayout(self.grid)

          # Widget setup
          course_list = list(dept_dict.keys())
          course_list.sort()
          self.dept_combo = QComboBox(self)
          self.dept_combo.addItems(course_list)

          self.dept_label = QLabel("Select Department: ")
          self.dept_label.setAlignment(Qt.AlignRight)
          
          self.add_class_button = QPushButton("Add class")
          self.add_class_button.setFixedWidth(110)
          self.enroll_button = QPushButton("Start bot")
          self.enroll_button.setFixedWidth(120)

          self.time_check = QCheckBox("Set enrollment time")
          self.email_check = QCheckBox("Email me if enrollment is successful")

          self.enroll_time = QTimeEdit()
          self.enroll_time.hide()
          
          # Events and signals
          self.enroll_button.clicked.connect(self.enroll)
          self.add_class_button.clicked.connect(self.add_course)
          self.time_check.stateChanged.connect(self.time_layout_handler)

          # Adds Widgets to Grid
          self.grid.addWidget(self.dept_label, 0, 0)
          self.grid.addWidget(self.dept_combo, 0, 1, 1, 4)
          self.grid.addWidget(self.add_class_button, 1, 2)
          self.grid.addWidget(self.email_check, 1, 3, 1, 2)
          self.grid.addWidget(self.time_check, 2, 0)
          self.grid.addWidget(self.enroll_time, 2, 1)
          self.grid.addWidget(self.enroll_button, 2, 4)
          

          # Sets window's properties
          self.setWindowTitle("AutoEnroll")
          self.setGeometry(400, 400, 500, 200)
          self.grid.setColumnMinimumWidth(3, 120)
          self.grid.setColumnMinimumWidth(4, 120)
          self.grid.setContentsMargins(20, 10, 10, 5)
          

     def add_course(self) -> None:
          ''' Adds a text field for course code and a discussion checkbox as a row in the layout '''

          # Attribute for tracking row number (number of class fields added)
          self.course_count += 1

          # widget setup
          self.course_label = QLabel("Class " + str(self.course_count)+": ")
          self.course_label.setAlignment(Qt.AlignRight)
          self.course_input = QLineEdit()
          self.course_input.setMaxLength(5)
          self.discussion_check = QCheckBox("Discussions/Labs?")
          self.discussion_check.stateChanged.connect(self.discussion_layout_handler) 
          
          # Adding widgets to layout
          self.grid.addWidget(self.course_label, self.course_count, 0)
          self.grid.addWidget(self.course_input, self.course_count, 1, 1, 1)
          self.grid.addWidget(self.discussion_check, self.course_count, 2, 1, 1)

          # Shifts Widgets at the bottom two rows further down
          self.grid.removeWidget(self.time_check)
          self.grid.removeWidget(self.enroll_time)
          self.grid.removeWidget(self.add_class_button)
          self.grid.removeWidget(self.email_check)
          self.grid.removeWidget(self.enroll_button)
          self.grid.addWidget(self.time_check, self.course_count + 2, 0)
          self.grid.addWidget(self.enroll_time, self.course_count +2, 1)
          self.grid.addWidget(self.add_class_button, self.course_count + 1, 2)
          self.grid.addWidget(self.email_check, self.course_count + 1, 3, 1, 2)
          self.grid.addWidget(self.enroll_button, self.course_count + 2, 4)
          

          # Stores input field and checkbox into their respective object lists
          self.input_list.append(self.course_input)
          self.checkbox_list.append(self.discussion_check)

     def discussion_layout_handler(self) -> None:
          ''' Hides or shows text field for discussion course codes according to checkbox status'''
          
          try:
               # Gets position of the checkbox that sent the signal
               index = self.grid.indexOf(self.sender())
               position = self.grid.getItemPosition(index)
               # Hides or shows LineEdit object at the corresponding row according to the sender's status
               if self.sender().isChecked():
                    # If object is already in dict, call show, otherwise create object and add to dict
                    if position[0] in self.discussions.keys():
                         self.discussions[position[0]].show()
                    else:
                         discussion_input = QLineEdit()
                         self.grid.addWidget(discussion_input, position[0], position[1] + 1, 1, 2)
                         self.discussions[position[0]] = discussion_input
               else:
                    self.discussions[position[0]].hide()
          except Exception as e:
               print(e)

     def time_layout_handler(self) -> None:
          ''' Hides or shows TimEdit field for enrollment time setting according to checkbox status'''
          if self.sender().isChecked():
               self.enroll_time.show()
          else:
               self.enroll_time.hide()
               

     def enroll(self) -> None:
          ''' Retrieves a list that represents course codes and lecture/discussion dependencies.
          Later sends this list to a WebSoc handler object, and calls the object's main course
          checking routine. This routine executes until all courses are successfully enrolled
          in, or until the user terminates the app.
          '''
          
          # Gets a list of lists of course codes from a helper method
          course_list = self.build_course_list()

          # Gets the department form value using the user's selected department as the key for the global department dictionary
          dept = dept_dict[str(self.dept_combo.currentText())]

          # gets the enrollment time from the QTimeEdit field as a datetime object
          enroll_datetime = QTime_to_datetime(self.enroll_time)

          print("Department selected: "+dept)
          print("Courses specified by user: ")
          for c in course_list:
               print(c)
          
          try:
               # Initiates WebSoc handler object with enrollment list and user data
               websoc_bot = websoc.WebSoc(dept)
               webreg_bot = legacy.Legacy(self.username, self.password)
               self.close() # Closes Main window and leaves bot running in background

               # MAIN ROUTINE: continously checks course status until course list is empty
               while enroll_bot.check_enrolled() == False:
                    if self.time_check.isChecked() == False or datetime.now() > enroll_datetime:
                         enroll_bot.main_routine()
                         sleep(10)
                         print('Rechecking')
                         if self.email.isChecked() and enroll_bot.enrolled:
                              message = ''
                              for ld in enroll_bot.enrolled:
                                   for c in ld:
                                        message += "Successfully enrolled in " + c + "\n"
                              mailbot = sender.default_sender()
                              mailbot.send_email(message, self.username +"@uci.edu", 'AutoEnroll Notification')
                    else:
                         print("Enrollment is set to begin at "+self.enroll_time.text())
                         sleep(60)
                    
          except Exception as e:
              print(e)
              self.close()

     def build_course_list(self) -> [Course]:
          ''' Condenses all the user inputs into a list of Course objects and returns it. '''
          course_list = []
          for i in range(len(self.input_list)):
               lecture = self.input_list[i].text().strip()
               
               course_codes = []
               course_codes.append(lecture)

               index = self.grid.indexOf(self.input_list[i])
               position = self.grid.getItemPosition(index)
               if position[0] in self.discussions.keys() and self.checkbox_list[i].isChecked():
                    discussion_input = self.discussions[position[0]].text().split(',')
                    course_codes.extend([x.strip() for x in discussion_input])

               if _check_input(course_codes):
                    course_list.append(Course(course_codes))
          return course_list

def _check_input(courses: [str]) -> bool:
     ''' Checks course codes to see if they are strings representing five digit numbers.
     Returns True if all the codes in the list pass the check, False otherwise. '''
     
     try:
          for c in courses:
               int(c)
               assert len(c) == 5, "Course code "+c+" is of the wrong length."
          return True
     except Exception as e:
         print("Invalid course input. All course codes must be five digit numbers.")
         print(e)
         return False

class LoginWindow(QWidget):
     ''' Initial GUI app window for handling user login input and authentication. '''
     
     def __init__(self):
          ''' Initiates the Login window and builds its layout. '''
          
          super().__init__()

          # Grid layout setup
          grid = QGridLayout()
          self.setLayout(grid)

          # Widget setup
          self.title_label = QLabel("Login")
          self.title_label.setAlignment(Qt.AlignCenter)
          
          self.username_label = QLabel("UCINetID: ")
          self.username_input = QLineEdit()
          
          self.password_label = QLabel("Password: ")
          self.password_input = QLineEdit()
          self.password_input.setEchoMode(QLineEdit.Password)

          self.OK_button = QPushButton("OK")

          self.warning_label = QLabel("NOTE: When OK is pressed a quick login test will start.\nPlease wait until the test is finished to continue!")

          # Button events
          self.OK_button.clicked.connect(self.submit)

          # Adds Widgets to Grid
          grid.addWidget(self.title_label, 0, 0, 1, 3)
          grid.addWidget(self.username_label, 1, 0)
          grid.addWidget(self.username_input, 1, 1, 1, 2)
          grid.addWidget(self.password_label, 2, 0)
          grid.addWidget(self.password_input, 2, 1, 1, 2)
          grid.addWidget(self.OK_button, 3, 2)
          grid.addWidget(self.warning_label, 4, 0, 2, 3)

     def submit(self) -> None:
          ''' Submits user input to a login check. If check passes, the Main window is
          intiated and the Login window is closed. Alerts the user if the check failed. '''
          
          # Try/except block for debugging purposes, may remove later
          username = str(self.username_input.text())
          password = str(self.password_input.text())
          try:
               browser = webreg.login(username, password)
               if webreg.login_check(browser):
                    # Starts main window and brings it to the front. Closes login window
                    self.main_window = Main(username, password)
                    self.main_window.show()
                    self.main_window.activateWindow()
                    self.close()
               else:
                    QMessageBox.about(self, "Invalid login", "The username and password combination you have entered is invalid. Please try again.")
          except Exception as e:
               print(e)

def QTime_to_datetime(qtime: QTimeEdit) -> datetime:
     ''' Helper funcion that converts a Qt.QTime object into a Python datetime object. '''
     time_string = qtime.text()
     hour_minute = time_string[:5].split(':')
     hours = int(hour_minute[0])
     minutes = int(hour_minute[1])
     if 'AM' in time_string:
          t = time(hours, minutes)
     else:
          t = time(hours + 12, minutes)
               
     d = datetime.now().date()

     return datetime.combine(d, t)
     

if __name__ == '__main__':
     app = QApplication(sys.argv)

     #login_window = LoginWindow()
     #login_window.show()
     main_window = Main('john', 'abba')
     main_window.show()
     

     sys.exit(app.exec_())

