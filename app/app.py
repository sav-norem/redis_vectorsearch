import redis
from load_anime_data import *
from run_demo import *
from sys import argv

def main(load_flag = True, demo_flag = True):
    r = redis.Redis(host='localhost', port=6379, db=0)
    if load_flag:
        load_data(r)
    if demo_flag:
        run_demo(r)


if __name__ == "__main__":
    demo_flag, load_flag = True, True
    if len(argv) == 2:
        if argv[1] == 'loadonly':
            demo_flag = False
        if argv[1] == 'demoonly':
            load_flag = False
        
    main(load_flag, demo_flag)
