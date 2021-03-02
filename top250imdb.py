#!pip install BeautifulSoup4
import pandas as pd
import requests 
from bs4 import BeautifulSoup

from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt

#################################
# find info of particular show #
#################################

# finds creators, stars, genres
def find_info(url):
    
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # info of this show = str
    str_creators = ''
    str_stars = ''
    str_genre = ''
    sep = ' | '
    
    # some show has no creators
    has_creators = False
    has_stars = False
    
    # find div for credit summary
    div_creditSummary = soup.find_all("div",{'class':'credit_summary_item'})

    list_creators = []
    list_stars = []

    # creator and star
    # if h4 tag.text = creators or stars
    # find 'a' in the credit summary, get names 
    for summary in div_creditSummary:
        if 'Creator' in summary.find_all('h4')[0].get_text():
            has_creators = True
            for a in summary.find_all('a'):
                creator = a.get_text().strip() # creator name
                list_creators.append(creator)

        if 'Star' in summary.find_all('h4')[0].get_text():
            has_stars = True
            for a in summary.find_all('a'):
                if 'See full cast' not in a.get_text().strip():
                    star = a.get_text().strip() # star name
                    list_stars.append(star)    


    # if no names, get N/A
    if has_creators:                
        str_creators = sep.join(list_creators)
    else:
        str_creators = 'N/A'
        
    if has_stars:
        str_stars = sep.join(list_stars)
    else:
        str_stars = 'N/A'
    

    # [1] of all div is genre, could change when website changes
    div_genres = soup.find_all("div",{'class':'see-more inline canwrap'})[1]

    # empty list of THIS show
    list_genre = []

    # find <a>, get text
    for line in div_genres.find_all('a'):

        genre = line.get_text().strip() # genre type

        list_genre.append(genre)

    str_genre = sep.join(list_genre)

    return str_creators, str_stars, str_genre


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
    list_creators = []
    list_stars = []
    
    # title and link
    titles = soup.find_all("td", {"class": "titleColumn"})
    
    
    # for each show, get the tile then url
    # with url, go into title's page, get "info"
    for title in titles:
        show_name = title.find('a').get_text()
        list_titles.append(show_name)

        show_link = title.find('a').get('href')
        show_url = 'https://www.imdb.com' + show_link
        list_links.append(show_url)
        
        show_creators = find_info(show_url)[0]
        list_creators.append(show_creators)
        
        show_stars = find_info(show_url)[1]
        list_stars.append(show_stars)
        
        show_genres = find_info(show_url)[2]
        list_genres.append(show_genres)
        
    imdb_rating_table['Title'] = list_titles
    imdb_rating_table['link'] = list_links
    imdb_rating_table['Genre'] = list_genres
    imdb_rating_table['Creators'] = list_creators
    imdb_rating_table['Stars'] = list_stars    
    
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
