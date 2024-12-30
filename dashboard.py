from PySide6.QtWidgets import QMainWindow,QLabel, QLineEdit, QVBoxLayout, QHBoxLayout, QWidget, QComboBox, QGridLayout
from PySide6.QtGui import QIcon,Qt
from PySide6.QtCore import QSize
import sqlite3

class Dashboard(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Farm Feeds System")
        self.setWindowIcon(QIcon("logo.png"))
        self.setMinimumSize(QSize(1000,600))
        con = sqlite3.connect("files/data/database.db")
        cursor = con.cursor()
        
        #Menu
        menuBar = self.menuBar()
        file = menuBar.addMenu("File")
        settings = menuBar.addMenu("Settings")
        fileMenu = file.addAction("Home", self.home)
        file.addSeparator()
        fileMenu = file.addAction("Quit", self.quit_app)
        settingsMenu = settings.addAction("Profile", self.profile)
        settings.addSeparator()
        settingsMenu = settings.addAction("Weeks Data")
        settings.addSeparator()
        settingsMenu = settings.addAction("Logout",self.logout)
        
        #Call the home widget
        self.home()
        
    def home(self):
        dashboard_vlayout = QGridLayout()
        #Dashboard title
        dashboard_title = QLabel("Farm Feeds Formulation System")
        dashboard_title.setProperty("class","auth_title")
        dashboard_title_layout = QHBoxLayout()
        dashboard_title_layout.addWidget(dashboard_title,1,Qt.AlignmentFlag.AlignTop)
        dashboard_central_widget = QWidget()
        dashboard_vlayout.addLayout(dashboard_title_layout,0,0)
        
        #Second row
        second_row_layout = QHBoxLayout()
        
        #Weeks
        week_layout = QVBoxLayout()
        week_title = QLabel("Week")
        week_title.setProperty("class","labels")
        week_title.setFixedWidth(100)
        self.week_selection = QComboBox()
        self.week_selection.setStyleSheet("""
        padding:7px;
        font-size:15px;
        """)
        self.week_selection.addItem("1")
        self.week_selection.addItem("2")
        self.week_selection.setFixedWidth(100)
        self.week_selection.currentTextChanged.connect(self.week_change)
        week_layout.addWidget(week_title)
        week_layout.addWidget(self.week_selection)
        week_layout.addStretch()
        week_layout.setSpacing(10)
        dashboard_vlayout.addLayout(week_layout,1,0)
        
        #Ratios
        ratios_layout = QVBoxLayout()
        ratios_row_layout = QHBoxLayout()
        ratio_title = QLabel("Ratios")
        #ratio_title.setFixedWidth(300)
        ratio_title_layout = QHBoxLayout()
        ratio_title_layout.addWidget(ratio_title,1,Qt.AlignmentFlag.AlignLeft)
        ratio_title.setProperty("class","labels")
        self.ratio_one = QLineEdit()
        self.ratio_one.setFixedSize(QSize(40,40))
        self.ratio_one.setMaxLength(3)
        self.ratio_one.setProperty("class","small_input")
        self.ratio_two = QLineEdit()
        self.ratio_two.setFixedSize(QSize(40,40))
        self.ratio_two.setMaxLength(3)
        self.ratio_two.setProperty("class","small_input")
        self.ratio_three = QLineEdit()
        self.ratio_three.setFixedSize(QSize(40,40))
        self.ratio_three.setMaxLength(3)
        self.ratio_three.setProperty("class","small_input")
        ratios_row_layout.addWidget(self.ratio_one)
        ratios_row_layout.addWidget(self.ratio_two)
        ratios_row_layout.addWidget(self.ratio_three)
        ratios_row_layout.addStretch()
        ratios_row_layout.setSpacing(20)
        ratios_layout.addLayout(ratio_title_layout)
        ratios_layout.addLayout(ratios_row_layout)
        ratios_layout.addStretch()
        ratios_layout.setSpacing(10)
        ratios_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        dashboard_vlayout.addLayout(ratios_layout,1,1)
        #on change of the ratios
        self.ratio_one.textChanged.connect(self.ratio_one_validator)
        self.ratio_two.textChanged.connect(self.ratio_two_validator)
        self.ratio_three.textChanged.connect(self.ratio_three_validator)
        
        #Ratio Values
        ratio_value_layout = QVBoxLayout()
        kbc30 = QLabel("Ratio 1: KBC30")
        kbc30.setProperty("class","small_input")
        broken = QLabel("Ratio 1: Broken")
        broken.setProperty("class","small_input")
        maize_brand_ratio = QLabel("Ratio 3: Maize Brand")
        maize_brand_ratio.setProperty("class","small_input")
        ratio_value_layout.addWidget(kbc30)
        ratio_value_layout.addWidget(broken)
        ratio_value_layout.addWidget(maize_brand_ratio)
        ratio_value_layout.addStretch()
        ratio_value_layout.setSpacing(20)
        dashboard_vlayout.addLayout(ratio_value_layout,1,2)
        
        #Home layout
        dashboard_central_widget.setLayout(dashboard_vlayout)
        self.setCentralWidget(dashboard_central_widget)
    
    def quit_app(self):
        self.close()
    
    def profile(self):
        profile_title_layout = QHBoxLayout()
        profile_title = QLabel("User Profile")
        profile_title.setProperty("class","auth_title")
        profile_title_layout.addWidget(profile_title,1,Qt.AlignmentFlag.AlignTop)
        centralWidget = QWidget()
        centralWidget.setLayout(profile_title_layout)
        self.setCentralWidget(centralWidget)
    
    #Check if the ratio values are integers
    def ratio_one_validator(self):
        values = self.ratio_one.text()
        if(values.isnumeric() == False):
            self.ratio_one.setText("")
            
    def ratio_two_validator(self):
        values = self.ratio_two.text()
        if(values.isnumeric() == False):
            self.ratio_two.setText("")
            
    def ratio_three_validator(self):
        values = self.ratio_three.text()
        if(values.isnumeric() == False):
            self.ratio_three.setText("")
            
    def week_change(self):
        current_value = self.week_selection.currentText()
        print(f"Week has changed to {current_value}")
        
    def logout(self):
        self.close()