import os
import sys
import configparser
from PyQt5.QtWidgets import QApplication, QMainWindow, \
    QWidget, QPushButton, QLabel, QListWidget, QStackedWidget, QListWidgetItem, \
    QDialog, QGridLayout, QScrollArea, QSpacerItem, QSizePolicy, QFileDialog
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtWidgets import QGraphicsBlurEffect
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout
# 导入Qt
from PyQt5.QtCore import Qt
from infobar import InfoBar
from get_show_data import get_data
from data_analysis import run


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init()

    def init(self):
        self.setWindowTitle("原神数据可视化工具")
        self.resize(920, 600)
        # self.setFixedSize(self.width(), self.height())
        self.move(400, 200)

        # 创建一个模糊的背景小部件
        background = QWidget(self)
        background.resize(1920, 1080)
        background.setStyleSheet("background-color:rgba(255, 255, 255);")  # 设置背景小部件半透明白色
        blur_effect = QGraphicsBlurEffect(background)
        blur_effect.setBlurRadius(5)
        background.setGraphicsEffect(blur_effect)

        page0 = Index_Pages()
        page1 = Data_Pages()
        page2 = Album_Pages()

        # 将页面中的按钮变为主窗口的按钮
        self.button1 = page0.button1
        self.button2 = page0.button2
        self.button3 = page2.path_button

        # 创建一个QListWidget用来作为左侧的导航栏
        self.list_widget = QListWidget(self)
        self.list_widget.setStyleSheet(
            "QListWidget::item { height: 40px;}")
        # 设置list_widget的大小
        self.list_widget.setSpacing(5)
        self.list_widget.setFixedWidth(100)
        # 创建一个QStackedWidget用来作为右侧的页面部件
        self.stacked_widget = QStackedWidget(self)

        # 添加布局
        # 创建一个水平布局器
        tal_layout = QHBoxLayout(self)
        # 将左侧的list_widget和右侧的stacked_widget添加到水平布局器中
        tal_layout.addWidget(self.list_widget)
        tal_layout.addWidget(self.stacked_widget, 1)

        # 将左侧的list_widget和右侧的stacked_widget关联起来
        self.list_widget.currentRowChanged.connect(self.stacked_widget.setCurrentIndex)

        self.addTab(page0, "主页")
        self.addTab(page1, "数据")
        self.addTab(page2, "相册")

        # 创建一个小部件作为主窗口的中央小部件
        central_widget = QWidget()
        central_widget.setLayout(tal_layout)

        # 设置为主窗口的中央小部件
        self.setCentralWidget(central_widget)

    def addTab(self, widget, label):
        self.stacked_widget.addWidget(widget)
        item = QListWidgetItem(label)
        font = QFont("宋体", 12)  # 设置字体为 Arial，字体大小为 12 像素
        item.setFont(font)
        # 设置item的对齐方式为居中对齐
        item.setTextAlignment(Qt.AlignCenter)
        # 设置item的flags属性，使其可被选中
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.list_widget.addItem(item)


