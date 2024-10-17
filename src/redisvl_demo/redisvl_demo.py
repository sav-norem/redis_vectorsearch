import redis
from load_anime_data import DataLoader
from run_search_ui import SearchUI
from sys import argv
import argparse
parser = argparse.ArgumentParser(exit_on_error=False)

def main(load_flag = True, demo_flag = True):
    # This function initializes the Redis connection and runs the data loading and demo functions
    r = redis.Redis(host='localhost', port=6379, db=0) # make host & port env variable
    if load_flag:
        loader = DataLoader(r)
        loader.load_data()
    if demo_flag:
        search_ui = SearchUI(r)
        search_ui.run_search_ui()

if __name__ == "__main__":
    load_flag = True
    demo_flag = True
    if len(argv) == 2:
        if argv[1] == 'loadonly':
            demo_flag = False
        if argv[1] == 'demoonly':
            load_flag = False
        
    main(load_flag, demo_flag)
