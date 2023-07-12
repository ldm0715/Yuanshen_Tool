import json
import os
import configparser


def get_data(label):
    with open("./data/average_probability.json", "r", encoding="utf-8") as f:
        data = json.load(f)
        f.close()
    character_all, character_3, character_4, \
        character_5, character_5_average = deal_show_info(data, label)
    return character_all, character_3, character_4, character_5, character_5_average


def deal_show_info(data: dict, label):
    all = data[label]["总抽数"]
    three = str(data[label]["3星概率"] * 100) + "%"
    four = str(data[label]["4星概率"] * 100) + "%"
    five = str(data[label]["5星概率"] * 100) + "%"
    avarage = data[label]["五星平均抽卡数"]
    return all, three, four, five, avarage




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