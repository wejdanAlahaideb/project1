#!/usr/bin/env python3
# A buggy web service in need of a database.
from __future__ import division
from flask import Flask, request, redirect, url_for

from newsDB import get_articles, get_authors, get_days_with_error

app = Flask(__name__)

print "=====================\r\n"
print "Most visited articles \r\n=====================\r\n"
for row in get_articles():
    print "\n" + str(row[0]) + ' - ' + str(row[1]) + ' views'
print "\n\n\r\n=================================\r\n"
print "Authors of Most visited articles \r\n"
print "=================================\r\n"
for row in get_authors():
    print "\n" + str(row[0]) + ' - ' + str(row[1]) + ' views'
print "\n\n\r\n==================================\r\n"
print "Days with error ratio more than 1% \r\n"
print "==================================\r\n"
for row in get_days_with_error():
    ratio = ((row[3] / (row[1] + row[3])) * 100)
    print "\n" + str(row[0]) + ' - ' + str(round(ratio, 2)) + '% errors'
