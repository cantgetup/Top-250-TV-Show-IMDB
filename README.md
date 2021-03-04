# Web-Scraping Top 250 TV Show from IMDB
### top250imdb.py: scrapes data from https://www.imdb.com/chart/toptv/
### imdb_to_sql.py: Import data into local SQL database

Collects `Title`, `url`, `Creator`, `Star` and `Rating` from the movie pages
Then generates word cloud based on the frequency of appearance:

## Genre:
![alt text](https://github.com/charliesong66/Top-250-TV-Show-IMDB/blob/main/imdb_top250_tvshow_genre.png)

## Stars:
![alt text](https://github.com/charliesong66/Top-250-TV-Show-IMDB/blob/main/imdb_top250_tvshow_stars.png)

## Creators
![alt text](https://github.com/charliesong66/Top-250-TV-Show-IMDB/blob/main/imdb_top250_tvshow_creators.png)

Import data into local SQL database using imdb_to_sql.py
