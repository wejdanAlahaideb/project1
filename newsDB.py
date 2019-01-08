# DatabASe code for the DB Forum, full solution!

import psycopg2
import bleach

DBNAME = "news"


def get_articles():
    """Return all articles from the 'databASe', most visited first."""
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute("""SELECT articles.title AS title, count(log.path) AS views
                FROM log
                JOIN articles
                ON articles.slug = reverse(split_part(reverse(path), '/', 1))
                GROUP BY title
                ORDER BY views DESC limit 3""")
    articles = c.fetchall()
    db.close()
    return articles


def get_authors():
    """Return authors with most visited articles."""
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute("""SELECT authors.name AS author, count(log.path) AS views
                FROM log
                JOIN articles
                ON articles.slug = reverse(split_part(reverse(path), '/', 1))
                JOIN authors ON articles.author = authors.id
                GROUP BY authors.name
                ORDER BY views DESC""")
    authors = c.fetchall()
    db.close()
    return authors


def get_days_with_error():
    """Return days with error ratio > 1%."""
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute("""SELECT *
                FROM
                (SELECT time::timestamp::date AS goodTime,
                count(status) AS goodStatus
                FROM log
                WHERE status = '200 OK'
                GROUP BY goodTime) AS goodrequests,
                (SELECT time::timestamp::date AS badTime,
                count(status) AS badStatus
                FROM log
                WHERE status = '404 NOT FOUND'
                GROUP BY badTime)AS badRequest
                WHERE goodrequests.goodTime = badRequest.badTime
                and ((goodrequests.goodStatus +  badRequest.badStatus) * .01)
                < badRequest.badStatus""")
    errors = c.fetchall()
    db.close()
    return errors
