from redisvl.utils.vectorize import HFTextVectorizer
from redisvl.query import VectorQuery
from redisvl.index import SearchIndex
from PIL import Image
import redis
import gradio as gr
import csv
import ast

# Create a Redis connection
r = redis.Redis(host='localhost', port=6379, db=0)

# keys = [title,episodes,rating,short_description,tags,image]
schema = {
    "index": {
        "name": "anime_demo",
        "prefix": "anime",
	},
    "fields": [
        {"name": "title", "type": "text"},
        {"name": "episodes", "type": "numeric"},
        {"name": "rating", "type": "numeric"},
        {"name": "short_description", "type": "text"},
        {"name": "tags", "type": "tag"},
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

data = []
tag_set = set()
# keys = [title,episodes,rating,short_description,tags,image]
with open('anime_data.csv', newline='') as csvfile:
    animereader = csv.reader(csvfile)
    next(animereader, None)
    for row in animereader:
        embedding = vectorizer.embed(Image.open(f'anime_posters/{row[5]}'), as_buffer=True)
        tag_list = ast.literal_eval(row[4])
        for tag in tag_list:
            if tag == "Sh*nen":
                tag = "Shounen"
            if tag == "Sh*jo":
                tag = "Shoujo"
        tag_set.update(tag_list)
        tag_string = ','.join(tag_list)
        datum = {
            "title": row[0],
            "episodes": row[1],
            "rating": row[2],
            "short_description": row[3],
            "poster_vector": embedding,
            "tags": tag_string,
            "img_name": row[5]
        }   
        data.append(datum)
    
tag_set.remove("")
index.load(data)
r.sadd("tag_set", *tag_set)



with gr.Blocks() as demo:
    search_term = gr.Textbox(label="Search the top 100 anime by their posters")
    search_results = gr.Textbox(label="Closest Anime (by poster search)")
    poster = gr.Image(label="Closest Anime Poster")

    def anime_search(text):
        embedding = vectorizer.embed(text, as_buffer=True)
        query = VectorQuery(vector = embedding, vector_field_name = "poster_vector", return_fields=["title", "img_name"])
        results = index.query(query)[0]
        title = results['title']
        img = results['img_name']
        return title, Image.open(f'anime_posters/{img}')
    
    gr.Button("Search").click(fn=anime_search, inputs=search_term, outputs=[search_results, poster])

demo.launch()