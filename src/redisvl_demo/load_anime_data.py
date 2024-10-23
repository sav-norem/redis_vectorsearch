from redisvl.query import VectorQuery
from redisvl.index import SearchIndex
from PIL import Image
import csv
from io import BytesIO
import pandas as pd
import os
import urllib.request
import sys
import json
from schema import schema
from vector_extend import HF_Images
import logging

class DataLoader:
    def __init__(self, redis, initial_data_file="anime-test.csv", index_name="anime_demo", anime_limit=1000):
        # This class assumes data that needs to be parsed
        # however parse_data can be skipped if the data is already in the correct format amd passed in as the parsed_data_file
        self.redis = redis
        self.initial_data = initial_data_file
        self.index_name = index_name
        try:
            self.index = SearchIndex.from_dict(schema)
        except:
            logging.critical("Index could not be created. Exiting.")
            sys.exit(1)
        self.index.set_client(redis)
        self.index.create(overwrite=True, drop=True)
        self.img_vectorizer = HF_Images(model="sentence-transformers/clip-ViT-L-14")
        self.txt_vectorizer = HF_Images(model="all-MiniLM-L6-v2")
        self.anime_limit = anime_limit


    def load_data(self):
        # The data is in the following format:
        # anime_id,Name,English name,Other name,Score,Genres,Synopsis,Type,Episodes,Aired,Premiered,Status,Producers,Licensors,Studios,Source,Duration,Rating,Rank,Popularity,Favorites,Scored By,Members,Image URL

        # Example: (with the description split into multiple lines for readability)
        # 5114,Fullmetal Alchemist: Brotherhood,Fullmetal Alchemist: Brotherhood,鋼の錬金術師 FULLMETAL ALCHEMIST,9.1,"Action, Adventure, Drama, Fantasy","After a horrific alchemy experiment goes wrong in the Elric household, brothers Edward and Alphonse are left in a catastrophic new reality. Ignoring the alchemical principle banning human transmutation, the boys attempted to bring their recently deceased mother back to life. Instead, they suffered brutal personal loss: Alphonse's body disintegrated while Edward lost a leg and then sacrificed an arm to keep Alphonse's soul in the physical realm by binding it to a hulking suit of armor.
        # The brothers are rescued by their neighbor Pinako Rockbell and her granddaughter Winry. Known as a bio-mechanical engineering prodigy, Winry creates prosthetic limbs for Edward by utilizing ""automail,"" a tough, versatile metal used in robots and combat armor. After years of training, the Elric brothers set off on a quest to restore their bodies by locating the Philosopher's Stone—a powerful gem that allows an alchemist to defy the traditional laws of Equivalent Exchange.
        # As Edward becomes an infamous alchemist and gains the nickname ""Fullmetal,"" the boys' journey embroils them in a growing conspiracy that threatens the fate of the world.",TV,64.0,"Apr 5, 2009 to Jul 4, 2010",spring 2009,Finished Airing,"Aniplex, Square Enix, Mainichi Broadcasting System, Studio Moriken","Funimation, Aniplex of America",Bones,Manga,24 min per ep,R - 17+ (violence & profanity),1.0,3,217606,2020030.0,3176556,https://cdn.myanimelist.net/images/anime/1208/94745.jpg

        df = (
            pd.read_csv(self.initial_data)
            .query("Type in ['TV', 'Movie']")
            .assign(Score=pd.to_numeric(pd.read_csv(self.initial_data)["Score"], errors='coerce'))
            .dropna(subset=["Score"])
        )
        if self.anime_limit:
            df = df.nlargest(self.anime_limit, "Score")
        if not os.path.exists("anime_images"):
            os.makedirs("anime_images")
        df.rename(columns={"Name": "title", "English name": "english_name", "Score": "rating", "Genres": "genres", "Synopsis": "synopsis", "Image URL": "image_url", "Rank": "popularity_rank"}, inplace=True)
        df["index"] = df.index
        df["image_path"] = df["index"].apply(lambda idx: f"anime_images/{idx}.jpg")
        df["poster_vector"] = None
        for index, val in df['image_url'].items():
            try:
                urllib.request.urlretrieve(val, f"anime_images/{index}.jpg")
                image = Image.open(f'anime_images/{index}.jpg')
                embedding = self.img_vectorizer.embed(image, as_buffer=True)
                df.at[index, 'poster_vector'] = embedding
            except Exception as e:
                logging.error(f"Failed to process image at index {index}: {e}")
                continue

        df["description_vector"] = df["synopsis"].apply(lambda x: self.txt_vectorizer.embed(x, as_buffer=True))
        df = df[["title", "english_name", "rating", "synopsis", "genres", "popularity_rank", "image_path", "index", "poster_vector", "description_vector"]]
        df = df.dropna(subset=["poster_vector", "description_vector"])
        keys_loaded = self.index.load(df.to_dict(orient="records"))
        logging.info(len(keys_loaded))
