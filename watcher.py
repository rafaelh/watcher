""" A simple website feed watcher """

import sqlite3
import feedparser

DATABASE = '/var/tmp/watcher_rss.sqlite'
FEED = 'https://xkcd.com/rss.xml'

db_connection = sqlite3.connect(DATABASE)
db = db_connection.cursor()
db.execute('CREATE TABLE IF NOT EXISTS website (title TEXT, date TEXT)')

def article_is_not_db(article_title, article_date):
    """ Check if a given pair of article title and date is in the database
    Args:
        article_title (str): The title of an article
        article_date  (str): The publication date of an article
    Return:
        True if the article is not in the database
        False if the article is already present in the database
    """
    db.execute("SELECT * from website WHERE title=? AND date=?", (article_title, article_date))
    if not db.fetchall():
        return True
    else:
        return False

def add_article_to_db(article_title, article_date):
    """ Add a new article title and date to the database
    Args:
        article_title (str): The title of an article
        article_date (str): The publication date of an article
    """
    db.execute("INSERT INTO website VALUES (?,?)", (article_title, article_date))
    db_connection.commit()

def send_notification(article_title, article_url):

    print("Hi there is a new website article:" + article_title + ". You can read it here " + article_url)

def read_article_feed():
    """ Get articles from RSS feed """
    feed = feedparser.parse(FEED)
    for article in feed['entries']:
        if article_is_not_db(article['title'], article['published']):
            send_notification(article['title'], article['link'])
            add_article_to_db(article['title'], article['published'])

if __name__ == '__main__':
    read_article_feed()
    db_connection.close()
