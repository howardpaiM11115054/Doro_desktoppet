from PyQt5.QtCore import Qt, QTimer, QPropertyAnimation, QPoint
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QMenu
from PyQt5 import QtGui
import os
import sys
import random


class Deskpet(QWidget):
    tool_name = 'Doro'

    def __init__(self, parent=None, **kwargs):
        super(Deskpet, self).__init__(parent)

        # Pet counters
        self.against=0
        self.stop=False
        self.sleep_counter = 0
        self.dark_counter = 0
        self.death_counter=0
        self.nope_counter=0
        self.animation_type = 'walk'  # animation type

        # window for invisible
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.SubWindow)
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

    
    def load_frames(self, folder):
        """加載所有動畫類型的幀"""
        frames = {
            'walk': [],
            'dark': [],
            'death': [],
            'sleep': [],
            'death':[],
            'Nope':[]
        }

        animation_types = ['walk', 'dark', 'death', 'sleep','death','Nope']
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
        


    def contextMenuEvent(self, event):
        """右鍵菜單事件"""
        # 創建一個 QMenu
        self.setStyleSheet("QMenu{background:rgb(255,102,204);margin: 0;padding: 5px;border-radius: 20px;}"
                           "QMenu::item{background:rgb(255,189,255);}"
                           "QMenu::separator{height:9px}")
        menu = QMenu(self)
        

        # 添加操作（QAction）
        action_exit = menu.addAction("EXIT")  # 添加一個 "退出" 選項
        action_kill = menu.addAction("Kill") 
        action_stop = menu.addAction("Stop")
        action_move = menu.addAction("Move")
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
    def random_move(self):
        """讓桌寵隨機移動"""
        if self.stop==False and self.animation_type=='walk':
            screen_geometry = QApplication.primaryScreen().availableGeometry()
            screen_width = screen_geometry.width()
            screen_height = screen_geometry.height()

            # 隨機新位置
            new_x = random.randint(0, screen_width - self.width())
            new_y = random.randint(0, screen_height - self.height())
            
            # 動畫移動
            self.animation = QPropertyAnimation(self, b"pos")
            self.animation.setDuration(2000)  # 動畫持續時間 (毫秒)
            self.animation.setEndValue(QPoint(new_x, new_y))
            self.animation.start()
        else:
            pass

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # 創建 Deskpet 實例
    pet = Deskpet()
    pet.show()

    sys.exit(app.exec_())
