from PyQt5.QtCore import Qt, QTimer, QPropertyAnimation, QPoint,QDate
from PyQt5.QtGui import QPixmap,QTextCharFormat,QColor
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QMenu,QMessageBox, QMainWindow, QAction
import webbrowser
from PyQt5 import QtGui
import timer_win
import schedual_EN_doro
import os
import sys
import random
import json

class Deskpet(QWidget):
    tool_name = 'Doro'

    def __init__(self, parent=None, **kwargs):
        super(Deskpet, self).__init__(parent)
        self.clocktimer=QTimer
        # Pet counters
        self.against=0
        self.stop=False
        self.sleep_counter = 0
        self.dark_counter = 0
        self.death_counter=0
        self.nope_counter=0
        self.timer_counter=0
        self.animation_type = 'walk'  # animation type

        # window for invisible
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint )
        # | Qt.SubWindow
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.resize(900, 900)



        # init load
        self.image_label = QLabel(self)
        self.image_label.setScaledContents(True) 
         # 自動縮放圖片以適應窗口大小

        # 加載圖片
        self.frames = self.load_frames("img")  # 替換為你的動畫圖片文件夾路徑
        self.current_frame = 0

        # 設置定時器進行動畫切換
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(100)  # 每 100 毫秒更新一幀

        # 定時器用於桌寵移動
        self.timer_move = QTimer(self)
        
        self.timer_move.timeout.connect(self.random_move)
        self.timer_move.start(2000)  # 每2秒移動一次

       # ✅ 檢查今天是否有行程
        self.schedule_manager = schedual_EN_doro.CalendarPlanner()  # ✅ 創建行程管理器
        if self.schedule_manager.check_today_schedule():
            self.mark_with_green_dot()  # ✅ 如果有行程，顯示綠點

    def mark_with_green_dot(self):
        """在 Deskpet 上顯示一個小綠點"""
        self.dot_label = QLabel(self)
        self.dot_label.setGeometry(40, 10, 20, 20)  # ✅ 設置綠點位置 (右上角)
        self.dot_label.setStyleSheet("background-color: green; border-radius: 10px;")  # ✅ 圓形綠點
        self.dot_label.show()  


    def start_timer(self):
        """開始倒數計時"""
        try:
            input_time = int(self.input_box.text())  # 取得輸入的秒數
            if input_time <= 0:
                raise ValueError  # 確保輸入為正數
            self.remaining_time = input_time
            self.timer_label.setText(f"剩餘時間: {self.remaining_time} 秒")
            self.clocktimer.start(1000)  # 每秒更新一次
        except ValueError:
            QMessageBox.warning(self, "輸入錯誤", "請輸入有效的正整數！")

    def update_timer(self):
        """更新倒計時"""
        if self.remaining_time > 0:
            self.remaining_time -= 1
            self.timer_label.setText(f"剩餘時間: {self.remaining_time} 秒")
        else:
            self.timer_label.setText("時間到！")
            self.clocktimer.stop()  # 停止計時器
    
    def load_frames(self, folder):
        """加載所有動畫類型的幀"""
        frames = {
            'walk': [],
            'dark': [],
            'death': [],
            'sleep': [],
            'death':[],
            'Nope':[],
            'Timer':[]
        }

        animation_types = ['walk', 'dark', 'death', 'sleep','death','Nope','Timer']
        for animation in animation_types:
            animation_folder = os.path.join(folder, animation)
            num_of_frames = len(os.listdir(animation_folder))-1
            for i in range(num_of_frames):
                path = os.path.join(animation_folder, f"0{i}.png")
                if os.path.exists(path):
                    pixmap = QPixmap(path)
                    scaled_pixmap = pixmap.scaled(
                        pixmap.width() * 4, pixmap.height() * 4, Qt.KeepAspectRatio
                    )
                    frames[animation].append(scaled_pixmap)
                else:
                    print(f"圖片未找到: {path}")
        return frames

    def animation_types(self):
        """更新當前的動畫類型"""
        if self.timer_counter>0:
            self.animation_type ='Timer'
            return
        if self.nope_counter > 0:
            self.sleep_counter=0
            self.dark_counter=0
            self.nope_counter -= 1
            self.animation_type = 'Nope'
            return
        if self.death_counter > 0:
            self.death_counter -= 1
            self.animation_type = 'death'
            return
        if self.sleep_counter > 0:
            self.sleep_counter -= 1
            self.animation_type = 'sleep'
            return
        if self.dark_counter > 0:
            self.dark_counter -= 1
            self.animation_type = 'dark'
            return
        
        # 隨機選擇動畫類型
        if random.randint(1, 200) == 2:
            self.animation_type = 'sleep'
            self.sleep_counter = 40
        elif random.randint(1, 100) == 1:
            self.animation_type = 'dark'
            self.dark_counter = 60
        else:
            self.animation_type = 'walk'
    def update_frame(self):
        
        """切換到下一幀"""
        # 獲取當前動畫類型的幀列表
        current_frames = self.frames.get(self.animation_type, [])
        self.animation_types()  # 更新動畫類型
        if not current_frames:  # 如果列表為空
            print(f"動畫類型 {self.animation_type} 沒有可用幀")
            return

        # 確保索引不超出範圍
        if self.current_frame >= len(current_frames):
            self.current_frame = 0

        # 更新圖片
        self.image_label.setPixmap(current_frames[self.current_frame])
        self.image_label.resize(current_frames[self.current_frame].size())

        # 更新幀索引
        self.current_frame += 1

    def mousePressEvent(self, event):
        """支持滑鼠拖動"""
        if event.button() == Qt.LeftButton:
            self.old_pos = event.globalPos()  # 記錄鼠標位置

    def mouseMoveEvent(self, event):
        """拖動窗口"""
       
        if hasattr(self, "old_pos") and self.old_pos is not None:
                delta = event.globalPos() - self.old_pos
                self.move(self.x() + delta.x(), self.y() + delta.y())
                self.old_pos = event.globalPos()  # 更新舊位置
                self.against+=1
        
            

    def mouseReleaseEvent(self, event):
        """釋放滑鼠"""
        if event.button() == Qt.LeftButton:
            self.animation_type = 'Nope'  # 切換動畫類型為 'death'
            self.current_frame = 0  # 重置動畫幀索引，從頭開始播放動畫
            self.nope_counter=30
            self.old_pos = None 
            
            self.move(self.x() , self.y() )#反抗
            self.against-=1 # 清空舊位置
    # def mousePressEvent(self, event): 這樣會沒辦法拉
    #     """左鍵按下事件"""
    #     if event.button() == Qt.LeftButton:  # 檢查是否是左鍵
    #         print("e04")  # Debug 信息
    #         self.animation_type = 'death'  # 切換動畫類型為 'death'
    #         self.current_frame = 0  # 重置動畫幀索引，從頭開始播放動畫
        

    def open_website(self):
        """用默認瀏覽器打開網站"""
        url = "https://github.com/howardpaiM11115054/Doro_desktoppet_exe.git"  # 替換為您的網站連結
        webbrowser.open(url)
    def contextMenuEvent(self, event):
        """右鍵菜單事件"""
        # 創建一個 QMenu
        self.setStyleSheet("QMenu{background:rgb(255,102,204);margin: 0;padding: 5px;border-radius: 20px;}"
                           "QMenu::item{background:rgb(255,189,255);}"
                           "QMenu::separator{height:9px}"
                           "QMenu::separator{border-radius: 10px}"
                           )
        menu = QMenu(self)
        

        # 添加操作（QAction）
        action_exit = menu.addAction("EXIT")  # 添加一個 "退出" 選項
        action_kill = menu.addAction("Kill") 
        action_stop = menu.addAction("Stop")
        action_move = menu.addAction("Move")
        action_timer=menu.addAction("time")
        action_link = menu.addAction("github")
        action_schedual = menu.addAction("schedual")

        # 為 action_link 綁定觸發事件
        action_link.triggered.connect(self.open_website)
        #set icon
        '''add a label'''
        path_kill=os.path.join('img','icon','Kill.png')
        action_kill.setIcon(QtGui.QIcon(path_kill))
        path_exit=os.path.join('img','icon','Exit.png')
        action_exit.setIcon(QtGui.QIcon(path_exit))
        path_stop=os.path.join('img','icon','Stop.png')
        action_stop.setIcon(QtGui.QIcon(path_stop))
        path_move=os.path.join('img','icon','Move.png')
        action_move.setIcon(QtGui.QIcon(path_move))
        path_link=os.path.join('img','icon','GitHub.png')
        action_link.setIcon(QtGui.QIcon(path_link))
        path_timer=os.path.join('img','icon','Timer.png')
        action_timer.setIcon(QtGui.QIcon(path_timer))
        path_Dochedual=os.path.join('img','icon','Dochedual.png')
        action_schedual.setIcon(QtGui.QIcon(path_Dochedual))


        # 在鼠標位置顯示菜單
        action = menu.exec_(self.mapToGlobal(event.pos()))
        
        # 判斷選擇的選項
        if action == action_move:
            self.stop=False
        if action == action_stop:
            self.stop=True
        if action ==action_kill:
            self.animation_type = 'death'  # 切換動畫類型為 'death'
            self.current_frame = 0  # 重置動畫幀索引，從頭開始播放動畫
            self.death_counter=50
            # self.update_frame()
        if action == action_exit:
            self.close() 
            sys.exit(app.exec_()) # 如果選擇了 "退出"，則關閉窗口
        if action == action_timer:
           self.animation_type='Timer'
           self.timer_counter=1
           self.stop=True
           self.open_timer_window()
        if action == action_schedual:
            self.open_schedual()
          

    def open_timer_window(self):
        """打開計時器視窗，確保計時結束時恢復桌寵運行"""
        if not hasattr(self, "timer_window") or self.timer_window is None:
            self.timer_window = timer_win.TimerWindow(self)

        # ✅ 監聽 `finished` 事件，而不是 `destroyed`
        self.timer_window.finished.connect(self.on_timer_window_closed)

        self.stop = True  # 停止桌寵
        self.timer_window.show()
    def open_schedual(self):
        """Open the schedule window separately"""
        self.schedual = schedual_EN_doro.CalendarPlanner()
        self.schedual.show()  # ✅ Use show() instead of exec_()
    # def open_schedual(self):
    # """開啟行程視窗，確保 Deskpet 不會跟著關閉"""
    
    # # ✅ 如果 `self.schedual` 存在但已被刪除，就重新創建
    # if hasattr(self, 'schedual') and self.schedual is not None:
    #     if not self.schedual.isVisible():
    #         self.schedual = schedual_EN_doro.CalendarPlanner()  # ✅ 重新創建新視窗
    #         self.schedual.setAttribute(Qt.WA_DeleteOnClose, True)  # ✅ 關閉時刪除物件
    #         self.schedual.show()
    #     else:
    #         self.schedual.activateWindow()  # ✅ 視窗還在時，讓它浮到最前
    # else:
    #     self.schedual = schedual_EN_doro.CalendarPlanner()  # ✅ 創建新視窗
    #     self.schedual.setAttribute(Qt.WA_DeleteOnClose, True)
    #     self.schedual.show()

    



    def on_timer_window_closed(self):
        """當計時器視窗關閉時，恢復桌寵運行"""
        print("[DEBUG] 計時視窗已關閉，桌寵恢復移動")
        self.stop = False  # 恢復桌寵移動
        self.timer_counter=0
        print(f"[DEBUG] self.stop 設定為: {self.stop}")  # 確認 stop 狀態

    

    def random_move(self):
        """讓桌寵隨機移動，並確保計時視窗始終位於其正下方"""
        
        if self.stop is False and self.animation_type == 'walk':
            screen_geometry = QApplication.primaryScreen().availableGeometry()
            screen_width = screen_geometry.width()
            screen_height = screen_geometry.height()

            # 計算桌寵新位置
            new_x = random.randint(0, screen_width - self.width())
            new_y = random.randint(0, screen_height - self.height())

           

            # 設定桌寵移動動畫
            self.animation = QPropertyAnimation(self, b"pos")
            self.animation.setDuration(2000)
            self.animation.setEndValue(QPoint(new_x, new_y))
            self.animation.start()



if __name__ == "__main__":
    app = QApplication(sys.argv)
    # ✅ 創建主應用視窗
    
    # 創建 Deskpet 實例
    pet = Deskpet()
    pet.show()

    sys.exit(app.exec_())
