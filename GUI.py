# I chose the PyQt grid layout
import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class_dict = {"AC ENG . . . . . .Academic English and ESL (started 2012 Fall)" : "AC ENG",
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
"PP&amp;D . . . . . . . Planning, Policy, and Design" : "PP&amp;D",
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
     def __init__(self, username, password):
          super().__init__()
          self.username = username
          self.password = password

          grid = QGridLayout()
          self.setLayout(grid)

          course_list = list(class_dict.keys())
          course_list.sort()
          dept_combo = QComboBox(self)
          dept_combo.addItems(course_list)

          dept_label = QLabel("Select Department: ")
          
          # Main user input 
          class_label = QLabel("Class codes (separated by commas): ")
          self.class_input = QLineEdit()
   
          enroll_button = QPushButton("Start bot")

          # Button events
          enroll_button.clicked.connect(self.enroll)

          grid.addWidget(dept_label, 0, 0, 1, 1)
          grid.addWidget(dept_combo, 0, 1, 1, 3)
          grid.addWidget(class_label, 1, 0, 1, 2)
          grid.addWidget(self.class_input, 1, 2, 1, 2)

          self.setWindowTitle("AutoEnroll")
          self.setGeometry(400, 400, 500, 200)
          

     def enroll(self):
          pass

class LoginWindow(QWidget):
     def __init__(self):
          super().__init__()

          grid = QGridLayout()
          self.setLayout(grid)

          self.title_label = QLabel("Login")
          self.title_label.setAlignment(Qt.AlignCenter)
          
          self.username_label = QLabel("UCINetID: ")
          self.username_input = QLineEdit()
          
          self.password_label = QLabel("Password: ")
          self.password_input = QLineEdit()
          self.password_input.setEchoMode(QLineEdit.Password)

          self.OK_button = QPushButton("OK")

          self.OK_button.clicked.connect(self.submit)
          
          grid.addWidget(self.title_label, 0, 0, 1, 2)
          grid.addWidget(self.username_label, 1, 0)
          grid.addWidget(self.username_input, 1, 1)
          grid.addWidget(self.password_label, 2, 0)
          grid.addWidget(self.password_input, 2, 1)
          grid.addWidget(self.OK_button, 3, 1)

     def submit(self):
          ''' Creates a new window with the truth table information for the inputs provided in the main window. '''
          # Try/except block for debugging purposes, may remove later
          username = str(self.username_input.text())
          password = str(self.password_input.text())
         
          self.main_window = Main(username, password)
          self.main_window.show()
          self.close()
          

if __name__ == '__main__':
     app = QApplication(sys.argv)

     login_window = LoginWindow()
     login_window.show()

     sys.exit(app.exec_())

