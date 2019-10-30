from movie_data_scraper import TMDB_Scraper
import pandas as pd
import json

trailers = pd.read_csv("trailers.csv", index_col=0)
trailer_ids = trailers['movie_id'].unique().astype(int)

tmdb_scraper = TMDB_Scraper(api_key="abd17a9f250807b76ebbfa9997ca6ade")
movie_details = {}
movie_crew = {}
for i, id in enumerate(trailer_ids):
    print(f"Getting details of movie {i} / {len(trailer_ids)}")
    movie_details[str(id)] = tmdb_scraper.movie_details(id)
    movie_crew[str(id)] = tmdb_scraper.movie_crew(id)

    with open('movie_details.json', 'w') as outfile:
        json.dump(movie_details, outfile)

    with open('movie_crew.json', 'w') as outfile:
        json.dump(movie_crew, outfile)
