"""
Emily Giverts
CSE 163 AC

A file that processes covid vaccine hesitancy- related data and produces
visualizations showing various insights from that data.
"""

from textblob import TextBlob
from wordcloud import WordCloud
import re
import matplotlib.pyplot as plt
import seaborn as sns
import geopandas as gpd


def clean_data(data):
    """
    Cleans the api data for analysis and word cloud creation. Returns the
    cleaned data.
    """
    data = re.sub(r'@[A-Za-z0-9]+:', '', data)
    data = re.sub(r'#', '', data)
    data = re.sub(r'RT[\s]+', '', data)
    data = re.sub(r'https?:\/\/\S+', '', data)
    return data


def getSubjectivity(tweet):
    """
    Returns the subjectivity sentiments analysis on the cleaned tweets.
    """
    return TextBlob(tweet).sentiment.subjectivity


def getPolarity(tweet):
    """
    Returns the polarity sentiments analysis on the cleaned tweets.
    """
    return TextBlob(tweet).sentiment.polarity


def make_cloud(data):
    """
    Creates a word cloud of the cleaned tweets, representing more common words
    or phrases in a larger size.
    """
    # Splits up tweets for analysis
    words = ' '.join([twts for twts in data['Tweet']])
    # Generats Word Cloud
    word_cloud = WordCloud(width=500, height=300, random_state=21,
                           max_font_size=119).generate(words)
    fig, ax = plt.subplots(1)
    plt.imshow(word_cloud, interpolation='bilinear')
    plt.axis('off')
    # plt.title('')
    # ax.legend().set_visible(False)
    plt.savefig('word_cloud.png', bbox_inches='tight')


def get_analysis(score):
    """
    Translates polarity score to represent words that are easier to
    interpret such as Negative if the score is less than 0, Neutral
    if the score is 0, and Positive if the score is grater than 0.
    Returns the word.
    """
    if score < 0:
        return 'Negative'
    elif score == 0:
        return 'Neutral'
    else:
        return 'Positive'


def location_analysis(data):
    """
    Creates bar graph of narrative polarities according to each state. Only
    includes the states that were represented within the tweets.
    """
    sns.catplot(kind="bar", data=data, x="State", y="Polarity")
    plt.title("Covid Narrative Polarities Within Each State")
    plt.xlabel('State')
    plt.ylabel('Polarity')
    plt.xticks(rotation=-60, fontsize=5)
    plt.savefig('location_analysis.png', bbox_inches='tight')


def geo(data):
    """
    Creates a map represenation of narrative polarities according to each
    state. Only includes the states that were represented within the tweets.
    """
    # Merges geo data with API data
    country = gpd.read_file('covid_vaccine_hesitency/main_data/gz_2010_us_040_00_5m.json')
    country = country[country['NAME'] != 'Hawaii']
    country = country[country['NAME'] != 'Alaska']
    country = country[country['NAME'] != 'Puerto Rico']
    country_copy = country
    combined_data = data.merge(country, left_on='State', right_on='NAME')
    # Creates visualization
    fig, ax = plt.subplots(1)
    combined_data = gpd.GeoDataFrame(combined_data, geometry='geometry')
    country_copy.plot(ax=ax, color='#EEEEEE')
    combined_data.plot(ax=ax, column='Polarity', legend=True)
    plt.title("Covid Narrative Polarities Within Each State")
    plt.savefig('geo_polarity.png')