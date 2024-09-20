from redisvl.utils.vectorize import HFTextVectorizer
from redisvl.query import VectorQuery
from redisvl.index import SearchIndex
from PIL import Image
import redis
import gradio as gr

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

data = []

images = ["strawberries_white_bowl_brown_background.jpg", "strawberries.jpg", "strawberries_sparse_white_background.jpg", "strawberries_growing.jpg", "strawberries_in_hands_leaf_background.jpg", "strawberries_white_background.jpg"]
for image in images:
    embedding = vectorizer.embed(Image.open(f'{image}'), as_buffer=True)
    datum = { 
        "image": image,
		"embedding": embedding
	}
    data.append(datum)
    
index.load(data)

def strawberry_search(text):
    embedding = vectorizer.embed(text, as_buffer=True)
    query = VectorQuery(vector = embedding, vector_field_name = "embedding", return_fields=["image"])
    results = index.query(query)
    return results


demo = gr.Interface(
    fn=strawberry_search,
    inputs=["text"],
    outputs=["text"],
)

demo.launch()
