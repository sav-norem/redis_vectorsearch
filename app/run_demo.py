import gradio as gr
from redisvl.utils.vectorize import HFTextVectorizer
from redisvl.query import VectorQuery
from redisvl.index import SearchIndex
import redis
from PIL import Image

def run_demo(r):
    try:
        index = SearchIndex.from_existing("anime_demo", redis_client=r)
    except:
        print("Index not found. Please run load_anime_data.py first.")
        return
    index.set_client(r)
    index.create(overwrite=False)

    vectorizer = HFTextVectorizer(model="sentence-transformers/clip-ViT-L-14")

    with gr.Blocks() as demo:
        search_term = gr.Textbox(label="Search the top 1,000 anime by their posters")
        search_results = gr.Textbox(label="Closest Anime (by poster search)")
        poster = gr.Image(label="Closest Anime Poster")

        def anime_search(text):
            embedding = vectorizer.embed(text, as_buffer=True)
            query = VectorQuery(vector = embedding, vector_field_name = "poster_vector", return_fields=["title", "image_name"])
            results = index.query(query)
            print(results, type(results))
            title = results[0]['title']
            img = results[0]['image_name']
            return title, Image.open(f'anime_images/{img}')
        
        gr.Button("Search").click(fn=anime_search, inputs=search_term, outputs=[search_results, poster])

    demo.launch()