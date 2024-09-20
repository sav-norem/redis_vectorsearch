from redisvl.utils.vectorize import HFTextVectorizer
from redisvl.query import VectorQuery
from redisvl.index import SearchIndex
from PIL import Image
import csv
import urllib.request
import pandas as pd
import os


def load_data(r):
    schema = {
        "index": {
            "name": "anime_demo",
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

    index = SearchIndex.from_dict(schema)
    index.set_client(r)
    index.create(overwrite=True, drop=True)

    vectorizer = HFTextVectorizer(model="sentence-transformers/clip-ViT-L-14")

    genre_set = set()
    data = []
    # anime_id,Name,English name,Other name,Score,Genres,Synopsis,Type,Episodes,Aired,Premiered,Status,Producers,Licensors,Studios,Source,Duration,Rating,Rank,Popularity,Favorites,Scored By,Members,Image URL
    df = (
        pd.read_csv("anime-dataset-2023.csv")
        .query("Type in ['TV', 'Movie']")
        .assign(Score=pd.to_numeric(pd.read_csv("anime-dataset-2023.csv")["Score"], errors='coerce'))
        .dropna(subset=["Score"])
        .nlargest(1010, "Score")
    )

    df.to_csv("anime-sorted.csv", index=False)
    if not os.path.exists('./anime_images'):
        os.mkdir("anime_images")
    else:
        pass

    with open("anime-sorted.csv", "r") as f:
        reader = csv.reader(f)
        next(reader, None)
        for row in reader:
            title = row[1].replace(" ", "_").replace('/', '_')
            genres = row[5].split(", ")
            genre_set.update(genres)
            print(row[1], row[4])
            try:
                urllib.request.urlretrieve(row[23], f"anime_images/{title}.jpg")
            except:
                continue
            embedding = vectorizer.embed(Image.open(f'anime_images/{title}.jpg'), as_buffer=True)
            datum = {
                "title": row[1],
                "english_name": row[2],
                "episodes": row[8],
                "rating": row[4],
                "synopsis": row[6],
                "genres": row[5],
                "image_name": f'{title}.jpg',
                "popularity_rank": row[19],
                "poster_vector": embedding
            }
            data.append(datum)

    print(len(data))

    genre_set.remove("UNKNOWN")
    index.load(data)
    r.sadd("tag_set", *genre_set)