# A Redis Vector Search Demo

Using the RedisVL library, I'm building out a simple vector search demo. 

### Usage
If you want to run `vl_demo_anime`, you'll need to 
1. Have a Redis connection
2. Get the anime dataset for yourself from [Kaggle](https://www.kaggle.com/code/yasminebenj/anime-reviews) since I ain't about to get in trouble for redistributing that data (but all it requires is an email to download) and put it in the project folder*
3. Clone this repository
4. Run `poetry install`
5. Run `python app/vl_demo_anime.py`

* You may find it's easier for you to put the datafile elsewhere, just note that you'll need to adjust where `load_anime_data.py` looks for this file.

### Redis Connection
To connect to Redis you have options. The route I took was to run Redis from docker with `docker run -d --name redis-stack -p 6379:6379 -p 8001:8001 redis/redis-stack:latest`, so if you're also running Redis locally with the default port you shouldn't have to touch the connection string. If you want to connect to a Cloud database you can replace the `r = redis.Redis(host='localhost', port=6379, db=0)` in `app.py` with your connection details. Those can be found in the Redis Cloud console by clicking Connect on your database, then navigating to Redis Client
![Screenshot 2024-09-20 at 9 15 37 AM](https://github.com/user-attachments/assets/b78d4b83-5aad-4881-989b-de42dd7e5347)

#### Notes
This demo takes a bit to load at the moment and has a print statement mostly for entertainment / progress purpose. If you'd rather stare at an empty terminal while dtaa gets loaded, you're more than welcome to take out the print statement. Regardless, at the moment this demo takes a bit of setup time.

Features I'm planning to add:
1. ~~Refactor to separate the data loader and the demo runner~~
2. Search over synopsis and title as well as image
3. A way to see more than just the top result from the search
4. Filter buttons for different genres

If you want to check out the extra simple version, the first iteration, `vl_demo` under `old_versions`, uses images of strawberries since I'd been writing about why LLMs are bad at [spelling](https://dev.to/savannah_norem/how-many-rs-are-in-strawberry-and-do-llms-know-how-to-spell-2513). You'll still need to do the `poetry install` followed by `python vl_demo.py` and you'll see a simple search interface that allows you to search by text and see which strawberry image is closest to the text you entered. This demo will load a lot faster, but doesn't display images.

I'm blogging about this project as I go, so if you have any questions or want to know more, feel free to reach out to me on [dev.to](https://dev.to/savannah_norem) or [LinkedIn](https://www.linkedin.com/in/savannah-norem/).
