<p align="center">
  <img width="15%" align="center" src="https://z4a.net/images/2023/07/12/Yuanshen_Tool_logo.png" alt="logo">
</p>
  <h1 align="center">
  Yuanshen Tool
</h1>
<p align="center">
<img src="https://img.shields.io/badge/Version-v1.0-green?style=flat&logo">
<img src="https://img.shields.io/badge/Platform-Win|macOS-blue?color=#4ec820" alt="Platform Win|macOS"/>
<img src="https://img.shields.io/badge/Python-3.7%20-blue?color=#4ec820" alt="Python 3.7"/>
</p>
<p align="center">
  原神小工具
</p>

<p align="center">
  <img width="70%" align="center" src="https://z4a.net/images/2023/07/12/Yuanshen_Tool_index.png" alt="ui">
</p>

## 运行与使用说明

本界面使用`PyQt5`编写，相关代码可以在项目文件中查看。



主要功能如下：
1. 打开游戏，打开游戏截图文件夹。
  <p align="center">
  <img width="70%" align="center" src="https://z4a.net/images/2023/07/12/Yuanshen_Tool_index.png" alt="ui">
</p>
2. 处理抽卡祈愿数据，自动分析相关数据，最后显示在界面上。
  <p align="center">
  <img width="70%" align="center" src="https://z4a.net/images/2023/07/12/show_wish_data.png" alt="ui">
</p>
3. 游戏截图相册，可以查看游戏截图。
  <p align="center">
  <img width="70%" align="center" src="https://z4a.net/images/2023/07/12/ablum.png" alt="ui">
</p>

## 使用方法

项目文件结构（多余文件不展示）：

```Dir Tree
Yuanshen_Tool_v1.0
├─ data
│    ├─ Wishlog_163056907_20230711_113840.json
│    └─ average_probability.json
├─ image
│    ├─ app.ico
│    └─ index_image.png
├─ path.ini
└─ run.exe
```

本工具为傻瓜式操作，但是**需要知道相应文件夹的作用，否则会出现无法使用的情况。**

* path.ini：配置文件，用于配置游戏截图文件夹路径（可自行修改）。
  * wishlog：祈愿数据文件夹路径。
  * game：游戏启动路径。
  * ablum：游戏截图相册文件夹路径。
* run.exe：程序运行文件。
* data：祈愿数据文件夹，用于存放祈愿数据。
  * 祈愿数据必须为json格式
  * 祈愿数据必须遵循原神祈愿数据格式：https://github.com/DGP-Studio/Snap.Genshin/wiki/StandardFormat
* image：图片文件夹，用于存放程序运行所需图片。
  * app.ico：程序图标。
  * index_image.png：程序启动界面图片。
* 其他文件：程序运行所需文件。

## 注意事项

**本项目为试水，由于本人水平有限，不是很好用（自己都不用）**。
测试时在大部分场景应该是没问题的，但肯定也有其他问题。上传只是为了存储，**祝大家使用愉快**。

Copyright © 2023 by gcnanmu.
