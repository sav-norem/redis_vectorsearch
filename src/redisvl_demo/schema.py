schema = {
    "index": {
        "name": "anime_demo",
        "prefix": "anime"
    },
    "fields": [
        {"name": "title", "type": "text"},
        {"name": "english_name", "type": "text"},
        {"name": "episodes", "type": "numeric"},
        {"name": "rating", "type": "numeric"},
        {"name": "synopsis", "type": "text"},
        {"name": "genres", "type": "tag"},
        {"name": "popularity_rank", "type": "numeric"},
        {"name": "image_path", "type": "text"},
        {"name": "index", "type": "numeric"},
        {"name": "poster_vector", "type": "vector", 
            "attrs": {
                "dims": 768,
                "distance_metric": "cosine",
                "algorithm": "flat",
                "datatype": "float32"
            }
        },
        {"name": "description_vector", "type": "vector", 
            "attrs": {
                "dims": 384,
                "distance_metric": "cosine",
                "algorithm": "flat",
                "datatype": "float32"
            }
        }
    ]
}