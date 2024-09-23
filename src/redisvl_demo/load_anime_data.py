from redisvl.utils.vectorize import HFTextVectorizer
from redisvl.query import VectorQuery
from redisvl.index import SearchIndex
from PIL import Image
import csv
from io import BytesIO
import pandas as pd
import os
import urllib.request

class DataLoader:
    def __init__(self, r, initial_data_file="anime-dataset-2023.csv", parsed_data_file="anime-sorted.csv", index_name="anime_demo"):
        self.r = r
        self.initial_data = initial_data_file
        self.parsed_data_file = parsed_data_file
        self.index_name = index_name
        self.schema = {
            "index": {
                "name": self.index_name,
                "prefix": "anime",
            },
            "fields": [
                {"name": "title", "type": "text"},
                {"name": "english_name", "type": "text"},
                {"name": "episodes", "type": "numeric"},
                {"name": "rating", "type": "numeric"},
                {"name": "synopsis", "type": "text"},
                {"name": "genres", "type": "tag"},
                {"name": "popularity_rank", "type": "numeric"},
                {"name": "image_path", "type": "text"},
                {"name": "poster_vector", "type": "vector", 
                    "attrs": {
                        "dims": 768,
                        "distance_metric": "cosine",
                        "algorithm": "flat",
                        "datatype": "float32"
                    }
                }
            ]
        }
        self.index = SearchIndex.from_dict(self.schema)
        self.index.set_client(r)
        self.index.create(overwrite=True, drop=True)
        self.vectorizer = HFTextVectorizer(model="sentence-transformers/clip-ViT-L-14")

    def parse_data(self):
        df = (
            pd.read_csv(self.initial_data)
            .query("Type in ['TV', 'Movie']")
            .assign(Score=pd.to_numeric(pd.read_csv(self.initial_data)["Score"], errors='coerce'))
            .dropna(subset=["Score"])
            .nlargest(1010, "Score")
        )

        df.to_csv(self.parsed_data_file, index=False)

    def load_data(self, test_flag=False):
        genre_set = set()
        data = []
        with open(self.parsed_data_file, "r") as f:
            reader = csv.reader(f)
            next(reader, None)
            for row in reader:
                title = row[1].replace(" ", "_").replace('/', '_')
                genres = row[5].split(", ")
                genre_set.update(genres)
                print(row[1], row[4])
                if not os.path.exists("anime_images"):
                    os.makedirs("anime_images")
                try:
                    urllib.request.urlretrieve(row[23], f"anime_images/{title}.jpg")
                except:
                    continue
                embedding = self.vectorizer.embed(Image.open(f'anime_images/{title}.jpg'), as_buffer=True)
                datum = {
                    "title": row[1],
                    "english_name": row[2],
                    "episodes": row[8],
                    "rating": row[4],
                    "synopsis": row[6],
                    "genres": row[5],
                    "image_path": f"anime_images/{title}.jpg",
                    "popularity_rank": row[19],
                    "poster_vector": embedding
                }
                data.append(datum)

        if "UNKNOWN" in genre_set:
            genre_set.remove("UNKNOWN")
        keys_loaded = self.index.load(data)
        print(len(keys_loaded))
        self.r.sadd("tag_set", *genre_set)

        if test_flag:
            return keys_loaded, data
