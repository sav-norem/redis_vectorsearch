import redisvl_demo
import pytest
import redis
from redisvl.utils.vectorize import HFTextVectorizer
from redisvl.query import VectorQuery
from redisvl.index import SearchIndex

import redisvl_demo.load_anime_data
import redisvl_demo.run_demo

r = redis.Redis(host='localhost', port=6379, db=0)
vectorizer = HFTextVectorizer(model="sentence-transformers/clip-ViT-L-14")
test_schema =  {
    "index": {
        "name": "test_demo",
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

def test_load():
    # this test checks that the data is loading to an index and being pushed to Redis
    loader = redisvl_demo.load_anime_data.DataLoader(r, parsed_data_file="anime-test.csv", index_name="test_demo")
    keys_loaded, data = loader.load_data(test_flag=True)
    assert len(data) == 10
    assert len(keys_loaded) == 10

def test_vector_search():
    # this test is to check if the query is returning results
    demo = redisvl_demo.run_demo.Demo(r, index_name="test_demo")
    results = demo.vector_search("brothers")
    assert len(results) > 0
