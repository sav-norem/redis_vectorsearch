from redisvl.utils.vectorize import HFTextVectorizer
from redisvl.query import VectorQuery
from redisvl.index import SearchIndex
from PIL import Image
import redis

# Create a Redis connection
r = redis.Redis(host='localhost', port=6379, db=0)

schema = {
    "index": {
        "name": "image_simple",
        "prefix": "image_vector",
	},
    "fields": [
        {"name": "image", "type": "tag"},
        {"name": "embedding", "type": "vector", 
         	"attrs": {
                 "dims": 512,
                 "distance_metric": "cosine",
                 "algorithm": "flat",
                 "datatype": "float32"
			}
         }
	]
}

index = SearchIndex.from_dict(schema)
index.set_client(r)
index.create()

vectorizer = HFTextVectorizer(model="sentence-transformers/clip-ViT-L-14")

data = []

images = ["straws.jpg", "strawberries.jpg", "strawberries_vertical.jpg"]
for image in images:
    embedding = vectorizer.embed(Image.open(image), as_buffer=True)
    datum = { 
        "image": image,
		"embedding": embedding
	}
    data.append(datum)
    
index.load(data)


embedding = vectorizer.embed(Image.open("strawberries.jpg"), as_buffer=True)
query = VectorQuery(vector = embedding, vector_field_name = "embedding", num_results = 1)
results = index.query(query)

print(results)