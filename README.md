# A Redis Vector Search Demo

Using the RedisVL library, I'm building out a simple vector search demo. I'll be taking a dataset of anime from [Kaggle](https://www.kaggle.com/code/yasminebenj/anime-reviews) and vectorizing both the main poster image and the description. I'll then be able to search over the dataset using text and see either the closest image or the closest description to the text I entered. As a _nerd_ who loves anime, this is a fun project for me to work on.

### Usage
If you want to run the search over anime posters, you'll need to first get the anime dataset for yourself from [Kaggle](https://www.kaggle.com/code/yasminebenj/anime-reviews) - it requires is an email to download, but it's free.

You'll also need a Redis connection, with the two easiest options presented below.

For me and my environment, running this from scratch looks like:
1. `git clone https://github.com/sav-norem/redis_vectorsearch.git`
2. `CD redis_vectorsearch`
3. `python3 -m venv .`
4. `source bin/activate`
5. `poetry install`
6. Put `anime-dataset-2023.csv` (the file you downloaded from Kaggle) in the same folder as the `poetry.lock` file
7. `python3 src/redisvl_demo/redisvl_demo.py`

This will bring up a link to the local web app where you can now search using text over the top ~1,000 anime posters.


### Basics
This project has a `DataLoader` and a `SearchUI`. 

Optional arguments are:
`-loadfile` - A different source for the data to be loaded from.
`-limit` - A limit for how many items to be loaded.
`-imagepath` - A folder for where the poster images will be stored.
`-indexname` - The name of the index where data will be loaded and where the SearchUI will be looking.
`-redisconnection` - The host and port for a Redis connection.
`-noload` - An option to bypass loading the data and just run the SearchUI.


#### Notes
This demo takes a bit to load and has a print statement mostly for entertainment / progress purpose. If you'd rather stare at an empty terminal while data gets loaded, you're more than welcome to take out the print statement. Regardless, parsing this data, getting the images, vectorizing them and loading them, takes a bit of time.

The `vector_extend` file overwrites the HuggingFace embed function from the [RedisVL](https://github.com/redis/redis-vl-python) library to allow for images. I'm currently using two different models, one for the images and one for the synopsis. While `sentence-transformers/clip-ViT-L-14` is multi-modal and can be used for text, the limit for tokens was too low to vectorize the entire synopsis. I'll definitely be exploring other models for these purposes and seeing how they impact the search results.

