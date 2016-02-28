# I chose the PyQt grid layout
import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class Main(QWidget):
     def __init__(self, username, password):
          super().__init__()
          self.username = username
          self.password = password

          grid = QGridLayout()
          self.setLayout(grid)

          dept_combo = QComboBox(self)
          dept_combo.addItems(['crab', 'snake', 'snail', 'monkey'])

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

