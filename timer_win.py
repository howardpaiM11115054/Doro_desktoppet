from PyQt5.QtCore import QTimer,Qt,QUrl
from PyQt5.QtWidgets import QDialog, QLabel, QVBoxLayout, QPushButton, QLineEdit, QMessageBox
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
# self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.SubWindow)
# self.setAttribute(Qt.WA_TranslucentBackground, True)
class TimerWindow(QDialog):
    """獨立的計時器視窗"""
    # timer_finished = pyqtSignal(bool)  
    def __init__(self, parent=None):
        
        super().__init__(parent)
        
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.SubWindow)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setGeometry(150, -70, 300, 200)
        
        self.layout = QVBoxLayout()
        self.timer_label = QLabel("PLS enter Time", self)
        self.timer_label.setFixedWidth(180)  # 設定固定寬度為 150 像素




        self.layout.addWidget(self.timer_label)

        self.input_box = QLineEdit(self)
        self.input_box.setStyleSheet("""
                                    QLineEdit {
                                        border: 2px solid rgb(255,153,204);  /* 邊框顏色 */
                                        border-radius: 8px;  /* 圓角 */
                                        padding: 5px;
                                        font-size: 16px;
                                        background-color: white;
                                    }
                                """)

        self.input_box.setPlaceholderText("enter time...")
        self.input_box.setFixedWidth(180)
        self.layout.addWidget(self.input_box)

        self.start_button = QPushButton("Start", self)
        self.start_button.setStyleSheet("""
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

        self.start_button.setFixedWidth(180)  # 設定輸入框寬度為 100 像素
        self.start_button.clicked.connect(self.start_timer)
        self.layout.addWidget(self.start_button)

        self.setLayout(self.layout)

        self.remaining_time = 0
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer)

    def start_timer(self):
        """開始倒數計時"""
        try:
            input_time = int(self.input_box.text().strip())  # 取得輸入的秒數
            if input_time <= 0:
                raise ValueError  # 確保輸入為正數
            self.remaining_time = input_time
            min_time=self.remaining_time//60
            s_time=self.remaining_time%60
            self.timer_label.setText(f"Time: {min_time:02d}:{s_time:02d} s")
            self.timer_label.setStyleSheet("font-size: 32px; font-weight: bold;")  # ✅ 設定字體大小
            # ✅ 隱藏輸入框與按鈕
            self.input_box.hide()
            self.start_button.hide()
            print(f"[DEBUG] 計時開始，倒數 {self.remaining_time} 秒")
            self.timer.start(1000)  # 每秒更新一次
        except ValueError:
            QMessageBox.warning(self, "type error", "PLS check！")

    def update_timer(self):
        """更新倒計時"""
        if self.remaining_time > 0:
            self.remaining_time -= 1
            min_time=self.remaining_time//60
            s_time=self.remaining_time%60
            self.timer_label.setText(f"Time: {min_time:02d}:{s_time:02d} s")
            self.timer_label.setStyleSheet("font-size: 32px; font-weight: bold;")  
        else:
            self.timer_label.setText("Time out！")
            self.timer.stop()  # 停止計時器
            # ✅ 播放聲音
            self.player = QMediaPlayer()
            self.player.setMedia(QMediaContent(QUrl.fromLocalFile("doro.mp3")))  # 指定音效檔案
            self.player.setVolume(50)  # 設定音量 (0~100)
            self.player.play()
            
           # ✅ 等待 10 秒後自動關閉視窗,,
            QTimer.singleShot(4000, lambda: (self.close(), self.input_box.show(), self.start_button.show()))  # ✅ 正確

            # QTimer.singleShot(2000, self.close)
            # QTimer.singleShot(2100, self.input_box.show())
            # QTimer.singleShot(2100, self.start_button.show())
            
            
    
    # def closeEvent(self, event):
    #     """當視窗關閉時，重設計時器視窗的狀態"""
    #     self.timer.stop()
    #     self.timer_label.setText("請輸入倒數秒數")
        
    #     self.remaining_time = 0  # 重設倒數時間
    #     event.accept()  # 允許關閉視窗    
            
