#!pip install BeautifulSoup4
import pandas as pd
import requests 
from bs4 import BeautifulSoup

from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt

#################################
# find genre of particular show #
#################################
def find_genre(url):
    
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # genres of this show = str
    list_genre = ''
    
    # [1] of all div is genre, could change when website changes
    div_genres = soup.find_all("div",{'class':'see-more inline canwrap'})[1]
    
    # separator, empty list of THIS show
    sep = ' | '
    list_genre_per_show = []
    
    # find <a>, get text
    for line in div_genres.find_all('a'):
        
        genre = line.get_text().strip() # genre type
        
        list_genre_per_show.append(genre)

    list_genre = sep.join(list_genre_per_show)

    return list_genre

############################
# create_imdb_rating_table #
############################
def create_imdb_rating_table():
    
    url = 'https://www.imdb.com/chart/toptv/'
    headers = {"Accept-Language": "en-US,en;q=0.5"}
    response = requests.get(url, headers=headers)
    
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # create dataframe and columns
    imdb_rating_table = pd.DataFrame()
    
    list_titles = []
    list_links = []
    list_ratings = []
    list_genres = []
    
    # title and link
    titles = soup.find_all("td", {"class": "titleColumn"})
     
    for title in titles:
        show_name = title.find('a').get_text()
        list_titles.append(show_name)

        show_link = title.find('a').get('href')
        show_url = 'https://www.imdb.com' + show_link
        list_links.append(show_url)
        
        show_genres = find_genre(show_url)
        list_genres.append(show_genres)
        
    imdb_rating_table['Title'] = list_titles
    imdb_rating_table['link'] = list_links
    imdb_rating_table['Genre'] = list_genres    
    
    # ratings
    ratings = soup.find_all("td", {"class": "imdbRating"})

    for rating in ratings:
        show_rating = rating.get_text().strip()
        list_ratings.append(show_rating)

    imdb_rating_table['Rating'] = list_ratings
    
    return imdb_rating_table

imdb_table = create_imdb_rating_table()

# save to csv
#imdb_table.to_csv('imdb_table.csv')

# save genre to list
list_genres = []
for genres in imdb_table['Genre']:
    list_genres.append(genres.split(' | '))

# flatten list
list_genres = [genre for sub_list_genre in list_genres for genre in sub_list_genre]
word_genres = ' '.join(list_genres)

# create word cloud
def one_color_func(word=None, font_size=None, 
                   position=None, orientation=None, 
                   font_path=None, random_state=None):
    h = random_state.randint(250, 350) # 0 - 360
    s = random_state.randint(60, 100) # 0 - 100
    l = random_state.randint(15, 60) # 0 - 100
    return "hsl({}, {}%, {}%)".format(h, s, l)

wc = WordCloud(background_color="yellow", color_func=one_color_func, width=1600, height=1200)
wc.generate_from_frequencies(Counter(list_genres))
plt.figure(figsize=(12,8))
plt.imshow(wc)
plt.axis('off')
plt.show()
