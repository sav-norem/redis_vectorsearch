import redis
from load_anime_data import DataLoader
from run_demo import Demo
from sys import argv


def main(load_flag = True, demo_flag = True):
    r = redis.Redis(host='localhost', port=6379, db=0)
    if load_flag:
        loader = DataLoader(r)
        loader.parse_data()
        loader.load_data()
    if demo_flag:
        demo = Demo(r)
        demo.run_demo()

if __name__ == "__main__":
    demo_flag, load_flag = True, True
    if len(argv) == 2:
        if argv[1] == 'loadonly':
            demo_flag = False
        if argv[1] == 'demoonly':
            load_flag = False
        
    main(load_flag, demo_flag)
