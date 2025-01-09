from PySide6.QtWidgets import QMainWindow,QLabel, QLineEdit, QVBoxLayout, QHBoxLayout, QWidget, QComboBox, QGridLayout, QPushButton
from PySide6.QtGui import QIcon,Qt
from PySide6.QtCore import QSize
import sqlite3

class Dashboard(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Farm Feeds System")
        self.setWindowIcon(QIcon("logo.png"))
        # self.setMinimumSize(QSize(1000,600))
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
        #Home Page title
        farm_title = QLabel("Farm Feeds System")
        dashboard_vlayout.addWidget(farm_title)

        #Weeks Layout
        weeks_layout = QVBoxLayout()
        weeks_title = QLabel("Weeks")
        self.week_selection = QComboBox()
        self.week_selection.addItems(["1","2","3","4","5","6","7","8","9"])
        self.week_selection.setFixedSize(QSize(70,40))
        self.week_selection.currentTextChanged.connect(self.week_change)
        weeks_title.setFixedSize(QSize(50,40))
        weeks_layout.addWidget(weeks_title)
        weeks_layout.addWidget(self.week_selection)
        dashboard_vlayout.addLayout(weeks_layout,1,0,Qt.AlignmentFlag.AlignTop)

        #Ratios layout
        ratios_layout = QHBoxLayout()
        ratios_vertical = QVBoxLayout()
        ratios_title = QLabel("Ratios")
        ratios_title.setFixedSize(QSize(150,40))
        ratios_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.ratio1 = QLineEdit()
        self.ratio2 = QLineEdit()
        self.ratio3 = QLineEdit()
        self.ratio1.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.ratio2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.ratio3.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.ratio1.setMaxLength(3)
        self.ratio2.setMaxLength(3)
        self.ratio3.setMaxLength(3)
        self.ratio1.setFixedSize(QSize(40,40))
        self.ratio2.setFixedSize(QSize(40, 40))
        self.ratio3.setFixedSize(QSize(40, 40))
        ratios_vertical.addWidget(ratios_title)
        ratios_layout.addWidget(self.ratio1)
        ratios_layout.addWidget(self.ratio2)
        ratios_layout.addWidget(self.ratio3)

        #Connect input values to functions
        self.ratio1.textChanged.connect(self.ratio_one_validator)
        self.ratio2.textChanged.connect(self.ratio_two_validator)
        self.ratio3.textChanged.connect(self.ratio_three_validator)

        ratios_vertical.addLayout(ratios_layout)
        ratios_vertical.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        ratios_layout.addStretch()
        ratios_layout.setSpacing(10)
        dashboard_vlayout.addLayout(ratios_vertical,1,1,Qt.AlignmentFlag.AlignTop)

        #Ratios Values
        ratio_value_layout = QVBoxLayout()
        maize_brand = QLabel("Ratio 1: Maize Brand")
        kbc_30 = QLabel("Ratio 2: KBC30")
        broken = QLabel("Ratio 3: Broken")
        ratio_value_layout.addWidget(maize_brand)
        ratio_value_layout.addWidget(kbc_30)
        ratio_value_layout.addWidget(broken)
        ratio_value_layout.setSpacing(10)
        ratio_value_layout.addStretch()
        dashboard_vlayout.addLayout(ratio_value_layout,1,2,Qt.AlignmentFlag.AlignTop)

        #Third row
        third_row_layout = QVBoxLayout()
        chicken_label = QLabel("Total Chicken")
        total_feeds_label = QLabel("Total Feeds (Kgs)")
        self.total_chicken_input = QLineEdit()
        self.total_chicken_input.setPlaceholderText("Enter number of birds")
        self.total_feeds_input = QLineEdit()
        self.total_feeds_input.setPlaceholderText("Enter amount in kgs")
        self.total_chicken_input.setMaxLength(3)
        self.total_feeds_input.setMaxLength(5)
        self.total_chicken_input.textChanged.connect(self.numeric_input_only_chicken)
        self.total_feeds_input.textChanged.connect(self.numeric_input_only_feeds)
        spacer = QWidget()
        spacer.setFixedHeight(5)
        self.total_chicken_input.setFixedSize(QSize(300,40))
        self.total_feeds_input.setFixedSize(QSize(300,40))
        third_row_layout.addWidget(chicken_label)
        third_row_layout.addWidget(self.total_chicken_input)
        third_row_layout.addWidget(spacer)
        third_row_layout.addWidget(total_feeds_label)
        third_row_layout.addWidget(self.total_feeds_input)
        third_row_layout.addStretch()
        third_row_layout.setSpacing(10)
        third_row_layout.setAlignment(Qt.AlignmentFlag.AlignTop)


        #Feeds Formulations
        feeds_formulations_row = QHBoxLayout()
        feeds_formulations_label = QLabel("Feed Formulations")
        reset_btn = QPushButton("Reset")
        reset_btn.setStyleSheet("""
            background:red;
            padding:5px;
        """)

        reset_btn.setMaximumWidth(80)
        feeds_formulations_row.addWidget(feeds_formulations_label)
        feeds_formulations_row.addWidget(reset_btn)
        maize_brand_row = QHBoxLayout()
        kbc_30_row = QHBoxLayout()
        broken_row = QHBoxLayout()

        #Maize Brand
        maize_brand_title = QLabel("Maize Brand: ")
        self.maize_brand_input = QLineEdit()
        self.maize_brand_input.setProperty("class","formulation_input")
        self.maize_brand_input.setDisabled(True)
        maize_brand_row.addWidget(maize_brand_title)
        maize_brand_row.addWidget(self.maize_brand_input)

        #KBC
        kbc_30_title = QLabel("KBC30: ")
        self.kbc_30_input = QLineEdit()
        self.kbc_30_input.setProperty("class", "formulation_input")
        self.kbc_30_input.setDisabled(True)
        kbc_30_row.addWidget(kbc_30_title)
        kbc_30_row.addWidget(self.kbc_30_input)

        #Broken
        broken_title = QLabel("Broken: ")
        self.broken_input = QLineEdit()
        self.broken_input.setProperty("class", "formulation_input")
        self.broken_input.setDisabled(True)
        broken_row.addWidget(broken_title)
        broken_row.addWidget(self.broken_input)

        #Calculate reset buttons
        calculate_reset_btn_row = QHBoxLayout()
        self.calculate_btn = QPushButton("Calculate")
        self.save_btn = QPushButton("Save")
        self.calculate_btn.setStyleSheet("""
            background:blue;
            padding:5px;
        """)
        self.save_btn.setStyleSheet("""
            background:green;
            padding:5px;
        """)
        calculate_reset_btn_row.addWidget(self.calculate_btn)
        calculate_reset_btn_row.addWidget(self.save_btn)

        third_row_layout.addWidget(spacer)
        third_row_layout.addLayout(feeds_formulations_row)
        third_row_layout.addWidget(spacer)
        third_row_layout.addLayout(maize_brand_row)
        third_row_layout.addWidget(spacer)
        third_row_layout.addLayout(kbc_30_row)
        third_row_layout.addWidget(spacer)
        third_row_layout.addLayout(broken_row)
        third_row_layout.addWidget(spacer)
        third_row_layout.addLayout(calculate_reset_btn_row)

        dashboard_vlayout.addLayout(third_row_layout, 2, 0, Qt.AlignmentFlag.AlignTop)
        #Home Central Widget
        central_widget = QWidget()
        central_widget.setLayout(dashboard_vlayout)
        self.setCentralWidget(central_widget)

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
        values = self.ratio1.text()
        if not values.isnumeric():
            self.ratio1.setText("")
            
    def ratio_two_validator(self):
        values = self.ratio2.text()
        if not values.isnumeric():
            self.ratio2.setText("")
            
    def ratio_three_validator(self):
        values = self.ratio3.text()
        if not values.isnumeric():
            self.ratio3.setText("")

    def numeric_input_only_chicken(self):
        values = self.total_chicken_input.text()
        if not values.isnumeric():
            self.total_chicken_input.setText("")

    def numeric_input_only_feeds(self):
        values = self.total_feeds_input.text()
        if not values.isnumeric():
            self.total_feeds_input.setText("")
            
    def week_change(self):
        current_value = self.week_selection.currentText()
        print(f"Week has changed to {current_value}")
        
    def logout(self):
        self.close()