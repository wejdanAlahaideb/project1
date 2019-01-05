# Database code for the DB Forum, full solution!

import psycopg2, bleach

DBNAME = "news"

def get_articles():
	"""Return all articles from the 'database', most visited first."""
	db = psycopg2.connect(database=DBNAME)
	c = db.cursor()
	c.execute("select articles.title as title, count(log.path) as views from articles join log on lower(articles.title) LIKE replace(reverse(split_part(reverse(path), '/', 1)), '-', ' ') || '%' group by title order by views DESC")
	articles = c.fetchall()
	db.close()
	return articles
  
def get_authors():
	"""Return all authors from the 'database', most visited articles' author first."""
	db = psycopg2.connect(database=DBNAME)
	c = db.cursor()
	c.execute("select authors.name as author, count(log.path) as views from articles join log on lower(articles.title) LIKE replace(reverse(split_part(reverse(path), '/', 1)), '-', ' ') || '%'  join authors on articles.author = authors.id group by authors.name order by views DESC")
	authors = c.fetchall()
	db.close()
	return authors 

def get_days_with_error():
	"""get all days where status code '404 NOT FOUNd' was more than 1% of the requests in that day."""
	db = psycopg2.connect(database=DBNAME)
	c = db.cursor()
	c.execute("select * from (select time::timestamp::date as goodTime, count(status) as goodStatus from log where status = '200 OK' group by goodTime) as goodrequests, (select time::timestamp::date as badTime, count(status) as badStatus from log where status = '404 NOT FOUND' group by badTime) as badRequest where goodrequests.goodTime = badRequest.badTime and ((goodrequests.goodStatus +  badRequest.badStatus) * .01) < badRequest.badStatus")
	errors = c.fetchall()
	db.close()
	return errors 

