import sys
import os
import subprocess
import configparser
from PyQt5.QtWidgets import QApplication, QFileDialog
from PyQt5.QtGui import QIcon
from main_ui import MainWindow
from infobar import InfoBar

# 设置任务栏图标
import ctypes

# 项目基础路径
BASE_DIR = os.path.dirname(os.path.realpath(sys.argv[0]))

ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("myappid")
# 图标路径
ICO_PATH = os.path.join(BASE_DIR, "./image/app.ico")

wishlog_path = None
album_path = None
game_path = None

app = QApplication(sys.argv)
window = MainWindow()


def open_game():
    game_path = read_ini()["game"]
    inspection = game_path[3:]
    print(inspection)
    inspection_list = ["Genshin Impact/launcher.exe", "Genshin Impact Game/YuanShen.exe"]
    if os.path.exists(game_path) & (inspection in inspection_list):
        # subprocess.Popen(path, shell=True)
        bash_command = game_path
        subprocess.run(bash_command, capture_output=True, shell=True)
        showInfoBar(window, message="游戏打开成功")
    else:
        showInfoBar(window, message="游戏路径不存在,请重新选择")
        game_path = open_file()
        write_ini("game", game_path)
        open_game()


def open_album():
    album_path = read_ini()["album"]
    inspection = album_path.split("/")[-1]
    print(inspection)
    if os.path.exists(album_path) & (inspection == "ScreenShot"):
        # files = os.listdir(album_path)
        # print(files)
        # 打开文件夹
        os.startfile(album_path)
        showInfoBar(window, message="文件夹已打开")
    else:
        showInfoBar(window, message="文件夹路径不存在,请重新选择")
        album_path = open_foler()
        write_ini("album", album_path)
        open_album()


def showInfoBar(window, message):
    infoBar = InfoBar(message, parent=window)
    infoBar.show()
    infoBar.adjustSize()
    infoBar.move(window.width() / 2 - infoBar.width() / 2, window.height() - infoBar.height())


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


# 实现打开文件操作
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


def open_foler():
    # 选取文件
    try:
        folder_path = QFileDialog.getExistingDirectory(None, "选择文件夹", "/")
        if folder_path == "":
            return ""
    except:
        folder_path = ""
    finally:
        return folder_path


window.button1.clicked.connect(open_game)
window.button2.clicked.connect(open_album)
window.setWindowIcon(QIcon(ICO_PATH))
window.show()
sys.exit(app.exec_())
