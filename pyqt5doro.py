from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QMenu
import os
import sys
import random


class Deskpet(QWidget):
    tool_name = 'Doro'

    def __init__(self, parent=None, **kwargs):
        super(Deskpet, self).__init__(parent)

        # Pet counters
        self.sleep_counter = 0
        self.dark_counter = 0
        self.animation_type = 'walk'  # 預設動畫類型

        # 設置窗口透明和無邊框
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.SubWindow)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.resize(900, 900)

        # 初始化圖片
        self.image_label = QLabel(self)
        self.image_label.setScaledContents(True)  # 自動縮放圖片以適應窗口大小

        # 加載圖片
        self.frames = self.load_frames("img")  # 替換為你的動畫圖片文件夾路徑
        self.current_frame = 0

        # 設置定時器進行動畫切換
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(100)  # 每 100 毫秒更新一幀

    def load_frames(self, folder):
        """加載所有動畫類型的幀"""
        frames = {
            'walk': [],
            'dark': [],
            'death': [],
            'sleep': []
        }

        animation_types = ['walk', 'dark', 'death', 'sleep']
        for animation in animation_types:
            animation_folder = os.path.join(folder, animation)
            num_of_frames = len(os.listdir(animation_folder))-1
            for i in range(num_of_frames):
                path = os.path.join(animation_folder, f"0{i}.png")
                if os.path.exists(path):
                    pixmap = QPixmap(path)
                    scaled_pixmap = pixmap.scaled(
                        pixmap.width() * 3, pixmap.height() * 3, Qt.KeepAspectRatio
                    )
                    frames[animation].append(scaled_pixmap)
                else:
                    print(f"圖片未找到: {path}")
        return frames

    def animation_types(self):
        """更新當前的動畫類型"""
        if self.sleep_counter > 0:
            self.sleep_counter -= 1
            self.animation_type = 'sleep'
        elif self.dark_counter > 0:
            self.dark_counter -= 1
            self.animation_type = 'dark'
        else:
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
        self.animation_types()  # 更新動畫類型

        # 獲取當前動畫類型的幀列表
        current_frames = self.frames.get(self.animation_type, [])
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

    def mouseReleaseEvent(self, event):
        """釋放滑鼠"""
        if event.button() == Qt.LeftButton:
            self.old_pos = None  # 清空舊位置


    def contextMenuEvent(self, event):
        """右鍵菜單事件"""
        # 創建一個 QMenu
        menu = QMenu(self)

        # 添加操作（QAction）
        action_exit = menu.addAction("退出")  # 添加一個 "退出" 選項

        # 在鼠標位置顯示菜單
        action = menu.exec_(self.mapToGlobal(event.pos()))

        # 判斷選擇的選項
        if action == action_exit:
            self.close() 
            sys.exit(app.exec_()) # 如果選擇了 "退出"，則關閉窗口


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # 創建 Deskpet 實例
    pet = Deskpet()
    pet.show()

    sys.exit(app.exec_())
