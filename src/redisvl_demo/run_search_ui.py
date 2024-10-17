import gradio as gr
from redisvl.utils.vectorize import HFTextVectorizer
from redisvl.query import VectorQuery
from redisvl.index import SearchIndex
from PIL import Image
from redisvl.query.filter import Tag
import sys
import requests
from vector_extend import HF_Images
import logging

class SearchUI:
    def __init__(self, redis, index_name="anime_demo"):
        self.redis = redis
        self.index_name = index_name
        try:
            self.index = SearchIndex.from_existing(self.index_name, redis_client=self.redis)
        except:
            logging.critical("Index not found. Exiting.")
            sys.exit(1)
        self.index.set_client(self.redis)
        self.img_vectorizer = HF_Images(model="sentence-transformers/clip-ViT-L-14")
        self.txt_vectorizer = HF_Images(model="all-MiniLM-L6-v2")
        genres = redis.smembers("tag_set")
        self.genres = [genre.decode("utf-8") for genre in genres]
        self.results = []
        self.result_index = 0

    def run_search_ui(self):
        # This function runs the Gradio UI
        with gr.Blocks() as demo:
            search_term = gr.Textbox(label="Search the top 1,000 anime by their posters")
            search_target = gr.Radio(choices=["Poster", "Description"])
            search_results = gr.Textbox(label="Closest Anime (by poster search)")
            poster = gr.Image(label="Closest Anime Poster")
            synopsis = gr.Textbox(label="Synopsis")
            index = gr.Textbox(label="Index")
            gr.Button("Search").click(fn=self.vector_search, inputs=[search_term, search_target], outputs=[search_results, poster, synopsis, index])
            gr.Button("Next").click(fn=self.next_result, inputs=[], outputs=[search_results, poster, synopsis, index])
            gr.Button("Back").click(fn=self.last_result, inputs=[], outputs=[search_results, poster, synopsis, index])

        demo.launch()

    def vector_search(self, search_text, search_target):
        # This function takes a search term, vectorizes it, and queries the RedisVL index for the closest anime poster
        if search_target == "Description":
            vector_field = "description_vector"
            search_embedding = self.txt_vectorizer.embed(search_text, as_buffer=True)
        else:
            vector_field = "poster_vector"
            search_embedding = self.img_vectorizer.embed(search_text, as_buffer=True)
        
        query = VectorQuery(vector = search_embedding, vector_field_name = vector_field, return_fields=["title", "image_path", "synopsis"])
        logging.debug(query)
        self.results = self.index.query(query)
        logging.debug(len(self.results))
        logging.debug(self.results)
        if len(self.results) > 0:
            return self.results[self.result_index]["title"], Image.open(self.results[self.result_index]['image_path']), self.results[self.result_index]["synopsis"], self.result_index
        else:
            raise gr.Error("No results found")
    
    def next_result(self):
        # This function returns the next result from the RedisVL query
        self.result_index += 1
        if len(self.results) > 1:
            return self.results[self.result_index]["title"], Image.open(self.results[self.result_index]['image_path']), self.results[self.result_index]["synopsis"], self.result_index
        else:
            raise gr.Error("No results found")
        
    def last_result(self):
        # This function retrieves the last result from the RedisVL query
        self.result_index -= 1
        if len(self.results) > 1:
            return self.results[self.result_index]["title"], Image.open(self.results[self.result_index]['image_path']), self.results[self.result_index]["synopsis"], self.result_index
        else:
            raise gr.Error("No results found")