# A Redis Vector Search Demo

Using the RedisVL library, I'm building out a simple vector search demo. 

### Usage
If you want to run `vl_demo_anime`, you'll need to 
1. Get the anime dataset for yourself from [Kaggle](https://www.kaggle.com/code/yasminebenj/anime-reviews) since I ain't about to get in trouble for redistributing that data (but all it requires is an email to download)
2. Clone this repository
3. Run `poetry install`
4. Run `python vl_demo_anime.py`

This demo takes a bit to load at the moment and has a print statement mostly for entertainment / progress purpose. If you'd rather stare at an empty terminal while dtaa gets loaded, you're more than welcome to take out the print statement. Regardless, at the moment this demo takes a bit of setup time.

Features I'm planning to add:
1. Refactor to separate the data loader and the demo runner
2. Search over synopsis and title as well as image
3. A way to see more than just the top result from the search
4. Filter buttons for different genres

If you want to check out the extra simple version, the first iteration, `vl_demo`, uses images of strawberries since I'd been writing about why LLMs are bad at [spelling](https://dev.to/savannah_norem/how-many-rs-are-in-strawberry-and-do-llms-know-how-to-spell-2513). You'll still need to do the `poetry install` followed by `python vl_demo.py` and you'll see a simple search interface that allows you to search by text and see which strawberry image is closest to the text you entered. This demo will load a lot faster, but doesn't display images.

I'm blogging about this project as I go, so if you have any questions or want to know more, feel free to reach out to me on [dev.to](https://dev.to/savannah_norem) or [LinkedIn](https://www.linkedin.com/in/savannah-norem/).
