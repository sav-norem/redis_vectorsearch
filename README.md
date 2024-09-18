# A Redis Vector Search Demo

Using the RedisVL library, I'm building out a simple vector search demo. For the first iteration, `vl_demo`, uses images of strawberries since I'd been writing about why LLMs are bad at [spelling](https://dev.to/savannah_norem/how-many-rs-are-in-strawberry-and-do-llms-know-how-to-spell-2513). If you clone this repo and run `python vl_demo` you'll see a simple search interface that allows you to search by text and see which strawberry image is closest to the text you entered.

If you want to run `vl_demo_anime`, you'll need to get the anime dataset for yourself from [Kaggle](https://www.kaggle.com/code/yasminebenj/anime-reviews) since I ain't about to get in trouble for redistributing that data (but all it requires is an email to download). This demo is a little more fun since you can search over anime posters by text and see which is closest to the text you entered.

Features I'm planning to add:
1. Search over synopsis and title as well as image
2. A way to see more than just the top result from the search
3. Filter buttons for different genres


I'm blogging about this project as I go, so if you have any questions or want to know more, feel free to reach out to me on [dev.to](https://dev.to/savannah_norem) or [LinkedIn](https://www.linkedin.com/in/savannah-norem/).
