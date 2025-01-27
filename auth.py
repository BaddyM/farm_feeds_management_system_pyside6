from PySide6.QtWidgets import QWidget,QVBoxLayout,QLineEdit, QLabel, QHBoxLayout, QPushButton, QMessageBox
from PySide6.QtGui import QIcon
from PySide6.QtCore import QSize,Qt
import sqlite3
import sys
import os
from database import Database

class Auth(QWidget):
    def __init__(self):
        global file_path
        super().__init__()
        self.setWindowTitle("Login")
        self.setWindowIcon(QIcon("logo.png"))
        self.setMinimumSize(QSize(500,250))

        database = Database()
        self.db_path = database.db_path
        con = sqlite3.connect(self.db_path)
        cursor = con.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS user(id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT NOT NULL,password INTEGER NOT NULL)")
        cursor.execute("INSERT INTO user(username, password) VALUES(?,?)",["admin","admin"])
        con.commit()
        
        vlayout = QVBoxLayout()
        
        #Title
        title_layout = QHBoxLayout()
        title_widget = QLabel("Farm Feeds System Authentication")
        title_widget.setProperty("class","auth_title")
        title_layout.addWidget(title_widget,1,Qt.AlignmentFlag.AlignHCenter)
        
        #username
        self.username_layout = QHBoxLayout()
        self.username_label = QLabel("Username")
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Enter UserName")
        self.username_input.setProperty("class","auth_input")
        self.username_layout.addWidget(self.username_label)
        self.username_layout.addWidget(self.username_input)
        
        #Password
        self.password_layout = QHBoxLayout()
        self.password_label = QLabel("Password")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setPlaceholderText("Enter Password")
        self.password_input.setProperty("class","auth_input")
        self.password_layout.addWidget(self.password_label)
        self.password_layout.addWidget(self.password_input)
        
        #submit_btn
        submit_btn = QPushButton("Login")
        submit_btn.setProperty("class","submit_btn")
        submit_btn.clicked.connect(self.authenticate)
        
        #Main Layout
        vlayout.addLayout(title_layout)
        vlayout.addLayout(self.username_layout)
        vlayout.addLayout(self.password_layout)
        vlayout.addWidget(submit_btn)
        vlayout.addStretch()
        vlayout.setSpacing(30)
        self.setLayout(vlayout)
        
        #cursor.execute("SELECT * FROM user WHERE username = '' AND password = ''; ")
    def authenticate(self):
        username = self.username_input.text()
        password = self.password_input.text()
        
        #check database
        if username != "" and password != "" :
            con = sqlite3.connect(self.db_path)
            cursor = con.cursor()
            result = cursor.execute(f"SELECT * FROM user WHERE username='{username}' AND password = '{password}';")
            if result.fetchone() is None:
                alert = QMessageBox.critical(self,"Alert","Invalid Credentials",QMessageBox.Ok)
            else:
                # Go to dashboard
                from dashboard import Dashboard
                self.window = Dashboard()
                self.window.show()

                #close current window
                self.hide()
        else:
            alert = QMessageBox.critical(self,"Alert","All fields must be filled",QMessageBox.Ok)