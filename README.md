# A Redis Vector Search Demo

Using the RedisVL library, I'm building out a simple vector search demo. I'll be taking a dataset of anime from [Kaggle](https://www.kaggle.com/code/yasminebenj/anime-reviews) and vectorizing both the main poster image and the description. I'll then be able to search over the dataset using text and see either the closest image or the closest description to the text I entered.

### Usage
If you want to run the search over anime posters, you'll need to first get the anime dataset for yourself from [Kaggle](https://www.kaggle.com/code/yasminebenj/anime-reviews) - it requires is an email to download, but it's free.

You'll also need a Redis connection, with the two easiest options presented below.

For me and my environment, running this from scratch looks like:
1. `git clone https://github.com/sav-norem/redis_vectorsearch.git`
2. `CD redis_vectorsearch`
3. `python3 -m venv .`
4. `source bin/activate`
5. `poetry install`
6. Put `anime-dataset-2023.csv` (the file you downloaded from Keggle) in the same folder as the `poetry.lock` file
7. `python3 src/redisvl_demo/redisvl_demo.py`

This will bring up a link to the local website where you can now search using text over the top ~1,000 anime posters.


### Basics
This project has a `DataLoader` and a `Demo`. The `DataLoader` will take optional arguments for both an initial file and a parsed file path. If you're doing this with the same data I did, you won't need to change anything. However if you want to swap out data, change file paths, etc. both of these inputs will need to change. You can do so in `redisvl_demo.py` on the initialization of `DataLoader`. Both `Demo` and `DataLoader` will take an optional argument for an `index_name`. Again, if you're not trying to change up the data or do your own testing, you can leave this alone. They both also take a Redis connection, meaning `redisvl_demo.py` is where you'll need to change that if you want to use anything other than `r = redis.Redis(host='localhost', port=6379, db=0)`.


### Redis Connection
To connect to Redis you have options. The route I took was to run Redis from docker with `docker run -d --name redis-stack -p 6379:6379 -p 8001:8001 redis/redis-stack:latest`, so if you're also running Redis locally with the default port you shouldn't have to touch the connection string. If you want to connect to a Cloud database you can replace the `r = redis.Redis(host='localhost', port=6379, db=0)` with your connection details. Those can be found in the Redis Cloud console by clicking Connect on your database, then navigating to `Redis Client`:

![Screenshot 2024-09-20 at 9 15 37 AM](https://github.com/user-attachments/assets/b78d4b83-5aad-4881-989b-de42dd7e5347)

#### Notes
This demo takes a bit to load and has a print statement mostly for entertainment / progress purpose. If you'd rather stare at an empty terminal while data gets loaded, you're more than welcome to take out the print statement. Regardless, parsing this data, getting the images, vectorizing them and loading them, takes a bit of time.

The `vector_extend` file overwrites the HuggingFace embed function to allow for images. I'm currently using two different models, one for the images and one for the synopsis. While `sentence-transformers/clip-ViT-L-14` is multi-modal and can be used for text, the limit for tokens was too low to vectorize the entire synopsis. I'll definitely be exploring other models for these purposes and seeing how they impact the search results.

Features I'm planning to add:
1. ~~Refactor to separate the data loader and the demo runner~~
2. Search over synopsis and title as well as image
3. A way to see more than just the top result from the search
4. Filter buttons for different genres

If you want to check out the extra simple version, the first iteration, `vl_demo` under `old_versions`, uses images of strawberries since I'd been writing about why LLMs are bad at [spelling](https://dev.to/savannah_norem/how-many-rs-are-in-strawberry-and-do-llms-know-how-to-spell-2513). You'll still need to do the `poetry install` followed by `python3 old_versions/vl_demo.py` and you'll see a simple search interface that allows you to search by text and see which strawberry image is closest to the text you entered. This demo will load a lot faster, but doesn't display images.

I'm blogging about this project as I go, so if you have any questions or want to know more, feel free to reach out to me on [dev.to](https://dev.to/savannah_norem) or [LinkedIn](https://www.linkedin.com/in/savannah-norem/).
