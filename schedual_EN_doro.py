import json # ✅ Import JSON for file storage
from PyQt5.QtWidgets import  QWidget, QVBoxLayout, QCalendarWidget, QTableWidget, QTableWidgetItem, QPushButton, QLineEdit, QLabel, QHBoxLayout
from PyQt5.QtCore import QDate
from PyQt5.QtGui import QTextCharFormat, QColor


class CalendarPlanner(QWidget):  # ✅ 繼承 QWidget，確保關閉時不影響 Deskpet
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Dochedual")
        self.setGeometry(100, 100, 500, 500)# Set window size

        # 🔹 Create UI elements
        self.layout = QVBoxLayout(self)

        # 📅 Calendar Widget
        self.calendar = QCalendarWidget(self)
        self.calendar.clicked.connect(self.show_schedule)  # Display schedule when a date is clicked
        self.layout.addWidget(self.calendar)

        # ✅ Highlight today's date
        self.mark_today()

        # 📋 Schedule Table
        self.schedule_table = QTableWidget(0, 1, self)  # 1 column (Schedule)
        self.schedule_table.setHorizontalHeaderLabels(["Schedule"])
        self.layout.addWidget(self.schedule_table)

        # ➕ Input box & Add Button
        self.input_layout = QHBoxLayout()
        self.schedule_input = QLineEdit(self)
        self.schedule_input.setPlaceholderText("Enter schedule...")
        self.add_button = QPushButton("Add Schedule", self)
        self.add_button.clicked.connect(self.add_schedule)
        self.input_layout.addWidget(self.schedule_input)
        self.input_layout.addWidget(self.add_button)
        self.layout.addLayout(self.input_layout)

        # ❌ Delete Button
        self.delete_button = QPushButton("Delete Selected Schedule", self)
        self.delete_button.clicked.connect(self.delete_schedule)
        self.layout.addWidget(self.delete_button)

        # 📌 Dictionary to store schedules ({date: [schedule list]})
        self.schedule_data = {}

        # 📌 Load schedules from file
        self.schedule_data = self.load_schedule_data()
        
        # 🔹 Apply Styles
        self.apply_styles()

    def mark_today(self):
        """Highlight today's date"""
        today = QDate.currentDate()  # Get today's date
        highlight_format = QTextCharFormat()
        highlight_format.setForeground(QColor("red"))  # Set red text color
        highlight_format.setBackground(QColor(255, 220, 220))  # Light red background
        self.calendar.setDateTextFormat(today, highlight_format)

    def show_schedule(self, date):
        """Display the schedule when a date is clicked"""
        selected_date = date.toString("yyyy-MM-dd")  # Format the date
        self.schedule_table.setRowCount(0)  # Clear table

        if selected_date in self.schedule_data:
            for event in self.schedule_data[selected_date]:
                row_position = self.schedule_table.rowCount()
                self.schedule_table.insertRow(row_position)
                self.schedule_table.setItem(row_position, 0, QTableWidgetItem(event))
    def highlight_date(self, date, highlight=True):
        """Change the color of a date when a schedule is added or removed"""
        today = QDate.currentDate()  # Get today's date
        date_format = QTextCharFormat()
        if date == today:
            date_format.setForeground(QColor("red"))
            date_format.setBackground(QColor(255, 220, 220))  # Light red background
        elif highlight:
            date_format.setForeground(QColor("blue"))  # Change text color to blue
            date_format.setBackground(QColor(200, 230, 255))  # Light blue background
        else:
            date_format.setForeground(QColor("black"))  # Restore default text color
            date_format.setBackground(QColor(255, 255, 255))  # Restore default background
        
        self.calendar.setDateTextFormat(date, date_format)
    def add_schedule(self):
        """Add a schedule to the selected date"""
        selected_date = self.calendar.selectedDate().toString("yyyy-MM-dd")
        new_schedule = self.schedule_input.text().strip()

        if new_schedule:
            # Add schedule to dictionary
            if selected_date not in self.schedule_data:
                self.schedule_data[selected_date] = []
            self.schedule_data[selected_date].append(new_schedule)

            # Highlight the date
            self.highlight_date(self.calendar.selectedDate(), highlight=True)

            # Update UI
            row_position = self.schedule_table.rowCount()
            self.schedule_table.insertRow(row_position)
            self.schedule_table.setItem(row_position, 0, QTableWidgetItem(new_schedule))

            self.schedule_input.clear()  # Clear input box

            # ✅ Save to file
            self.save_schedule_data()

    def delete_schedule(self):
        """Delete selected schedule"""
        selected_date = self.calendar.selectedDate().toString("yyyy-MM-dd")
        selected_rows = self.schedule_table.selectionModel().selectedRows()

        for row in sorted(selected_rows, reverse=True):  # Delete in reverse order to avoid index errors
            item = self.schedule_table.item(row.row(), 0)
            if item:
                self.schedule_data[selected_date].remove(item.text())
            self.schedule_table.removeRow(row.row())
        # If no more schedules exist for the selected date, remove the highlight
        if selected_date in self.schedule_data and not self.schedule_data[selected_date]:
            del self.schedule_data[selected_date]  # Remove empty key
            self.highlight_date(self.calendar.selectedDate(), highlight=False)

        # ✅ Save to file
        self.save_schedule_data()
    
    def save_schedule_data(self):
        """Save the schedule data to a file"""
        with open("schedule_data.json", "w") as file:
            json.dump(self.schedule_data, file, indent=4)
    def closeEvent(self, event):
        """確保關閉行程視窗時，將變數設為 None，避免存取已刪除的物件"""
        print("行程視窗已關閉")  # ✅ Debug 訊息
        if hasattr(self.parent(), 'schedual'):  # ✅ 確保父類有 `schedual` 變數
            self.parent().schedual = None  # ✅ 將 `self.schedual` 設為 None，避免存取錯誤
        event.accept()  # ✅ 允許關閉

   
    def load_schedule_data(self):
        """Load schedule data from a file and highlight scheduled dates"""
        try:
            with open("schedule_data.json", "r") as file:
                self.schedule_data = json.load(file)

            # ✅ Highlight all saved schedule dates
            for date_str in self.schedule_data.keys():
                date = QDate.fromString(date_str, "yyyy-MM-dd")
                if date.isValid():  # ✅ 確保日期有效
                    self.highlight_date(date, highlight=True)

            return self.schedule_data

        except (FileNotFoundError, json.JSONDecodeError):
            return {}  # Return empty dictionary if file does not exist


    def apply_styles(self):
        """Apply CSS styles to UI elements"""
        self.schedule_table.setStyleSheet("""
            QTableWidget {
                background-color: rgb(255,245,250);  /* Light pink background */
                border: 2px solid rgb(255,153,204);  /* Pink border */
                border-radius: 10px;
                font-size: 14px;
                color: black;
            }
            QHeaderView::section {
                background-color: rgb(255,153,204);  /* Header background */
                color: white;
                font-weight: bold;
                padding: 5px;
            }
            QTableWidget::item {
                padding: 5px;
                background-color: rgb(255,153,204);
            }
        """)

        self.add_button.setStyleSheet("""
            QPushButton {
                background-color: rgb(255,153,204);  /* Pink background */
                color: white;  /* White text */
                font-size: 16px;  /* Text size */
                border-radius: 10px;  /* Rounded corners */
                padding: 5px;
            }
            QPushButton:hover {
                background-color: rgb(255,102,178);  /* Darker pink on hover */
            }
        """)

        self.delete_button.setStyleSheet("""
            QPushButton {
                background-color: rgb(255,153,204);  /* Pink background */
                color: white;
                font-size: 16px;
                border-radius: 10px;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: rgb(255,102,178);
            }
        """)

# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     # ✅ 設定整個應用程式為英文
#     QLocale.setDefault(QLocale(QLocale.English, QLocale.UnitedStates))

#     window = CalendarPlanner()
#     window.show()
#     sys.exit(app.exec_())
#     # sys.exit(app.close())
#     # schedule_window = CalendarPlanner()
#     # schedule_window.exec_()  # ✅ This will keep it independent
#     # sys.exit(app.exec_())  # ✅ Keep the main app running




    

