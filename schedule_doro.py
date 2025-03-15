from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QCalendarWidget, QTableWidget, QTableWidgetItem, QPushButton, QLineEdit, QLabel, QHBoxLayout
from PyQt5.QtCore import QDate
from PyQt5.QtGui import QTextCharFormat, QColor
import sys

class CalendarPlanner(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("日曆行程規劃")
        self.setGeometry(100, 100, 500, 500)  # 設定視窗大小

        # 🔹 建立 UI 元件
        self.layout = QVBoxLayout(self)

        # 📅 日曆
        self.calendar = QCalendarWidget(self)
        self.calendar.clicked.connect(self.show_schedule)  # 點選日期時，顯示行程
        self.layout.addWidget(self.calendar)
        self.calendar.setStyleSheet("""
                                            QTableWidget {
                                                background-color: rgb(255,245,250);  /* 淺粉背景 */
                                                border: 2px solid rgb(255,153,204);  /* 粉色邊框 */
                                                border-radius: 10px;
                                                font-size: 14px;
                                                color: black;
                                            }
                                            QHeaderView::section {
                                                background-color: rgb(255,153,204);  /* 標題列背景 */
                                                color: white;
                                                font-weight: bold;
                                                padding: 5px;
                                            }
                                            QTableWidget::item {
                                                padding: 5px;
                                            }
                                        """)
        # ✅ 標記今天的日期
        self.mark_today()

    
        # 📋 行程表
        self.schedule_table = QTableWidget(0, 1, self)  # 1 欄（行程）
        self.schedule_table.setHorizontalHeaderLabels(["行程"])
        self.layout.addWidget(self.schedule_table)
        self.schedule_table.setStyleSheet("""
                                            QTableWidget {
                                                background-color: rgb(255,245,250);  /* 淺粉背景 */
                                                border: 2px solid rgb(255,153,204);  /* 粉色邊框 */
                                                border-radius: 10px;
                                                font-size: 14px;
                                                color: black;
                                            }
                                            QHeaderView::section {
                                                background-color: rgb(255,153,204);  /* 標題列背景 */
                                                color: white;
                                                font-weight: bold;
                                                padding: 5px;
                                            }
                                            QTableWidget::item {
                                                padding: 5px;
                                            }
                                        """)


        # ➕ 新增行程輸入框 & 按鈕
        self.input_layout = QHBoxLayout()
        self.schedule_input = QLineEdit(self)
        self.schedule_input.setPlaceholderText("輸入行程...")
        self.add_button = QPushButton("新增行程", self)
        self.add_button.clicked.connect(self.add_schedule)
        self.input_layout.addWidget(self.schedule_input)
        self.input_layout.addWidget(self.add_button)
        self.layout.addLayout(self.input_layout)
        self.add_button.setStyleSheet("""
                    QPushButton {
                        background-color: rgb(255,153,204);  /* 粉色背景 */
                        color: white;  /* 文字顏色 */
                        font-size: 16px;  /* 文字大小 */
                        border-radius: 10px;  /* 圓角 */
                        padding: 5px;
                    }
                    QPushButton:hover {
                        background-color: rgb(255,102,178);  /* 滑鼠懸停時變深 */
                    }
                """)

        # ❌ 刪除行程按鈕
        self.delete_button = QPushButton("刪除選取行程", self)
        self.delete_button.clicked.connect(self.delete_schedule)
        self.layout.addWidget(self.delete_button)
        self.delete_button.setStyleSheet("""
                    QPushButton {
                        background-color: rgb(255,153,204);  /* 粉色背景 */
                        color: white;  /* 文字顏色 */
                        font-size: 16px;  /* 文字大小 */
                        border-radius: 10px;  /* 圓角 */
                        padding: 5px;
                    }
                    QPushButton:hover {
                        background-color: rgb(255,102,178);  /* 滑鼠懸停時變深 */
                    }
                """)

        # 📌 存儲行程（字典格式：{日期: [行程列表]})
        self.schedule_data = {}
    def mark_today(self):
            """標記今天的日期"""
            today = QDate.currentDate()  # 獲取今天的日期
            highlight_format = QTextCharFormat()
            highlight_format.setForeground(QColor("red"))  # 設定紅色標記
            highlight_format.setBackground(QColor(255, 220, 220))  # 設定淺紅色背景
            self.calendar.setDateTextFormat(today, highlight_format)
    def show_schedule(self, date):
        """當使用者點擊日曆時，顯示該日期的行程"""
        selected_date = date.toString("yyyy-MM-dd")  # 格式化日期
        self.schedule_table.setRowCount(0)  # 清空行程表

        if selected_date in self.schedule_data:
            for event in self.schedule_data[selected_date]:
                row_position = self.schedule_table.rowCount()
                self.schedule_table.insertRow(row_position)
                self.schedule_table.setItem(row_position, 0, QTableWidgetItem(event))

    def add_schedule(self):
        """新增行程到選取的日期"""
        selected_date = self.calendar.selectedDate().toString("yyyy-MM-dd")
        new_schedule = self.schedule_input.text().strip()

        if new_schedule:
            # 新增行程至字典
            if selected_date not in self.schedule_data:
                self.schedule_data[selected_date] = []
            self.schedule_data[selected_date].append(new_schedule)

            # 更新 UI
            row_position = self.schedule_table.rowCount()
            self.schedule_table.insertRow(row_position)
            self.schedule_table.setItem(row_position, 0, QTableWidgetItem(new_schedule))

            self.schedule_input.clear()  # 清空輸入框

    def delete_schedule(self):
        """刪除選取的行程"""
        selected_date = self.calendar.selectedDate().toString("yyyy-MM-dd")
        selected_rows = self.schedule_table.selectionModel().selectedRows()

        for row in sorted(selected_rows, reverse=True):  # 反向刪除，避免索引錯誤
            item = self.schedule_table.item(row.row(), 0)
            if item:
                self.schedule_data[selected_date].remove(item.text())
            self.schedule_table.removeRow(row.row())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CalendarPlanner()
    window.show()
    sys.exit(app.exec_())
