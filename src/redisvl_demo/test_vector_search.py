from redisvl.utils.vectorize import HFTextVectorizer
from redisvl.query import VectorQuery
from redisvl.index import SearchIndex
from PIL import Image
from redisvl.query.filter import Tag
import sys
import requests
from vector_extend import HF_Images
import logging
import redis
from schema import schema
import numpy as np

redis = redis.Redis(host='localhost', port=6379, db=0)

print(redis.hget("anime:0d1da9a056504914a7d4aafb83251fc5", "description_vector"))

index = SearchIndex.from_existing("anime_demo", redis_client=redis)

search_text = "swords"
search_vectorizer = HFTextVectorizer(model="all-MiniLM-L6-v2")
search_embedding = np.array(search_vectorizer.embed(search_text)).astype(np.float32).tobytes()
print(type(search_embedding))

query = VectorQuery(vector = search_embedding, vector_field_name = "description_vector", return_fields=["title", "image_path", "synopsis"])
print(query)
print(index.query(query))