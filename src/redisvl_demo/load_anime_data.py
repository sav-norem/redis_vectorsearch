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
from vector_extend import HF_Images

class DataLoader:
    def __init__(self, redis, initial_data_file="anime-dataset-2023.csv", parsed_data_file="anime-sorted.csv", index_name="anime_demo"):
        # This class assumes data that needs to be parsed
        # however parse_data can be skipped if the data is already in the correct format amd passed in as the parsed_data_file
        self.redis = redis
        self.initial_data = initial_data_file
        self.parsed_data_file = parsed_data_file
        self.index_name = index_name
        with open("schema.json", "r") as f:
            self.schema = json.load(f)
        try:
            self.index = SearchIndex.from_dict(self.schema)
        except:
            print("Index could not be created. Exiting.")
            sys.exit(1)
        self.index.set_client(redis)
        self.index.create(overwrite=True, drop=True)
        self.img_vectorizer = HF_Images(model="sentence-transformers/clip-ViT-L-14")
        self.txt_vectorizer = HF_Images(model="all-MiniLM-L6-v2")

    def parse_data(self):
        # The data is in the following format:
        # anime_id,Name,English name,Other name,Score,Genres,Synopsis,Type,Episodes,Aired,Premiered,Status,Producers,Licensors,Studios,Source,Duration,Rating,Rank,Popularity,Favorites,Scored By,Members,Image URL

        # Example: (with the description split into multiple lines for readability)
        # 5114,Fullmetal Alchemist: Brotherhood,Fullmetal Alchemist: Brotherhood,鋼の錬金術師 FULLMETAL ALCHEMIST,9.1,"Action, Adventure, Drama, Fantasy","After a horrific alchemy experiment goes wrong in the Elric household, brothers Edward and Alphonse are left in a catastrophic new reality. Ignoring the alchemical principle banning human transmutation, the boys attempted to bring their recently deceased mother back to life. Instead, they suffered brutal personal loss: Alphonse's body disintegrated while Edward lost a leg and then sacrificed an arm to keep Alphonse's soul in the physical realm by binding it to a hulking suit of armor.
        # The brothers are rescued by their neighbor Pinako Rockbell and her granddaughter Winry. Known as a bio-mechanical engineering prodigy, Winry creates prosthetic limbs for Edward by utilizing ""automail,"" a tough, versatile metal used in robots and combat armor. After years of training, the Elric brothers set off on a quest to restore their bodies by locating the Philosopher's Stone—a powerful gem that allows an alchemist to defy the traditional laws of Equivalent Exchange.
        # As Edward becomes an infamous alchemist and gains the nickname ""Fullmetal,"" the boys' journey embroils them in a growing conspiracy that threatens the fate of the world.",TV,64.0,"Apr 5, 2009 to Jul 4, 2010",spring 2009,Finished Airing,"Aniplex, Square Enix, Mainichi Broadcasting System, Studio Moriken","Funimation, Aniplex of America",Bones,Manga,24 min per ep,R - 17+ (violence & profanity),1.0,3,217606,2020030.0,3176556,https://cdn.myanimelist.net/images/anime/1208/94745.jpg
        
        # This function parses the initial data file and filters out the top 1010 TV and Movie entries with a valid score
        df = (
            pd.read_csv(self.initial_data)
            .query("Type in ['TV', 'Movie']")
            .assign(Score=pd.to_numeric(pd.read_csv(self.initial_data)["Score"], errors='coerce'))
            .dropna(subset=["Score"])
            .nlargest(1010, "Score")
        )

        df.to_csv(self.parsed_data_file, index=False)

    def load_data(self, test_flag=False):
        # This function loads the parsed data into the RedisVL index, along with a set of genres
        # To display posters later, we'll need to store them locally
        if not os.path.exists("anime_images"):
            os.makedirs("anime_images")
        genre_set = set()
        anime_list = []
        with open(self.parsed_data_file, "r") as f:
            reader = csv.reader(f)
            next(reader, None)
            for row in reader:
                title = row[1].replace(" ", "_").replace('/', '_')
                genres = row[5].split(", ")
                genre_set.update(genres)
                print(row[1], row[4])
                description_embedding = self.txt_vectorizer.embed(row[6], as_buffer=True)
                try:
                    urllib.request.urlretrieve(row[23], f"anime_images/{title}.jpg")
                except:
                    continue
                poster_embedding = self.img_vectorizer.embed(Image.open(f'anime_images/{title}.jpg'), as_buffer=True)
                anime = {
                    "title": row[1],
                    "english_name": row[2],
                    "episodes": row[8],
                    "rating": row[4],
                    "synopsis": row[6],
                    "genres": row[5],
                    "image_path": f"anime_images/{title}.jpg",
                    "popularity_rank": row[19],
                    "poster_vector": poster_embedding,
                    "description_vector": description_embedding
                }
                anime_list.append(anime)

        if "UNKNOWN" in genre_set:
            genre_set.remove("UNKNOWN")
        keys_loaded = self.index.load(anime_list)
        print(len(keys_loaded))
        self.redis.sadd("tag_set", *genre_set)

        if test_flag:
            return keys_loaded, anime_list
