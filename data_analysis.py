import os
import json
from matplotlib import pyplot as plt

# https://github.com/DGP-Studio/Snap.Genshin/wiki/StandardFormat

plt.rc("font", family='SimHei', size=13)


# 100	新手祈愿
# 200	常驻祈愿
# 301	角色活动祈愿
# 400	角色活动祈愿-2
# 302	武器活动祈愿




def get_data(path):
    file = open(path, "r", encoding="utf-8")
    json_data = json.load(file)
    data = json_data["list"]
    data_dict = dict()
    for item in data:
        # 按照gacha_type分类
        gacha_type = item["gacha_type"]
        name = item["name"]
        item_type = item["item_type"]
        rank_type = item["rank_type"]

        if gacha_type not in data_dict:
            data_dict[gacha_type] = {}

        if name not in data_dict[gacha_type]:
            data_dict[gacha_type][name] = {"item_type": item_type, "rank_type": rank_type, "count": 1}
        else:
            data_dict[gacha_type][name]["count"] += 1
    file.close()
    path = "./data/data_dict.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data_dict, f, ensure_ascii=False)
    print("按照卡池类型分类的数据已保存到data_dict.json")
    return path


def deal_data(data_path):
    # 指定中文字体文件路径和字体大小
    file = open(data_path, "r", encoding="utf-8")
    json_data = json.load(file)
    data_400 = json_data["400"]
    data_301 = json_data["301"]
    data_302 = json_data["302"]
    data_200 = json_data["200"]

    print(f"合并前：{data_400}")
    result = data_400.copy()
    for key, value in data_301.items():
        if key in result:
            result[key]["count"] += value["count"]
        else:
            result[key] = value
    print(f"合并后：{result}")

    files_name = ["常驻祈愿", "角色活动祈愿", "武器活动祈愿"]
    files_list = [data_200, result, data_302]
    for i in range(3):
        path = "./data/" + files_name[i] + ".json"
        with open(path, "w", encoding="utf-8") as f:
            json.dump(files_list[i], f, ensure_ascii=False)

    chacater = different_star_ratings(result)
    weapons = different_star_ratings(data_302)
    resident = different_star_ratings(data_200)
    print(f"角色祈愿：{chacater}")
    print(f"武器祈愿：{weapons}")
    print(f"常驻祈愿：{resident}")

    file.close()

    chacater_label = list([key + "星" for key in chacater.keys()])
    chacater_size = list(chacater.values())
    chacater_explode = (0, 0, 0.3)

    weapons_label = list([key + "星" for key in weapons.keys()])
    weapons_size = list(weapons.values())
    weapons_explode = (0, 0, 0.3)

    resident_label = list([key + "星" for key in resident.keys()])
    resident_size = list(resident.values())
    resident_explode = (0, 0, 0.3)

    get_pie_image(chacater_size, chacater_label, chacater_explode, "角色活动祈愿")
    get_pie_image(weapons_size, weapons_label, weapons_explode, "武器活动祈愿")
    get_pie_image(resident_size, resident_label, resident_explode, "常驻祈愿")

    # fig, ax = plt.subplots(1,2,dpi=200)
    # ax[0].pie(chacater_size, labels=chacater_label, explode=chacater_explode, autopct='%1.1f%%', shadow=False,
    #           startangle=150)
    # ax[0].title.set_text("角色活动祈愿")
    #
    # ax[1].pie(weapons_size, labels=weapons_label, explode=weapons_explode, autopct='%1.1f%%', shadow=False,
    #             startangle=150)
    # ax[1].title.set_text("武器活动祈愿")

    # # 紧凑布局
    # plt.tight_layout()
    # plt.show()

    chacater_all = sum(chacater_size)
    weapons_all = sum(weapons_size)
    resident_all = sum(resident_size)

    chacater_3_probability = round(chacater["3"] / chacater_all, 5)
    chacater_4_probability = round(chacater["4"] / chacater_all, 5)
    chacater_5_probability = round(chacater["5"] / chacater_all, 5)

    weapons_3_probability = round(weapons["3"] / weapons_all, 5)
    weapons_4_probability = round(weapons["4"] / weapons_all, 5)
    weapons_5_probability = round(weapons["5"] / weapons_all, 5)

    resident_3_probability = round(resident["3"] / resident_all, 5)
    resident_4_probability = round(resident["4"] / resident_all, 5)
    resident_5_probability = round(resident["5"] / resident_all, 5)

    average_chacater = chacater_all / chacater["5"]
    average_weapons = weapons_all / weapons["5"]
    average_resident = resident_all / resident["5"]

    result_dict = dict()
    result_dict["角色活动祈愿"] = {"总抽数": chacater_all, "3星概率": chacater_3_probability,
                                   "4星概率": chacater_4_probability,
                                   "5星概率": chacater_5_probability,
                                   "五星平均抽卡数": average_chacater}
    result_dict["武器活动祈愿"] = {"总抽数": weapons_all, "3星概率": weapons_3_probability,
                                   "4星概率": weapons_4_probability,
                                   "5星概率": weapons_5_probability,
                                   "五星平均抽卡数": average_weapons}
    result_dict["常驻祈愿"] = {"总抽数": resident_all, "3星概率": resident_3_probability,
                               "4星概率": resident_4_probability,
                               "5星概率": resident_5_probability,
                               "五星平均抽卡数": average_resident}
    with open("./data/average_probability.json", "w", encoding="utf-8") as f:
        json.dump(result_dict, f, ensure_ascii=False)
    return "./data/average_probability.json"


def different_star_ratings(data_dict: dict):
    result = dict()
    for key, value in data_dict.items():
        if value["rank_type"] not in result:
            result[value["rank_type"]] = value["count"]
        else:
            result[value["rank_type"]] += value["count"]
    return result


def get_pie_image(size, label, explode, title):
    # 既要显示比例，也要显示size中具体的数量
    plt.pie(size, labels=label, explode=explode, autopct=lambda pct: f"{pct:.1f}%\n({pct / 100 * sum(size):.0f})",
            shadow=False,
            startangle=150)
    plt.title(title)
    plt.tight_layout()
    plt.savefig(f"./image/{title}.png", dpi=200)
    print(f"{title}图片保存成功！")
    plt.close()


def data_run(path):
    try:
        first_data = get_data(path)
        result_data = deal_data(first_data)
        return "数据处理成功！"
    except:
        return "或者不符合统一的json格式!"


if __name__ == '__main__':
    # data_path = get_data()
    # path = deal_data("./data/data_dict.json")
    # path = "./data/Wishlog_163056907_20230711_113840.json"
    path = ""
    data_run(path)