class Index_Pages(QWidget):
    def __init__(self):
        super().__init__()
        self.init()

    def init(self):
        self.resize(800, 600)
        index_image_path = "./image/index_image.png"
        self.index_image = QLabel("主页图像", self)
        # self.move(0,0)
        # self.index_image.setFixedSize(800, 500)
        self.load_image(index_image_path)

        # 设置样式表显示边框
        self.index_image.setStyleSheet("border: 1px solid black;")

        qspacer1 = QSpacerItem(500, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        qspacer2 = QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        tips = QLabel("快捷指令", self)
        # tips.move(30, 520)
        tips.setFixedSize(80, 50)
        tips.resize(100, 30)

        self.button1 = QPushButton("启动游戏", self)
        # self.button1.move(100, 520)
        self.button1.setFixedSize(120, 50)
        self.button1.setStyleSheet(
            "QPushButton {"
            "background-color: #E0E0E0;"
            "border-radius: 10px;"
            "}"
            "QPushButton:pressed {"
            "background-color: #CCCCCC;"
            "}"
        )
        self.button1.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        self.button2 = QPushButton("截图相册", self)
        # self.button2.move(220, 520)
        self.button2.setFixedSize(120, 50)
        self.button2.setStyleSheet(
            "QPushButton {"
            "background-color: #E0E0E0;"
            "border-radius: 10px;"
            "}"
            "QPushButton:pressed {"
            "background-color: #CCCCCC;"
            "}"
        )
        self.button2.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        Hlayout1 = QHBoxLayout()
        Hlayout1.addWidget(tips)
        Hlayout1.addWidget(self.button1)
        Hlayout1.addWidget(self.button2)
        Hlayout1.addItem(qspacer1)

        author = QLabel("作者：gcnanmu", self)
        # author.move(650, 550)
        author.setFixedSize(100, 50)

        Hlayout2 = QHBoxLayout()
        Hlayout2.addItem(qspacer2)
        Hlayout2.addWidget(author)

        Vlayout = QVBoxLayout()
        Vlayout.addWidget(self.index_image)
        Vlayout.addLayout(Hlayout1)
        Vlayout.addLayout(Hlayout2)

        self.setLayout(Vlayout)

    def load_image(self, image_path):
        pixmap = QPixmap(image_path)
        scaled_pixmap = pixmap.scaled(self.width(), self.height() - 50, Qt.KeepAspectRatio)
        self.index_image.setPixmap(scaled_pixmap)
        self.index_image.setScaledContents(True)


class Data_Pages(QWidget):
    def __init__(self):
        super().__init__()
        self.init()

    def init(self):

        # 创建一个滚动区域
        scroll = QScrollArea()
        # 设定滚动区域的widgetResizable属性为True，这将允许滚动区域自动调整其内容
        scroll.setWidgetResizable(True)

        # 创建一个QWidget作为滚动区域的内容
        scroll_content = QWidget(scroll)

        # 在这个QWidget上添加你的布局
        scroll_layout = QVBoxLayout(scroll_content)

        button = QPushButton("获取数据", self)
        button.clicked.connect(self.get_wish_data)

        title_font = QFont("黑体", 15)
        font = QFont("宋体", 12)

        character_all, character_3, character_4, \
            character_5, character_5_average = get_data("角色活动祈愿")
        weapon_all, weapon_3, weapon_4, \
            weapon_5, weapon_5_average = get_data("武器活动祈愿")
        standard_all, standard_3, standard_4, \
            standard_5, standard_5_average = get_data("常驻祈愿")

        qhbox1 = QHBoxLayout()
        qvbox1 = QVBoxLayout()
        character_label = QLabel("角色活动祈愿", self)
        character_label.setFont(title_font)
        info1 = f"总计:  {character_all}\n五星概率:  {character_5}\n" \
                f"四星概率:  {character_4}\n三星概率:  {character_3}\n五星平均抽取次数:  {character_5_average}"
        character_all_label = QLabel(info1, self)
        character_all_label.setFont(font)
        qvbox1.addWidget(character_label)
        qvbox1.addWidget(character_all_label)

        character_all_label.move(50, 50)
        character_image_label = QLabel("角色活动祈愿", self)
        pixmap1 = QPixmap("./image/角色活动祈愿.png")
        self.load_image(pixmap1, character_image_label, 500, 500)
        qhbox1.addLayout(qvbox1)
        qhbox1.addWidget(character_image_label)

        qhbox2 = QHBoxLayout()
        qvbox2 = QVBoxLayout()
        weapon_label = QLabel("武器活动祈愿", self)
        weapon_label.setFont(title_font)
        info2 = f"总计:  {weapon_all}\n五星概率:  {weapon_5}\n" \
                f"四星概率:  {weapon_4}\n三星概率:  {weapon_3}\n五星平均抽取次数:  {weapon_5_average}"
        weapon_all_label = QLabel(info2, self)
        weapon_all_label.setFont(font)

        qvbox2.addWidget(weapon_label)
        qvbox2.addWidget(weapon_all_label)

        weapon_all_label.move(50, 150)
        weapon_image_label = QLabel("武器活动祈愿", self)
        # weapon_all_label.move(150,50)
        pixmap2 = QPixmap("./image/武器活动祈愿.png")
        self.load_image(pixmap2, weapon_image_label, 500, 500)

        qhbox2.addLayout(qvbox2)
        qhbox2.addWidget(weapon_image_label)

        qhbox3 = QHBoxLayout()
        qvbox3 = QVBoxLayout()

        standard_label = QLabel("常驻祈愿", self)
        standard_label.setFont(title_font)
        info3 = f"总计:  {standard_all}\n五星概率:  {standard_5}\n" \
                f"四星概率:  {standard_4}\n三星概率:  {standard_3}\n五星平均抽取次数:  {standard_5_average}"
        standard_all_label = QLabel(info3, self)
        standard_all_label.setFont(font)
        # standard_all_label.move(50, 250)

        qvbox3.addWidget(standard_label)
        qvbox3.addWidget(standard_all_label)

        standard_image_label = QLabel("常驻祈愿", self)
        # standard_all_label.move(150, 50)
        pixma3 = QPixmap("./image/常驻祈愿.png")
        self.load_image(pixma3, standard_image_label, 500, 500)

        qhbox3.addLayout(qvbox3)
        qhbox3.addWidget(standard_image_label)

        scroll_layout.addWidget(button)
        scroll_layout.addLayout(qhbox1)
        scroll_layout.addLayout(qhbox2)
        scroll_layout.addLayout(qhbox3)

        # 将QWidget设置为滚动区域的内容
        scroll.setWidget(scroll_content)

        # 最后，将滚动区域设置为窗口的布局
        self.setLayout(QVBoxLayout(self))
        self.layout().addWidget(scroll)

    def load_image(self, pixmap, label, w, h):
        scaled_pixmap = pixmap.scaled(w, h, Qt.KeepAspectRatio)
        label.setPixmap(scaled_pixmap)
        label.setScaledContents(True)

    def get_wish_data(self):
        wish_path = read_ini()["wishlog"]
        inspection = wish_path.split(".")[-1]
        print(inspection)
        if os.path.exists(wish_path) & (inspection == "json"):

            message = run(wish_path)
            self.showInfoBar(message)
        elif wish_path == "":
            return
        else:
            self.showInfoBar("wishlog路径错误!")
            wish_path = open_file()
            write_ini("wishlog", wish_path)
            self.get_wish_data()

    def showInfoBar(self, message):
        infoBar = InfoBar(message, parent=self)
        infoBar.show()
        infoBar.adjustSize()
        infoBar.move(self.width() / 2 - infoBar.width() / 2, self.height() - infoBar.height())


class Album_Pages(QWidget):
    def __init__(self):
        super().__init__()
        self.image_path = []
        self.init()

    def init(self):
        self.albumWidget = QWidget(self)
        self.path_button = QPushButton("打开相册路径", self)
        self.path_button.clicked.connect(self.get_album_path)

        self.album = QGridLayout()
        # 将album往下移动一点
        # self.album.setContentsMargins(0, 10, 0, 0)
        self.albumWidget.setLayout(self.album)

        # 创建一个垂直布局器
        self.Vlayout = QVBoxLayout(self)

        # 创建QScrollArea
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(self.albumWidget)

        self.Vlayout.addWidget(self.path_button)
        self.Vlayout.addWidget(scroll_area)
        if self.image_path != []:
            self.loadImages(self.image_path)
        self.setLayout(self.Vlayout)

    def loadImages(self, path):
        # 首先清除当前的图片标签
        for i in reversed(range(self.album.count())):
            widget_to_remove = self.album.itemAt(i).widget()
            self.album.removeWidget(widget_to_remove)
            widget_to_remove.setParent(None)
        # 假设在当前文件夹有名为 'image1.jpg', 'image2.jpg', 'image3.jpg' 的图片
        image_files = path

        for i, image_file in enumerate(image_files):
            pixmap = QPixmap(image_file)
            # 根据QLabel的大小缩放图片
            scaled_pixmap = pixmap.scaled(self.width() / 2, self.height() / 2, Qt.KeepAspectRatio)

            label = ImageLabel(scaled_pixmap, pixmap)
            # label.setFixedSize(QSize(100, 100))  # 设置QLabel的大小

            # 每两个图片换一行
            row = i // 2
            col = i % 2
            self.album.addWidget(label, row, col)
            self.showInfoBar("加载完成！")

    def showInfoBar(self, message):
        infoBar = InfoBar(message, parent=self)
        infoBar.show()
        infoBar.adjustSize()
        infoBar.move(self.width() / 2 - infoBar.width() / 2, self.height() - infoBar.height())

    def get_album_path(self):
        album_path = read_ini()["album"]
        inspection = album_path.split("/")[-1]
        print(inspection)
        if os.path.exists(album_path) & (inspection == "ScreenShot"):
            files = os.listdir(album_path)
            for i in range(len(files)):
                new_path = album_path + "\\" + files[i]
                files[i] = new_path
            print(files)
            self.image_path = files
            self.loadImages(files)
        else:
            self.showInfoBar("相册路径错误！请回到主页重新选择！")

    def resizeEvent(self, event):
        print('窗口大小已改变：', self.size())
        super(Album_Pages, self).resizeEvent(event)
        self.loadImages(self.image_path)


class ImageViewer(QDialog):
    def __init__(self, pixmap):
        super().__init__()
        self.label = QLabel(self)
        self.label.resize(1536, 864)
        self.label.setPixmap(pixmap)
        self.label.setScaledContents(True)


class ImageLabel(QLabel):
    def __init__(self, pixmap, originalPixmap):
        super().__init__()
        self.setPixmap(pixmap)
        self.originalPixmap = originalPixmap

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.imageViewer = ImageViewer(self.originalPixmap)
            self.imageViewer.show()


def read_ini():
    path = "./path.ini"
    config = configparser.ConfigParser()
    config.read(path)

    path_dict = dict()
    wishlog_path = config.get("wishlog", "path")
    path_dict["wishlog"] = wishlog_path
    print(wishlog_path)
    album_path = config.get("album", "path")
    path_dict["album"] = album_path
    print(album_path)
    game_path = config.get("game", "path")
    path_dict["game"] = game_path
    print(game_path)
    return path_dict


def write_ini(label, new_path):
    path = "./path.ini"
    config = configparser.ConfigParser()
    config.read(path)

    config.set(label, 'path', new_path)
    print(config)
    with open(path, 'w') as configfile:
        config.write(configfile)


def open_file():
    # 选取文件
    try:
        file_path = QFileDialog.getOpenFileName(None, "选择文件", "/")
        if file_path == "":
            return ""
    except:
        file_path = ""
    finally:
        # print(folder_path)
        return file_path[0]


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
