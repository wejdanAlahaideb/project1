#!/usr/bin/env python3
# 
# A buggy web service in need of a database.
from __future__ import division
from flask import Flask, request, redirect, url_for

from newsDB import get_articles, get_authors, get_days_with_error

app = Flask(__name__)

# HTML template for the forum page
HTML_WRAP = '''\
<!DOCTYPE html>
<html>
  <head>
    <title>DB News</title>
    <style>
      h1, form { text-align: center; }
	  .info{
		font-size: x-large;
		text-align: -webkit-center;
	  }
	  
    </style>
  </head>
  <body>
    <h1>News database log analysis</h1>
      <div><p class="info">Text file with name (report.txt) contains the log report please have a look to it</p></div>
    <!-- post content will go here -->
  </body>
</html>
'''

@app.route('/', methods=['GET'])
def main():
	'''Main page of the forum.'''
	with open('report.txt', 'w') as f:
		f.write("=====================\r\nMost visited articles \r\n=====================\r\n")
		for row in get_articles():
			f.write("\n" + str(row[0]) + ' - ' + str(row[1]) + ' views')
		f.write("\n\n\r\n=================================\r\nAuthors of Most visited articles \r\n=================================\r\n")
		for row in get_authors():
			f.write("\n" + str(row[0]) + ' - ' + str(row[1]) + ' views')
		f.write("\n\n\r\n==================================\r\nDays with error ratio more than 1% \r\n==================================\r\n")
		for row in get_days_with_error():
			ratio = ((row[3] /(row[1] + row[3])) * 100 )
			f.write("\n" + str(row[0]) + ' - ' + str(round(ratio,2)) + '% errors')
	f.close()
	HTML_WRAP
	return HTML_WRAP


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=8000)

