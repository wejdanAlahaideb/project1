#!/usr/bin/env python3
# A buggy web service in need of a database.
from __future__ import division
from flask import Flask, request, redirect, url_for

from newsDB import get_articles, get_authors, get_days_with_error

app = Flask(__name__)

print("=====================")
print("Most visited articles \n=====================")
for row in get_articles():
    print("\n" + str(row[0]) + ' - ' + str(row[1]) + ' views')
print("\n\n=================================")
print("Authors of Most visited articles")
print("=================================")
for row in get_authors():
    print("\n" + str(row[0]) + ' - ' + str(row[1]) + ' views')
print("\n\n==================================")
print("Days with error ratio more than 1%")
print("==================================")
for row in get_days_with_error():
    ratio = ((row[3] / (row[1] + row[3])) * 100)
    print("\n" + str(row[0]) + ' - ' + str(round(ratio, 2)) + '% errors')
print("\n\n====== Report completed ====== \n\n")
