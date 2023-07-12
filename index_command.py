import configparser
def show_image(func):
    def wrapper(*args, **kw):
        print("async")
        func()
        print("async end")

    return wrapper


@show_image
def test():
    print("test")

def get_ini():
    path = "./path.ini"
    config = configparser.ConfigParser()
    config.read(path)

    wish_data = config.get("wishlog", "path")
    print(wish_data)
    ablum_data = config.get("album","path")
    print(ablum_data)
    game_data = config.get("game","path")
    print(game_data)

test()
get_ini()