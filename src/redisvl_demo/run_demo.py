import gradio as gr
from redisvl.utils.vectorize import HFTextVectorizer
from redisvl.query import VectorQuery
from redisvl.index import SearchIndex
from PIL import Image
import requests

class Demo:
    def __init__(self, r, index_name="anime_demo"):
        self.r = r
        self.index_name = index_name
        try:
            self.index = SearchIndex.from_existing(self.index_name, redis_client=self.r)
        except:
            print("Index not found. Exiting.")
            return
        self.index.set_client(self.r)
        self.index.create(overwrite=False)
        self.vectorizer = HFTextVectorizer(model="sentence-transformers/clip-ViT-L-14")

    def run_demo(self):
        with gr.Blocks() as demo:
            search_term = gr.Textbox(label="Search the top 1,000 anime by their posters")
            search_results = gr.Textbox(label="Closest Anime (by poster search)")
            poster = gr.Image(label="Closest Anime Poster")   
            gr.Button("Search").click(fn=self.vector_search, inputs=search_term, outputs=[search_results, poster])

        demo.launch()

    def vector_search(self, search_text):
        embedding = self.vectorizer.embed(search_text, as_buffer=True)
        query = VectorQuery(vector = embedding, vector_field_name = "poster_vector", return_fields=["title", "image_path"])
        results = self.index.query(query)
        return results[0]['title'], Image.open(results[0]['image_path'])