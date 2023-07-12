import sys
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QLabel, QWidget
from PyQt5.QtGui import QFont

class InfoBar(QWidget):
    def __init__(self, message, timeout=2, parent=None):
        super().__init__(parent)
        self.setAutoFillBackground(True)
        self.setStyleSheet("background-color: #007BFF; color: #FFF; padding: 10px; border-radius: 4px;border-radius: 10px;")
        self.layout = QVBoxLayout()
        self.messageLabel = QLabel(message)
        self.messageLabel.setFont(QFont('Arial', 12)) # Set font size
        self.layout.addWidget(self.messageLabel)
        self.setLayout(self.layout)
        # 指定的时间后发送一个信号或者定期发送信号
        self.timer = QTimer()
        # 设置了定时器为单次定时器
        self.timer.setSingleShot(True)
        # 定时器超时后发送信号
        self.timer.timeout.connect(self.close)
        # 定时器启动
        self.timer.start(timeout * 1000)

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.resize(800,600)
        self.button = QPushButton('Show InfoBar', self)
        self.button.clicked.connect(self.showInfoBar)
        self.setCentralWidget(self.button)

    def showInfoBar(self):
        self.infoBar = InfoBar("This is an info message.", parent=self)
        self.infoBar.show()
        self.infoBar.adjustSize()
        self.infoBar.move(0, self.height() - self.infoBar.height())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
