from PySide6.QtWidgets import QMainWindow, QLabel, QLineEdit, QVBoxLayout, QHBoxLayout, QWidget, QComboBox, QGridLayout, \
    QPushButton, QTableWidget, QTableWidgetItem, QMessageBox, QAbstractScrollArea
from PySide6.QtGui import QIcon,Qt
from PySide6.QtCore import QSize
import sqlite3
from datetime import datetime

class Dashboard(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Farm Feeds System")
        self.setWindowIcon(QIcon("logo.png"))
        self.setMinimumSize(QSize(1220,600))
        con = sqlite3.connect("files/data/database.db")
        cursor = con.cursor()

        #Create feeds formulation table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS feeds_formulation(id INTEGER PRIMARY KEY AUTOINCREMENT, date TEXT NOT NULL, week INTEGER NOT NULL DEFAULT 0, 
        total_chicken INTEGER NOT NULL DEFAULT 0, total_feeds INTEGER NOT NULL DEFAULT 0, maize_brand INETGER NOT NULL DEFAULT 0, kbc INTEGER NOT NULL DEFAULT 0,
        broken INTEGER NOT NULL DEFAULT 0
        )
        """)

        #Create ratios table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS ratios(id INTEGER PRIMARY KEY AUTOINCREMENT, ratio_title TEXT NOT NULL, ratio_value INTEGER NOT NULL)
        """)

        #Fetch ratios data
        self.ratios = cursor.execute("""
            SELECT * FROM ratios;
        """).fetchall()

        #Fetch feeds formulation data
        self.data = cursor.execute("""
            SELECT date,week,total_chicken, total_feeds, maize_brand, kbc, broken FROM feeds_formulation ORDER BY id DESC;
        """).fetchall()

        con.close()

        self.selected_row = 0
        self.selected_row_value = ""
        
        #Menu
        menuBar = self.menuBar()
        file = menuBar.addMenu("File")
        settings = menuBar.addMenu("Settings")
        file.addAction("Home", self.home)
        file.addSeparator()
        file.addAction("Quit", self.quit_app)
        settings.addAction("Profile", self.profile)
        # settings.addSeparator()
        # settings.addAction("Weeks Data")
        settings.addSeparator()
        settings.addAction("Logout",self.logout)
        
        #Call the home widget
        self.home()

    def home(self):
        dashboard_vlayout = QGridLayout()
        #Home Page title
        farm_title = QLabel("Farm Feeds Formulation System")
        farm_title.setStyleSheet("""
            font-weight:bold;
            text-transform:uppercase;
        """)
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

        #Assign the default values
        try:
            self.ratio1.setText(str(self.ratios[0][2]))
            self.ratio2.setText(str(self.ratios[1][2]))
            self.ratio3.setText(str(self.ratios[2][2]))
        except:
            alert = QMessageBox.information(self,"Notification","Please add all ratios!",QMessageBox.Ok)

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

        #Add or Update Ratios
        self.ratio1.editingFinished.connect(self.addUpdateRatio1)
        self.ratio2.editingFinished.connect(self.addUpdateRatio2)
        self.ratio3.editingFinished.connect(self.addUpdateRatio3)

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
        self.total_feeds_input.setStyleSheet("""
        color:white;
        """)
        self.total_feeds_input.setDisabled(True)
        self.total_feeds_input.setPlaceholderText("Enter amount in kgs")
        # self.total_chicken_input.setMaxLength(3)
        self.total_feeds_input.setMaxLength(5)
        self.total_chicken_input.textChanged.connect(self.numeric_input_only_chicken)
        # self.total_feeds_input.textChanged.connect(self.numeric_input_only_feeds)
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
        self.reset_btn = QPushButton("Reset")
        self.reset_btn.setStyleSheet("""
            background:red;
            padding:5px;
        """)
        self.reset_btn.clicked.connect(self.reset_inputs)
        self.reset_btn.setMaximumWidth(80)
        feeds_formulations_row.addWidget(feeds_formulations_label)
        feeds_formulations_row.addWidget(self.reset_btn)
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
        self.maize_brand_input.setMaximumWidth(200)

        #KBC
        kbc_30_title = QLabel("KBC30: ")
        self.kbc_30_input = QLineEdit()
        self.kbc_30_input.setProperty("class", "formulation_input")
        self.kbc_30_input.setDisabled(True)
        kbc_30_row.addWidget(kbc_30_title)
        kbc_30_row.addWidget(self.kbc_30_input)
        self.kbc_30_input.setMaximumWidth(200)

        #Broken
        broken_title = QLabel("Broken: ")
        self.broken_input = QLineEdit()
        self.broken_input.setProperty("class", "formulation_input")
        self.broken_input.setDisabled(True)
        broken_row.addWidget(broken_title)
        broken_row.addWidget(self.broken_input)
        self.broken_input.setMaximumWidth(200)

        #Calculate reset buttons
        calculate_reset_btn_row = QHBoxLayout()
        self.calculate_btn = QPushButton("Calculate")
        self.calculate_btn.clicked.connect(self.calculate_formula)
        self.save_btn = QPushButton("Save")
        self.calculate_btn.setStyleSheet("""
            background:blue;
            padding:5px;
        """)
        self.save_btn.setStyleSheet("""
            background:green;
            padding:5px;
        """)
        self.save_btn.clicked.connect(self.save_data)
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
        third_row_widget = QWidget()
        third_row_widget.setLayout(third_row_layout)
        third_row_widget.setMaximumWidth(350)

        #Place layout on 3rd row 1st column
        dashboard_vlayout.addWidget(third_row_widget, 2, 0, Qt.AlignmentFlag.AlignTop)

        #table
        history_section_widget = QWidget()
        history_section_layout = QVBoxLayout()
        table_title = QLabel("Formulations History")
        table_title.setAlignment(Qt.AlignmentFlag.AlignTop)
        table_title.setStyleSheet("""
            font-weight:bold;
            text-transform:uppercase;
        """)
        
        #Create the table instance
        self.history_table = QTableWidget()
        self.history_table.setMinimumSize(QSize(700,300))
        rows = len(self.data)
        self.history_table.setRowCount(rows)
        self.history_table.setColumnCount(7)
        
        #create the table header leables
        self.history_table.setHorizontalHeaderLabels(["Date","Week","Total Chicken","Total Feeds","Maize Brand","KBC30","Broken"])
        
        #Add rows to the table
        row_counter=-1
        # keys = ["date","week","total_chicken","total_feeds","maize_brand","kbc","broken"]
        for x in self.data:
            row_counter = row_counter + 1
            for y in range(len(x)):
                if y == 2 or y == 3:
                    self.history_table.setItem(row_counter, y, QTableWidgetItem(str("{:,}".format(x[y]))))
                else:
                    self.history_table.setItem(row_counter, y, QTableWidgetItem(str(x[y])))

        #Select a row of the table
        self.history_table.itemClicked.connect(self.selected_item)

        self.delete_btn = QPushButton("Delete")
        self.delete_btn.setMaximumSize(QSize(100,100))
        self.delete_btn.setStyleSheet("""
            background:red;
            padding:5px;
        """)
        self.delete_btn.setDisabled(True)
        self.delete_btn.clicked.connect(self.delete_table_row)
        history_section_layout.addWidget(table_title,1)
        history_section_layout.addWidget(self.history_table,2)
        info_text = QLabel("To delete a row, select the DATE of that row first, then click Delete.")
        history_section_layout.addWidget(spacer)
        history_section_layout.addWidget(info_text)
        history_section_layout.addWidget(spacer)
        history_section_layout.addWidget(self.delete_btn)
        history_section_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        history_section_widget.setLayout(history_section_layout)
        dashboard_vlayout.addWidget(history_section_widget,2,1,Qt.AlignmentFlag.AlignTop)

        #Home Central Widget
        central_widget = QWidget()
        central_widget.setLayout(dashboard_vlayout)
        self.setCentralWidget(central_widget)

    def quit_app(self):
        self.close()
    
    def profile(self):
        profile_layout = QVBoxLayout()
        profile_layout.setSpacing(10)
        profile_title = QLabel("User Profile")
        profile_title.setProperty("class","auth_title")
        profile_layout.addWidget(profile_title,1,Qt.AlignmentFlag.AlignTop)

        #Old username
        user_name_layout = QHBoxLayout()
        user_name_label = QLabel("Username")
        self.user_name_input = QLineEdit()
        self.user_name_input.setStyleSheet("""
            padding:7px;
        """)
        self.user_name_input.EchoMode(QLineEdit.EchoMode.Password)
        self.user_name_input.setPlaceholderText("Enter username")
        user_name_layout.addWidget(user_name_label)
        user_name_layout.addWidget(self.user_name_input)

        #New Username
        new_user_name_layout = QHBoxLayout()
        new_user_name_label = QLabel("New Username")
        self.new_user_name_input = QLineEdit()
        self.new_user_name_input.setStyleSheet("""
            padding:7px;
        """)
        self.new_user_name_input.EchoMode(QLineEdit.EchoMode.Password)
        self.new_user_name_input.setPlaceholderText("Enter new username")
        new_user_name_layout.addWidget(new_user_name_label)
        new_user_name_layout.addWidget(self.new_user_name_input)

        #Old Password
        old_password_layout = QHBoxLayout()
        old_password_label = QLabel("Old password")
        self.old_password_input = QLineEdit()
        self.old_password_input.setStyleSheet("""
            padding:7px;
        """)
        self.old_password_input.EchoMode(QLineEdit.EchoMode.Password)
        self.old_password_input.setPlaceholderText("Enter old password")
        old_password_layout.addWidget(old_password_label)
        old_password_layout.addWidget(self.old_password_input)
        #New Password
        new_password_layout = QHBoxLayout()
        new_password_label = QLabel("New password")
        self.new_password_input = QLineEdit()
        self.new_password_input.setStyleSheet("""
            padding:7px;
        """)
        self.new_password_input.EchoMode(QLineEdit.EchoMode.Password)
        self.new_password_input.setPlaceholderText("Enter new password")
        new_password_layout.addWidget(new_password_label)
        new_password_layout.addWidget(self.new_password_input)

        #Confirm button
        auth_btn = QPushButton("Update")
        auth_btn.setStyleSheet("""
            background:blue;
            padding:7px;
        """)
        auth_btn.setMaximumWidth(100)
        auth_btn.clicked.connect(self.update_profile)

        #Add to layout
        profile_layout.addLayout(user_name_layout)
        profile_layout.addLayout(new_user_name_layout)
        profile_layout.addLayout(old_password_layout)
        profile_layout.addLayout(new_password_layout)
        profile_layout.addWidget(auth_btn)
        central_widget = QWidget()
        central_widget.setFixedSize(QSize(500,300))
        central_widget.setLayout(profile_layout)
        self.setCentralWidget(central_widget)

    def update_profile(self):
        # Fetch Data
        con = sqlite3.connect("files/data/database.db")
        cursor = con.cursor()
        res = cursor.execute("""
                    SELECT * FROM user WHERE username = ? AND password = ?;
                """, [self.user_name_input.text(), self.old_password_input.text()]).fetchall()

        if (len(res) > 0 and self.old_password_input.text() != "" and self.new_password_input.text() != ""
                and self.user_name_input.text() != "" and self.new_user_name_input.text() != ""):
            # Update the password
            cursor.execute("""
                        UPDATE user SET username = ?, password = ? WHERE username = ?;
                    """, [str.lower(self.new_user_name_input.text()), self.new_password_input.text(), self.user_name_input.text()])
            con.commit()
            con.close()
            alert = QMessageBox.information(self, "Notification", "Success: Profile updated successfully!", QMessageBox.Ok)

            #clear the inputs
            self.new_user_name_input.setText("")
            self.user_name_input.setText("")
            self.old_password_input.setText("")
            self.new_password_input.setText("")
        else:
            alert = QMessageBox.critical(self, "Alert", "Failed: Check credentials again!", QMessageBox.Ok)

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

    #Add or update ratio values
    def addUpdateRatio1(self):
        values = self.ratio1.text()
        # Add to DB
        con = sqlite3.connect("files/data/database.db")
        cursor = con.cursor()
        res = cursor.execute("""
                        SELECT ratio_value FROM ratios WHERE ratio_title = ?
                    """, ["maize_brand"]).fetchone()
        if res == None:
            cursor.execute("""
                            INSERT INTO ratios(ratio_title, ratio_value) VALUES(?,?)
                        """, ["maize_brand", values])
            con.commit()
        else:
            cursor.execute("""
                            UPDATE ratios SET ratio_value = ? WHERE ratio_title = ?
                        """, [values,"maize_brand"])
            con.commit()

    def addUpdateRatio2(self):
        values = self.ratio2.text()
        # Add to DB
        con = sqlite3.connect("files/data/database.db")
        cursor = con.cursor()
        res = cursor.execute("""
                        SELECT ratio_value FROM ratios WHERE ratio_title = ?
                    """, ["kbc"]).fetchone()
        if res == None:
            cursor.execute("""
                            INSERT INTO ratios(ratio_title, ratio_value) VALUES(?,?)
                        """, ["kbc", values])
            con.commit()
        else:
            cursor.execute("""
                            UPDATE ratios SET ratio_value = ? WHERE ratio_title = ?
                        """, [values,"kbc"])
            con.commit()

    def addUpdateRatio3(self):
        values = self.ratio3.text()
        # Add to DB
        con = sqlite3.connect("files/data/database.db")
        cursor = con.cursor()
        res = cursor.execute("""
                        SELECT ratio_value FROM ratios WHERE ratio_title = ?
                    """, ["broken"]).fetchone()
        if res == None:
            cursor.execute("""
                            INSERT INTO ratios(ratio_title, ratio_value) VALUES(?,?)
                        """, ["broken", values])
            con.commit()
        else:
            cursor.execute("""
                            UPDATE ratios SET ratio_value = ? WHERE ratio_title = ?
                        """, [values,"broken"])
            con.commit()

    def numeric_input_only_chicken(self):
        values = self.total_chicken_input.text()
        if not values.isnumeric():
            self.total_chicken_input.setText("")

    def numeric_input_only_feeds(self):
        values = self.total_feeds_input.text()
        if not values.isnumeric():
            self.total_feeds_input.setText("")
            
    def week_change(self):
        week = int(self.week_selection.currentText())
        if week == 1:
            self.ratio1.setText(str(36))
            self.ratio2.setText(str(50))
            self.ratio3.setText(str(57))
        elif week == 2:
            self.ratio1.setText(str(36))
            self.ratio2.setText(str(50))
            self.ratio3.setText(str(36))
        elif week == 3:
            self.ratio1.setText(str(39))
            self.ratio2.setText(str(50))
            self.ratio3.setText(str(67))
        elif week == 4:
            self.ratio1.setText(str(39))
            self.ratio2.setText(str(50))
            self.ratio3.setText(str(67))
        elif week == 5:
            self.ratio1.setText(str(45))
            self.ratio2.setText(str(50))
            self.ratio3.setText(str(84))
        elif week == 6:
            self.ratio1.setText(str(75))
            self.ratio2.setText(str(50))
            self.ratio3.setText(str(75))
        elif week == 7:
            self.ratio1.setText(str(75))
            self.ratio2.setText(str(50))
            self.ratio3.setText(str(75))
        elif week == 8:
            self.ratio1.setText(str(75))
            self.ratio2.setText(str(50))
            self.ratio3.setText(str(75))
        elif week == 9:
            self.ratio1.setText(str(75))
            self.ratio2.setText(str(50))
            self.ratio3.setText(str(75))
        else:
            self.ratio1.setText("")
            self.ratio2.setText("")
            self.ratio3.setText("")

    def selected_item(self):
        selected = self.history_table.selectedItems()
        #Activate the button
        self.delete_btn.setDisabled(False)
        for x in selected:
            self.selected_row_value = x.text()
            self.selected_row = x.row()

    def delete_table_row(self):
        self.delete_btn.setDisabled(True)
        #Delete row from DB
        con = sqlite3.connect("files/data/database.db")
        cursor = con.cursor()
        cursor.execute("""
            DELETE FROM feeds_formulation WHERE date = ?
        """,[str(self.selected_row_value)])
        con.commit()
        con.close()

        # Delete row from table
        self.history_table.removeRow(self.selected_row)

    def calculate_formula(self):
        try:
            ratio1 = int(self.ratio1.text())
            ratio2 = int(self.ratio2.text())
            ratio3 = int(self.ratio3.text())
            total_ratio = (ratio1 + ratio2 + ratio3)
            week = int(self.week_selection.currentText())
            if week == 1:
                week_value = 0.167
            elif week == 2:
                week_value = 0.375
            elif week == 3:
                week_value = 0.65
            elif week == 4:
                week_value = 0.945
            elif week == 5:
                week_value = 1.215
            elif week == 6:
                week_value = 1.434
            elif week == 7:
                week_value = 1.593
            elif week == 8:
                week_value = 1.691
            elif week == 9:
                week_value = 1.715
            else:
                week_value = 0

            total_chicken = int(self.total_chicken_input.text())
            total_feeds = float(total_chicken * week_value)
            self.total_feeds_input.setText(str(total_feeds))
            calculated_maize_brand = "{:.2f}".format((ratio1 / total_ratio) * total_feeds)
            calculated_kbc = "{:.2f}".format((ratio2 / total_ratio) * total_feeds)
            calculated_broken = "{:.2f}".format((ratio3 / total_ratio) * total_feeds)
            self.maize_brand_input.setText(str(calculated_maize_brand))
            self.kbc_30_input.setText(str(calculated_kbc))
            self.broken_input.setText(str(calculated_broken))
        except:
            alert = QMessageBox.critical(self, "Alert","All fields must be filled!",QMessageBox.Ok)

    def reset_inputs(self):
        self.total_feeds_input.setText("")
        self.total_chicken_input.setText("")
        self.maize_brand_input.setText("")
        self.kbc_30_input.setText("")
        self.broken_input.setText("")

    def save_data(self):
        date = datetime.today().strftime('%d-%m-%Y')
        week = self.week_selection.currentText()
        total_chicken = self.total_chicken_input.text()
        total_feeds = self.total_chicken_input.text()
        maize_brand = self.maize_brand_input.text()
        broken = self.broken_input.text()
        kbc = self.kbc_30_input.text()
        data = [date,week,total_chicken,total_feeds, maize_brand, broken, kbc]
        if date != "" and week != "" and total_chicken != "" and total_feeds != "" and maize_brand != "" and broken != "" and kbc != "":
            # Save to DB
            con = sqlite3.connect("files/data/database.db")
            cursor = con.cursor()
            res = cursor.execute("""
                SELECT date FROM feeds_formulation WHERE date = ?;
            """,[date]).fetchall()
            print(res)
            if len(res) == 0:
                cursor.execute("""
                                    INSERT INTO feeds_formulation(date,week,total_chicken,total_feeds,maize_brand,kbc,broken) VALUES(?,?,?,?,?,?,?)
                                """, data)
                con.commit()
                con.close()

                # Display in the table
                self.history_table.insertRow(0)
                for x in range(len(data)):
                    if x == 2 or x == 3 or x == 4 or x == 5 or x == 6:
                        self.history_table.setItem(0, x, QTableWidgetItem(str("{:,}".format(float(data[x])))))
                    else:
                        self.history_table.setItem(0, x, QTableWidgetItem(str(data[x])))
            else:
                alert = QMessageBox.critical(self, "Alert", "Sorry, today's data already saved!", QMessageBox.Ok)
        else:
            alert = QMessageBox.critical(self,"Alert","Error: Cannot save, check fields!",QMessageBox.Ok)
        
    def logout(self):
        self.close()