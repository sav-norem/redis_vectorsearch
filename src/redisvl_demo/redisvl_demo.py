import redis
from load_anime_data import DataLoader
from run_search_ui import SearchUI
from sys import argv
import argparse
parser = argparse.ArgumentParser(prog="Redis Vector Search Demo", description="Load data and run a vector search UI for anime data")


def create_arg_parser():
    parser = argparse.ArgumentParser(description="Anime Data Loader")
    parser.add_argument('-loadfile', help="File to load data from. Default: anime-dataset-2023.csv", default='anime-dataset-2023.csv')
    parser.add_argument('-limit', type=int, help="Number of anime to load. Default: 1000", default=1000)
    parser.add_argument('-imagepath', help="Path to save images. Default: anime_images", default='anime_images')
    parser.add_argument('-indexname', help="Name of the index to create. Default: anime_demo", default='anime_demo')
    parser.add_argument('-redisconnection', nargs=2, help="Redis connection details (host and port). Default: localhost:6379", default=['localhost', 6379])
    parser.add_argument('-noload', help="Don't load any data, assumes data can be found at index name.", default=False)
    return parser
        
def main():
    # Parse command line arguments
    parser = create_arg_parser()
    args = parser.parse_args()
    
    host, port = args.redisconnection
    r = redis.Redis(host=host, port=int(port), db=0)

    # Dataloader needs: redis connection, initial_data_file, index_name, anime_limit
    # SearchUI needs: redis connection, index_name
    if not args.noload:
        loader = DataLoader(
            r,
            initial_data_file=args.loadfile,
            index_name=args.indexname,
            limit=args.limit,
            image_path=args.imagepath
        )
        loader.load_data()

    search_ui = SearchUI(r, index_name=args.indexname)
    search_ui.run_search_ui()


if __name__ == '__main__':
    main()